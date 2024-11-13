import streamlit as st
from models.auth import authenticate_user, authenticate_frontdesk, authenticate_airline, authenticate_admin
from models.passenger import signup_passenger

def handle_login():
    st.header("Login")
    login_option = st.radio("Login as", ["Passenger", "Airline", "Front Desk", "Admin"])
    email = st.text_input("Login ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_option == "Front Desk":
            user = authenticate_frontdesk(email, password)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.user_type = "frontdesk"
                st.session_state.should_rerun = True
                st.rerun()
        elif login_option == "Admin":
            user = authenticate_admin(email, password)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.user_type = "admin"
                st.session_state.should_rerun = True
                st.rerun()
        elif login_option == "Airline":
            user = authenticate_airline(email, password)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.user_type = "airline"
                st.session_state.should_rerun = True
                st.rerun()
        elif login_option == "Passenger":
            user = authenticate_user(email, password)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.user_type = "passenger"
                st.session_state.should_rerun = True
                st.rerun()

def handle_signup():
    st.header("Passenger Signup")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        signup_passenger(name, phone, email, password)