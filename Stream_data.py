import pickle
import streamlit as st

# Load the model
try:
    with open('Pred_lokasi11.sav', 'rb') as file:
        LokasiKM = pickle.load(file)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    LokasiKM = None  # Assign None if there is an error loading the model

# Web Title
st.title('Pertamina Field Jambi')
st.subheader('Prediksi Lokasi Kebocoran Line MGS KAS-MOS TPN')


# User Inputs
Titik_1_PSI = st.text_input('Input delta pressure drop di MGS KAS (PSI)')
Titik_2_PSI = st.text_input('Input delta Pressure drop di MOS (PSI)')

# Code prediction
suspect_loct = ''

# Prediction Button
if LokasiKM is not None and st.button('Prediksi Lokasi'):
    try:
        prediksi_lokasi = LokasiKM.predict([[float(Titik_1_PSI), float(Titik_2_PSI)]])
        if prediksi_lokasi[0] == 0: #titik nol
            suspect_loct = 'It is safe that there is no fluid flowingr'
        elif prediksi_lokasi[0] >= 23.1: #total panjang trunkline
            suspect_loct = 'Safe, there are no leaks'
        else:
            suspect_loct = f'Estimated leak location {prediksi_lokasi[0]} KM'
        st.success(suspect_loct)
    except Exception as e:
        st.error(f"Error predicting location: {e}")
