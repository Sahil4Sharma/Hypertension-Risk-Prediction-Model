import streamlit as st
import pandas as pd
import joblib

model = joblib.load("model.joblib")

st.title("Hypertension Risk Estimator")

male = 1 if st.selectbox("Gender", ["Male", "Female"]) == "Male" else 0
age = st.number_input("Age", 20, 100, 45)
smoker = st.selectbox("Current smoker?", ["No", "Yes"]) == "Yes"
cigs = st.number_input("Cigarettes per day", 0, 70, 0) if smoker else 0
bpmeds = int(st.selectbox("Taking BP medicine?", ["No", "Yes"]) == "Yes")
diabetes = int(st.selectbox("Diabetes?", ["No", "Yes"]) == "Yes")
chol = st.number_input("Total cholesterol", 100, 700, 200)
sys_bp = st.number_input("Systolic BP", 80, 300, 120)
dia_bp = st.number_input("Diastolic BP", 40, 150, 80)
bmi = st.number_input("BMI", 10.0, 60.0, 25.0)
hr = st.number_input("Heart rate", 40, 150, 75)
glucose = st.number_input("Glucose", 40, 400, 90)

if st.button("Predict"):
    data = pd.DataFrame([{
        "male": male,
        "age": age,
        "currentSmoker": int(smoker),
        "cigsPerDay": cigs,
        "BPMeds": bpmeds,
        "diabetes": diabetes,
        "totChol": chol,
        "sysBP": sys_bp,
        "diaBP": dia_bp,
        "BMI": bmi,
        "heartRate": hr,
        "glucose": glucose,
    }])
    p = model.predict_proba(data)[0][1] * 100
    if p < 25:
        st.success(f"Low risk. Estimated chance: {p:.1f}%")
    elif p < 50:
        st.info(f"Mild risk. Estimated chance: {p:.1f}%")
    elif p < 75:
        st.warning(f"Elevated risk. Estimated chance: {p:.1f}%")
    else:
        st.error(f"High risk. Estimated chance: {p:.1f}%")
    st.caption("This is an estimate from a statistical model, not a medical diagnosis.")
