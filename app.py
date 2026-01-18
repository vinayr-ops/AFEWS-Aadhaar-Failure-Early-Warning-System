import gradio as gr
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# --- 1. BACKEND: TRAIN MODEL ---
# The model learns from "Synthetic Truth" derived from biological/technical rules.

def train_risk_model():
    np.random.seed(42)
    data = []
    
    # Generate 3000 records to train the robust model
    for _ in range(3000):
        # 1. Inputs (Integers)
        age = np.random.randint(5, 95)
        bio_years = np.random.randint(0, 12)    
        mobile_years = np.random.randint(0, 10) 
        scanner_qual = np.random.randint(30, 100) 
        device_type = np.random.choice(["Fingerprint", "Iris", "OTP"], p=[0.7, 0.2, 0.1])
        auth_count = np.random.randint(10, 1000) 
        recent_failures = np.random.randint(0, 5)
        
        # 2. RISK SCORING LOGIC (The "Ground Truth")
        score = 0
        
        # A. SENIOR DECAY (High Risk)
        if age >= 60 and bio_years >= 7: score += 85 
            
        # B. CHILD GROWTH (Critical Risk)
        elif 15 <= age <= 18 and bio_years >= 2: score += 90
            
        # C. FRICTION WEAR (High Risk)
        elif recent_failures >= 3: score += 80
            
        # D. DIGITAL DORMANCY (Medium Risk)
        elif mobile_years >= 5: score += 60
            
        # E. HARDWARE FAULT (Medium Risk)
        elif scanner_qual < 60: score += 40
            
        # Noise
        score += np.random.randint(-5, 5)
        score = max(0, min(100, score))
        
        # Target: 1 if Risk >= 50
        target = 1 if score >= 50 else 0
        
        data.append([age, bio_years, mobile_years, scanner_qual, device_type, auth_count, recent_failures, target])
        
    df = pd.DataFrame(data, columns=["Age", "Bio_Years", "Mobile_Years", "Scanner_Quality", "Device_Type", "Auth_Count", "Recent_Failures", "Target"])
    
    le = LabelEncoder()
    df['Device_Type_Encoded'] = le.fit_transform(df['Device_Type'])
    
    features = ["Age", "Bio_Years", "Mobile_Years", "Scanner_Quality", "Device_Type_Encoded", "Auth_Count", "Recent_Failures"]
    X = df[features]
    y = df["Target"]
    
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X, y)
    
    return clf, le

model, encoder = train_risk_model()

# --- 2. FRONTEND: PREDICTION ---

def predict_aadhaar_risk(age, bio_years, mobile_years, scanner_qual, device_type, auth_count, failures):
    # Ensure inputs are treated as integers (though Gradio sliders handle this, good for safety)
    age = int(age)
    bio_years = int(bio_years)
    mobile_years = int(mobile_years)
    scanner_qual = int(scanner_qual)
    auth_count = int(auth_count)
    failures = int(failures)

    try:
        device_encoded = encoder.transform([device_type])[0]
    except:
        device_encoded = 0 
        
    input_vector = pd.DataFrame([[age, bio_years, mobile_years, scanner_qual, device_encoded, auth_count, failures]], 
                                columns=["Age", "Bio_Years", "Mobile_Years", "Scanner_Quality", "Device_Type_Encoded", "Auth_Count", "Recent_Failures"])
    
    prob = model.predict_proba(input_vector)[0][1]
    score = int(prob * 100)
    
    if score >= 75:
        status = "CRITICAL RISK 🔴"
        if age >= 60: reason = "Aging Skin + Old Data."
        elif 15 <= age <= 18: reason = "Missed Age-15 Update."
        elif failures >= 3: reason = "High Friction Wear."
        else: reason = "Multiple Factors."
        advice = f"Reason: {reason} \nAction: Immediate Biometric Update Required."
        
    elif score >= 50:
        status = "MODERATE RISK 🟠"
        advice = "Reason: Digital Dormancy / Hardware Risk. \nAction: Advisory Sent. Check Mobile Link."
    else:
        status = "SAFE 🟢"
        advice = "No Action Needed."
        
    return status, f"{score}/100", advice

# --- 3. UI ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ AFEWS: Aadhaar Failure Predictor (Live Demo)")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 👤 Citizen Profile")
            # step=1 ensures WHOLE NUMBERS
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
        score_out = gr.Label(label="Probability")
    advice_out = gr.Textbox(label="Recommendation")
            
    btn.click(fn=predict_aadhaar_risk, 
              inputs=[age_in, bio_in, mob_in, qual_in, device_in, auth_in, fail_in], 
              outputs=[status_out, score_out, advice_out])

demo.launch()