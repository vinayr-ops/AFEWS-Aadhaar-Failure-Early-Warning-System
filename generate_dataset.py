import pandas as pd
import numpy as np

def generate_final_dataset(num_records=5000):
    np.random.seed(42)  # Ensures the "random" data is the same every time you run it
    data = []
    
    print(f"Generating {num_records} synthetic records based on 'AFEWS Logic'...")
    
    for i in range(num_records):
        # --- 1. Generate Metadata (Whole Numbers) ---
        age = np.random.randint(5, 95)
        bio_years = np.random.randint(0, 12)    
        mobile_years = np.random.randint(0, 10) 
        scanner_qual = np.random.randint(30, 100) 
        # Device Type: 70% Fingerprint, 20% Iris, 10% OTP
        device_type = np.random.choice(["Fingerprint", "Iris", "OTP"], p=[0.7, 0.2, 0.1])
        auth_count = np.random.randint(10, 1000) 
        recent_failures = np.random.randint(0, 5)
        
        # --- 2. Apply The Risk Logic (The "Brain") ---
        score = 0
        reasons = []
        
        # Logic A: Senior Decay (Critical) - Age > 60 & Old Data
        if age >= 60 and bio_years >= 7: 
            score += 85
            reasons.append("Senior Decay")
            
        # Logic B: Child Growth (Critical) - Age 15-18 & Old Data
        elif 15 <= age <= 18 and bio_years >= 2: 
            score += 90
            reasons.append("Child Growth")
            
        # Logic C: Friction Wear (High) - Recent failures > 3
        elif recent_failures >= 3: 
            score += 80
            reasons.append("Friction Wear")
            
        # Logic D: Digital Dormancy (Medium) - No mobile link > 5 yrs
        elif mobile_years >= 5: 
            score += 60
            reasons.append("Digital Dormancy")
            
        # Logic E: Hardware Fault (Medium) - Poor Scanner
        elif scanner_qual < 60: 
            score += 40
            reasons.append("Hardware Quality")
            
        # Add slight random noise to simulate real-world variance
        score += np.random.randint(-5, 5)
        score = max(0, min(100, score)) # Clamp between 0-100
        
        # Determine Target (1 = At Risk, 0 = Safe)
        target = 1 if score >= 50 else 0
        
        # Advisory Text Generation
        if score >= 75: 
            advisory = "CRITICAL: Immediate Biometric Update Required"
        elif score >= 50: 
            advisory = "MODERATE: Advisory Sent. Check Mobile Link."
        else: 
            advisory = "SAFE: No Action Needed"
        
        data.append([age, bio_years, mobile_years, scanner_qual, device_type, 
                     auth_count, recent_failures, score, target, advisory])
        
    # --- 3. Save to CSV ---
    columns = ["Age", "Years_Since_Bio_Update", "Years_Since_Mobile_Link", 
               "Scanner_Quality_Score", "Device_Type", "Total_Auth_History", 
               "Recent_Failures", "Risk_Score", "Failure_Target", "Advisory_Label"]
    
    df = pd.DataFrame(data, columns=columns)
    
    filename = "final_training_data.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Success! Dataset saved as '{filename}' with {num_records} records.")
    print(df.head())

if __name__ == "__main__":
    generate_final_dataset()