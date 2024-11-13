import mysql.connector
from mysql.connector import Error
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_database():
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return db
    except Error as e:
        st.error(f"Error: {e}")
        return None