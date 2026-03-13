import streamlit as st
import pandas as pd

# Хуудасны тохиргоо
st.set_page_config(page_title="Эрчим Хүчний Тооцоолуур", layout="wide")

# Дамжуулагчийн сан
CONDUCTOR_DATA = {
    "СИП-2 3х16": {"R20": 1.91, "alpha": 0.00403, "I_max": 100},
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403, "I_max": 130},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403, "I_max": 195},
    "АС-50/8.0": {"R20": 0.595, "alpha": 0.00403, "I_max": 210}
}

st.title("📊 КТП-201: Техникийн Алдагдал ба Сүлжээний Хяналт")

# --- SIDEBAR ---
with st.sidebar:
    st.header("📂 Удирдлага")
    main_meter = st.number_input("Толгой тоолуур (кВт.цаг):", value=555578.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=524270.0)
    hours = st.number_input("Хугацаа (цаг):", value=720.0)
    st.divider()
    temp = st.slider("Температура (°C):", -40, 50, 20)
    cos_phi = st.slider("cosφ:", 0.7, 1.0, 0.9)

# --- ДЭЭД ХЭСЭГ: Үндсэн метрикүүд (Зурган дээрх шиг) ---
m1, m2, m3, m4 = st.columns(4)
total_loss = main_meter - users_sum
loss_percent = (total_loss / main_meter) * 100

m1.metric("Нийт эрчим хүч", f"{main_meter:,.0f} кВт.цаг")
m2.metric("Нийт алдагдал", f"{total_loss:,.0f}", f"{loss_percent:.2f}%", delta_color="inverse")
m3.metric("Айлын тоо", "254")
m4.metric("Дундаж ачаалал", f"{(main_meter/hours):.1f} кВт")

# --- ТӨВ ХЭСЭГ: Гаргалгааны нарийвчилсан тооцоо ---
st.subheader("📌 Гаргалгаа бүрийн фазын ачаалал ба алдагдал")
col_main, col_info = st.columns([2, 1])

feeder_names = ["1-р гаргалгаа (А фаз)", "2-р гаргалгаа (В фаз)", "3-р гаргалгаа (С фаз)", "4-р гаргалгаа"]
# Зурган дээрх хувь хэмжээгээр ачааллыг хуваарилав
feeder_ratios = [0.35, 0.32, 0.31, 0.02] 

total_tech_loss = 0
selected_info = []

with col_main:
    for i in range(4):
        with st.expander(feeder_names[i], expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                wire = st.selectbox(f"Марк:", list(CONDUCTOR_DATA.keys()), key=f"w{i}", index=1)
                length = st.number_input(f"Урт (км):", value=0.75, key=f"l{i}")
            
            data = CONDUCTOR_DATA[wire]
            r_t = data["R20"] * (1 + data["alpha"] * (temp - 20))
            i_current = ( (main_meter/hours) * feeder_ratios[i] ) / (0.4 * 1.732 * cos_phi)
            loss = (3 * (i_current**2) * (r_t * length) * hours) / 1000
            total_tech_loss += loss
            
            with c2:
                st.write(f"**Гүйдэл:** {i_current:.1f} А")
                st.write(f"**Алдагдал:** {loss:,.1f} кВт.цаг")
            with c3:
                # Зурган дээрх шиг фазын эрчим хүчийг харуулах
                phase_energy = main_meter * feeder_ratios[i]
                st.write(f"**Эрчим хүч:**")
                st.write(f"{phase_energy:,.0f} кВт.цаг")

            selected_info.append({"Гар": i+1, "Марк": wire, "Урт": length, "Rt": round(r_t, 3)})

# --- БАРУУН ТАЛ: Техникийн мэдээлэл ---
with col_info:
    st.info("📋 Техникийн өгөгдөл")
    st.table(pd.DataFrame(selected_info))
    st.write(f"⚡ **Сүлжээний хүчдэл:** 0.4 кВ")
    st.write(f"🌡️ **Тооцсон температур:** {temp}°C")

# --- ДООД ХЭСЭГ: Эцсийн дүгнэлт ---
st.divider()
comm_loss = total_loss - total_tech_loss
res1, res2, res3 = st.columns(3)
res1.metric("Техникийн алдагдал", f"{total_tech_loss:,.1f}")
res2.metric("Арилжааны алдагдал", f"{comm_loss:,.1f}")
res3.progress(min(max(total_tech_loss/total_loss, 0.0), 1.0) if total_loss > 0 else 0, text="Техникийн алдагдлын эзлэх хувь")
