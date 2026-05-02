# Import the FastAPI framework to build the web API
from fastapi import FastAPI
# Import CORS middleware to handle cross-origin requests from the frontend
from fastapi.middleware.cors import CORSMiddleware
# Import BaseModel from Pydantic for automatic request body validation
from pydantic import BaseModel
# Import joblib to deserialize (load) the pre-trained model and scaler files
import joblib
# Import NumPy for numerical array operations required by Scikit-Learn
import numpy as np

# Create the FastAPI application instance — this is the core of our API server
app = FastAPI()

# Register CORS middleware so the React frontend (running on a different port) can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Accept requests from any origin (lock this down in production)
    allow_credentials=True,     # Allow cookies and auth headers to be sent cross-origin
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],        # Allow all request headers (Content-Type, Authorization, etc.)
)

# ─── LOAD ALL MODELS & SCALER ──────────────────────────────────────────
# Load both models and the scaler once at startup — avoids reloading on every request

# Load the Support Vector Machine model trained on the diabetes dataset
svm_model = joblib.load('../models/svm_model.pkl')
# Load the Neural Network model trained on the same dataset
nn_model = joblib.load('../models/nn_model.pkl')
# Load the StandardScaler fitted on training data — must use the SAME scaler used during training
scaler = joblib.load('../models/scaler.pkl')

# Define the expected shape of the incoming JSON request body using Pydantic
class PatientData(BaseModel):
    # Each field maps to one of the Top 5 most important features identified during feature selection
    # The order here must match the column order used when the models were trained
    Glucose: float                    # Plasma glucose concentration (most predictive feature)
    BMI: float                        # Body Mass Index — weight in kg / (height in m)^2
    Age: float                        # Patient age in years
    Pregnancies: float                # Number of times the patient has been pregnant
    DiabetesPedigreeFunction: float   # Genetic risk score based on family history

# Define the POST endpoint — the frontend sends patient data here to get a prediction
@app.post("/predict")
def predict_diabetes(data: PatientData):
    # --- Step 1: Prepare the input array ---
    # Scikit-Learn models expect a 2D array of shape (n_samples, n_features)
    # We wrap the values in double brackets to create shape (1, 5) — one patient, five features
    input_data = np.array([[
        data.Pregnancies, data.Glucose, data.BMI,data.DiabetesPedigreeFunction ,data.Age
    ]])

    # --- Step 2: Scale the input features ---
    # Apply the same StandardScaler transformation used on training data
    # This converts raw values to z-scores: (value - mean) / std
    # Without this step, features with large ranges (e.g. Glucose) would dominate the prediction
    scaled_data = scaler.transform(input_data)

    # --- Step 3: Get probability estimates from each model independently ---
    # predict_proba() returns a 2D array: [[prob_negative, prob_positive]]
    # [0] selects the first (and only) sample row
    # [1] selects the probability of class 1 (diabetic)
    prob_svm = svm_model.predict_proba(scaled_data)[0][1]   # SVM's confidence the patient is diabetic
    prob_nn  = nn_model.predict_proba(scaled_data)[0][1]    # Neural Network's confidence the patient is diabetic

    # --- Step 4: Combine predictions via soft voting (ensemble averaging) ---
    # Averaging the two probabilities reduces variance and improves reliability
    # This is called a "soft voting ensemble" — each model gets equal weight (0.5 each)
    avg_probability = (prob_svm + prob_nn) / 2

    # --- Step 5: Apply classification threshold ---
    # If the ensemble probability is >= 50%, classify as diabetic (1), otherwise healthy (0)
    # 0.5 is the standard threshold; lower it to catch more true positives at the cost of more false positives
    final_prediction = 1 if avg_probability >= 0.5 else 0

    # --- Step 6: Return a structured JSON response ---
    return {
        "outcome": int(final_prediction),              # Binary result: 1 = diabetic, 0 = healthy
        "probability": float(avg_probability),         # Ensemble confidence score (0.0 – 1.0)
        "details": {
            "svm_confidence": float(prob_svm),         # SVM's individual probability estimate
            "nn_confidence":  float(prob_nn)           # Neural Network's individual probability estimate
        },
        # Human-readable interpretation of the final prediction
        "message": "High risk of diabetes" if final_prediction == 1 else "Low risk of diabetes"
    }
