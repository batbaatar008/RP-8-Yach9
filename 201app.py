import streamlit as st
import pandas as pd

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="Эрчим Хүчний Тооцоолуур", layout="wide")

# 2. Дамжуулагчийн өгөгдлийн сан (R20 - Ом/км)
CONDUCTOR_DATA = {
    "СИП-2 3х16": {"R20": 1.91, "alpha": 0.00403, "I_max": 100},
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403, "I_max": 130},
    "СИП-2 3х35": {"R20": 0.868, "alpha": 0.00403, "I_max": 160},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403, "I_max": 195},
    "СИП-2 3х70": {"R20": 0.443, "alpha": 0.00403, "I_max": 240},
    "АС-25/4.2": {"R20": 1.15, "alpha": 0.00403, "I_max": 125},
    "АС-50/8.0": {"R20": 0.595, "alpha": 0.00403, "I_max": 210}
}

st.title("⚡ КТП-201: Техникийн Алдагдал Тооцоолуур V4.3")

# --- SIDEBAR: Удирдлага ---
with st.sidebar:
    st.header("📂 Оролтын өгөгдөл")
    main_meter = st.number_input("Толгой тоолуур (кВт.цаг):", value=555578.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=524270.0)
    hours = st.number_input("Хугацаа (цаг):", value=720.0)
    st.divider()
    temp = st.slider("Ажлын температур (°C):", -40, 50, 20)
    cos_phi = st.slider("Чадлын коэффициент (cosφ):", 0.7, 1.0, 0.9)

# --- ДЭЭД ХЭСЭГ: Үр дүнгийн хураангуй ---
total_loss = main_meter - users_sum
m1, m2, m3 = st.columns(3)
m1.metric
