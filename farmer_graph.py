import matplotlib.pyplot as plt

land_size = "More than 5 acres"
budget = 20000
loan_amount = 1000
risk_level = "Low"   # output from your AI model

# =========================
# Map risk to numeric score
# =========================
risk_map = {
    "Low": 30,
    "Medium": 60,
    "High": 85
}

risk_score = risk_map[risk_level]

# =========================
# Calculate profit potential
# =========================
profit_score = round(((budget - loan_amount) / budget) * 100, 2)

# =========================
# Plot Graph
# =========================
labels = ["Profit Potential", "Risk Level"]
values = [profit_score, risk_score]

plt.figure(figsize=(6, 4))
plt.bar(labels, values)
plt.ylim(0, 100)

plt.title("Profit & Risk Analysis")
plt.ylabel("Score (%)")

# Value labels
for i, val in enumerate(values):
    plt.text(i, val + 2, f"{val}%", ha="center")

plt.show()
