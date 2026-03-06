import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("model.pkl","rb"))

st.set_page_config(
    page_title="Heart Disease Predictor",
    layout="wide"
)

# Glassmorphism CSS
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

.big-title{
font-size:70px;
font-weight:800;
text-align:center;
color:white;
}

.subtitle{
text-align:center;
font-size:22px;
color:#d1d1d1;
margin-bottom:30px;
}

.stButton>button{
width:100%;
height:60px;
font-size:20px;
font-weight:bold;
background:#ff4b4b;
color:white;
border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="big-title">Heart Disease Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Powered Medical Risk Detection System</div>', unsafe_allow_html=True)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", 1, 120)

    sex = st.selectbox(
        "Gender",
        ["Male","Female"]
    )

    cp = st.selectbox(
        "Chest Pain Type",
        ["Typical Angina","Atypical Angina","Non-anginal Pain","Asymptomatic"]
    )

    trestbps = st.number_input("Resting Blood Pressure")

with col2:
    chol = st.number_input("Cholesterol")

    fbs = st.selectbox(
        "Fasting Blood Sugar >120",
        ["No","Yes"]
    )

    restecg = st.selectbox(
        "Rest ECG",
        ["Normal","ST-T abnormality","Left ventricular hypertrophy"]
    )

    thalach = st.number_input("Max Heart Rate")

with col3:
    exang = st.selectbox(
        "Exercise Induced Angina",
        ["No","Yes"]
    )

    oldpeak = st.number_input("ST Depression")

    slope = st.selectbox(
        "Slope",
        ["Upsloping","Flat","Downsloping"]
    )

    ca = st.selectbox(
        "Major Vessels",
        ["0","1","2","3"]
    )

    thal = st.selectbox(
        "Thalassemia",
        ["Normal","Fixed Defect","Reversible Defect"]
    )

st.markdown("</div>", unsafe_allow_html=True)

# Convert values
sex = 1 if sex=="Male" else 0

cp_map={
"Typical Angina":0,
"Atypical Angina":1,
"Non-anginal Pain":2,
"Asymptomatic":3
}
cp=cp_map[cp]

fbs = 1 if fbs=="Yes" else 0

restecg_map={
"Normal":0,
"ST-T abnormality":1,
"Left ventricular hypertrophy":2
}
restecg=restecg_map[restecg]

exang = 1 if exang=="Yes" else 0

slope_map={
"Upsloping":0,
"Flat":1,
"Downsloping":2
}
slope=slope_map[slope]

ca=int(ca)

thal_map={
"Normal":1,
"Fixed Defect":2,
"Reversible Defect":3
}
thal=thal_map[thal]

st.write("")
st.write("")

# Predict
if st.button("Predict Heart Disease"):

    input_data=np.array([[age,sex,cp,trestbps,chol,fbs,
                          restecg,thalach,exang,
                          oldpeak,slope,ca,thal]])

    prediction=model.predict(input_data)

    # probability
    if hasattr(model,"predict_proba"):
        prob=model.predict_proba(input_data)[0][1]
        risk_percent=round(prob*100,2)
    else:
        risk_percent=50

    st.write("")

    if prediction[0]==1:

        st.error(f"⚠️ High Risk of Heart Disease")

        st.progress(risk_percent/100)

        st.metric("Heart Disease Risk",f"{risk_percent}%")

    else:

        st.success("✅ Low Risk of Heart Disease")

        st.progress(risk_percent/100)

        st.metric("Risk Percentage",f"{risk_percent}%")