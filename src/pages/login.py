import streamlit as st
from config.database import execute_query

def show_login_page():
    """Display the login page."""
    st.title("Login")

    user_type = st.selectbox("Select User Type", ["Customer", "Staff"])
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if user_type == "Customer":
            if validate_customer_login(user_id, password):
                st.success("Login successful!")
                # Redirect to customer dashboard
            else:
                st.error("Invalid Customer ID or Password")
        elif user_type == "Staff":
            if validate_staff_login(user_id, password):
                st.success("Login successful!")
                # Redirect to staff dashboard
            else:
                st.error("Invalid Staff ID or Password")

def handle_logout():
    """Handle user logout."""
    st.session_state.logged_in = False
    st.success("Logged out successfully!")

def validate_customer_login(passenger_id, password):
    """Validate customer login credentials."""
    query = "SELECT * FROM passengers WHERE passenger_id = %s AND password = %s"
    result = execute_query(query, (passenger_id, password))
    return len(result) > 0

def validate_staff_login(staff_id, password):
    """Validate staff login credentials."""
    query = "SELECT * FROM staff_login WHERE staff_id = %s AND password = %s"
    result = execute_query(query, (staff_id, password))
    return len(result) > 0