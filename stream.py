import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model yang telah disimpan
model = joblib.load("saved_models/Decision_Tree_tuned.pkl")  # Ganti sesuai nama model yang kamu simpan

# Mapping hasil prediksi numerik ke label asli
mapping_nobeyesdad = {
    'Insufficient_Weight': 0,
    'Normal_Weight': 1,
    'Overweight_Level_I': 2,
    'Overweight_Level_II': 3,
    'Obesity_Type_I': 4,
    'Obesity_Type_II': 5,
    'Obesity_Type_III': 6
}
reverse_mapping_nobeyesdad = {v: k for k, v in mapping_nobeyesdad.items()}

# Judul
st.title("Prediksi Tingkat Obesitas Berdasarkan Data Pribadi")

# Input user
gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
age = st.number_input("Usia", min_value=1, max_value=120)
height = st.number_input("Tinggi Badan (meter)", min_value=1.0, step=0.01)
weight = st.number_input("Berat Badan (kg)", min_value=1.0, step=0.1)
family_history = st.selectbox("Apakah ada riwayat obesitas di keluarga?", ["yes", "no"])
favc = st.selectbox("Sering konsumsi makanan tinggi kalori?", ["yes", "no"])
fcvc = st.slider("Konsumsi sayur tiap makan (1=Jarang, 3=Sering)", 1, 3)
ncp = st.slider("Jumlah makan besar per hari", 1, 5)
caec = st.selectbox("Suka ngemil di luar jam makan?", ["no", "Sometimes", "Frequently", "Always"])
smoke = st.selectbox("Apakah Anda merokok?", ["yes", "no"]) 
ch2o = st.slider("Jumlah konsumsi air harian (liter)", 0.5, 5.0, step=0.1)
scc = st.selectbox("Pantau asupan kalori harian?", ["yes", "no"])
faf = st.slider("Frekuensi olahraga per minggu (jam)", 0.0, 10.0, step=0.5)
tue = st.slider("Waktu menggunakan teknologi per hari (jam)", 0, 24)
calc = st.selectbox("Konsumsi alkohol", ["no", "Sometimes", "Frequently", "Always"])
mtrans = st.selectbox("Transportasi utama", ["Public_Transportation", "Walking", "Automobile", "Motorbike", "Bike"])

# Mapping input user ke numerik
def encode_input():
    return [
        1 if gender == "Male" else 0,
        age,
        height,
        weight,
        1 if family_history == "yes" else 0,
        1 if favc == "yes" else 0,
        fcvc,
        ncp,
        {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}[caec],
        1 if smoke == "yes" else 0,
        ch2o,
        1 if scc == "yes" else 0,
        faf,
        tue,
        {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}[calc],
        {
            "Public_Transportation": 0,
            "Walking": 1,
            "Automobile": 2,
            "Motorbike": 3,
            "Bike": 4
        }[mtrans]
    ]

# Prediksi saat tombol ditekan
if st.button("Prediksi Tingkat Obesitas"):
    input_data = np.array([encode_input()])
    prediction_num = model.predict(input_data)[0]
    prediction_label = reverse_mapping_nobeyesdad[prediction_num]
    
    st.success(f"Prediksi Tingkat Obesitas Anda: **{prediction_label}**")
