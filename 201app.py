import streamlit as st
import pandas as pd
import math

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="КТП-201 Олон Мөчиртэй Тооцоо", layout="wide")

# 2. Дамжуулагчийн өгөгдөл
CONDUCTOR_DATA = {
    "СИП-2 3х16": {"R20": 1.91, "alpha": 0.00403},
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403},
    "СИП-2 3х35": {"R20": 0.868, "alpha": 0.00403},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403},
    "СИП-2 3х70": {"R20": 0.443, "alpha": 0.00403}
}

st.title("⚡ КТП-201: Олон мөчиртэй Нарийвчилсан Тооцоо V7.0")

# --- SIDEBAR: Ерөнхий өгөгдөл ---
with st.sidebar:
    st.header("📂 Ерөнхий тохиргоо")
    total_p_kwh = st.number_input("Толгой тоолуур (кВт.цаг):", value=259148.0)
    hours = st.number_input("Хугацаа (цаг):", value=720.0)
    m_voltage = st.number_input("Магистраль хүчдэл (В):", value=400)
    cos_phi = st.slider("cosφ:", 0.7, 1.0, 0.9)
    temp = st.slider("Температура (°C):", -40, 50, 20)

# --- ТӨВ ХЭСЭГ: Хүснэгтээр өгөгдөл оруулах ---
st.subheader("📝 Шугамын бүтэц (Тулгуур ба Салбарлалт)")
st.info("💡 Тулгуур бүрийн хоорондох зай, дамжуулагч болон салбар шугамын хүчдэлийг доорх хүснэгтэд нэмж оруулна уу.")

# Анхны өгөгдөл бүхий хүснэгт
initial_data = pd.DataFrame([
    {"Тулгуур": "1-2", "Төрөл": "Магистраль (3ф)", "Марк": "СИП-2 3х50", "Урт (м)": 40.0, "Хүчдэл (В)": 400, "220В Тоолуур": 5, "380В Тоолуур": 1},
    {"Тулгуур": "2-3 (Салбар)", "Төрөл": "Салбар (1ф)", "Марк": "СИП-2 3х16", "Урт (м)": 35.0, "Хүчдэл (В)": 220, "220В Тоолуур": 10, "380В Тоолуур": 0},
])

# Editable Table
edited_df = st.data_editor(
    initial_data, 
    num_rows="dynamic", 
    use_container_width=True,
    column_config={
        "Төрөл": st.column_config.SelectboxColumn(options=["Магистраль (3ф)", "Салбар (1ф)"]),
        "Марк": st.column_config.SelectboxColumn(options=list(CONDUCTOR_DATA.keys()))
    }
)

# --- ТООЦООЛОЛ ---
st.divider()
total_tech_loss = 0
calculation_results = []

# Нийт тоолуурын тоогоор ачааллыг жинлэж хуваах (Хялбарчилсан)
total_u220 = edited_df["220В Тоолуур"].sum()
total_u380 = edited_df["380В Тоолуур"].sum()
total_weight = total_u220 + (total_u380 * 3)

for index, row in edited_df.iterrows():
    # Тухайн хэсгийн ачаалал
    weight = row["220В Тоолуур"] + (row["380В Тоолуур"] * 3)
    ratio = weight / total_weight if total_weight > 0 else 0
    p_segment = (total_p_kwh / hours) * ratio
    
    # Эсэргүүцэл
    wire_info = CONDUCTOR_DATA[row["Марк"]]
    r_t = wire_info["R20"] * (1 + wire_info["alpha"] * (temp - 20))
    
    # Алдагдал тооцох (3-фаз vs 1-фаз)
    if row["Төрөл"] == "Магистраль (3ф)":
        i_curr = (p_segment * 1000) / (math.sqrt(3) * row["Хүчдэл (В)"] * cos_phi) if p_segment > 0 else 0
        loss = (3 * (i_curr**2) * (r_t * (row["Урт (м)"] / 1000)) * hours) / 1000
    else:
        i_curr = (p_segment * 1000) / (row["Хүчдэл (В)"] * cos_phi) if p_segment > 0 else 0
        loss = (2 * (i_curr**2) * (r_t * (row["Урт (м)"] / 1000)) * hours) / 1000
    
    total_tech_loss += loss
    calculation_results.append(round(loss, 2))

# Үр дүнг харуулах
st.subheader("📊 Тооцооны нэгдсэн дүн")
c1, c2 = st.columns(2)
with c1:
    st.metric("Нийт техникийн алдагдал", f"{total_tech_loss:,.1f} кВт.цаг")
with c2:
    measured_loss = total_p_kwh - (total_p_kwh * 0.7) # Жишээ баланс
    st.metric("Арилжааны алдагдал (Багцаалсан)", f"{max(0, measured_loss - total_tech_loss):,.1f} кВт.цаг")

st.success("✅ Хүснэгтээр оруулсан бүх мөчир, тулгуурын алдагдлыг тооцож дууслаа.")
