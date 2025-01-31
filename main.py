from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

app = FastAPI()

# Load historical NEET data
neet_data = pd.read_csv("neet_historical_results.csv")

# Selecting features and target
features = ["accuracy", "time_efficiency", "difficulty_avg", "improvement_rate"]
target = "neet_rank"

X = neet_data[features]
y = neet_data[target]

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "neet_rank_model.pkl")

# Load model function
def load_model():
    return joblib.load("neet_rank_model.pkl")

# Predict Rank API
@app.post("/predict-rank")
def predict_rank(accuracy: float, time_efficiency: float, difficulty_avg: float, improvement_rate: float):
    model = load_model()
    input_data = np.array([[accuracy, time_efficiency, difficulty_avg, improvement_rate]])
    predicted_rank = model.predict(input_data)[0]
    return {"predicted_rank": int(predicted_rank)}

# College Prediction API
@app.get("/predict-college/{rank}")
def predict_college(rank: int):
    college_cutoffs = pd.read_csv("neet_college_cutoffs.csv")
    eligible_colleges = college_cutoffs[college_cutoffs["cutoff_rank"] >= rank]["college_name"].tolist()
    return {"eligible_colleges": eligible_colleges}
