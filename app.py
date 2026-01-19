import gradio as gr
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

# --- 1. BACKEND: LOAD & TRAIN ---
def load_and_train():
    # 🔗 This is the Key Link: Loading the file from your new folder
    csv_path = "datasets/final_training_data.csv"
    
    # Safety Check: If file is missing, warn the user
    if not os.path.exists(csv_path):
        return None, None, "⚠️ Error: Data file not found. Please run 'src/data_generator.py' first."

    # Load Data
    df = pd.read_csv(csv_path)
    
    # Prepare Features
    le = LabelEncoder()
    df['Device_Type_Encoded'] = le.fit_transform(df['Device_Type'])
    
    features = ["Age", "Bio_Years", "Mobile_Years", "Scanner_Quality", "Device_Type_Encoded", "Auth_Count", "Recent_Failures"]
    X = df[features]
    y = df["Target"]
    
    # Train Model
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X, y)
    
    return clf, le

# Load model immediately on app start
model, encoder = load_and_train()

# --- 2. FRONTEND: PREDICTION LOGIC ---
def predict_aadhaar_risk(age, bio_years, mobile_years, scanner_qual, device_type, auth_count, failures):
    # Error Handling: If model failed to load
    if isinstance(encoder, str): 
        return "System Error", "0/0", encoder

    # Feature Encoding
    try:
        device_encoded = encoder.transform([device_type])[0]
    except:
        device_encoded = 0 
        
    input_vector = pd.DataFrame([[age, bio_years, mobile_years, scanner_qual, device_encoded, auth_count, failures]], 
                                columns=["Age", "Bio_Years", "Mobile_Years", "Scanner_Quality", "Device_Type_Encoded", "Auth_Count", "Recent_Failures"])
    
    # Predict Probability
    prob = model.predict_proba(input_vector)[0][1]
    score = int(prob * 100)
    
    # --- The "Explainable AI" Logic ---
    if score >= 75:
        status = "CRITICAL RISK 🔴"
        if int(age) >= 60: reason = "Aging Skin + Data Decay."
        elif 15 <= int(age) <= 18: reason = "Biometric Growth Spurt (Age 15)."
        elif int(failures) >= 3: reason = "High Friction/Wear Detected."
        else: reason = "Multiple Cumulative Factors."
        advice = f"Reason: {reason} \nAction: Dispatch Mobile Update Van."
        
    elif score >= 50:
        status = "MODERATE RISK 🟠"
        advice = "Reason: Digital Inactivity. \nAction: Send SMS Advisory."
    else:
        status = "SAFE 🟢"
        advice = "No Action Needed."
        
    return status, f"{score}/100", advice

# --- 3. UI LAYOUT ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ AFEWS: Aadhaar Failure Predictor")
    gr.Markdown("### *Predictive Maintenance for Digital Identity*")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 👤 Citizen Metadata")
            age_in = gr.Slider(5, 100, value=65, label="Age")
            bio_in = gr.Slider(0, 15, value=8, label="Years Since Last Update")
            mob_in = gr.Slider(0, 15, value=5, label="Years Since Mobile Link")
            
        with gr.Column():
            gr.Markdown("### 🖥️ Technical Logs")
            device_in = gr.Dropdown(["Fingerprint", "Iris", "OTP"], value="Fingerprint", label="Auth Mode")
            fail_in = gr.Slider(0, 10, value=1, label="Recent Failure Count")
            qual_in = gr.Slider(0, 100, value=90, label="Scanner Quality Score")
            auth_in = gr.Number(value=150, label="Total Auth Count", visible=False) # Hidden param
            
    btn = gr.Button("🔍 Analyze Biometric Health", variant="primary")
    
    with gr.Row():
        status_out = gr.Textbox(label="Risk Status")
        score_out = gr.Label(label="Failure Probability")
    advice_out = gr.Textbox(label="Recommended Intervention")
            
    btn.click(fn=predict_aadhaar_risk, 
              inputs=[age_in, bio_in, mob_in, qual_in, device_in, auth_in, fail_in], 
              outputs=[status_out, score_out, advice_out])

if __name__ == "__main__":
    demo.launch()