import pandas as pd
import numpy as np
import os

# Ensure the 'datasets' folder exists (one level up)
output_folder = "datasets"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("generating synthetic AFEWS data...")

np.random.seed(42)
data = []

# Generate 3000 records
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

# --- SAVE TO CSV (This is the line you were looking for!) ---
output_path = os.path.join(output_folder, "final_training_data.csv")
df.to_csv(output_path, index=False)

print(f"✅ Success! Data saved to: {output_path}")