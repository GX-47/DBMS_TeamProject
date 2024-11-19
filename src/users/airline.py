import streamlit as st
from models.flight import get_available_flights, add_flight, update_flight, view_bookings
from datetime import datetime
from config.database import connect_to_database
from mysql.connector import Error

def handle_add_flight():
    st.header("Add New Flight")
    origin = st.text_input("Origin")
    destination = st.text_input("Destination")
    departure_date = st.date_input("Departure Date")
    departure_time = st.time_input("Departure Time")
    arrival_date = st.date_input("Arrival Date")
    arrival_time = st.time_input("Arrival Time")
    
    # Combine date and time
    departure_datetime = datetime.combine(departure_date, departure_time)
    arrival_datetime = datetime.combine(arrival_date, arrival_time)
    
    capacity = st.number_input("Capacity", min_value=1, value=180)
    price = st.number_input("Price", min_value=0.0, value=5000.0)
    
    if st.button("Add Flight"):
        add_flight(st.session_state.user_id, origin, destination,
                  departure_datetime, arrival_datetime, capacity, price)

def handle_edit_flight():
    st.header("Edit Flight")
    flights = get_available_flights()
    
    if flights:
        flight_options = [f"{flight[0]} - {flight[8]} - {flight[2]} to {flight[3]} - ₹{flight[7]}"
                        for flight in flights]
        selected_flight = st.selectbox("Select Flight to Edit", flight_options)
        
        if selected_flight:
            flight_id = selected_flight.split('-')[0].strip()
            selected_flight_data = next(f for f in flights if f[0] == flight_id)
            
            origin = st.text_input("Origin", value=selected_flight_data[2])
            destination = st.text_input("Destination", value=selected_flight_data[3])
            departure_date = st.date_input("Departure Date", value=selected_flight_data[4].date())
            departure_time = st.time_input("Departure Time", value=selected_flight_data[4].time())
            arrival_date = st.date_input("Arrival Date", value=selected_flight_data[5].date())
            arrival_time = st.time_input("Arrival Time", value=selected_flight_data[5].time())
            
            # Combine date and time
            departure_datetime = datetime.combine(departure_date, departure_time)
            arrival_datetime = datetime.combine(arrival_date, arrival_time)
            
            capacity = st.number_input("Capacity", min_value=1, value=selected_flight_data[6])
            price = st.number_input("Price", min_value=0.0, value=float(selected_flight_data[7]))
            
            if st.button("Update Flight"):
                update_flight(flight_id, origin, destination, departure_datetime, arrival_datetime, capacity, price)

def handle_view_flight_bookings():
    st.header("Flight Bookings")
    bookings = view_bookings(st.session_state.user_id, "airline")
    if bookings:
        for booking in bookings:
            st.write(f"""
            Booking ID: {booking[0]}
            Passenger ID: {booking[1]}
            Passenger Name: {booking[2]}
            Flight ID: {booking[3]}
            Route: {booking[4]} to {booking[5]}
            Departure: {booking[6]}
            Status: {booking[7]}
            """)
            
            # Add option to confirm booking
            if booking[7] == "Pending":
                if st.button(f"Confirm Booking {booking[0]}", key=booking[0]):
                    try:
                        db = connect_to_database()
                        cursor = db.cursor()
                        cursor.callproc('ConfirmBooking', [booking[1]])
                        db.commit()
                        st.success(f"Booking {booking[0]} confirmed successfully!")
                        st.rerun()
                    except Error as e:
                        st.error(f"Error: {e}")
                    finally:
                        if db:
                            db.close()
            
            st.markdown("---")

def handle_airline_dashboard():
    st.header("Airline Dashboard")
    
    try:
        db = connect_to_database()
        cursor = db.cursor()

        # Display Airline Metrics (Aggregate Query)
        cursor.execute("""
            SELECT * FROM airline_metrics 
            WHERE airline_id = %s
        """, (st.session_state.user_id,))
        metrics = cursor.fetchone()
        
        if metrics:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Flights", metrics[2])
            with col2:
                st.metric("Total Bookings", metrics[3])
            with col3:
                st.metric("Average Bookings/Flight", f"{metrics[6] / 100}")
            
            st.metric("Total Revenue", f"₹{metrics[5]:,.2f}")
        
        # Display Premium Flights (Nested Query)
        st.subheader("Premium Flights")
        cursor.execute("SELECT * FROM expensive_flights WHERE airline_id = %s", 
                      (st.session_state.user_id,))
        premium_flights = cursor.fetchall()
        
        if premium_flights:
            for flight in premium_flights:
                st.write(f"""
                Flight {flight[0]}: {flight[2]} to {flight[3]}
                Price: ₹{flight[7]:,.2f} ({flight[-1]} above average)
                """)
        else:
            st.write("No premium flights available.")
    finally:
        if db:
            db.close()
