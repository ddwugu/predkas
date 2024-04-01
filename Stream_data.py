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

# Display the oil loss calculation section
st.subheader('Perhitungan Oil Losses')

def predict_loss(R1, P1, P2, s):
    R2 = P2 * R1 / P1
    los = R2 - R1
    y = los * s
    return y

Rate1 = st.text_input('Input rate awal(BBL/Jam)')
Pressure1 = st.text_input('Input pressure 1 saat rate awal (PSI)')
Pressure2 = st.text_input('Input pressure 2 saat terjadi pressure drop (PSI)')
Durasi = st.text_input('Durasi pressure drop (Jam)')

if st.button('Hitung Losses'):
    try:
        R1 = float(Rate1)
        P1 = float(Pressure1)
        P2 = float(Pressure2)
        s = float(Durasi) # Perbaikan pada nama variabel
        Hitung_Losses = predict_loss(R1, P1, P2, s) # Perbaikan pada argumen

        if Hitung_Losses < 0: # titik nol
            suspect_loss = f'Terjadi losses sebesar {Hitung_Losses} BBL/Jam '
        elif Hitung_Losses > 0: # total panjang trunkline
            suspect_loss = f'Gain sebesar {Hitung_Losses} BBL/Jam'
        else:
            suspect_loss = f'Tidak terjadi losses'
        st.success(suspect_loss)
    except Exception as e:
        st.error(f"Error predicting location: {e}")
st.markdown("[Opsi 2 : Prediksi Linear Model](https://1prediksilokasi-eld9x5crdkcrc69g3nzbgv.streamlit.app/)")
# Shortcut Link
st.markdown("[Opsi 2 : Prediksi Linear Model](https://predkas-jfsc9tajwgwqxpzb8wui4e.streamlit.app/)")
