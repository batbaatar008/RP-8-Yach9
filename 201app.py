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

st.title("⚡ КТП-201: Нарийвчилсан Тооцоо V5.1")

# --- SIDEBAR: Удирдлага ---
with st.sidebar:
    st.header("📂 Ерөнхий өгөгдөл")
    main_meter = st.number_input("Толгой тоолуур (кВт.цаг):", value=259148.0)
    users_sum = st.number_input("Хэрэглэгчдийн нийлбэр (кВт.цаг):", value=178040.0)
    hours = st.number_input("Хугацаа (цаг):", value=720.0)
    st.divider()
    temp = st.slider("Температура (°C):", -40, 50, 20)
    cos_phi = st.slider("cosφ:", 0.7, 1.0, 0.9)
    # Хүчдэлийг Вольт (В) нэгжээр оруулна
    voltage_v = st.number_input("Шугамын хүчдэл (В):", value=400, min_value=350, max_value=450, step=1)

# --- ТӨВ ХЭСЭГ: Гаргалгааны тооцоо ---
st.subheader("📌 Гаргалгаа бүрийн ачаалал ба хэрэглэгчид")
col_main, col_info = st.columns([2, 1])

feeder_names = ["1-р гаргалгаа", "2-р гаргалгаа", "3-р гаргалгаа", "4-р гаргалгаа"]
temp_feeders = []
total_weight = 0

with col_main:
    for i in range(4):
        with st.expander(feeder_names[i], expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                wire = st.selectbox(f"Марк {i+1}:", list(CONDUCTOR_DATA.keys()), key=f"w_{i}", index=1)
                length_m = st.number_input(f"Урт (м) {i+1}:", value=500.0, key=f"l_{i}")
            with c2:
                u_220 = st.number_input(f"220В тоолуур {i+1}:", value=50, key=f"u220_{i}")
            with c3:
                u_380 = st.number_input(f"380В тоолуур {i+1}:", value=2, key=f"u380_{i}")
            
            # Ачааллын жинг тооцох (380В хэрэглэгчийг 3 дахин их жинтэй гэж үзэв)
            weight = u_220 + (u_380 * 3)
            total_weight += weight
            temp_feeders.append({"wire": wire, "len": length_m, "weight": weight, "u220": u_220, "u380": u_380})

# --- ТӨГСГӨЛ: Үр дүн ба Баланс ---
st.divider()
total_tech_loss = 0
summary_list = []

for i, f in enumerate(temp_feeders):
    # Ачаалал хуваарилах хувь
    ratio = f["weight"] / total_weight if total_weight > 0 else 0
    
    # Дамжуулагчийн эсэргүүцэл температурын хамаарлаар
    data = CONDUCTOR_DATA[f["wire"]]
    r_t = data["R20"] * (1 + data["alpha"] * (temp - 20))
    
    # Дундаж ачаалал (кВт)
    avg_p = (main_meter / hours) * ratio
    
    # Хүчдэлийг кВ-д шилжүүлж гүйдэл тооцох
    u_kv = voltage_v / 1000
    i_current = avg_p / (u_kv * 1.732 * cos_phi) if (u_kv > 0 and ratio > 0) else 0
    
    # Техникийн алдагдал (кВт.цаг)
    loss = (3 * (i_current**2) * (r_t * (f["len"] / 1000)) * hours) / 1000
    total_tech_loss += loss
    
    summary_list.append({
        "Гар": i+1, 
        "220В": f["u220"], 
        "380В": f["u380"], 
        "Гүйдэл (А)": round(i_current, 1), 
        "Тех.Алдагдал": round(loss, 1)
    })

res_col1, res_col2 = st.columns([2, 1])
with res_col1:
    st.table(pd.DataFrame(summary_list))

with res_col2:
    total_measured_loss = main_meter - users_sum
    comm_loss = total_measured_loss - total_tech_loss
    
    st.metric("Хэмжсэн нийт алдагдал", f"{total_measured_loss:,.1f}")
    st.metric("Техникийн алдагдал", f"{total_tech_loss:,.1f}")
    st.metric("Арилжааны алдагдал", f"{comm_loss:,.1f}")

st.success(f"✅ Хүчдэлийг {voltage_v} В-оор тооцож дууслаа.")
