from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

# Mock ML Model Logic
def calculate_risk(txn):
    score = 0
    # Rule 1: High Amount
    if txn.get('amount', 0) > 10000:
        score += 40
    # Rule 2: Suspicious Location
    if txn.get('location') == 'High Risk Zone':
        score += 30
    # Rule 3: Random Anomaly
    score += random.randint(0, 30)
    return min(100, score)

@app.route('/api/process-transaction', methods=['POST'])
def process_txn():
    data = request.json
    print(f"Received transaction: {data}")
    
    # Simulate processing time
    time.sleep(0.5)
    
    # Calculate Risk
    risk_score = calculate_risk(data)
    
    # Mock KYC Verification
    kyc_status = "Verified" if random.random() > 0.1 else "Flagged"
    
    response = {
        "status": "success",
        "data": {
            "transaction_id": data.get('id'),
            "risk_score": risk_score,
            "kyc_status": kyc_status,
            "decision": "Blocked" if risk_score > 80 else "Approved"
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    print("Swift AI - Mock Backend Running on http://localhost:5000")
    app.run(port=5000)
