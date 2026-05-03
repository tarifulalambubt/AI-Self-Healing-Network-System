import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("--- Step 1: Generating Synthetic Telemetry Dataset ---")

# 1000 লাইনের একটি ফেক নেটওয়ার্ক ডেটাসেট তৈরি করছি
data = []
for _ in range(1000):
    state = np.random.choice(['Normal', 'Congestion', 'Node_Down', 'High_CPU'])
    
    if state == 'Normal':
        data.append([np.random.randint(10, 50), np.random.uniform(0, 0.5), np.random.randint(20, 60), np.random.randint(10, 40), np.random.randint(100, 500), 0])
    elif state == 'Congestion':
        data.append([np.random.randint(150, 300), np.random.uniform(2, 10), np.random.randint(80, 100), np.random.randint(40, 70), np.random.randint(800, 1500), 1])
    elif state == 'Node_Down':
        data.append([999, 100.0, 0, 0, 0, 2])
    elif state == 'High_CPU':
        data.append([np.random.randint(50, 100), np.random.uniform(0, 1), np.random.randint(30, 70), np.random.randint(90, 100), np.random.randint(200, 600), 3])

columns = ['Latency_ms', 'Packet_Loss_pct', 'Bandwidth_Mbps', 'CPU_Usage_pct', 'Traffic_Count', 'Fault_Label']
df = pd.DataFrame(data, columns=columns)

# ডেটাসেটটি 'data' ফোল্ডারে সেভ করছি
os.makedirs('data', exist_ok=True)
df.to_csv("data/network_dataset.csv", index=False)
print("[+] Dataset saved successfully at 'data/network_dataset.csv'")

print("\n--- Step 2: Training Random Forest Model ---")
X = df.drop('Fault_Label', axis=1)
y = df['Fault_Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# মডেল টেস্ট করছি
predictions = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"[+] Model Training Completed! Accuracy: {accuracy * 100:.2f}%")

print("\n--- Step 3: Saving the Trained Model ---")
# ট্রেইন করা মডেলটি 'model' ফোল্ডারে সেভ করছি
os.makedirs('model', exist_ok=True)
joblib.dump(rf_model, 'model/rf_model.pkl')
print("[+] Model saved successfully at 'model/rf_model.pkl'")
print("\nAll Done! The Brain is ready.")