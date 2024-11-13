import streamlit as st
from models.flight import get_available_flights, book_flight, view_bookings
from models.utils import get_food_menu

def handle_book_flight():
    st.header("Book Flight")
    flights = get_available_flights()
    
    if flights:
        flight_options = [f"{flight[0]} - {flight[8]} - {flight[2]} to {flight[3]} - ₹{flight[7]}"
                        for flight in flights]
        selected_flight = st.selectbox("Select Flight", flight_options)
        
        if selected_flight:
            flight_id = selected_flight.split('-')[0].strip()
            selected_flight_data = next(f for f in flights if f[0] == flight_id)
            
            num_passengers = st.number_input("Number of Passengers", 1, 5, 1)
            passenger_details = []
            
            for i in range(num_passengers):
                st.subheader(f"Passenger {i+1}")
                name = st.text_input(f"Name", key=f"name_{i}")
                seat = st.selectbox(f"Seat Preference", ["Window", "Middle", "Aisle"], key=f"seat_{i}")
                meal = st.selectbox(f"Meal Preference", 
                                  ['Vegetarian', 'Non-Vegetarian', 'None'],
                                  key=f"meal_{i}")
                passenger_details.append((name, seat, meal))
            
            st.subheader("Food Order")
            food_menu = get_food_menu()
            food_orders = {}
            for food in food_menu:
                quantity = st.number_input(f"{food[1]} (₹{food[2]})", min_value=0, key=f"food_{food[0]}")
                if quantity > 0:
                    food_orders[food[0]] = quantity

            if st.button("Book Now"):
                booking_id = book_flight(st.session_state.user_id, flight_id,
                                      selected_flight_data[1], passenger_details, food_orders)
                if booking_id:
                    st.info(f"Booking ID: {booking_id}")

def handle_view_bookings():
    st.header("My Bookings")
    bookings = view_bookings(st.session_state.user_id, "passenger")
    if bookings:
        for booking in bookings:
            st.write(f"""
            Booking ID: {booking[0]}
            Flight: {booking[1]}
            Airline: {booking[2]}
            Route: {booking[3]} to {booking[4]}
            Departure: {booking[5]}
            Total Price: ₹{booking[6]}
            Status: {booking[7]}
            """)
            st.markdown("---")