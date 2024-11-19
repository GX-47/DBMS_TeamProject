import streamlit as st

def display_sidebar_menu():
    st.sidebar.title("Menu")
    if st.session_state.user_type == "passenger":
        return st.sidebar.radio("Choose an option", ["Book Flight", "View My Bookings"])
    elif st.session_state.user_type == "airline":
        return st.sidebar.radio("Choose an option", ["Dashboard", "Add Flight", "Edit Flight", "View Bookings"])
    elif st.session_state.user_type == "frontdesk":
        return st.sidebar.radio("Choose an option", ["Print Ticket", "Register Luggage"])
    elif st.session_state.user_type == "admin":
        return st.sidebar.radio("Choose an option", ["User Management"])
    else:
        return st.sidebar.radio("Choose an option", ["Login", "Signup"])