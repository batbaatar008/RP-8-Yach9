import streamlit as st
import pandas as pd

st.set_page_config(page_title="КТП-201 Нарийвчилсан Тооцоолуур", layout="wide")

# --- ӨГӨГДЛИЙН САН (Дамжуулагчийн үзүүлэлтүүд) ---
CONDUCTOR_DATA = {
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403, "I_max": 130},
    "СИП-2 3х35": {"R20": 0.868, "alpha": 0.00403, "I_max": 160},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403, "I_max": 195},
    "СИП-2 3х70": {"R20": 0.443, "alpha": 0.00403, "I_max": 240},
    "АС-25": {"R20": 1.15, "alpha": 0.00403, "I_max": 125},
    "АС-50": {"R20": 0.595, "alpha": 0.00403, "I_max": 210}
}

st.title("⚡ КТП-201: Техникийн Алдагдал Тооцоолуур V3.3")

# --- SIDEBAR: Ерөнхий тохиргоо ---
with st.sidebar:
    st.header("⚙️ Ерөнхий тохиргоо")
    main_meter = st.number_input("Толгой тоолуур (кВт.цаг):", value=259148.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=178040.0)
    hours = st.number_input("Тооцсон хугацаа (цаг):", value=720.0)
    
    st.divider()
    cos_phi = st.slider("Чадлын коэффициент (cosφ):", 0.70, 1.0, 0.90, 0.01)
    temp = st.slider("Ажлын температур (°C):", -40, 40, 20, 1)
    voltage_kv = 0.4 # Хүчдэл (kV)

# --- ТӨВ ХЭСЭГ: Гаргалгаанууд ---
st.subheader("📌 Гаргалгааны нарийвчилсан тооцоо")
col_main, col_info = st.columns([2, 1])

total_line_loss = 0
avg_p_kw = (main_meter / hours)
feeder_names = ["1-р гаргалгаа (Хар)", "2-р гаргалгаа (Улаан)", "3-р гаргалгаа (Цагаан)", "4-р гаргалгаа (Хөх)"]
feeder_ratios = [0.25, 0.30, 0.25, 0.20]

selected_info = []

with col_main:
    for i in range(4):
        with st.expander(feeder_names[i], expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                wire = st.selectbox(f"Дамжуулагч марк:", list(CONDUCTOR_DATA.keys()), key=f"w{i}", index=i%len(CONDUCTOR_DATA))
                length_km = st.number_input(f"Шугамын урт (км):", value=0.5, step=0.1, key=f"l{i}")
            
            # Тооцоолол
            data = CONDUCTOR_DATA[wire]
            # Температурын залруулгатай эсэргүүцэл
            r_t = data["R20"] * (1 + data["alpha"] * (temp - 20))
            # Гүйдэл (A)
            i_current = (avg_p_kw * feeder_ratios[i]) / (voltage_kv * 1.732 * cos_phi)
            # Алдагдал (кВт.цаг)
            loss = (3 * (i_current**2) * (r_t * length_km) * hours) / 1000
            total_line_loss
