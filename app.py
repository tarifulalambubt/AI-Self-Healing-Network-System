from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import joblib
import random
import csv
import os
from datetime import datetime
from recovery_scripts.auto_recovery import trigger_recovery

app = Flask(__name__)

# AI মডেল লোড করা
try:
    model = joblib.load('model/rf_model.pkl')
except:
    print("Error: Model not found. Please run train_model.py first!")

# লগ ফাইল সেটআপ
os.makedirs('data', exist_ok=True)
log_file = 'data/history_log.csv'
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Latency_ms", "Traffic", "Fault_Status", "Recovery_Action"])

def log_fault(latency, traffic, status, action):
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), latency, traffic, status, action])

# নতুন ফাংশন: সর্বশেষ ৫টি লগ পড়ে আনার জন্য
def get_recent_logs():
    if not os.path.exists(log_file): return []
    try:
        with open(log_file, mode='r') as file:
            reader = list(csv.reader(file))
            if len(reader) <= 1: return []
            logs = reader[1:] # হেডার বাদ দেওয়া
            return logs[-5:][::-1] # শেষের ৫টি ডেটা উল্টো করে (নতুনটা আগে) পাঠানো
    except:
        return []

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/network_status')
def get_network_status():
    is_faulty = random.choice([True, False, False, False, False]) 
    
    if is_faulty:
        latency = random.randint(150, 999)
        packet_loss = round(random.uniform(5.0, 100.0), 2)
        bandwidth = random.randint(0, 30)
        cpu_usage = random.randint(85, 100)
        traffic = random.randint(800, 1500)
    else:
        latency = random.randint(10, 50)
        packet_loss = round(random.uniform(0.0, 1.0), 2)
        bandwidth = random.randint(40, 100)
        cpu_usage = random.randint(10, 40)
        traffic = random.randint(100, 500)

    features = pd.DataFrame([[latency, packet_loss, bandwidth, cpu_usage, traffic]], 
                            columns=['Latency_ms', 'Packet_Loss_pct', 'Bandwidth_Mbps', 'CPU_Usage_pct', 'Traffic_Count'])
    
    prediction = int(model.predict(features)[0])
    status_map = {0: "Normal", 1: "Congestion Detected", 2: "Node Down!", 3: "High CPU Usage"}
    current_status = status_map.get(prediction, "Unknown")
    recovery_action = trigger_recovery(prediction)

    if prediction != 0:
        log_fault(latency, traffic, current_status, recovery_action)

    # লগ ডেটা ফেচ করা
    recent_logs = get_recent_logs()

    return jsonify({
        'time': datetime.now().strftime("%H:%M:%S"),
        'latency': latency,
        'packet_loss': packet_loss,
        'bandwidth': bandwidth,
        'cpu_usage': cpu_usage,
        'traffic': traffic,
        'status': current_status,
        'status_code': prediction,
        'recovery_action': recovery_action,
        'recent_logs': recent_logs # ফ্রন্টএন্ডে লগ পাঠানো হচ্ছে
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)