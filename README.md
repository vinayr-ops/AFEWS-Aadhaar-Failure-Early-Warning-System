# 🛡️ AFEWS: Aadhaar Failure Early Warning System

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Machine Learning](https://img.shields.io/badge/AI-RandomForest-green)
![Status](https://img.shields.io/badge/Hackathon-Prototype-orange)

> **"Shifting from Reactive Correction to Predictive Protection."**

AFEWS is a machine learning-based decision support system designed to predict **Aadhaar Authentication Failures** before they happen. By analyzing metadata trends (Age, Biometric Update Latency, Device Quality), it identifies citizens at risk of service exclusion and triggers proactive advisories.

## 🔗 Live Demo
**Try the Risk Engine Live:** [👉 Click Here to Open App](https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME)

## ⚙️ How It Works (The Logic)
Our Random Forest model is trained on **Societal Trends** derived from official UIDAI datasets:

| Risk Factor | Threshold | Reason |
| :--- | :--- | :--- |
| **Senior Decay** | Age > 60 + Bio Update > 7 Years | Skin elasticity loss degrades fingerprint quality. |
| **Child Growth** | Age 15-18 + Bio Update > 2 Years | Hand geometry changes rapidly during puberty. |
| **Digital Dormancy** | Mobile Link > 5 Years Old | High risk of lost access to OTP backup. |

## 🚀 How to Run Locally
1. Clone the repo:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/AFEWS-Aadhaar-Failure-Early-Warning-System.git](https://github.com/YOUR_USERNAME/AFEWS-Aadhaar-Failure-Early-Warning-System.git)
