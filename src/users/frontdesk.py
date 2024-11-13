import streamlit as st
from models.flight import get_booking_details
from models.luggage import register_luggage
from models.utils import print_boarding_pass

def handle_print_ticket():
    st.header("Print Boarding Pass")
    booking_id = st.text_input("Enter Booking ID")
    if booking_id:
        booking_details = get_booking_details(booking_id)
        if booking_details:
            print_boarding_pass(booking_details)
        else:
            st.error("No confirmed booking found with this ID")

def handle_register_luggage():
    st.header("Register Luggage")
    booking_id = st.text_input("Enter Booking ID")
    
    if booking_id:
        booking_details = get_booking_details(booking_id)
        if booking_details:
            st.success("Booking found!")
            weight = st.number_input("Luggage Weight (kg)", min_value=0.0, max_value=50.0)
            category = st.selectbox("Luggage Category", 
                                  ["Regular", "Fragile", "Sports Equipment", "Musical Instrument"])
            handling_instructions = st.text_area("Special Handling Instructions")
            
            if st.button("Register Luggage"):
                luggage_id = register_luggage(booking_id, weight, category,
                                            handling_instructions, st.session_state.user_id)
                if luggage_id:
                    st.success(f"Luggage registered successfully! Luggage ID: {luggage_id}")
        else:
            st.error("No confirmed booking found with this ID")