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
    "СИП-2 3х70": {"R20": 0.443, "alpha": 0.00403, "I_max": 240},
    "АС-25/4.2": {"R20": 1.15, "alpha": 0.00403, "I_max": 125},
    "АС-50/8.0": {"R20": 0.595, "alpha": 0.00403, "I_max": 210}
}

st.title("⚡ КТП-201: Нарийвчилсан Тооцоо V4.8")

# --- SIDEBAR: Удирдлага ---
with st.sidebar:
    st.header("📂 Ерөнхий өгөгдөл")
    main_meter = st.number_input("Толгой тоолуур (кВт.цаг):", value=259148.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=178040.0)
    hours = st.number_input("Хугацаа (цаг):", value=720.0)
    st.divider()
    temp = st.slider("Температура (°C):", -40, 50, 20)
    cos_phi = st.slider("cosφ:", 0.7, 1.0, 0.9)
    # Шинээр нэмэгдсэн хүчдэлийн тохируулга
    voltage_kv = st.number_input("Шугамын хүчдэл (кВ):", value=0.40, min_value=0.35, max_value=0.45, step=0.01)

# --- ДЭЭД ХЭСЭГ: СХЕМ ---
st.subheader("🖼️ Сүлжээний схем зураглал")
with st.container(border=True):
    s1, s2, s3, s4, s5 = st.columns([1,2,2,2,2])
    s1.markdown("### 🏠 \n **КТП-201**")
    s2.info("─── 1-р гар ───▶")
    s3.error("─── 2-р гар ───▶")
    s4.success("─── 3-р гар ───▶")
    s5.warning("─── 4-р гар ───▶")

# --- ТӨВ ХЭСЭГ: Гаргалгааны тооцоо ---
st.subheader("📌 Гаргалгаа бүрийн ачаалал ба хэрэглэгчид")
col_main, col_info = st.columns([2, 1])

feeder_names = ["1-р гаргалгаа (Хар)", "2-р гаргалгаа (Улаан)", "3-р гаргалгаа (Цагаан)", "4-р гаргалгаа (Хөх)"]
temp_feeders = []
total_weight = 0

with col_main:
    for i in range(4):
        with st.expander(feeder
