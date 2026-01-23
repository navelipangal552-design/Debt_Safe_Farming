console.log("Starting server...");

const express = require("express");
const fs = require("fs");
const axios = require("axios");

const app = express();

app.use(express.json());
app.use(express.static("public"));

/* ===========================
   SAVE + AI PREDICTION ROUTE
=========================== */
app.post("/save", async (req, res) => {
  try {
    console.log("Received data:", req.body);

    const data = req.body;

    /* -------- Save to CSV -------- */
    const row = `${data.land_size},${data.budget},${data.previous_loan},${data.loan_amount},${data.soil_type},${data.season}\n`;
    fs.appendFileSync("farmers_data.csv", row);

// normalize loan value
let prevLoan = data.previous_loan.toLowerCase();

if (prevLoan === "yes") prevLoan = "Yes";
if (prevLoan === "no") prevLoan = "No";

data.previous_loan = prevLoan;

// normalize loan amount
if (!data.loan_amount || isNaN(data.loan_amount)) {
  data.loan_amount = 0;
}

    /* -------- Call Python AI -------- */
    const aiResponse = await axios.post("http://127.0.0.1:5000/predict", {
      "Land Size": data.land_size,
      "Budget": Number(data.budget),
      "Previous Loan": data.previous_loan,
      "Loan Amount": Number(data.loan_amount),
      "Soil Type": data.soil_type,
      "Season": data.season
    });

    const risk = aiResponse.data.debt_risk;

    /* -------- AI-based Recommendations -------- */
    // let recommendedCrops = [];
    // let budgetAdvice = "";
    // let seedAdvice = "";

    // if (risk === "Low") {
    //   recommendedCrops = ["Wheat", "Soybean"];
    //   budgetAdvice = "Stable budget – expansion possible";
    //   seedAdvice = "Bulk purchase recommended";
    // } 
    // else if (risk === "Medium") {
    //   recommendedCrops = ["Maize", "Pulses"];
    //   budgetAdvice = "Controlled spending advised";
    //   seedAdvice = "Phase-wise seed purchase";
    // } 
    // else {
    //   recommendedCrops = ["Millets", "Pulses"];
    //   budgetAdvice = "Low budget recommended – avoid loans";
    //   seedAdvice = "Minimal investment in seeds";
    // }

function recommendCrop(soil, season, budget) {
  if (soil === "Black Soil" && season === "Zaid") {
    return budget > 8000 ? ["Cotton", "Maize"] : ["Pulses", "Millets"];
  }
  if (soil === "Black Soil" && season === "Kharif") {
    return budget > 10000 ? ["Soybean", "Cotton"] : ["Bajra", "Jowar"];
  }
  return ["Pulses", "Millets"];
}

const recommendedCrops  = recommendCrop(data.soil_type, data.season, Number(data.budget));


// const recommendedCrops = aiResponse.data.recommended_crops;
const warning = aiResponse.data.warning || "";

let budgetAdvice = "";
let seedAdvice = "";

if (risk === "Low") {
  budgetAdvice = "Stable budget – expansion possible";
  seedAdvice = "Bulk purchase recommended";
}
else if (risk === "Medium") {
  budgetAdvice = "Controlled spending advised";
  seedAdvice = "Phase-wise seed purchase";
}
else {
  budgetAdvice = "Low budget recommended – avoid loans";
  seedAdvice = "Minimal investment in seeds";
}


// let riskScoreMap = {
//   "Low": 30,
//   "Medium": 60,
//   "High": 85
// };
let riskScores = { Low: 0, Medium: 0, High: 0 };

if (risk === "Low") {
  riskScores = { Low: 70, Medium: 20, High: 10 };
}
else if (risk === "Medium") {
  riskScores = { Low: 20, Medium: 60, High: 20 };
}
else {
  riskScores = { Low: 10, Medium: 20, High: 70 };
}


// const profitScore = Math.round(
//   ((Number(data.budget) - Number(data.loan_amount || 0)) / Number(data.budget)) * 100
// );
const budgetNum = Number(data.budget) || 0;
const loanNum = Number(data.loan_amount) || 0;

const profitScore = budgetNum > 0
  ? Math.round(((budgetNum - loanNum) / budgetNum) * 100)
  : 0;


// const riskScore = riskScoreMap[risk];

    /* -------- Send to Frontend -------- */
    res.json({
      debt_risk: risk,
      crops: recommendedCrops,
      budget: budgetAdvice,
      seed: seedAdvice,
      warning: warning,
      profit_score: profitScore,
     risk_score: riskScores

    });
  } catch (error) {
    console.error("Server error:", error);
    res.status(500).json({ error: "Backend error" });
  }
});

/* ===========================
   START SERVER
=========================== */
app.listen(4000, () => {
  console.log("Server running on http://localhost:4000");
});

