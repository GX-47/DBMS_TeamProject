import streamlit as st
from mysql.connector import Error
from config.database import connect_to_database

def register_luggage(booking_id, weight, category, handling_instructions, user_id):
    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = "INSERT INTO luggage (booking_id, weight, category, handling_instructions, registered_by) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (booking_id, weight, category, handling_instructions, user_id))
        luggage_id = cursor.lastrowid
        db.commit()
        return luggage_id
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if db:
            db.close()