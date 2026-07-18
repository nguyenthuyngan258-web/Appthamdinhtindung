import streamlit as st
import mysql.connector

# Hàm kết nối database
def get_connection():
    return mysql.connector.connect(
        host="your-aiven-host-url",
        user="avnadmin",
        password="your-password",
        database="defaultdb",
        port=22830, # Port của Aiven thường khác mặc định
        ssl_ca="path_to_ca_cert" # Aiven yêu cầu SSL
    )

# Lưu hồ sơ vào database
def save_to_db(name, dti, ltv):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO credit_records (name, dti, ltv) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, dti, ltv))
    conn.commit()
    cursor.close()
    conn.close()
