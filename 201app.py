import streamlit as st
import pandas as pd

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="КТП-201 Тооцоолуур", layout="wide")

# 2. Сүлжээний тогтмол өгөгдөл
CONDUCTOR_R = {"СИП 25": 1.20, "СИП 50": 0.641}
TR_DATA = {"400 kVA": {"P0": 0.95, "Pk": 5.5}}

st.title("⚡ КТП-201: Техникийн Алдагдал Тооцоолуур V3.1")

# --- SIDEBAR: Ерөнхий өгөгдөл ---
with st.sidebar:
    st.header("📊 Ерөнхий мэдээлэл")
    main_meter = st.number_input("Толгой тоолуур (кВт.цаг):", value=50000.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=42000.0)
    hours = st.number_input("Тооцсон хугацаа (цаг):", value=720.0)

# --- ГАРГАЛГААНЫ ХЭСЭГ ---
st.subheader("📌 Гаргалгаа бүрийн тооцоо (0.4 кВ)")
col1, col2 = st.columns(2)

feeders = [
    {"нэр": "1-р гаргалгаа (Хар)", "марк": "СИП 25", "тулгуур": 15, "хувь": 0.25},
    {"нэр": "2-р гаргалгаа (Улаан)", "марк": "СИП 50", "тулгуур": 20, "хувь": 0.30},
    {"нэр": "3-р гаргалгаа (Цагаан)", "марк": "СИП 25", "тулгуур": 18, "хувь": 0.25},
    {"нэр": "4-р гаргалгаа (Хөх)", "марк": "СИП 25", "тулгуур": 12, "хувь": 0.20},
]

total_line_loss = 0
avg_p_kw = (main_meter / hours)

for i, f in enumerate(feeders):
    with col1 if i < 2 else col2:
        with st.expander(f["нэр"], expanded=True):
            poles = st.number_input(f"Тулгуур ({f['нэр']}):", value=f["тулгуур"], key=f"p{i}")
            length_km = (poles * 50) / 1000 
            I_feeder = (avg_p_kw * f["хувь"]) / (0.4 * 1.732 * 0.9)
            r_total = CONDUCTOR_R[f["марк"]] * length_km
            loss = (3 * (I_feeder**2) * r_total * hours) / 1000
            total_line_loss += loss
            st.info(f"Урт: {length_km:.2f} км | Алдагдал: {loss:.2f} кВт.цаг")

# --- ТРАНСФОРМАТОРЫН АЛДАГДАЛ ---
k_load = avg_p_kw / 400 
tr_loss = (TR_DATA["400 kVA"]["P0"] * hours) + (TR_DATA["400 kVA"]["Pk"] * (k_load**2) * hours)

# --- НЭГДСЭН ҮР ДҮН ---
st.divider()
total_measured_loss = main_meter - users_sum
# Эндээс tr_loss-ийг хасаад зөвхөн шугамын алдагдлыг авна
total_tech_loss = total_line_loss 
comm_loss = total_measured_loss - total_tech_loss

res1, res2, res3, res4 = st.columns(4)
res1.metric("Нийт алдагдал", f"{total_measured_loss:.1f}")
res2.metric("Техникийн алдагдал", f"{total_tech_loss:.1f}")
res3.metric("ТР-ын алдагдал", f"{tr_loss:.1f}")
res4.metric("Арилжааны алдагдал", f"{comm_loss:.1f}")

# Дүгнэлт
if total_measured_loss > 0 and comm_loss > (total_measured_loss * 0.4):
    st.error("🚨 Арилжааны алдагдал өндөр байна!")
else:
    st.success("✅ Сүлжээний байдал хэвийн байна.")

