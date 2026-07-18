import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Credit Command Center", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .big-font {font-size:30px !important; color:#2c3e50;}
    .stMetric {background-color:#ffffff; padding:15px; border-radius:10px; border-left: 5px solid #2980b9;}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR MENU ---
with st.sidebar:
    selected = option_menu("Hệ thống thẩm định", ["Dashboard", "Thẩm định chi tiết", "Xuất báo cáo"],
                           icons=['speedometer2', 'calculator', 'file-earmark-pdf'], menu_icon="bank", default_index=0)

# --- LOGIC TÍNH TOÁN ---
def calculate_score(dti, cic, ltv):
    score = 100
    if dti > 45: score -= 30
    if "Xấu" in cic: score -= 50
    if ltv > 80: score -= 20
    return max(0, score)

# --- PAGE: DASHBOARD ---
if selected == "Dashboard":
    st.title("🏦 Credit Command Center")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng hạn mức", "500 tỷ", "12%")
    col2.metric("Số hồ sơ chờ", "45", "5")
    col3.metric("Tỷ lệ duyệt", "78%", "-2%")
    st.info("Chào mừng quay lại, chuyên viên tín dụng! Hệ thống đang hoạt động ổn định.")

# --- PAGE: THẨM ĐỊNH CHI TIẾT ---
elif selected == "Thẩm định chi tiết":
    st.subheader("Nhập thông tin thẩm định")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        thu_nhap = st.number_input("Thu nhập (Tr)", 5, 1000, 30)
        so_tien = st.number_input("Số tiền vay (Tr)", 10, 5000, 500)
    with c2:
        lai_suat = st.slider("Lãi suất (%)", 5.0, 20.0, 9.5)
        ky_han = st.number_input("Kỳ hạn (Tháng)", 6, 360, 60)
    with c3:
        tsdb = st.number_input("Giá trị TSĐB (Tr)", 0, 10000, 1000)
        cic = st.selectbox("Tình trạng CIC", ["Tốt", "Trung bình", "Xấu"])

    # Tính toán
    tra_gop = (so_tien * (lai_suat/100/12)) / (1 - (1 + lai_suat/100/12)**-ky_han)
    dti = (tra_gop / (thu_nhap + 1)) * 100
    ltv = (so_tien / (tsdb + 1)) * 100
    score = calculate_score(dti, cic, ltv)

    # Visualization
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = score,
        title = {'text': "Credit Health Score"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#2980b9"}}))
    st.plotly_chart(fig, use_container_width=True)

    # Hiển thị bảng chi tiết
    st.write(f"### Kết quả đánh giá: {'ĐẠT' if score > 60 else 'TỪ CHỐI'}")
    st.progress(score/100)

# --- PAGE: XUẤT BÁO CÁO ---
elif selected == "Xuất báo cáo":
    st.subheader("Tạo tài liệu phê duyệt")
    if st.button("Tạo file PDF hồ sơ"):
        st.success("Đang tạo file... Vui lòng đợi trong giây lát!")
        st.balloons()
