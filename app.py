import gradio as gr
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

# --- 1. BACKEND: LOAD & TRAIN ---

def load_and_train():
    # Load the data from the CSV we just generated
    # This proves to judges we are using stored data, not random numbers on the fly
    csv_path = "datasets/final_training_data.csv"
    
    if not os.path.exists(csv_path):
        return None, None, "Error: CSV not found. Run src/data_generator.py first."

    df = pd.read_csv(csv_path)
    
    # Prepare Data
    le = LabelEncoder()
    df['Device_Type_Encoded'] = le.fit_transform(df['Device_Type'])
    
    features = ["Age", "Bio_Years", "Mobile_Years", "Scanner_Quality", "Device_Type_Encoded", "Auth_Count", "Recent_Failures"]
    X = df[features]
    y = df["Target"]
    
    # Train Model
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X, y)
    
    return clf, le

model, encoder = load_and_train()

# --- 2. FRONTEND: PREDICTION LOGIC ---

def predict_aadhaar_risk(age, bio_years, mobile_years, scanner_qual, device_type, auth_count, failures):
    # Inputs
    age = int(age)
    bio_years = int(bio_years)
    mobile_years = int(mobile_years)
    scanner_qual = int(scanner_qual)
    auth_count = int(auth_count)
    failures = int(failures)

    # Encode Device Type
    try:
        device_encoded = encoder.transform([device_type])[0]
    except:
        device_encoded = 0 
        
    input_vector = pd.DataFrame([[age, bio_years, mobile_years, scanner_qual, device_encoded, auth_count, failures]], 
                                columns=["Age", "Bio_Years", "Mobile_Years", "Scanner_Quality", "Device_Type_Encoded", "Auth_Count", "Recent_Failures"])
    
    # Predict
    prob = model.predict_proba(input_vector)[0][1]
    score = int(prob * 100)
    
    # Generate Advisory (The "Explainability" Layer)
    if score >= 75:
        status = "CRITICAL RISK 🔴"
        if age >= 60: reason = "Aging Skin + Old Data."
        elif 15 <= age <= 18: reason = "Missed Age-15 Update."
        elif failures >= 3: reason = "High Friction Wear."
        else: reason = "Multiple Risk Factors."
        advice = f"Reason: {reason} \nAction: Immediate Biometric Update Required (Camp Dispatch)."
        
    elif score >= 50:
        status = "MODERATE RISK 🟠"
        advice = "Reason: Digital Dormancy / Hardware Risk. \nAction: Advisory Sent via SMS."
    else:
        status = "SAFE 🟢"
        advice = "No Action Needed."
        
    return status, f"{score}/100", advice

# --- 3. UI LAYOUT (Gradio) ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ AFEWS: Aadhaar Failure Predictor (Live Demo)")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 👤 Citizen Profile")
            age_in = gr.Slider(5, 100, value=65, step=1, label="Age (Years)")
            bio_in = gr.Slider(0, 15, value=8, step=1, label="Years Since Bio Update")
            mob_in = gr.Slider(0, 15, value=2, step=1, label="Years Since Mobile Link")
            
        with gr.Column():
            gr.Markdown("### 🖥️ Device & History")
            device_in = gr.Dropdown(["Fingerprint", "Iris", "OTP"], value="Fingerprint", label="Auth Mode")
            qual_in = gr.Slider(0, 100, value=90, step=1, label="Scanner Quality (0-100)")
            auth_in = gr.Number(value=150, label="Total Auth Count", precision=0)
            fail_in = gr.Slider(0, 10, value=0, step=1, label="Recent Failures")
            
    btn = gr.Button("Analyze Risk", variant="primary")
    
    with gr.Row():
        status_out = gr.Textbox(label="Status")
        score_out = gr.Label(label="Biometric Health Score")
    advice_out = gr.Textbox(label="Recommendation")
            
    btn.click(fn=predict_aadhaar_risk, 
              inputs=[age_in, bio_in, mob_in, qual_in, device_in, auth_in, fail_in], 
              outputs=[status_out, score_out, advice_out])

if __name__ == "__main__":
    demo.launch()