import streamlit as st
from config.database import connect_to_database
from mysql.connector import Error

def print_boarding_pass(booking_details):
    if len(booking_details) < 5:
        raise ValueError("Insufficient booking details provided")
    
    st.write(f"**Boarding Pass:**")
    st.write(f"**Passenger:** {booking_details[0]}")
    st.write(f"**Flight:** {booking_details[1]}")
    st.write(f"**Seat:** {booking_details[2]}")
    st.write(f"**Departure:** {booking_details[3]}")
    st.write(f"**Arrival:** {booking_details[4]}")

def get_food_menu():
    try:
        db = connect_to_database()
        if db is None:
            return []
        cursor = db.cursor()
        cursor.execute("SELECT food_id, food_name, price FROM food_menu")
        food_menu = cursor.fetchall()
        return food_menu
    except Error as e:
        st.error(f"Error: {e}")
        return []
    finally:
        if db:
            db.close()

def handle_print_ticket():
    st.header("Print Boarding Pass")
    booking_id = st.text_input("Enter Booking ID")
    if booking_id:
        booking_details = get_booking_details(booking_id)
        if booking_details:
            print(f"Booking Details: {booking_details}")  # Debugging statement
            print_boarding_pass(booking_details)
        else:
            st.error("No confirmed booking found with this ID")