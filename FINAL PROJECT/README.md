<div align="center">

# 🏥 Diabetes Prediction System
### A Full-Stack Machine Learning Pipeline for Real-Time Diabetes Risk Assessment

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)

> Predicts diabetes risk in real-time using four trained ML classifiers, served through a FastAPI backend and a modern React interface.

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Live Demo & Features](#-features)
- [ML Model Performance](#-ml-model-performance)
- [System Architecture](#️-system-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Project](#-running-the-project)
- [API Reference](#-api-reference)
- [Team Roles](#-team-roles)

---

## 🎯 Project Overview

The **Diabetes Prediction System** is a full-stack AI application that leverages the [Kaggle Pima Indians Diabetes Dataset](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database) to predict a patient's risk of diabetes. It combines a trained machine learning backend with a responsive React-based user interface to deliver real-time diagnostic probabilities.

### Key Engineering Decisions

| Decision | Detail |
|---|---|
| **Feature Selection** | `SelectKBest` with ANOVA F-values — selects the top 5 most predictive health indicators |
| **Scaling** | `StandardScaler` applied manually to ensure accuracy for distance-based models (SVM, kNN) |
| **Model Persistence** | Trained models exported as `.pkl` files via `joblib` for production inference |
| **API Layer** | `FastAPI` with CORS enabled for seamless frontend-backend communication |
| **UI Feedback** | Dynamic Tailwind CSS color theming based on predicted risk level |

---

## ✨ Features

- 🔍 **Automated Feature Selection** — Identifies the 5 most critical predictors: `Pregnancies`, `Glucose`, `BMI`, `DiabetesPedigreeFunction`, and `Age`
- 🤖 **4 ML Classifiers** — Run predictions through Neural Network, SVM, Naive Bayes, and kNN simultaneously
- ⚡ **Real-Time Inference** — Sub-second predictions via FastAPI REST endpoint
- 🎨 **Risk-Aware UI** — Interface dynamically changes color based on low/high risk outcomes
- 📊 **Comparative Results** — View probability scores from all models side by side

---

## 📊 ML Model Performance

Models were trained and evaluated on the Kaggle Diabetes Dataset using an 80/20 train-test split.

| Rank | Model | Accuracy |
|:---:|---|:---:|
| 🥇 | Neural Network (MLP) | **77.27%** |
| 🥈 | Support Vector Machine (SVM) | **76.62%** |
| 🥉 | Naive Bayes | **75.32%** |
| 4 | k-Nearest Neighbors (kNN) | **73.38%** |

> The MLP classifier achieved the highest accuracy, though all four models are available in the UI for comparative analysis.

---

## ⚙️ System Architecture

```
┌─────────────────────┐         HTTP POST          ┌──────────────────────┐
│                     │  ─────────────────────────► │                      │
│   React Frontend    │     /predict (JSON body)    │   FastAPI Backend    │
│   (Vite + Tailwind) │                             │   (Uvicorn Server)   │
│                     │ ◄─────────────────────────  │                      │
└─────────────────────┘    Probability Scores       └──────────┬───────────┘
                                                               │
                                                    Loads .pkl files
                                                               │
                                              ┌────────────────▼───────────────┐
                                              │         models/                │
                                              │  ├── svm_model.pkl             │
                                              │  └── scaler.pkl                │
                                              └────────────────────────────────┘
```

**Data Flow:**
1. User enters health indicators in the React form
2. Axios sends a POST request to the FastAPI `/predict` endpoint
3. Backend loads the scaler and model(s), runs inference
4. Prediction probabilities are returned as JSON
5. Frontend renders results with dynamic risk-level styling

---
\---
## 📁 Project Structure
```
diabetes\_prediction\_project\
│
├── 📂 data/
│   └── diabetes.csv                  # Raw Kaggle Pima Indians dataset
│
├── 📂 notebooks/
│   └── model_training.py             # ML training, feature selection & evaluation
│
├── 📂 models/
│   ├── svm_model.pkl                 # Serialized SVM model weights
│   ├── nn_model.pkl                  # Serialized Neural Network weights
│   └── scaler.pkl                    # Fitted StandardScaler parameters
│
├── 📂 backend/
│   └── main.py                       # FastAPI server — routing & model inference
│
└── 📂 frontend/
    ├── 📂 public/                    # Static assets (favicons, icons)
    ├── 📂 src/
    │   ├── 📂 assets/                # Images (hero.png, react.svg, vite.svg)
    │   ├── App.css                   # Main application styling
    │   ├── App.jsx                   # Main React component & state management
    │   ├── index.css                 # Global Tailwind/CSS styles
    │   └── main.jsx                  # React DOM entry point
    ├── index.html                    # Frontend entry page
    ├── package.json                  # Node dependencies & scripts
    ├── tailwind.config.js            # Tailwind CSS configuration
    └── vite.config.js                # Vite build configuration

```
\---
## 🛠️ Prerequisites

Ensure you have the following installed before proceeding:

- **Python** `3.11+` — [Download](https://python.org/downloads)
- **Node.js** `18+` — [Download](https://nodejs.org)
- **pip** (comes with Python)
- **npm** (comes with Node.js)

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AryanHussen/AI_Assignments.git
cd "FINAL PROJECT/diabetes_prediction_project"
```

### 2. Install Backend Dependencies

```bash
pip install pandas numpy scikit-learn fastapi uvicorn pydantic joblib
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## 🚀 Running the Project

The system requires **two terminals** running simultaneously.

### Terminal 1 — Start the Backend API

```bash
cd backend
python -m uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`  
Interactive API docs: `http://127.0.0.1:8000/docs`

### Terminal 2 — Start the Frontend

```bash
cd frontend
npm run dev
```

The UI will be available at: `http://localhost:5173`

### Stopping the Application

Press `Ctrl + C` in each terminal to stop the backend and frontend servers.

---

## 🔌 API Reference

### `POST /predict`

Accepts patient health data and returns diabetes risk predictions from all trained models.

**Request Body**

```json
{
  "Pregnancies": 2,
  "Glucose": 138,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 50
}
```

**Response**

```json
{
  "Neural Network (MLP)": 0.82,
  "SVM": 0.79,
  "Naive Bayes": 0.74,
  "kNN": 0.71
}
```

---

## 👥 Team Roles

| Role | Module | Responsibilities |
|---|---|---|
| 🧠 **ML Engineer** | `notebooks/model_training.py` | Data preprocessing, feature selection via `SelectKBest`, model training & `.pkl` export |
| 🔄 **Backend & System Lead** | `backend/main.py` | FastAPI construction, CORS configuration, model loading & inference pipeline |
| 🌐 **UI/UX Developer** | `frontend/src/App.jsx` | React state management, Axios API integration, dynamic Tailwind risk-based UI theming |

---

## 📄 License

This project was developed as a final academic assignment. Dataset sourced from the [Kaggle Pima Indians Diabetes Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database).

---

<div align="center">

Made with ❤️ by the Diabetes Prediction System Team

</div>
