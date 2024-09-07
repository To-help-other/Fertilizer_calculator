import numpy as np
import pickle
import pandas as pd
import streamlit as st
from PIL import Image

# Load models using context managers
def load_model(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)

stacking_model_N = load_model("stacking_model_N.pkl")
stacking_model_P = load_model("stacking_model_P.pkl")
stacking_model_K = load_model("stacking_model_K.pkl")

def calculate_deficiency(predicted, actual):
    return max(0, predicted - actual)

def predict_amount_of_fertilizer(N, P, K, temperature, humidity, ph, rainfall, hectares, label):
    input_data = [[temperature, humidity, ph, rainfall, label]]
    
    # Predictions
    predicted_N = stacking_model_N.predict(input_data)[0]
    predicted_P = stacking_model_P.predict(input_data)[0]
    predicted_K = stacking_model_K.predict(input_data)[0]
    
    # Calculate deficiencies
    deficient_N = calculate_deficiency(predicted_N, N)
    deficient_P = calculate_deficiency(predicted_P, P)
    deficient_K = calculate_deficiency(predicted_K, K)

    # Available fertilizers
    MOP, DAP, Urea = 0, 0, 0

    # Calculate recommendations
    if deficient_K > 0:
        deficient_K_levels = deficient_K * (2.24 * hectares)
        MOP = deficient_K_levels / 0.6

    if deficient_P > 0:
        deficient_P_levels = deficient_P * (2.24 * hectares)
        DAP = deficient_P_levels / 0.6
        remaining_deficient_N = max(0, deficient_N - (DAP * 0.18))
    else:
        remaining_deficient_N = deficient_N

    if remaining_deficient_N > 0:
        remaining_deficient_N_levels = remaining_deficient_N * (2.24 * hectares)
        Urea = remaining_deficient_N_levels / 0.6

    # Prepare recommendation message
    recommendation_message = []
    if MOP > 0:
        recommendation_message.append(f"{MOP:.2f} ኪሎ ግራም ሞፕ")
    if DAP > 0:
        recommendation_message.append(f"{DAP:.2f} ኪሎ ግራም ዲኤፒ")
    if Urea > 0:
        recommendation_message.append(f"{Urea:.2f} ኪሎ ግራም ዩሪያ")

    if recommendation_message:
        return "እንዲጨምሩ ምንመክርዎት " + ", ".join(recommendation_message) + "."
    else:
        return "ተጨማሪ ማዳበሪያ አያስፈልግም።"

def main():
    st.image('Artificial Intelligence Institute.jpg')
    # Styling for Streamlit
    st.markdown("""
    <div style="background-color:blue;padding:10px">
    <h1 style="color:white;text-align:center;">ኢትዮጵያ አርቴፊሻል ኢንተለጀንስ ኢንስቲትዩት </h1>
    <h2 style="color:white;text-align:center;"> የማዳበሪያ አማካሪ መተግበሪያ</h2>
    </div>
    """, unsafe_allow_html=True)


    # Input fields
      
    # Crop types
    my_list = ['ፖም', 'ሙዝ', 'አደንግዋሬ/ቦሎቄ', 'ሽምብራ', 'ኮኮናት', 'ቡና', 'ጥጥ', 'ወይን', 'ጁት', 'ምስር', 'በቆሎ', 'ማንጎ', 'አኩሪአተር', 'ማሾ', 'መስክሜሎን', 'ብርቱካን', 'ፓፓያ', 'ርግብ አተር', 'ሮማን', 'ሩዝ', 'ሀብሃብ']
    crop_dict = {crop: idx for idx, crop in enumerate(my_list)}
    
    label = st.selectbox('የሚተከለው የሰብል አይነት', my_list)
    crop_type = crop_dict[label]
    
    hectares = st.number_input('በሰብል የተሸፈነው መሬት መጠን (በሄክታር)', min_value=0.00, step=0.01, format="%.2f")
    N_amount = st.number_input('የአፈር ውስጥ የናይትሮጂን መጠን (ሚግ / ኪግ)', min_value=0.0, step=0.01, format="%.2f")
    P_amount = st.number_input('የአፈር ውስጥ የፎስፈረስ መጠን (ሚግ / ኪግ)', min_value=0.0, step=0.01, format="%.2f")
    K_amount = st.number_input('የአፈር ውስጥ የፖታስየም መጠን (ሚግ / ኪግ)', min_value=0.0, step=0.01, format="%.2f")
    temperature = st.number_input('አማካይ የሙቀት መጠን (°C)', min_value=0.0, step=0.01, format="%.2f")
    humidity = st.number_input('የአየር እርጥበት መጠን (%)', min_value=0.0, max_value=100.0, step=0.0001, format="%.4f")
    ph = st.number_input('ፒኤች(pH) መጠን ', min_value=0.0, step=0.000000000000001, format="%.15f")
    rainfall = st.number_input('አማካይ የዝናብ መጠን (ሚሚ)', min_value=0.00, step=0.01, format="%.2f")
    
  
    result = ""
    if st.button("መተንበይ"):
        result = predict_amount_of_fertilizer(N_amount, P_amount, K_amount, temperature, humidity, ph, rainfall, hectares, crop_type)
    
    st.success(result)

    if st.button("ስለዚህ መተግበሪያ"):
        st.text("ይህ በኢትዮጵያ አርቲፊሻል ኢንተለጀንስ ኢንስቲትዩት የ2024 ክረምት ካምፕ")
        st.text("ውስጥ የተሰራ የማሽን መማሪያ ፕሮጀክት ነው።")

if __name__ == '__main__':
    main()
