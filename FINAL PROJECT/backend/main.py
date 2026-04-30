# Import FastAPI framework to build the web API
from fastapi import FastAPI

# Import CORS middleware to handle cross-origin requests (e.g., from React frontend)
from fastapi.middleware.cors import CORSMiddleware

# Import BaseModel from Pydantic for request body validation and type checking
from pydantic import BaseModel

# Import joblib to load the pre-trained ML model and scaler from disk
import joblib

# Import numpy for numerical array operations required by the ML model
import numpy as np

# Initialize the FastAPI application instance
app = FastAPI()

# Register CORS middleware to allow the React frontend to make API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Accept requests from any origin (restrict in production)
    allow_credentials=True,    # Allow cookies and auth headers to be sent cross-origin
    allow_methods=["*"],       # Allow all HTTP methods: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],       # Allow all request headers (e.g., Content-Type, Authorization)
)

# Load the pre-trained SVM (Support Vector Machine) model saved as a .pkl file
# This model was previously trained and serialized using joblib
model = joblib.load('../models/svm_model.pkl')

# Load the pre-fitted scaler (e.g., StandardScaler) used during training
# It's critical to use the SAME scaler from training to ensure consistent feature normalization
scaler = joblib.load('../models/scaler.pkl')

# Define the expected shape and types of the incoming request body using Pydantic
# FastAPI will automatically validate and parse the JSON body into this model
class PatientData(BaseModel):
    Glucose: float                    # Blood glucose concentration level
    BMI: float                        # Body Mass Index (weight/height²)
    Age: float                        # Patient's age in years
    Pregnancies: float                # Number of times the patient has been pregnant
    DiabetesPedigreeFunction: float   # Genetic likelihood score of diabetes based on family history

# Define the POST endpoint at "/predict" that accepts patient data and returns a prediction
@app.post("/predict")
def predict_diabetes(data: PatientData):

    # Convert the incoming Pydantic model fields into a 2D NumPy array
    # Shape must be (1, 5) — one sample with five features — as required by scikit-learn
    input_data = np.array([[
        data.Glucose, data.BMI, data.Age, data.Pregnancies, data.DiabetesPedigreeFunction
    ]])

    # Apply the same scaling transformation used during model training
    # This standardizes features to have zero mean and unit variance
    # Skipping this step would cause incorrect predictions due to feature scale mismatch
    scaled_data = scaler.transform(input_data)

    # Use the loaded SVM model to predict the class label: 1 (diabetic) or 0 (non-diabetic)
    prediction = model.predict(scaled_data)

    # Get the predicted probability scores for both classes [class_0, class_1]
    # We extract index [0][1] to get the probability of being diabetic (class 1)
    probability = model.predict_proba(scaled_data)[0][1]

    # Return a JSON response containing:
    # - outcome: binary prediction (0 or 1) cast to Python int for JSON serialization
    # - probability: confidence score (0.0 to 1.0) of the diabetic prediction
    # - message: human-readable risk label based on the predicted class
    return {
        "outcome": int(prediction[0]),         # 1 = diabetic, 0 = non-diabetic
        "probability": float(probability),     # e.g., 0.87 means 87% chance of diabetes
        "message": "High risk of diabetes" if prediction[0] == 1 else "Low risk of diabetes"
    }
