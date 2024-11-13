import streamlit as st

def initialize_session_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_type" not in st.session_state:
        st.session_state.user_type = None
    if "should_rerun" not in st.session_state:
        st.session_state.should_rerun = False

def handle_rerun():
    if st.session_state.should_rerun:
        st.session_state.should_rerun = False
        st.rerun()

def handle_logout():
    if st.session_state.user_id:
        if st.sidebar.button("Logout"):
            st.session_state.user_id = None
            st.session_state.user_type = None
            st.rerun()