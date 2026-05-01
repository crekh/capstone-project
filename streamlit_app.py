

import streamlit as st
import numpy as np
import joblib

st.write("App version: NEW CODE LOADED")

st.set_page_config(page_title="Cardio Risk Dashboard", layout="wide")

model = joblib.load("cardio_model.pkl")

# -----------------------------
# SIDEBAR (Patient Inputs)
# -----------------------------
st.sidebar.title("🧾 Patient Input Form")

age = st.sidebar.slider("Age", 18, 100, 40)
bmi = st.sidebar.slider("BMI", 10.0, 50.0, 25.0)
ap_hi = st.sidebar.slider("Systolic BP", 80, 200, 120)
ap_lo = st.sidebar.slider("Diastolic BP", 40, 130, 80)

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
gender = 1 if gender == "Male" else 2

cholesterol = st.sidebar.radio(
    "Cholesterol Level",
    ["Normal", "Above Normal", "Well Above Normal"]
)
cholesterol = {"Normal":1, "Above Normal":2, "Well Above Normal":3}[cholesterol]

gluc = st.sidebar.radio(
    "Glucose Level",
    ["Normal", "Above Normal", "Well Above Normal"]
)
gluc = {"Normal":1, "Above Normal":2, "Well Above Normal":3}[gluc]

smoke = st.sidebar.selectbox("Smoker", ["No", "Yes"])
smoke = 1 if smoke == "Yes" else 0

alco = st.sidebar.selectbox("Alcohol Intake", ["No", "Yes"])
alco = 1 if alco == "Yes" else 0

active = st.sidebar.selectbox("Physically Active", ["No", "Yes"])
active = 1 if active == "Yes" else 0


# -----------------------------
# MAIN DASHBOARD
# -----------------------------
st.title("🫀 Cardiovascular Risk Prediction Dashboard")

st.markdown("### Patient Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Age", age)
    st.metric("Gender", "Male" if gender == 1 else "Female")

with col2:
    st.metric("BMI", bmi)
    st.metric("Blood Pressure", f"{ap_hi}/{ap_lo}")

with col3:
    st.metric("Cholesterol Level", cholesterol)
    st.metric("Glucose Level", gluc)


# -----------------------------
# PREDICTION
# -----------------------------
import pandas as pd

# Define features EXACTLY as used in training
features = ['age','gender','BMI','ap_hi','ap_lo',
            'cholesterol','gluc','smoke','alco','active']

# Create input as DataFrame
input_df = pd.DataFrame([[
    age, gender, bmi, ap_hi, ap_lo,
    cholesterol, gluc, smoke, alco, active
]], columns=features)

# Predict probability
proba = model.predict_proba(input_df)[0][1]

# Convert to class
prediction = 1 if proba > 0.5 else 0

if st.button("🧠 Analyze Risk"):

    proba = model.predict_proba(input_data)[0][1]
    prediction = model.predict(input_data)[0]

    st.markdown("---")
    st.subheader("📊 Risk Assessment")

    colA, colB = st.columns(2)

    with colA:
        st.metric("Risk Probability", f"{proba*100:.2f}%")

    with colB:
        if prediction == 1:
            st.error("⚠ HIGH CARDIOVASCULAR RISK DETECTED")
        else:
            st.success("✅ LOW RISK PROFILE")


    # -----------------------------
    # INTERPRETATION PANEL
    # -----------------------------
    st.markdown("### 🩺 Clinical Interpretation")

    if proba > 0.7:
        st.warning("High risk influenced by BP, BMI, and metabolic indicators.")
    elif proba > 0.4:
        st.info("Moderate risk detected. Lifestyle changes recommended.")
    else:
        st.success("Low cardiovascular risk. Maintain healthy habits.")
