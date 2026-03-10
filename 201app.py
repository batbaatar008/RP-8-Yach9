import streamlit as st
import pandas as pd

st.set_page_config(page_title="КТП-201 Нарийвчилсан Тооцоолуур", layout="wide")

# --- ӨГӨГДЛИЙН САН (Дамжуулагчийн бүх төрөл) ---
# R20: 20°C дахь идэвхтэй эсэргүүцэл (Ohm/km)
# alpha: Температурын коэффициент (Aluminium = 0.00403)
# I_max: Агаар дахь зөвшөөрөгдөх гүйдэл (A)
CONDUCTOR_DATA = {
    "СИП-2 3х16": {"R20": 1.91, "alpha": 0.00403, "I_max": 100},
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403, "I_max": 130},
    "СИП-2 3х35": {"R20": 0.868, "alpha": 0.00403, "I_max": 160},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403, "I_max": 195},
    "СИП-2 3х70": {"R20": 0.443, "alpha": 0.00403, "I_max": 240},
    "СИП-2 3х95": {"R20": 0.320, "alpha": 0.00403, "I_max": 300},
    "СИП-2 3х120": {"R20": 0.253, "alpha": 0.00403, "I_max": 340},
    "АС-16/2.7": {"R20": 1.80, "alpha": 0.00403, "I_max": 105},
    "АС-25/4.2": {"R20": 1.15, "alpha": 0.00403, "I_max": 125},
    "АС-35/6.0": {"R20": 0.821, "alpha": 0.00403, "I_max": 170},
    "АС-50/8.0": {"R20": 0.595, "alpha": 0.00403, "I_max": 210},
    "АС-70/11": {"R20": 0.422, "alpha": 0.00403, "I_max": 265},
    "АС-95/16": {"R20": 0.301, "alpha": 0.00403, "I_max": 330},
    "АС-120/19": {"R20": 0.244, "alpha": 0.00403, "I_max": 390}
}

st.title("⚡ КТП-201: Техникийн Алдагдал Тооцоолуур V3.4")

# --- SIDEBAR: Ерөнхий тохиргоо ---
with st.sidebar:
    st.header("⚙️ Ерөнхий тохиргоо")
    main_meter = st.number_input("Толгой тоолуур (кВт.цаг):", value=259148.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=178040.0)
    hours = st.number_input("Тооцсон хугацаа (цаг):", value=720.0)
    
    st.divider()
    cos_phi = st.slider("Чадлын коэффициент (cosφ):", 0.70, 1.0, 0.90, 0.01)
    temp = st.slider("Ажлын температура (°C):", -40, 50, 20, 1)
    voltage_kv = 0.4 

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
                wire = st.selectbox(f"Марк сонгох:", list(CONDUCTOR_DATA.keys()), key=f"w{i}", index=i+1)
                length_km = st.number_input(f"Шугамын урт (км):", value=0.5, step=0.05, format="%.3f", key=f"l{i}")
            
            data = CONDUCTOR_DATA[wire]
            # Температурын залруулгатай эсэргүүцэл
            r_t = data["R20"] * (1 + data["alpha"] * (temp - 20))
            # Гүйдэл
            i_current = (avg_p_kw * feeder_ratios[i]) / (voltage_kv * 1.732 * cos_phi)
            # Алдагдал
            loss = (3 * (i_current**2) * (r_t * length_km) * hours) / 1000
            total_line_loss += loss
            
            with c2:
                st.write(f"**Ажлын гүйдэл:** {i_current:.2f} А")
                if i_current > data["I_max"]:
                    st.warning(f"⚠️ Гүйдэл хэтэрсэн! (Max: {data['I_max']}A)")
                st.write(f"**Тех. алдагдал:** {loss:.2f} кВт.цаг")
            
            selected_info.append({
                "Гаргалгаа": i+1,
                "Марк": wire,
                "R20 (Ω/км)": data["R20"],
                "Rt (Ω/км)": round(r_t, 4),
                "Урт (км)": length_km
            })

# --- БАРУУН ТАЛ: Нарийвчилсан мэдээллийн хүснэгт ---
with col_info:
    st.subheader("📋 Техникийн өгөгдөл")
    df = pd.DataFrame(selected_info)
    st.dataframe(df, hide_index=True)
    
    st.markdown(f"""
    **Одоогийн нөхцөл:**
    - Температура: `{temp}°C`
    - cosφ: `{cos_phi}`
    - Цаг: `{hours}ц`
    """)
    
    st.info("""
    **Тайлбар:**
    - **R20:** 20 градус дахь хувийн эсэргүүцэл.
    - **Rt:** Тухайн температур дахь тооцоот эсэргүүцэл.
    """)

# --- ҮР ДҮН ---
st.divider()
total_measured_loss = main_meter - users_sum
total_tech_loss = total_line_loss
comm_loss = total_measured_loss - total_tech_loss

res1, res2, res3 = st.columns(3)
res1.metric("Хэмжсэн нийт алдагдал", f"{total_measured_loss:.1f}")
res2.metric("Техникийн алдагдал", f"{total_tech_loss:.1f}")
res3.metric("Арилжааны алдагдал", f"{comm_loss:.1f}")
