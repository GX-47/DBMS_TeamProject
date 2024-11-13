"""
src
├── config
│   ├── .env: Stores sensitive information such as database credentials.
│   └── database.py: Contains functions to connect to the database.
├── models
│   ├── passenger.py: Contains functions related to passenger operations such as signup.
│   ├── auth.py: Contains functions for user authentication.
│   ├── flight.py: Contains functions related to flight operations such as booking and viewing flights.
│   ├── luggage.py: Contains functions for registering luggage.
│   └── utils.py: Contains utility functions such as printing boarding passes and getting the food menu.
├── users
│   ├── sidebar.py: Contains functions to display the sidebar menu in the Streamlit application.
│   ├── login.py: Contains functions to handle user login and signup processes.
│   ├── passenger.py: Contains functions for passenger-specific operations such as booking flights and viewing bookings.
│   ├── airline.py: Contains functions for airline-specific operations such as adding, editing, and viewing flights.
│   ├── frontdesk.py: Contains functions for front desk operations such as printing tickets and registering luggage.
│   ├── admin.py: Contains functions for admin operations such as user management.
│   └── utils.py: Contains utility functions for user operations such as initializing session state, handling reruns, and logging out.
├── main.py: The main entry point of the Streamlit application, handling user interactions and displaying the UI.
└── db.sql: Contains the SQL schema for the database.
"""

import streamlit as st
from users.sidebar import display_sidebar_menu
from users.login import handle_login, handle_signup
from users.passenger import handle_book_flight, handle_view_bookings
from users.airline import handle_add_flight, handle_edit_flight, handle_view_flight_bookings
from users.frontdesk import handle_print_ticket, handle_register_luggage
from users.admin import handle_user_management
from users.utils import initialize_session_state, handle_rerun, handle_logout

def main():
    initialize_session_state()
    handle_rerun()
    menu_option = display_sidebar_menu()

    if st.session_state.user_id is None:
        if menu_option == "Login":
            handle_login()
        elif menu_option == "Signup":
            handle_signup()
    else:
        if menu_option == "Book Flight" and st.session_state.user_type == "passenger":
            handle_book_flight()
        elif menu_option == "View My Bookings" and st.session_state.user_type == "passenger":
            handle_view_bookings()
        elif menu_option == "Add Flight" and st.session_state.user_type == "airline":
            handle_add_flight()
        elif menu_option == "Edit Flight" and st.session_state.user_type == "airline":
            handle_edit_flight()
        elif menu_option == "View Bookings" and st.session_state.user_type == "airline":
            handle_view_flight_bookings()
        elif menu_option == "Print Ticket" and st.session_state.user_type == "frontdesk":
            handle_print_ticket()
        elif menu_option == "Register Luggage" and st.session_state.user_type == "frontdesk":
            handle_register_luggage()
        elif menu_option == "User Management" and st.session_state.user_type == "admin":
            handle_user_management()

    handle_logout()

if __name__ == "__main__":
    main()