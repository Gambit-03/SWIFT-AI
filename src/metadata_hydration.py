"""
METADATA HYDRATION MODULE (FIXED)
==================================
This script creates FAKE but realistic metadata to make your dashboard impressive.
It maps anonymous codes to realistic names, cities, merchants, etc.
"""

import pandas as pd
import numpy as np
import json
import random
import sys
from typing import Dict, List, Optional, Any

# ============================================================================
# FAKE DATA MAPPINGS (SEED DATA)
# ============================================================================

FAKE_CITIES = {
    1: "New York", 2: "Los Angeles", 3: "Chicago", 4: "Houston", 5: "Phoenix",
    10: "San Francisco", 11: "Seattle", 12: "Boston", 13: "Miami", 14: "Denver",
    15: "Austin", 20: "London", 21: "Paris", 22: "Tokyo", 23: "Berlin",
    24: "Moscow", 25: "Dubai", 30: "Toronto", 31: "Sydney", 32: "Singapore",
    100: "Mumbai", 101: "Hong Kong", 102: "Bangkok", 103: "Istanbul", 104: "Seoul",
    150: "Lagos", 151: "Cairo", 152: "Johannesburg", 153: "São Paulo", 154: "Mexico City",
    200: "Unknown_City_A", 201: "Unknown_City_B", 202: "Unknown_City_C"
}

FAKE_BANK_NAMES = {
    1: "Chase Bank", 2: "Bank of America", 3: "Wells Fargo", 4: "Citibank", 5: "US Bank",
    10: "Capital One", 11: "Discover Bank", 12: "American Express", 13: "Bank of NY Mellon",
    100: "HSBC", 101: "Barclays", 102: "Deutsche Bank", 103: "Credit Suisse", 104: "ING",
    150: "Standard Chartered", 151: "DBS Bank", 152: "OCBC", 153: "UOB", 154: "CIMB",
}

FAKE_MERCHANTS = {
    1: "Amazon.com", 2: "Walmart", 3: "Target", 4: "Best Buy", 5: "Home Depot",
    10: "Apple Store", 11: "Nike", 12: "Sephora", 13: "Ulta Beauty", 14: "H&M",
    100: "McDonald's", 101: "Starbucks", 102: "Uber", 103: "Airbnb", 104: "Netflix",
    150: "British Airways", 151: "Emirates Airlines", 152: "Singapore Airlines", 153: "Lufthansa",
    200: "Unknown_Merchant_A", 201: "Unknown_Merchant_B"
}

FAKE_DEVICES = {
    1: "iPhone 12", 2: "iPhone 13", 3: "Samsung Galaxy S21", 4: "Samsung Galaxy S22",
    5: "Pixel 6", 10: "iPad", 11: "Samsung Tablet", 12: "Desktop PC (Windows)",
    13: "Desktop PC (Mac)", 14: "Unknown Device"
}

FAKE_NAMES = [
    "John Smith", "Sarah Johnson", "Michael Chen", "Jessica Williams", "David Lee",
    "Emma Brown", "James Anderson", "Olivia Martinez", "Robert Taylor", "Sophia Hernandez",
    "William Davis", "Ava Rodriguez", "Benjamin Garcia", "Isabella Wilson", "Lucas Moore",
    "Mia Jackson", "Henry Taylor", "Charlotte White", "Alexander Harris", "Amelia Martin"
]

# ============================================================================
# FUNCTIONS
# ============================================================================

def safe_int(value: Any, default: int) -> int:
    """Helper to safely convert anything to int (handles '325.0', NaNs, etc.)"""
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default

def hydrate_transaction(transaction_row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Take an anonymous transaction and add fake metadata.
    """
    
    # 1. Safely extract code values (Fixing the Pylance 'Hashable' error)
    addr1 = safe_int(transaction_row.get('addr1'), 200)
    card1 = safe_int(transaction_row.get('card1'), 1)
    amt_val = safe_int(transaction_row.get('TransactionAmt'), 100)
    dev_val = safe_int(transaction_row.get('DeviceInfo'), 10)
    
    # Map codes to realistic names
    hydrated = transaction_row.copy()
    
    hydrated['customer_name'] = random.choice(FAKE_NAMES)
    hydrated['home_city'] = FAKE_CITIES.get(addr1 % 300, "Unknown City")
    
    # Simulate a different city for high-risk transactions
    # (Fix: ensure integer math is clean)
    transaction_city_code = (addr1 + 100) % 300
    hydrated['transaction_city'] = FAKE_CITIES.get(transaction_city_code, "Unknown City")
    
    hydrated['bank_name'] = FAKE_BANK_NAMES.get(card1, "Unknown Bank")
    
    # Safe Merchant Lookup
    merchant_key = amt_val % 200
    hydrated['merchant_name'] = FAKE_MERCHANTS.get(merchant_key, "Unknown Merchant")
    
    # Safe Device Lookup
    # Logic: If 'DeviceInfo' exists, use it, else default to 1
    if 'DeviceInfo' in transaction_row and not pd.isna(transaction_row['DeviceInfo']):
        dev_key = dev_val % 14
    else:
        dev_key = 1
    hydrated['device_type'] = FAKE_DEVICES.get(dev_key, "Unknown Device")
    
    # Card type based on card1
    card_type = "Visa" if card1 % 2 == 0 else "Mastercard"
    hydrated['card_type'] = card_type
    
    # Email provider
    email_domain = transaction_row.get('P_emaildomain', 'unknown')
    hydrated['email_provider'] = str(email_domain).split('.')[0].upper() if '.' in str(email_domain) else "UNKNOWN"
    
    return hydrated

def generate_fraud_narratives(predictions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate human-readable fraud narratives for high-risk transactions.
    """
    narratives = []
    
    for idx, row in predictions_df.iterrows():
        fraud_prob = float(row.get('fraud_probability', 0))
        
        customer = str(row.get('customer_name', 'Unknown'))
        home_city = str(row.get('home_city', 'Unknown'))
        transaction_city = str(row.get('transaction_city', 'Unknown'))
        merchant = str(row.get('merchant_name', 'Unknown Merchant'))
        amount = float(row.get('TransactionAmt', 0))
        device = str(row.get('device_type', 'Unknown Device'))
        
        # Build narrative based on fraud signals
        narrative = f"{customer} "
        
        if fraud_prob > 0.8:
            narrative += f"attempted a ${amount:.2f} purchase of {merchant} in {transaction_city} "
            narrative += f"using {device}, but "
            
            if home_city != transaction_city:
                narrative += f"lives in {home_city} (GEOLOCATION MISMATCH). "
            
            narrative += f"FRAUD PROBABILITY: {fraud_prob:.1%}"
            
        elif fraud_prob > 0.5:
            narrative += f"made a ${amount:.2f} purchase from {merchant}. "
            narrative += f"Some unusual patterns detected ({fraud_prob:.1%} risk). "
            narrative += f"Recommend step-up authentication."
        else:
            narrative += f"made a normal transaction: ${amount:.2f} at {merchant}. "
            narrative += f"Low risk ({fraud_prob:.1%})."
        
        narratives.append(narrative)
    
    predictions_df['fraud_narrative'] = narratives
    return predictions_df

def hydrate_predictions(predictions_csv: str = "predictions.csv", 
                        output_csv: str = "predictions_hydrated.csv",
                        transactions_csv: str = "train_transaction.csv") -> Optional[pd.DataFrame]:
    """
    Main function to hydrate predictions with fake metadata.
    """
    
    print("="*70)
    print("METADATA HYDRATION FOR DASHBOARD")
    print("="*70)
    
    # Load predictions
    try:
        predictions = pd.read_csv(predictions_csv)
        print(f"✓ Loaded predictions from {predictions_csv}")
    except FileNotFoundError:
        print(f"✗ {predictions_csv} not found. Create predictions first.")
        # Fix: Return None explicitly to match type hint
        return None
    
    # Load original transactions for mapping
    try:
        transactions = pd.read_csv(transactions_csv)
        print(f"✓ Loaded transaction data from {transactions_csv}")
    except FileNotFoundError:
        print(f"⚠ {transactions_csv} not found. Using minimal metadata.")
        transactions = None
    
    # Merge predictions with transaction data
    if transactions is not None:
        # We merge on TransactionID to get the original columns (addr1, card1) back
        # because the model output might only have the probability score
        hydrated = predictions.merge(
            transactions[['TransactionID', 'addr1', 'card1', 'TransactionAmt', 'P_emaildomain', 'DeviceInfo']],
            on='TransactionID',
            how='left'
        )
    else:
        hydrated = predictions.copy()
    
    # Hydrate each transaction
    print("\n[Action] Hydrating transactions with fake metadata...")
    hydrated_rows = []
    
    for idx, row in hydrated.iterrows():
        # Convert row to dict for easier handling
        hydrated_row = hydrate_transaction(row.to_dict())
        hydrated_rows.append(hydrated_row)
        
        if (idx + 1) % 1000 == 0:
            print(f"   Processed {idx + 1} transactions...")
    
    hydrated_df = pd.DataFrame(hydrated_rows)
    
    # Generate narratives
    print("[Action] Generating fraud narratives...")
    hydrated_df = generate_fraud_narratives(hydrated_df)
    
    # Save output
    hydrated_df.to_csv(output_csv, index=False)
    print(f"\n✓ Saved to {output_csv}")
    
    return hydrated_df

def create_demo_metadata_file(output_json: str = "metadata_mappings.json"):
    """
    Create a JSON file with all the metadata mappings.
    Useful for your frontend to use these same mappings.
    """
    mappings = {
        "cities": FAKE_CITIES,
        "banks": FAKE_BANK_NAMES,
        "merchants": FAKE_MERCHANTS,
        "devices": FAKE_DEVICES,
        "names_sample": FAKE_NAMES[:5]
    }
    
    with open(output_json, 'w') as f:
        json.dump(mappings, f, indent=2)
    
    print(f"✓ Metadata mappings saved to {output_json}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SWIFT AI - METADATA HYDRATION FOR DASHBOARD")
    print("="*70)
    
    # Use arguments if provided, else defaults
    pred_file = sys.argv[1] if len(sys.argv) > 1 else "predictions.csv"
    trans_file = sys.argv[2] if len(sys.argv) > 2 else "train_transaction.csv"
    
    hydrate_predictions(pred_file, "predictions_hydrated.csv", trans_file)
    create_demo_metadata_file()