import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import requests
from streamlit_lottie import st_lottie

# Cấu hình Page
st.set_page_config(page_title="Credit Vision Pro", layout="wide")

# Hàm lấy animation Lottie cho chuyên nghiệp
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# --- UI Customization ---
st.markdown("""<style>
    .main {background-color: #f5f7f9;}
    .stMetric {background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>""", unsafe_allow_html=True)

# --- SIDEBAR: LOGIC NHẬP LIỆU ---
with st.sidebar:
    st.title("🏦 Input Data")
    so_tien_vay = st.number_input("Số tiền vay (Triệu VNĐ)", 10, 10000, 500)
    thoi_han = st.slider("Thời gian vay (Tháng)", 6, 360, 60)
    lai_suat = st.number_input("Lãi suất (%/năm)", 1.0, 30.0, 10.0)
    thu_nhap = st.number_input("Thu nhập hàng tháng (Triệu)", 5, 500, 30)
    du_no_cu = st.number_input("Dư nợ hiện tại (Triệu)", 0, 1000, 0)
    gia_tri_tsdb = st.number_input("Giá trị TSĐB (Triệu)", 0, 20000, 1000)
    cic = st.selectbox("Điểm CIC", ["Nhóm 1 - Tốt", "Nhóm 2 - Cần lưu ý", "Nhóm 3+ - Xấu"])

# --- MAIN CONTENT ---
st.title("📊 Hệ thống Thẩm định Tín dụng Cá nhân")
c1, c2 = st.columns([1, 2])

# Logic Tính toán
r = lai_suat / 100 / 12
tra_gop = (so_tien_vay * r * (1 + r)**thoi_han) / ((1 + r)**thoi_han - 1)
dti = ((du_no_cu + tra_gop) / (thu_nhap + 1)) * 100
ltv = (so_tien_vay / (gia_tri_tsdb + 1)) * 100

with c1:
    st.subheader("Kết quả thẩm định")
    st.metric("Tỷ lệ DTI", f"{dti:.1f}%")
    st.metric("Tỷ lệ LTV", f"{ltv:.1f}%")
    if dti < 40 and "Nhóm 1" in cic:
        st.success("✅ ĐỦ ĐIỀU KIỆN")
    else:
        st.error("⚠️ CẦN XEM XÉT")

with c2:
    st.subheader("Phân tích dòng tiền trả nợ")
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=dti,
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1e3d59"}, 
               'steps': [{'range': [0, 40], 'color': "lightgreen"}, {'range': [40, 70], 'color': "yellow"}]}))
    st.plotly_chart(fig, use_container_width=True)

# --- TÍNH NĂNG WOW: LỊCH TRẢ NỢ ---
if st.checkbox("Hiển thị chi tiết Lịch trả nợ"):
    schedule = []
    balance = so_tien_vay
    for i in range(1, thoi_han + 1):
        interest = balance * (lai_suat/100/12)
        principal = tra_gop - interest
        balance -= principal
        schedule.append([i, principal, interest, tra_gop])
    df = pd.DataFrame(schedule, columns=["Tháng", "Gốc", "Lãi", "Tổng trả"])
    st.table(df.head(12)) # Hiện 12 tháng đầu
