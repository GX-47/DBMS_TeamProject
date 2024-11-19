import streamlit as st
from mysql.connector import Error
from config.database import connect_to_database

def signup_passenger(name, phone, email, password):
    try:
        db = connect_to_database()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM passenger")
        passenger_count = cursor.fetchone()[0] + 1
        passenger_id = f"P_{passenger_count}"
        
        query = """
        INSERT INTO passenger (passenger_id, phone, name, email, password)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (passenger_id, phone, name, email, password))
        db.commit()

        st.success("Passenger registered successfully!")
        st.info(f"Your passenger ID: {passenger_id}")
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if db:
            db.close()