from flask import Flask, request, jsonify
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import os


app = Flask(__name__)

model = pickle.load(open("debt_risk_model.pkl", "rb"))
encoders = pickle.load(open("encoders.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    df = pd.DataFrame([data])


    for col in encoders:
     if df[col][0] in encoders[col].classes_:
        df[col] = encoders[col].transform(df[col])
     else:
        # Assign a default value (most frequent class)
        df[col] = encoders[col].transform([encoders[col].classes_[0]])


    # for col in encoders:
    #     df[col] = encoders[col].transform(df[col])

    # Predict risk
    risk = model.predict(df)[0]

    # Get probability (ML confidence)
    probs = model.predict_proba(df)[0]
    classes = model.classes_

    risk_scores = dict(zip(classes, (probs * 100).round(2)))

    return jsonify({
        "debt_risk": risk,
        "risk_scores": risk_scores
    })


if __name__ == "__main__":
    app.run(port=5000)
