import streamlit as st
from models.auth import create_user, delete_user, get_users_by_type

def handle_user_management():
    st.header("User Management")
    user_management_option = st.radio("Choose an option", ["Create User", "Delete User"])

    if user_management_option == "Create User":
        st.subheader("Create User")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        phone = st.text_input("Phone")
        user_type = st.selectbox("User Type", ["airline", "frontdesk"])

        if st.button("Create User"):
            success, message = create_user(name, email, password, phone, user_type)
            if success:
                st.success("User created successfully!")
            else:
                st.error(f"Error: {message}")

    elif user_management_option == "Delete User":
        st.subheader("Delete User")
        user_type = st.selectbox("Select User Type", ["airline", "frontdesk", "passenger"])
        users = get_users_by_type(user_type)
        user_options = [f"{user[0]} - {user[1]}" for user in users]
        selected_user = st.selectbox("Select User", user_options)

        if selected_user:
            user_id = selected_user.split('-')[0].strip()
            if st.button("Delete User"):
                success, message = delete_user(user_id, user_type)
                if success:
                    st.success("User deleted successfully!")
                else:
                    st.error(f"Error: {message}")