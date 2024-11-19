import streamlit as st
from mysql.connector import Error
from config.database import connect_to_database
import uuid

def register_luggage(booking_id, weight, category, handling_instructions, user_id):
    try:
        db = connect_to_database()
        cursor = db.cursor()
        luggage_id = str(uuid.uuid4())[:10]  # Generate a unique ID
        query = """
        INSERT INTO luggage (luggage_id, booking_id, weight, category, handling_instructions, staff_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (luggage_id, booking_id, weight, category, handling_instructions, user_id))
        db.commit()
        return luggage_id
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if db:
            db.close()