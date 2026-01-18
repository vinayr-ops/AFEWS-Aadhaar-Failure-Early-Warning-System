# 🛡️ AFEWS: Aadhaar Failure Early Warning System

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Machine Learning](https://img.shields.io/badge/AI-RandomForest-green)
![Status](https://img.shields.io/badge/Hackathon-Prototype-orange)

> **"Shifting from Reactive Correction to Predictive Protection."**

AFEWS is a machine learning-based decision support system designed to predict **Aadhaar Authentication Failures** before they happen. By analyzing metadata trends (Age, Biometric Update Latency, Device Quality), it identifies citizens at risk of service exclusion and triggers proactive advisories.

## 🔗 Live Demo
**Try the Risk Engine Live:** [👉 Click Here to Open Hugging Face App](https://huggingface.co/spaces/RatVin/demo)

---

## 🚨 The Problem
Currently, UIDAI's ecosystem is **Reactive**:
1.  Citizen visits a service center (Ration/Pension).
2.  Authentication **Fails** due to aging biometrics.
3.  Service is **Denied**.
4.  Citizen rushes to update data (takes 1-2 weeks).

## 💡 The Solution (AFEWS)
We propose a **Proactive** metadata analysis engine:
1.  **Predict:** The model scans update logs to calculate a "Biometric Health Score".
2.  **Warn:** If Risk > 75%, an automated advisory (SMS/WhatsApp) is sent.
3.  **Act:** Citizen updates biometrics *before* needing the service.

---

## ⚙️ How It Works (The Logic)
Our Random Forest model is trained on **Societal Trends** derived from official UIDAI datasets:

| Risk Factor | Threshold | Reason |
| :--- | :--- | :--- |
| **Senior Decay** | Age > 60 + Bio Update > 7 Years | Skin elasticity loss degrades fingerprint quality. |
| **Child Growth** | Age 15-18 + Bio Update > 2 Years | Hand geometry changes rapidly during puberty. |
| **Digital Dormancy** | Mobile Link > 5 Years Old | High risk of lost access to OTP backup. |

---

## 🛠️ Tech Stack
* **Core Engine:** Python, Scikit-Learn
* **Algorithm:** Random Forest Classifier (n_estimators=200)
* **Interface:** Gradio (Hosted on Hugging Face)
* **Data Strategy:** Hybrid (Official Aggregate Data for trends + Synthetic Data for individual scoring)

## 🚀 How to Run Locally
1. Clone the repo:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/AFEWS-Aadhaar-Predictor.git](https://github.com/YOUR_USERNAME/AFEWS-Aadhaar-Predictor.git)
