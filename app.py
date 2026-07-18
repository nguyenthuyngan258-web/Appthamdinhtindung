import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Credit Vision Pro", layout="wide")

# --- HÀM TÍNH TOÁN CỐT LÕI ---
def calculate_metrics(so_tien, lai_suat, ky_han, thu_nhap, du_no, tsdb):
    r = lai_suat / 100 / 12
    pmt = (so_tien * r * (1 + r)**ky_han) / ((1 + r)**ky_han - 1)
    dti = ((du_no + pmt) / (thu_nhap + 1)) * 100
    ltv = (so_tien / (tsdb + 1)) * 100
    return pmt, dti, ltv

# --- GIAO DIỆN CHÍNH ---
with st.sidebar:
    menu = option_menu("Ngân hàng số", ["Thẩm định", "Lịch sử", "Stress Test"], icons=['calculator', 'list', 'shield-lock'])

# --- PAGE 1: THẨM ĐỊNH ---
if menu == "Thẩm định":
    st.title("💳 Hệ thống Thẩm định Tín dụng")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Tên khách hàng")
        so_tien = st.number_input("Số tiền vay (Tr)", 10, 5000, 500)
        thu_nhap = st.number_input("Thu nhập (Tr)", 5, 500, 30)
    with col2:
        lai_suat = st.slider("Lãi suất (%)", 5.0, 20.0, 9.5)
        cic = st.selectbox("Điểm CIC", ["Nhóm 1", "Nhóm 2", "Nhóm 3+"])
        tsdb = st.number_input("Giá trị TSĐB (Tr)", 0, 10000, 1000)

    if st.button("🚀 Thẩm định ngay"):
        pmt, dti, ltv = calculate_metrics(so_tien, lai_suat, 60, thu_nhap, 0, tsdb)
        
        # Lưu vào session_state
        st.session_state.history = getattr(st.session_state, 'history', pd.DataFrame())
        new_row = {"Tên": name, "DTI": dti, "LTV": ltv, "Kết quả": "Đạt" if dti < 45 else "Từ chối"}
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])])
        
        # UI WOW
        m1, m2, m3 = st.columns(3)
        m1.metric("DTI", f"{dti:.1f}%")
        m2.metric("LTV", f"{ltv:.1f}%")
        m3.metric("Số tiền trả/tháng", f"{pmt:,.0f} Tr")
        
        fig = go.Figure(go.Indicator(mode="gauge+number", value=dti, gauge={'axis': {'range': [0, 100]}}))
        st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: LỊCH SỬ ---
elif menu == "Lịch sử":
    st.title("📂 Nhật ký thẩm định")
    if 'history' in st.session_state:
        st.table(st.session_state.history)
    else:
        st.info("Chưa có hồ sơ nào được thẩm định.")

# --- PAGE 3: STRESS TEST (Sáng tạo) ---
elif menu == "Stress Test":
    st.title("🛡️ Kiểm tra sức chịu đựng (Stress Test)")
    st.write("Nếu lãi suất thị trường tăng thêm 3%, khách hàng có khả năng trả nợ không?")
    st.button("Mô phỏng kịch bản khủng hoảng")
    # Biểu đồ đường so sánh lãi suất hiện tại vs lãi suất +3%
