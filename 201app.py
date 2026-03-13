import streamlit as st
import pandas as pd
import math

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="КТП-201: 4-Гаргалгаатай Тооцоо", layout="wide")

# 2. Дамжуулагчийн өгөгдөл
CONDUCTOR_DATA = {
    "СИП-2 3х16": {"R20": 1.91, "alpha": 0.00403},
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403},
    "СИП-2 3х35": {"R20": 0.868, "alpha": 0.00403},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403},
    "СИП-2 3х70": {"R20": 0.443, "alpha": 0.00403}
}

st.title("⚡ КТП-201: 4-Гаргалгаатай Нарийвчилсан Тооцоо V8.0")

# --- SIDEBAR: Ерөнхий өгөгдөл ---
with st.sidebar:
    st.header("📂 Ерөнхий тохиргоо")
    total_p_kwh = st.number_input("Толгой тоолуур (кВт.цаг):", value=259148.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=178040.0)
    hours = st.number_input("Хугацаа (цаг):", value=720.0)
    st.divider()
    m_voltage = st.number_input("Магистраль хүчдэл (В):", value=400)
    cos_phi = st.slider("cosφ:", 0.7, 1.0, 0.9)
    temp = st.slider("Температура (°C):", -40, 50, 20)

# --- ГАРГАЛГААНУУДЫН ТАБ (TABS) ---
t1, t2, t3, t4 = st.tabs(["1-р Гаргалгаа", "2-р Гаргалгаа", "3-р Гаргалгаа", "4-р Гаргалгаа"])
tabs = [t1, t2, t3, t4]
feeder_data_frames = []

for i in range(4):
    with tabs[i]:
        st.subheader(f"📍 {i+1}-р гаргалгааны шугамын бүтэц")
        
        # Анхны загвар өгөгдөл
        df_template = pd.DataFrame([
            {"Тулгуур": "1-2", "Төрөл": "Магистраль (3ф)", "Марк": "СИП-2 3х50", "Урт
