import streamlit as st
import mysql.connector
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Cấu hình Page
st.set_page_config(page_title="Hệ thống Thẩm định Tín dụng", layout="wide")

# Hàm kết nối Database (Sử dụng Streamlit Secrets)
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )

# Sidebar Menu
with st.sidebar:
    selected = option_menu("Menu", ["Thẩm định", "Lịch sử"], icons=['calculator', 'database'])

# Logic Thẩm định
if selected == "Thẩm định":
    st.title("💳 Hệ thống Thẩm định Vay")
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Tên khách hàng")
        so_tien = st.number_input("Số tiền vay (Triệu)", 10, 5000)
        thu_nhap = st.number_input("Thu nhập (Triệu)", 5, 500)
    with c2:
        lai_suat = st.slider("Lãi suất (%/năm)", 5.0, 20.0, 10.0)
        tsdb = st.number_input("Giá trị TSĐB (Triệu)", 0, 10000)
        
    if st.button("Lưu hồ sơ vào Database"):
        dti = (so_tien / (thu_nhap + 1)) # Logic đơn giản
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO credit_records (name, amount, dti) VALUES (%s, %s, %s)", (name, so_tien, dti))
        conn.commit()
        st.success("Đã lưu hồ sơ thành công!")
        conn.close()

# Logic Hiển thị Lịch sử
elif selected == "Lịch sử":
    st.title("📂 Lịch sử thẩm định")
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM credit_records", conn)
    st.table(df)
    conn.close()
