"""
SWIFT-AI ADAPTER
================
Connects fraud service with SWIFT-AI inference API.
"""

import requests
import json
from typing import Dict

class SwiftAIAdapter:
    """Adapter to connect with SWIFT-AI inference API."""
    
    def __init__(self, api_url="http://localhost:5002"):
        """
        Initialize SWIFT-AI adapter.
        
        Args:
            api_url: URL of SWIFT-AI inference API
        """
        self.api_url = api_url
        self.predict_endpoint = f"{api_url}/predict"
        self.health_endpoint = f"{api_url}/health"
        
    def is_available(self) -> bool:
        """Check if SWIFT-AI API is available."""
        try:
            response = requests.get(self.health_endpoint, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def map_transaction_to_features(self, transaction: Dict) -> Dict:
        """
        Map simple transaction data to SWIFT-AI features.
        
        Args:
            transaction: Simple transaction dict
            
        Returns:
            Features dict for SWIFT-AI
        """
        # Extract basic info
        amount = float(transaction.get('amount', 0))
        location = transaction.get('location', 'Unknown')
        merchant = transaction.get('merchant', 'Unknown')
        
        # Create feature mapping
        # Note: SWIFT-AI expects 100+ features, we'll provide what we can
        # and let the API handle missing features
        features = {
            'TransactionAmt': amount,
            # Add more mappings as needed
        }
        
        return features
    
    def predict(self, transaction: Dict) -> Dict:
        """
        Get fraud prediction from SWIFT-AI.
        
        Args:
            transaction: Transaction data
            
        Returns:
            Prediction result
        """
        try:
            # Map transaction to features
            features = self.map_transaction_to_features(transaction)
            
            # Prepare request
            payload = {
                'transaction_id': transaction.get('id', 'UNKNOWN'),
                'features': features
            }
            
            # Call SWIFT-AI API
            response = requests.post(
                self.predict_endpoint,
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Convert SWIFT-AI response to our format
                return {
                    'fraud_probability': result.get('fraud_probability', 0.5),
                    'is_fraud': result.get('is_fraud', False),
                    'risk_level': result.get('risk_level', 'UNKNOWN'),
                    'confidence': result.get('confidence', 0.5),
                    'inference_time_ms': result.get('inference_time_ms', 0),
                    'fraud_indicators': result.get('fraud_indicators', []),
                    'model_version': 'SWIFT-AI-v1.0'
                }
            else:
                print(f"[SWIFT-AI] API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[SWIFT-AI] Connection error: {e}")
            return None
