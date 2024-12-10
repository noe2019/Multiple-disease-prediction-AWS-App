import os
import joblib  # Use joblib for loading models
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Health Assistant",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# Get the working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to load models
def load_model(file_path):
    try:
        # Load the model using joblib
        return joblib.load(file_path)
    except Exception as e:
        st.error(f"Error loading model from {file_path}: {e}")
        return None

# Load the saved models using joblib
diabetes_model = load_model(os.path.join(BASE_DIR, 'models/diabetes/best_diabetes_prediction_model.pkl'))
heart_disease_model = load_model(os.path.join(BASE_DIR, 'models/heart_disease/best_heart_disease_prediction_model.pkl'))
parkinsons_model = load_model(os.path.join(BASE_DIR, 'models/parkinson/best_model.pkl'))

# Ensure all models are loaded successfully
if not all([diabetes_model, heart_disease_model, parkinsons_model]):
    st.stop()

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        "Multiple Disease Prediction System",
        ["Diabetes Prediction", "Heart Disease Prediction", "Parkinson's Prediction"],
        menu_icon="hospital-fill",
        icons=["activity", "heart", "person"],
        default_index=0
    )

# Helper function for predictions
def make_prediction(model, user_input, feature_names):
    try:
        # Validate empty inputs
        if any(val.strip() == "" for val in user_input):
            empty_fields = [feature_names[i] for i, val in enumerate(user_input) if val.strip() == ""]
            st.error(f"The following fields are empty: {', '.join(empty_fields)}. Please fill them out.")
            return None
        
        # Convert inputs to float
        input_data = [float(value) for value in user_input]

        # Make prediction
        prediction = model.predict([input_data])[0]
        return prediction
    except ValueError as ve:
        st.error(f"Input error: Please ensure all inputs are numeric. Error details: {ve}")
        return None
    except Exception as e:
        st.error(f"Unexpected error during prediction: {e}")
        return None

# Diabetes Prediction Page
if selected == "Diabetes Prediction":
    st.title("Diabetes Prediction using ML")

    diabetes_inputs = {
        "Pregnancy's age (Months)": st.text_input("Pregnancy's age (Months)"),
        "Glucose Level": st.text_input("Glucose Level"),
        "Blood Pressure Value": st.text_input("Blood Pressure Value"),
        "Skin Thickness Value": st.text_input("Skin Thickness Value"),
        "Insulin Level": st.text_input("Insulin Level"),
        "BMI Value": st.text_input("BMI Value"),
        "Diabetes Pedigree Function Value": st.text_input("Diabetes Pedigree Function Value"),
        "Age of the Person": st.text_input("Age of the Person")
    }

    if st.button("Diabetes Test Result"):
        prediction = make_prediction(
            diabetes_model,
            list(diabetes_inputs.values()),
            list(diabetes_inputs.keys())
        )
        if prediction is not None:
            result = "The person is diabetic" if prediction == 1 else "The person is not diabetic"
            st.success(result)

# Heart Disease Prediction Page
if selected == "Heart Disease Prediction":
    st.title("Heart Disease Prediction using ML")

    heart_inputs = {
        "Age": st.text_input("Age of the Person"),
        "Sex (1 = Male, 0 = Female)": st.text_input("Sex (1 = Male, 0 = Female)"),
        "Chest Pain Type (0-3)": st.text_input("Chest Pain Type (0 = Typical Angina, 1 = Atypical Angina, 2 = Non-anginal Pain, 3 = Asymptomatic)"),
        "Resting Blood Pressure (mmHg)": st.text_input("Resting Blood Pressure (mmHg)"),
        "Serum Cholesterol (mg/dl)": st.text_input("Serum Cholesterol (mg/dl)"),
        "Fasting Blood Sugar (>120 mg/dl, 1 = Yes, 0 = No)": st.text_input("Fasting Blood Sugar (>120 mg/dl, 1 = Yes, 0 = No)"),
        "Resting ECG Results (0-2)": st.text_input("Resting ECG Results (0 = Normal, 1 = ST-T Wave Abnormality, 2 = Left Ventricular Hypertrophy)"),
        "Maximum Heart Rate Achieved": st.text_input("Maximum Heart Rate Achieved"),
        "Exercise Induced Angina (1 = Yes, 0 = No)": st.text_input("Exercise Induced Angina (1 = Yes, 0 = No)"),
        "ST Depression Induced by Exercise": st.text_input("ST Depression Induced by Exercise"),
        "Slope of Peak Exercise ST Segment (0-2)": st.text_input("Slope of Peak Exercise ST Segment (0 = Upsloping, 1 = Flat, 2 = Downsloping)"),
        "Number of Major Vessels Colored by Fluoroscopy (0-3)": st.text_input("Number of Major Vessels Colored by Fluoroscopy (0-3)"),
        "Thalassemia (1 = Normal, 2 = Fixed Defect, 3 = Reversible Defect)": st.text_input("Thalassemia (1 = Normal, 2 = Fixed Defect, 3 = Reversible Defect)")
    }

    if st.button("Heart Disease Test Result"):
        prediction = make_prediction(
            heart_disease_model,
            list(heart_inputs.values()),
            list(heart_inputs.keys())
        )
        if prediction is not None:
            result = "The person has heart disease" if prediction == 1 else "The person does not have heart disease"
            st.success(result)

# Parkinson's Prediction Page
if selected == "Parkinson's Prediction":
    st.title("Parkinson's Disease Prediction using ML")

    parkinsons_inputs = {
        "Unified Parkinson's Disease Rating Scale (UPDRS)": st.text_input("Unified Parkinson's Disease Rating Scale (UPDRS)"),
        "Functional Assessment Score": st.text_input("Functional Assessment Score (range: 0-100)"),
        "Tremor Severity Score": st.text_input("Tremor Severity Score (range: 0-10)"),
        "Montreal Cognitive Assessment (MoCA) Score": st.text_input("Montreal Cognitive Assessment (MoCA) Score (range: 0-30)"),
        "Postural Instability Score": st.text_input("Postural Instability Score (range: 0-10)"),
        "Bradykinesia Score": st.text_input("Bradykinesia Score (range: 0-10)"),
        "Education Level (Years)": st.text_input("Years of Education"),
        "Diabetes (1 = Yes, 0 = No)": st.text_input("Diabetes Diagnosis (1 = Yes, 0 = No)"),
        "Depression (1 = Yes, 0 = No)": st.text_input("Depression Diagnosis (1 = Yes, 0 = No)"),
        "Hypertension (1 = Yes, 0 = No)": st.text_input("Hypertension Diagnosis (1 = Yes, 0 = No)"),
        "Gender (1 = Male, 0 = Female)": st.text_input("Gender (1 = Male, 0 = Female)"),
        "Body Mass Index (BMI)": st.text_input("Body Mass Index (BMI)"),
        "History of Stroke (1 = Yes, 0 = No)": st.text_input("History of Stroke (1 = Yes, 0 = No)"),
        "Sleep Disorders (1 = Yes, 0 = No)": st.text_input("Sleep Disorders Diagnosis (1 = Yes, 0 = No)"),
        "Diastolic Blood Pressure (mmHg)": st.text_input("Diastolic Blood Pressure (mmHg)"),
        "Constipation (1 = Yes, 0 = No)": st.text_input("Constipation Diagnosis (1 = Yes, 0 = No)"),
        "Rigidity Score": st.text_input("Rigidity Score (range: 0-10)"),
        "Cholesterol/HDL Ratio": st.text_input("Cholesterol/HDL Ratio"),
        "Family History of Parkinson's (1 = Yes, 0 = No)": st.text_input("Family History of Parkinson's (1 = Yes, 0 = No)"),
        "Traumatic Brain Injury History (1 = Yes, 0 = No)": st.text_input("History of Traumatic Brain Injury (1 = Yes, 0 = No)")
    }

    if st.button("Parkinson's Test Result"):
        prediction = make_prediction(
            parkinsons_model,
            list(parkinsons_inputs.values()),
            list(parkinsons_inputs.keys())
        )
        if prediction is not None:
            result = "The person has Parkinson's disease" if prediction == 1 else "The person does not have Parkinson's disease"
            st.success(result)