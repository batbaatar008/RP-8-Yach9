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

st.title("⚡ КТП-201: 4-Гаргалгаатай Нарийвчилсан Тооцоо V8.1")

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
        st.info("💡 Тулгуур бүрийн хоорондох зай, дамжуулагчийг нэмж оруулна уу.")
        
        # Анхны загвар өгөгдөл
        df_template = pd.DataFrame([
            {"Тулгуур": "1-2", "Төрөл": "Магистраль (3ф)", "Марк": "СИП-2 3х50", "Урт (м)": 40.0, "Хүчдэл (В)": 400, "220В Тоолуур": 5, "380В Тоолуур": 1}
        ])
        
        # Гаргалгаа бүр дээр тусдаа хүснэгт
        edited_df = st.data_editor(
            df_template, 
            key=f"editor_v8_1_f{i}",
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Төрөл": st.column_config.SelectboxColumn(options=["Магистраль (3ф)", "Салбар (1ф)"]),
                "Марк": st.column_config.SelectboxColumn(options=list(CONDUCTOR_DATA.keys()))
            }
        )
        feeder_data_frames.append(edited_df)

# --- ТООЦООЛОЛ ---
st.divider()
total_tech_loss = 0
feeder_losses = []

# Нийт жинг тооцох (Бүх гаргалгааны нийлбэр)
overall_weight = sum(df["220В Тоолуур"].sum() + (df["380В Тоолуур"].sum() * 3) for df in feeder_data_frames)

for i, df in enumerate(feeder_data_frames):
    feeder_loss = 0
    for _, row in df.iterrows():
        weight = row["220В Тоолуур"] + (row["380В Тоолуур"] * 3)
        ratio = weight / overall_weight if overall_weight > 0 else 0
        p_segment = (total_p_kwh / hours) * ratio
        
        wire_info = CONDUCTOR_DATA[row["Марк"]]
        r_t = wire_info["R20"] * (1 + wire_info["alpha"] * (temp - 20))
        
        if row["Төрөл"] == "Магистраль (3ф)":
            i_curr = (p_segment * 1000) / (math.sqrt(3) * row["Хүчдэл (В)"] * cos_phi) if p_segment > 0 else 0
            loss = (3 * (i_curr**2) * (r_t * (row["Урт (м)"] / 1000)) * hours) / 1000
        else:
            # Салбар шугамын алдагдал (1-фаз, Фаз+Нойль тул 2 дахин авна)
            i_curr = (p_segment * 1000) / (row["Хүчдэл (В)"] * cos_phi) if p_segment > 0 else 0
            loss = (2 * (i_curr**2) * (r_t * (row["Урт (м)"] / 1000)) * hours) / 1000
        feeder_loss += loss
    
    feeder_losses.append(feeder_loss)
    total_tech_loss += feeder_loss

# --- ҮР ДҮН ---
st.subheader("📊 Тооцооны нэгдсэн дүн (Фидер бүрээр)")
res_cols = st.columns(4)
for i in range(4):
    res_cols[i].metric(f"{i+1}-р Гаргалгаа", f"{feeder_losses[i]:.2f} кВт.ц")

st.divider()
total_measured_loss = total_p_kwh - users_sum
comm_loss = total_measured_loss - total_tech_loss

c1, c2, c3 = st.columns(3)
c1.metric("Хэмжсэн нийт алдагдал", f"{total_measured_loss:,.1f} кВт.ц")
c2.metric("Нийт техникийн алдагдал", f"{total_tech_loss:,.1f} кВт.ц")
c3.metric("Арилжааны алдагдал", f"{max(0, comm_loss):,.1f} кВт.ц")

st.success("✅ Станцын 4 гаргалгааны тооцоог амжилттай хийж дууслаа.")
