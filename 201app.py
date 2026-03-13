import streamlit as st
import pandas as pd

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="Эрчим Хүчний Тооцоолуур", layout="wide")

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

st.title("⚡ КТП-201: Техникийн Алдагдал Тооцоолуур V4.2")

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
m1.metric("Нийт хэмжсэн алдагдал", f"{total_loss:,.1f} кВт.цаг")
m2.metric("Дундаж ачаалал", f"{(main_meter/hours):.1f} кВт")
m3.metric("Алдагдал (хувиар)", f"{(total_loss/main_meter*100):.2f}%")

# --- ТӨВ ХЭСЭГ: Гаргалгааны тооцоо ---
st.subheader("📌 Гаргалгаа бүрийн нарийвчилсан тооцоо (Уртыг метрээр)")
col_main, col_info = st.columns([2, 1])

feeder_names = ["1-р гаргалгаа", "2-р гаргалгаа", "3-р гаргалгаа", "4-р гаргалгаа"]
feeder_ratios = [0.35, 0.30, 0.25, 0.10] 

total_tech_loss = 0
summary_table = []

with col_main:
    for i in range(4):
        with st.expander(feeder_names[i], expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                wire = st.selectbox(f"Марк сонгох:", list(CONDUCTOR_DATA.keys()), key=f"w{i}", index=1)
                # Уртыг метрээр оруулж байна
                length_m = st.number_input(f"Шугамын урт (Метр):", value=500.0, step=10.0, key=f"l{i}")
            
            # Тооцоолол
            data = CONDUCTOR_DATA[wire]
            r_t = data["R20"] * (1 + data["alpha"] * (temp - 20))
            avg_p_feeder = (main_meter/hours) * feeder_ratios[i]
            i_current = avg_p_feeder / (0.4 * 1.732 * cos_phi)
            
            # Алдагдлын томьёо (length_m / 1000 хийж километрт шилжүүлэв)
            loss = (3 * (i_current**2) * (r_t * (length_m / 1000)) * hours) / 1000
            total_tech_loss += loss
            
            with c2:
                st.write(f"**Гүйдэл:** {i_current:.2f} А")
                st.write(f"**Тех. Алдагдал:** {loss:,.2f} кВт.цаг")
                if i_current > data["I_max"]:
                    st.error(f"⚠️ Ачаалал хэтэрсэн! Max: {data['I_max']}A")

            summary_table.append({
                "Гаргалгаа": i+1,
                "Марк": wire,
                "Урт (м)": length_m,
                "Гүйдэл (А)": round(i_current, 1)
            })

# --- БАРУУН ТАЛ: Хүснэгт ---
with col_info:
    st.info("📋 Сүлжээний өгөгдөл")
    st.table(pd.DataFrame(summary_table))

# --- ЭЦСИЙН ҮР ДҮН ---
st.divider()
comm_loss = total_loss - total_tech_loss
r1, r2, r3 = st.columns(3)
r1.metric("Техникийн алдагдал", f"{total_tech_loss:,.1f}")
r2.metric("Арилжааны алдагдал", f"{comm_loss:,.1f}")
r3.metric("Тех. алдагдлын хувь", f"{(total_tech_loss/total_loss*100 if total_loss > 0 else 0):.1f}%")

st.success("✅ Уртыг метрээр тооцож ду
