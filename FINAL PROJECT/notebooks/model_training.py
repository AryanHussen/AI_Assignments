# Import required libraries
import pandas as pd
import numpy as np

# Scikit-learn tools for preprocessing, modeling, and evaluation
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# For saving trained models
import joblib
import os

# ---------------------------------------------------------
# Ensure the models directory exists (to store trained files)
# ---------------------------------------------------------
os.makedirs('../models', exist_ok=True)

# ---------------------------------------------------------
# 1. Load Dataset
# ---------------------------------------------------------
print("Loading dataset...")

# Read dataset from CSV file
df = pd.read_csv('../data/diabetes.csv')

# Separate features (X) and target (y)
X = df.drop('Outcome', axis=1)  # Input features
y = df['Outcome']               # Target variable (0 or 1)

# ---------------------------------------------------------
# 2. Feature Selection
# ---------------------------------------------------------
print("\n--- Feature Selection ---")

# Select top 5 most important features using ANOVA F-test
selector = SelectKBest(score_func=f_classif, k=5)

# Apply feature selection
X_selected = selector.fit_transform(X, y)

# Get names of selected features
selected_features = X.columns[selector.get_support()].tolist()
print(f"Top 5 most effective features identified: {selected_features}")

# ---------------------------------------------------------
# 3. Data Preprocessing
# ---------------------------------------------------------

# Split dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X_selected, y, test_size=0.2, random_state=42
)

# Standardize features (important for distance-based models)
scaler = StandardScaler()

# Fit scaler on training data and transform both train and test data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler for later use in backend (FastAPI)
joblib.dump(scaler, '../models/scaler.pkl')
print("Scaler saved to '../models/scaler.pkl'")

# ---------------------------------------------------------
# 4. Initialize Models
# ---------------------------------------------------------
models = {
    # k-Nearest Neighbors model
    "kNN": KNeighborsClassifier(n_neighbors=5),

    # Naive Bayes model
    "Naive Bayes": GaussianNB(),

    # Support Vector Machine (RBF kernel)
    # probability=True enables confidence score output
    "SVM": SVC(kernel='rbf', probability=True),

    # Neural Network (Multi-Layer Perceptron)
    # 2 hidden layers with 16 and 8 neurons
    "Neural Network (MLP)": MLPClassifier(
        hidden_layer_sizes=(16, 8),
        activation='relu',
        max_iter=1000,
        random_state=42
    )
}

# ---------------------------------------------------------
# 5. Train and Evaluate Models
# ---------------------------------------------------------
print("\n--- Model Evaluation ---")

for name, model in models.items():

    # Train the model using training data
    model.fit(X_train_scaled, y_train)

    # Make predictions on test data
    y_pred = model.predict(X_test_scaled)

    # Calculate accuracy
    acc = accuracy_score(y_test, y_pred)
    print(f"{name} Accuracy: {acc:.4f}")

    # Save specific models for backend use

    # Save SVM model
    if name == "SVM":
        joblib.dump(model, '../models/svm_model.pkl')
        print("  -> Saved to '../models/svm_model.pkl'")

    # Save Neural Network model
    if name == "Neural Network (MLP)":
        joblib.dump(model, '../models/nn_model.pkl')
        print("  -> Saved to '../models/nn_model.pkl'")

# ---------------------------------------------------------
# Done
# ---------------------------------------------------------
print("\nTraining complete! Your pipeline is ready. You can now start the FastAPI backend.")
