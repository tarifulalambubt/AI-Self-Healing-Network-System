import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

print("Generating 100,000 synthetic dataset samples...")

# ১,০০,০০০ স্যাম্পল জেনারেট করার জন্য N_SAMPLES = 100000 সেট করা হলো
N_SAMPLES = 100000

# র্যান্ডম ডেটা জেনারেট করার জন্য সিড সেট করা
np.random.seed(42)

# Normal / Baseline metrics (70% data = 70,000 samples)
n_normal = int(N_SAMPLES * 0.70)
latency_normal = np.random.uniform(5, 50, n_normal)
packet_loss_normal = np.random.uniform(0, 1.5, n_normal)
bandwidth_normal = np.random.uniform(50, 100, n_normal)
cpu_normal = np.random.uniform(5, 45, n_normal)
traffic_normal = np.random.randint(100, 500, n_normal)
target_normal = np.zeros(n_normal, dtype=int) # Class 0: Normal

# Congestion Metrics (10% data = 10,000 samples)
n_cong = int(N_SAMPLES * 0.10)
latency_cong = np.random.uniform(80, 250, n_cong)
packet_loss_cong = np.random.uniform(2, 8, n_cong)
bandwidth_cong = np.random.uniform(10, 40, n_cong)
cpu_cong = np.random.uniform(40, 75, n_cong)
traffic_cong = np.random.randint(800, 1500, n_cong)
target_cong = np.ones(n_cong, dtype=int) # Class 1: Congestion

# Node Down Metrics (10% data = 10,000 samples)
n_down = int(N_SAMPLES * 0.10)
latency_down = np.random.uniform(300, 1000, n_down)
packet_loss_down = np.random.uniform(20, 100, n_down)
bandwidth_down = np.random.uniform(0, 5, n_down)
cpu_down = np.random.uniform(0, 20, n_down)
traffic_down = np.random.randint(0, 50, n_down)
target_down = np.full(n_down, 2, dtype=int) # Class 2: Node Down

# High CPU Usage Metrics (10% data = 10,000 samples)
n_cpu = N_SAMPLES - (n_normal + n_cong + n_down)
latency_cpu = np.random.uniform(40, 120, n_cpu)
packet_loss_cpu = np.random.uniform(0.5, 4, n_cpu)
bandwidth_cpu = np.random.uniform(30, 80, n_cpu)
cpu_cpu = np.random.uniform(85, 100, n_cpu)
traffic_cpu = np.random.randint(400, 900, n_cpu)
target_cpu = np.full(n_cpu, 3, dtype=int) # Class 3: High CPU

# সব ডেটা একসাথে Combine করা
latency = np.concatenate([latency_normal, latency_cong, latency_down, latency_cpu])
packet_loss = np.concatenate([packet_loss_normal, packet_loss_cong, packet_loss_down, packet_loss_cpu])
bandwidth = np.concatenate([bandwidth_normal, bandwidth_cong, bandwidth_down, bandwidth_cpu])
cpu = np.concatenate([cpu_normal, cpu_cong, cpu_down, cpu_cpu])
traffic = np.concatenate([traffic_normal, traffic_cong, traffic_down, traffic_cpu])
target = np.concatenate([target_normal, target_cong, target_down, target_cpu])

df = pd.DataFrame({
    'Latency_ms': latency,
    'Packet_Loss_pct': packet_loss,
    'Bandwidth_Mbps': bandwidth,
    'CPU_Usage_pct': cpu,
    'Traffic_Count': traffic,
    'Fault_Class': target
})

# CSV ফাইল হিসেবে সেভ করা
os.makedirs('data', exist_ok=True)
csv_path = 'data/synthetic_network_dataset_100k.csv'
df.to_csv(csv_path, index=False)
print(f"Dataset saved successfully at '{csv_path}' with shape {df.shape}")

# Train-Test Split (80% Train, 20% Test)
X = df.drop(columns=['Fault_Class'])
y = df['Fault_Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
print("Training Random Forest Classifier model on 100,000 samples...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {acc * 100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the updated model
os.makedirs('model', exist_ok=True)
model_path = 'model/rf_model.pkl'
joblib.dump(model, model_path)
print(f"Updated model saved successfully at '{model_path}'!")