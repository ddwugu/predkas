import streamlit as st


def predict_location(x1, x2):
    y = 21.73 - 2.45 * x1 + 0.01 * x2
    return y

# Main Streamlit app
def main():
    st.title('Pertamina Field Jambi-BJG-TPN')
    st.subheader('Prediksi Lokasi Kebocoran Line KAS-TPN Regresi Model')

    Titik_1_PSI = st.text_input('Input delta pressure drop di MGS KAS (PSI)')
    Titik_2_PSI = st.text_input('Input delta pressure drop di MOS (PSI)')

    if st.button('Prediksi Lokasi'):
        try:
            x1 = float(Titik_1_PSI)
            x2 = float(Titik_2_PSI)
            prediksi_lokasi = predict_location(x1, x2)
            
            if prediksi_lokasi <= 0: # titik nol
                suspect_loct = 'Pipa Aman, Tidak Terdapat Fluida yang Mengalir'
            elif prediksi_lokasi >= 23.1: # total panjang trunkline
                suspect_loct = 'Tidak Terdapat Kebocoran'
            else:
                suspect_loct = f'Terjadi kebocoran di titik {prediksi_lokasi} KM'
            st.success(suspect_loct)
        except Exception as e:
            st.error(f"Error predicting location: {e}")

if __name__ == "__main__":
    main()
