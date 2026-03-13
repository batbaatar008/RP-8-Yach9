import streamlit as st
import pandas as pd
import math

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="КТП-201 Салбарласан Шугамын Тооцоо", layout="wide")

# 2. Дамжуулагчийн өгөгдөл
CONDUCTOR_DATA = {
    "СИП-2 3х16": {"R20": 1.91, "alpha": 0.00403},
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403},
    "СИП-2 3х35": {"R20": 0.868, "alpha": 0.00403},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403},
    "СИП-2 3х70": {"R20": 0.443, "alpha": 0.00403}
}

st.title("⚡ КТП-201: Магистраль + 1-Фаз Салбарлалт V6.1")

# --- SIDEBAR: Ерөнхий өгөгдөл ---
with st.sidebar:
    st.header("📂 Ерөнхий өгөгдөл")
    total_p_kwh = st.number_input("Толгой тоолуур (кВт.цаг):", value=259148.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=178040.0)
    hours = st.number_input("Хугацаа (цаг):", value=720.0)
    st.divider()
    m_voltage = st.number_input("Магистраль хүчдэл (В):", value=400)
    cos_phi = st.slider("cosφ:", 0.7, 1.0, 0.9)
    temp = st.slider("Температура (°C):", -40, 50, 20)

# --- ГАРГАЛГААНЫ ТООЦОО ---
st.subheader("📌 Шугамын бүтэц ба Салбарлалт")
col_main, col_res = st.columns([2, 1])

total_tech_loss = 0
feeder_results = []

with col_main:
    # 1-р гаргалгааны жишээ
    with st.expander("1-р Гаргалгаа: Магистраль ба Салбар шугамын тохиргоо", expanded=True):
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("### 🛣️ Магистраль (3-фаз)")
            m_wire = st.selectbox("Марк (М):", list(CONDUCTOR_DATA.keys()), key="mw1")
            m_len = st.number_input("Урт (м) (М):", value=300.0, key="ml1")
            m_u380 = st.number_input("380В тоолуур:", value=2, key="mu380_1")
            m_u220 = st.number_input("Магистраль дээрх 220В тоолуур:", value=30, key="mu220_1")
            
        with c2:
            st.markdown("### 🌿 Салбар (1-фаз)")
            b_voltage = st.number_input("Салбарын хүчдэл (В):", value=220, key="bv1")
            b_wire = st.selectbox("Марк (С):", list(CONDUCTOR_DATA.keys()), key="bw1")
            b_len = st.number_input("Урт (м) (С):", value=150.0, key="bl1")
            b_u220 = st.number_input("Салбар дээрх 220В тоолуур:", value=15, key="bu220_1")

    # Тооцооллын логик
    # 1. Ачааллын хуваарилалт (Жин)
    b_weight = b_u220
    m_weight = m_u220 + (m_u380 * 3)
    total_feeder_weight = b_weight + m_weight # Энэ гаргалгааны нийт жин
    
    # Нийт чадлын энэ гаргалгаанд ноогдох хэсэг (Хялбарчилсан харьцаа)
    p_feeder = (total_p_kwh / hours) * 0.25 # Жишээ нь 4 гаргалгааны 1 нь гэж үзвэл
    p_branch = p_feeder * (b_weight / total_feeder_weight) if total_feeder_weight > 0 else 0
    
    # 2. Салбарын алдагдал (1-фаз)
    r_b = CONDUCTOR_DATA[b_wire]["R20"] * (1 + CONDUCTOR_DATA[b_wire]["alpha"] * (temp - 20))
    i_branch = (p_branch * 1000) / (b_voltage * cos_phi) if b_weight > 0 else 0
    # 1-фаз тул Фаз+Нойль = 2 дахин их эсэрг
