import streamlit as st
import pandas as pd
import graphviz

st.set_page_config(page_title="Эрчим Хүчний Сүлжээний Хяналт", layout="wide")

# --- ӨГӨГДЛИЙН САН ---
CONDUCTOR_DATA = {
    "СИП-2 3х25": {"R20": 1.20, "alpha": 0.00403},
    "СИП-2 3х50": {"R20": 0.641, "alpha": 0.00403},
    "АС-50/8.0": {"R20": 0.595, "alpha": 0.00403}
}

st.title("📊 Эрчим Хүчний Сүлжээний Техникийн Алдагдал V4.0")

# --- 1. SIDEBAR: МОД БҮТЭЦ ---
with st.sidebar:
    st.header("📂 Сүлжээний бүтэц")
    selected_node = st.selectbox("Сонгох хэсэг:", ["Шарын гол 110/6", "РП-1, яч22,33", "КТП-201", "КТП-204", "КТП-205"])
    
    st.divider()
    st.subheader("⚙️ Тохиргоо")
    temp = st.slider("Температура (°C):", -40, 40, 20)
    cos_phi = st.slider("cosφ:", 0.7, 1.0, 0.9)
    main_meter = st.number_input("Толгой тоолуур:", value=555578.0)

# --- 2. ТӨВ ХЭСЭГ: СХЕМ ЗУРАГ ---
st.subheader(f"📍 Сүлжээний схем: {selected_node}")

# Шугамын схем зурах (Graphviz)
dot = graphviz.Digraph()
dot.attr(rankdir='LR', size='8,5')

if selected_node == "КТП-201":
    dot.node('KTP', 'КТП-201\n400кВА', shape='box', color='red')
    dot.edge('KTP', 'F1', label='1-р гар (СИП-25)')
    dot.edge('KTP', 'F2', label='2-р гар (СИП-50)')
    dot.edge('KTP', 'F3', label='3-р гар (СИП-25)')
    dot.edge('F1', 'T15', label='15-р тулгуур')
    dot.edge('F2', 'T20', label='20-р тулгуур')
    st.graphviz_chart(dot)
else:
    st.info("Энэ хэсгийн схемийг харахын тулд КТП-201-ийг сонгоно уу.")

# --- 3. ДООД ХЭСЭГ: ТООЦООЛОЛ ---
st.divider()
col1, col2, col3, col4 = st.columns(4)

# Жишээ тооцоолол (Зурган дээрх шиг)
col1.metric("Эрчим хүч (кВт.цаг)", "555,578")
col2.metric("Алдагдал (кВт.цаг)", "31,308", delta="-5.635%", delta_color="inverse")
col3.metric("А фаз (кВт)", "196,858")
col4.metric("Айлын тоо", "254")

# Хүснэгтэн мэдээлэл
data = {
    "Фидер": ["1-р гар", "2-р гар", "3-р гар", "4-р гар"],
    "А фаз": [196, 181, 177, 150],
    "Алдагдал %": ["5.6%", "38.5%", "30.3%", "29.0%"],
    "Урт (км)": [0.75, 1.0, 0.9, 0.6]
}
st.table(pd.DataFrame(data))
