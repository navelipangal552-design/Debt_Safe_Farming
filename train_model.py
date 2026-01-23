import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

df = pd.read_csv("farmers_data.csv") #load the dataset

#Create Debt Risk Label
def risk_label(row):
    budget = row["Budget"]
    loan = row["Loan Amount"]

    if loan == 0:
        return "Low"
    ratio = loan / budget

    if ratio <= 0.3:
        return "Low"
    elif ratio <= 0.6:
        return "Medium"
    else:
        return "High"

df["Debt_Risk_Level"] = df.apply(risk_label, axis=1)

# ==============================
# STEP 4: Encode categorical columns
#text to numbers
label_encoders = {}

categorical_cols = ["Land Size", "Previous Loan", "Soil Type", "Season"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le   # save encoders for later use

#input to AI
X = df[
    [
        "Land Size",
        "Budget",
        "Previous Loan",
        "Loan Amount",
        "Soil Type",
        "Season"
    ]
]

y = df["Debt_Risk_Level"]


# ==============================
# STEP 6: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ==============================
# STEP 7: Train Decision Tree model
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)


# ==============================
# STEP 8: Evaluate the model
# ==============================
y_pred = model.predict(X_test)
print("Model Evaluation:\n")
print(classification_report(y_test, y_pred))


# ==============================
# STEP 9: Save model and encoders
# ==============================
pickle.dump(model, open("debt_risk_model.pkl", "wb"))
pickle.dump(label_encoders, open("encoders.pkl", "wb"))

print("\n✅ Model and encoders saved successfully.")
