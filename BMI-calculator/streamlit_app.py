from tkinter import Button
import streamlit as st

st.title('BMI Calculator')

weight = st.number_input("Enter your weight (KGS)")

units = st.radio('Select your height in units: ',('cms','metres','feet'))

if (units == 'cms'):
    height = st.number_input('Centimetres')
    try:
        bmi = weight/((height/100)**2)
    except:
        st.text("Enter height")

elif(units == 'metres'):
    height = st.number_input('Metres')

    try:
        bmi = weight/height**2
    except:
        st.text("Enter height")

else:
    height = st.number_input('Feet')
    try:
        bmi = weight/((height/3.28)) ** 2
    except:
        st.text("Enter height")

if (st.button('Calculate BMI')):

    try:
        st.text(f"Your BMI is {bmi}")

        if (bmi < 16):
            st.error("You are extremely Underweight")
        elif (bmi >= 16 and bmi < 18.5):
            st.warning("You are Underweight")
        elif (bmi >= 18.5 and bmi < 25):
            st.success("Healthy")
        elif(bmi >= 22.5 and bmi < 30):
            st.warning("Overweight")
        elif (bmi >= 30):
            st.error("Extremely Overweight")
    
    except:
        st.error("Enter Weight!!")