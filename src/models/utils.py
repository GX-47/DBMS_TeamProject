import streamlit as st

def print_boarding_pass(booking_details):
    if len(booking_details) < 2:
        raise ValueError("Insufficient booking details provided")
    
    print(f"Boarding Pass:\n"
          f"Passenger: {booking_details[0]}\n"
          f"Flight: {booking_details[1]}\n"
          f"Seat: {booking_details[2]}\n"
          f"Departure: {booking_details[3]}\n"
          f"Arrival: {booking_details[4]}")

def get_food_menu():
    return [
        (1, "Sandwich", 150),
        (2, "Burger", 200),
        (3, "Pasta", 250),
        (4, "Salad", 100),
        (5, "Juice", 50)
    ]