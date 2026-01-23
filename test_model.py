import pickle
import pandas as pd

# Load model & encoders
model = pickle.load(open("debt_risk_model.pkl", "rb"))
encoders = pickle.load(open("encoders.pkl", "rb"))

# Sample farmer input (same as form)
sample = {
    "Land Size": "1 – 2 acres",
    "Budget": 60000,
    "Previous Loan": "Yes",
    "Loan Amount": 25000,
    "Soil Type": "Red Soil",
    "Season": "Kharif"
}

df = pd.DataFrame([sample])

# Encode categorical values
for col in encoders:
    df[col] = encoders[col].transform(df[col])

# Predict
prediction = model.predict(df)

print("🧠 Predicted Debt Risk Level:", prediction[0])
