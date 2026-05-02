from fastapi import FastAPI  # FastAPI: modern web framework for building APIs; auto-generates docs and validates inputs
from fastapi.middleware.cors import CORSMiddleware  # CORS middleware: controls which external origins (domains) are allowed to call this API
from pydantic import BaseModel  # BaseModel: used to define and validate the shape/types of incoming request data
import joblib  # joblib: used to load the serialized (saved) sklearn model and scaler objects from disk
import numpy as np  # numpy: used to convert input data into an array format that sklearn models expect

app = FastAPI()  # create the FastAPI application instance; this is the main object that handles all routes and middleware

# Enable CORS so the React frontend can talk to this API
app.add_middleware(  # register a middleware layer that runs on every incoming request before it reaches the route handler
    CORSMiddleware,  # use the CORS middleware specifically to handle cross-origin request headers
    allow_origins=["*"],  # allow requests from ANY origin (domain); in production replace "*" with your actual frontend URL e.g. "http://localhost:3000"
    allow_credentials=True,  # allow cookies and HTTP authentication headers to be included in cross-origin requests
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, PUT, DELETE, etc.) from cross-origin requests
    allow_headers=["*"],  # allow all HTTP headers (e.g. Content-Type, Authorization) in cross-origin requests
)

model = joblib.load('../models/svm_model.pkl')  # deserialize and load the pre-trained SVM model from disk into memory so it's ready to make predictions
scaler = joblib.load('../models/scaler.pkl')  # deserialize and load the fitted StandardScaler from disk; needed to apply the exact same scaling used during training

class PatientData(BaseModel):  # define a Pydantic model (data schema) that describes the expected JSON body of the POST request
    Glucose: float  # patient's plasma glucose concentration — must be a float; Pydantic will reject the request if this field is missing or wrong type
    BMI: float  # Body Mass Index (weight/height²) — one of the top predictive features selected during training
    Age: float  # patient's age in years — stored as float for consistency with the scaler's expectations
    Pregnancies: float  # number of times the patient has been pregnant — float because scaler expects numeric, not int
    DiabetesPedigreeFunction: float  # a score representing genetic diabetes risk based on family history — continuous value between 0 and ~2.5

@app.post("/predict")  # register a POST route at the "/predict" endpoint; POST is used because we are sending data (patient inputs) in the request body
def predict_diabetes(data: PatientData):  # FastAPI automatically parses the JSON request body and validates it against PatientData; 'data' holds the validated values
    input_data = np.array([[  # convert the 5 patient feature values into a 2D NumPy array with shape (1, 5); sklearn models require 2D input — [[...]] creates 1 row, 5 columns
       data.Pregnancies, data.Glucose, data.BMI,data.DiabetesPedigreeFunction ,data.Age   # extract each field from the validated Pydantic object in the SAME ORDER the model was trained on
    ]])

    scaled_data = scaler.transform(input_data)  # apply the same StandardScaler (mean=0, std=1) that was used during training; ensures the model receives data in the same scale it learned from

    prediction = model.predict(scaled_data)  # run the SVM model on the scaled input; returns an array e.g. [1] (diabetic) or [0] (not diabetic)

    probability = model.predict_proba(scaled_data)[0][1]  # predict_proba returns [[prob_class_0, prob_class_1]]; [0] gets the first (only) sample; [1] gets the probability of class 1 (diabetic)

    return {  # return a JSON response object to the frontend with three fields
        "outcome": int(prediction[0]),  # prediction[0] extracts the scalar value from the array; cast to int so JSON can serialize it (numpy int64 is not JSON-serializable by default)
        "probability": float(probability),  # cast to Python float for the same reason — numpy float64 must be converted before returning as JSON
        "message": "High risk of diabetes" if prediction[0] == 1 else "Low risk of diabetes"  # human-readable verdict: if prediction is 1 → high risk, if 0 → low risk
    }
