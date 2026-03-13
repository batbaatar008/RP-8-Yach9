import streamlit as st
import pandas as pd

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="КТП-201 Нарийвчилсан Тооцоо", layout="wide")

# 2. Дамжуулагчийн өгөгдлийн сан
CONDUCTOR_DATA = {
    "СИП-2 3х16": {"R20": 1.91, "alpha": 0.00403, "I_max": 100},
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403, "I_max": 130},
    "СИП-2 3х35": {"R20": 0.868, "alpha": 0.00403, "I_max": 160},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403, "I_max": 195},
    "АС-25/4.2": {"R20": 1.15, "alpha": 0.00403, "I_max": 125},
    "АС-50/8.0": {"R20": 0.595, "alpha": 0.00403, "I_max": 210}
}

st.title("⚡ КТП-201: Техникийн Алдагдал (Хэрэглэгчийн ангиллаар) V4.6")

# --- SIDEBAR: Удирдлага ---
with st.sidebar:
    st.header("📂 Ерөнхий өгөгдөл")
    main_meter = st.number_input("Толгой тоолуур (кВт.цаг):", value=259148.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=178040.0)
    hours = st.number_input("Хугацаа (цаг):", value=720.0)
    st.divider()
    temp = st.slider("Температура (°C):", -40, 50, 20)
    cos_phi = st.slider("cosφ:", 0.7, 1.0, 0.9)

# --- ТӨВ ХЭСЭГ: Гаргалгааны тооцоо ---
st.subheader("📌 Гаргалгаа бүрийн ачаалал ба хэрэглэгчид")
col_main, col_info = st.columns([2, 1])

feeder_names = ["1-р гаргалгаа", "2-р гаргалгаа", "3-р гаргалгаа", "4-р гаргалгаа"]
total_tech_loss = 0
all_users_count = 0
feeder_data_list = []

with col_main:
    # Эхлээд бүх айлын тоог цуглуулж нийт жинг тооцох (ачаалал хуваарилахын тулд)
    temp
