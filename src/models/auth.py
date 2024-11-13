import streamlit as st
from mysql.connector import Error
from config.database import connect_to_database

def authenticate_user(email, password):
    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = "SELECT * FROM passenger WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        passenger = cursor.fetchone()
        return passenger if passenger else None
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()

def authenticate_frontdesk(staff_id, password):
    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = "SELECT * FROM frontdesk_staff WHERE staff_id = %s AND password = %s"
        cursor.execute(query, (staff_id, password))
        staff = cursor.fetchone()
        return staff if staff else None
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()

def authenticate_airline(airline_id, password):
    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = "SELECT * FROM airline WHERE airline_id = %s AND password = %s"
        cursor.execute(query, (airline_id, password))
        staff = cursor.fetchone()
        return staff if staff else None
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()

def authenticate_admin(admin_id, password):
    try:
        db = connect_to_database()
        cursor = db.cursor()

        query = "SELECT admin_id FROM admin WHERE admin_id = %s AND password = %s"
        cursor.execute(query, (admin_id, password))
        user = cursor.fetchone()
        return user
    except Error as e:
        return None
    finally:
        if db:
            db.close()

def create_user(name, email, password, phone, user_type):
    if user_type == "passenger":
        return False, "Creating passenger users is not allowed."
    
    try:
        db = connect_to_database()
        cursor = db.cursor()

        query = """
        INSERT INTO users (name, email, password, phone, user_type)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, password, phone, user_type))
        db.commit()
        return True, "User created successfully!"
    except Error as e:
        return False, str(e)
    finally:
        if db:
            db.close()

def delete_user(user_id, user_type):
    try:
        db = connect_to_database()
        cursor = db.cursor()

        if user_type == "passenger":
            query = "DELETE FROM passenger WHERE passenger_id = %s"
        elif user_type == "airline":
            query = "DELETE FROM airline WHERE airline_id = %s"
        elif user_type == "frontdesk":
            query = "DELETE FROM frontdesk_staff WHERE staff_id = %s"
        else:
            return False, "Invalid user type."

        cursor.execute(query, (user_id,))
        db.commit()
        return True, "User deleted successfully!"
    except Error as e:
        return False, str(e)
    finally:
        if db:
            db.close()

def get_users_by_type(user_type):
    try:
        db = connect_to_database()
        cursor = db.cursor()

        if user_type == "passenger":
            query = "SELECT passenger_id, name FROM passenger"
        elif user_type == "airline":
            query = "SELECT airline_id, airline_name FROM airline"
        elif user_type == "frontdesk":
            query = "SELECT staff_id, name FROM frontdesk_staff"
        else:
            return []

        cursor.execute(query)
        user_details = cursor.fetchall()
        return user_details
    except Error as e:
        st.error(f"Error: {e}")
        return []
    finally:
        if db:
            db.close()