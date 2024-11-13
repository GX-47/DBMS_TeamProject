import streamlit as st
from mysql.connector import Error
from config.database import connect_to_database
from decimal import Decimal
from datetime import datetime

def get_available_flights():
    try:
        db = connect_to_database()
        cursor = db.cursor()

        query = """
        SELECT f.*, a.airline_name 
        FROM flight f 
        JOIN airline a ON f.airline_id = a.airline_id 
        WHERE f.departure_time > NOW()
        """
        cursor.execute(query)
        flights = cursor.fetchall()

        return flights
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()

def book_flight(passenger_id, flight_id, airline_id, passenger_details, food_orders):
    try:
        db = connect_to_database()
        cursor = db.cursor()

        # Get flight price
        price_query = "SELECT price FROM flight WHERE flight_id = %s"
        cursor.execute(price_query, (flight_id,))
        base_price = cursor.fetchone()[0]

        # Calculate total price with tax using Decimal
        tax_rate = Decimal('1.18')  # Convert 1.18 to Decimal
        total_price = base_price * tax_rate  # Now both are Decimal types

        # Create booking
        booking_query = """
        INSERT INTO booking (booking_id, passenger_id, flight_id, booking_date, 
                           total_price, status, airline_id)
        VALUES (%s, %s, %s, CURDATE(), %s, 'Pending', %s)
        """
        
        cursor.execute("SELECT COUNT(*) FROM booking")
        booking_count = cursor.fetchone()[0] + 1
        booking_id = f"B_{booking_count}"
        
        cursor.execute(booking_query, (booking_id, passenger_id, flight_id, 
                                     total_price, airline_id))

        # Add passenger details
        for idx, (name, seat, meal) in enumerate(passenger_details):
            detail_id = f"D_{booking_id}_{idx+1}"
            detail_query = """
            INSERT INTO passenger_details (detail_id, booking_id, passenger_name, 
                                        seat_number, meal_preference)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(detail_query, (detail_id, booking_id, name, seat, meal))

        # Add food orders
        for food_id, quantity in food_orders.items():
            food_query = """
            INSERT INTO booking_food (booking_id, food_id, quantity)
            VALUES (%s, %s, %s)
            """
            cursor.execute(food_query, (booking_id, food_id, quantity))

        db.commit()
        st.success("Flight booked successfully!")
        return booking_id
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()

def view_bookings(user_id, user_type):
    try:
        db = connect_to_database()
        cursor = db.cursor()

        if user_type == "passenger":
            query = """
            SELECT b.booking_id, f.flight_id, a.airline_name, f.origin, f.destination,
                   f.departure_time, b.total_price, b.status
            FROM booking b
            JOIN flight f ON b.flight_id = f.flight_id
            JOIN airline a ON b.airline_id = a.airline_id
            WHERE b.passenger_id = %s
            """
            cursor.execute(query, (user_id,))
        else:  # airline
            query = """
            SELECT b.booking_id, b.passenger_id, p.name, f.flight_id,
                   f.origin, f.destination, f.departure_time, b.status
            FROM booking b
            JOIN flight f ON b.flight_id = f.flight_id
            JOIN passenger p ON b.passenger_id = p.passenger_id
            WHERE b.airline_id = %s
            """
            cursor.execute(query, (user_id,))

        bookings = cursor.fetchall()
        return bookings
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()

def add_flight(airline_id, origin, destination, departure_time, arrival_time, 
               capacity, price):
    try:
        db = connect_to_database()
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM flight")
        flight_count = cursor.fetchone()[0] + 1
        flight_id = f"FL_{flight_count}"

        query = """
        INSERT INTO flight (flight_id, airline_id, origin, destination, 
                          departure_time, arrival_time, capacity, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (flight_id, airline_id, origin, destination,
                             departure_time, arrival_time, capacity, price))
        db.commit()
        st.success("Flight added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()

def get_booking_details(booking_id):
    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = """
        SELECT b.booking_id, p.name, f.flight_id, a.airline_name, 
               f.origin, f.destination, f.departure_time, pd.passenger_name,
               pd.seat_number, pd.meal_preference, b.status
        FROM booking b
        JOIN passenger p ON b.passenger_id = p.passenger_id
        JOIN flight f ON b.flight_id = f.flight_id
        JOIN airline a ON b.airline_id = a.airline_id
        JOIN passenger_details pd ON b.booking_id = pd.booking_id
        WHERE b.booking_id = %s AND b.status = 'Confirmed'
        """
        cursor.execute(query, (booking_id,))
        return cursor.fetchall()
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()

def update_flight(flight_id, origin, destination, departure_time, arrival_time, capacity, price):
    try:
        db = connect_to_database()
        cursor = db.cursor()

        query = """
        UPDATE flight
        SET origin = %s, destination = %s, departure_time = %s, arrival_time = %s, 
            capacity = %s, price = %s
        WHERE flight_id = %s
        """
        cursor.execute(query, (origin, destination, departure_time, arrival_time, capacity, price, flight_id))
        db.commit()
        st.success("Flight updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()