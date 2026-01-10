"""
Quick Service Test
==================
Tests if fraud service is working.
"""

import requests
import json

print("Testing Fraud Service...")
print("=" * 50)

# Test 1: Health Check
try:
    response = requests.get("http://localhost:5001/", timeout=2)
    print(f"✅ Fraud Service Running: {response.status_code}")
except Exception as e:
    print(f"❌ Fraud Service Not Reachable: {e}")
    exit(1)

# Test 2: Analyze Endpoint
try:
    test_txn = {
        "id": "TEST-001",
        "amount": 1000,
        "merchant": "Test Store",
        "location": "New York",
        "type": "Standard"
    }
    
    response = requests.post(
        "http://localhost:5001/analyze",
        json=test_txn,
        timeout=5
    )
    
    print(f"\n✅ Analyze Endpoint: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nResponse:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"❌ Analyze Failed: {e}")

print("\n" + "=" * 50)
print("Test Complete!")
