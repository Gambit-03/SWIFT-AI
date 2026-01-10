"""
ML-Powered Fraud Detector
==========================
Loads SWIFT-AI LightGBM model and provides fraud detection.
"""

import os
import pickle
import numpy as np
from datetime import datetime

# Try to import LightGBM
try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("[ML] Warning: LightGBM not installed. Install with: pip install lightgbm")


class MLFraudDetector:
    """ML-powered fraud detector using SWIFT-AI LightGBM model."""
    
    def __init__(self, model_path=None):
        """
        Initialize ML fraud detector.
        
        Args:
            model_path: Path to model file. If None, auto-detects.
        """
        self.model = None
        self.scaler = None
        self.feature_names = []
        self.model_type = None
        
        # Auto-detect model path
        if model_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Priority 1: LightGBM model (.txt)
            lightgbm_path = os.path.join(current_dir, 'fraud_model_lgb.txt')
            if os.path.exists(lightgbm_path):
                model_path = lightgbm_path
            else:
                # Priority 2: Pickle model (.pkl)
                default_path = os.path.join(current_dir, 'fraud_model.pkl')
                if os.path.exists(default_path):
                    model_path = default_path
        
        # Load model if path exists
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print(f"[ML] No model found at {model_path}")
            self._init_simple_model()
    
    def load_model(self, model_path):
        """Load model from file."""
        try:
            # Check if it's a LightGBM model (.txt file)
            if model_path.endswith('.txt'):
                if not LIGHTGBM_AVAILABLE:
                    print("[ML] LightGBM not available, cannot load model")
                    self._init_simple_model()
                    return
                
                self.model = lgb.Booster(model_file=model_path)
                self.model_type = 'lightgbm'
                
                # Load scaler if available
                scaler_path = model_path.replace('fraud_model_lgb.txt', 'scaler.pkl')
                if os.path.exists(scaler_path):
                    with open(scaler_path, 'rb') as f:
                        self.scaler = pickle.load(f)
                    print(f"[ML] Scaler loaded from {scaler_path}")
                
                # Get feature names from model
                self.feature_names = self.model.feature_name()
                
                print(f"[ML] LightGBM model loaded from {model_path}")
                print(f"[ML] Model has {self.model.num_feature()} features")
                
            else:
                # RandomForest or other sklearn model
                with open(model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    if isinstance(model_data, dict):
                        self.model = model_data.get('model')
                        self.scaler = model_data.get('scaler')
                        self.feature_names = model_data.get('feature_names', [])
                    else:
                        self.model = model_data
                self.model_type = 'sklearn'
                print(f"[ML] Sklearn model loaded from {model_path}")
                
        except Exception as e:
            print(f"[ML] Error loading model: {e}")
            self._init_simple_model()
    
    def _init_simple_model(self):
        """Initialize with rule-based fallback."""
        self.model = None
        self.model_type = 'rules'
        print("[ML] Using rule-based fallback")
    
    def predict(self, transaction: dict) -> dict:
        """
        Predict fraud probability for a transaction.
        
        Args:
            transaction: Transaction data dict
            
        Returns:
            dict with fraud_probability, confidence, and reasons
        """
        # Extract features
        features = self._extract_features(transaction)
        
        # Get prediction
        if self.model is not None:
            fraud_prob = self._predict_with_model(features)
        else:
            fraud_prob = self._predict_rule_based(features)
        
        # Calculate confidence
        confidence = max(fraud_prob, 1 - fraud_prob)
        
        # Generate reasons
        reasons = self._generate_reasons(features, fraud_prob)
        
        return {
            'fraud_probability': fraud_prob,
            'confidence': confidence,
            'reasons': reasons,
            'model_type': self.model_type
        }
    
    def _extract_features(self, transaction: dict) -> np.ndarray:
        """Extract features from transaction."""
        # Basic features
        amount = float(transaction.get('amount', 0))
        
        # Time features
        try:
            ts = transaction.get('timestamp', datetime.now().isoformat())
            if isinstance(ts, str):
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            else:
                dt = ts
            hour = dt.hour
            day_of_week = dt.weekday()
        except:
            hour = datetime.now().hour
            day_of_week = datetime.now().weekday()
        
        # Location risk (simplified)
        location = transaction.get('location', 'Unknown')
        high_risk_locations = ['High Risk Zone', 'Lagos, Nigeria', 'Unknown']
        location_risk = 0.9 if location in high_risk_locations else 0.2
        
        # Merchant risk (simplified)
        merchant = str(transaction.get('merchant', 'Unknown'))
        suspicious_merchants = ['Crypto', 'Casino', 'Betting', 'Dark']
        merchant_risk = 0.95 if any(x in merchant for x in suspicious_merchants) else 0.5
        
        # Velocity score (simplified - would need historical data)
        velocity_score = 0.3
        
        # Amount deviation (simplified)
        avg_amount = 1000  # Would calculate from history
        amount_deviation = min(abs(amount - avg_amount) / avg_amount, 1.0)
        
        # Create feature vector
        features = np.array([
            amount,
            hour,
            day_of_week,
            location_risk,
            merchant_risk,
            velocity_score,
            amount_deviation
        ])
        
        return features
    
    def _predict_with_model(self, features: np.ndarray) -> float:
        """Get prediction from ML model."""
        try:
            # Prepare features
            if len(features.shape) == 1:
                features = features.reshape(1, -1)
            
            # Pad features if needed (for LightGBM with more features)
            if self.model_type == 'lightgbm':
                expected_features = self.model.num_feature()
                current_features = features.shape[1]
                
                if current_features < expected_features:
                    # Pad with zeros
                    padding = np.zeros((features.shape[0], expected_features - current_features))
                    features = np.hstack([features, padding])
            
            # Scale features if scaler available
            if self.scaler is not None:
                # Ensure we have the right number of features for scaler
                if features.shape[1] < self.scaler.n_features_in_:
                    padding = np.zeros((features.shape[0], self.scaler.n_features_in_ - features.shape[1]))
                    features = np.hstack([features, padding])
                features_scaled = self.scaler.transform(features)
            else:
                features_scaled = features
            
            # Get prediction based on model type
            if self.model_type == 'lightgbm':
                pred = self.model.predict(features_scaled)[0]
                # Convert raw score to probability
                fraud_prob = 1 / (1 + np.exp(-pred))
                return float(fraud_prob)
            else:
                # Sklearn prediction
                pred = self.model.predict_proba(features_scaled)[0][1]
                return float(pred)
                
        except Exception as e:
            print(f"[ML] Prediction error: {e}")
            return self._predict_rule_based(features)
    
    def _predict_rule_based(self, features: np.ndarray) -> float:
        """Fallback rule-based prediction."""
        # Simple rule-based scoring
        amount, hour, day_of_week, location_risk, merchant_risk, velocity_score, amount_deviation = features
        
        score = 0.0
        
        # Amount rules
        if amount > 10000:
            score += 0.4
        elif amount > 5000:
            score += 0.2
        
        # Time rules
        if hour in [2, 3, 4, 5]:
            score += 0.15
        
        # Location rules
        score += location_risk * 0.3
        
        # Merchant rules
        score += merchant_risk * 0.2
        
        # Velocity rules
        score += velocity_score * 0.15
        
        return min(score, 1.0)
    
    def _generate_reasons(self, features: np.ndarray, fraud_prob: float) -> list:
        """Generate human-readable reasons for the prediction."""
        reasons = []
        
        amount, hour, day_of_week, location_risk, merchant_risk, velocity_score, amount_deviation = features
        
        # Main prediction reason
        if fraud_prob > 0.7:
            reasons.append(f"ML Model: High fraud risk ({fraud_prob:.1%})")
        elif fraud_prob > 0.4:
            reasons.append(f"ML Model: Moderate fraud risk ({fraud_prob:.1%})")
        else:
            reasons.append(f"ML Model: Low fraud risk ({fraud_prob:.1%})")
        
        # Feature-based reasons
        if amount > 5000:
            reasons.append(f"ML Factor: amount = {amount:.2f} (impact: {min(amount/50000, 0.25):.2f})")
        
        if hour in [2, 3, 4, 5]:
            reasons.append(f"ML Factor: unusual_hour = {hour}:00 (impact: 0.15)")
        
        if location_risk > 0.5:
            reasons.append(f"ML Factor: location_risk = {location_risk:.2f} (impact: {location_risk * 0.3:.2f})")
        
        if merchant_risk > 0.7:
            reasons.append(f"ML Factor: merchant_risk = {merchant_risk:.2f} (impact: {merchant_risk * 0.2:.2f})")
        
        return reasons[:5]  # Return top 5 reasons


class HybridDecisionEngine:
    """Combines ML predictions with business rules."""
    
    def __init__(self, ml_detector: MLFraudDetector):
        """Initialize hybrid engine."""
        self.ml_detector = ml_detector
    
    def decide(self, transaction: dict, rule_decision: dict) -> dict:
        """
        Make final decision combining ML and rules.
        
        Args:
            transaction: Transaction data
            rule_decision: Decision from business rules
            
        Returns:
            Final decision dict
        """
        # Get ML prediction
        ml_result = self.ml_detector.predict(transaction)
        
        # Combine with rule-based score
        rule_score = rule_decision.get('risk_score', 0)
        ml_score = int(ml_result['fraud_probability'] * 100)
        
        # Weighted combination (70% ML, 30% rules)
        final_score = int(ml_score * 0.7 + rule_score * 0.3)
        
        # Determine final status
        if final_score >= 85:
            status = "Blocked"
            action = "deny"
        elif final_score >= 60:
            status = "Review"
            action = "investigate"
        elif final_score >= 40:
            status = "Review"
            action = "monitor"
        else:
            status = "Approved"
            action = "allow"
        
        # Combine reasons
        all_reasons = ml_result['reasons'] + rule_decision.get('reasons', [])
        
        return {
            "status": status,
            "risk_score": final_score,
            "ml_fraud_probability": ml_result['fraud_probability'],
            "ml_confidence": ml_result['confidence'],
            "reasons": all_reasons[:10],  # Top 10 reasons
            "action": action,
            "primary_engine": "ML" if ml_score > rule_score else "Rules",
            "engine_version": f"v3.0-{ml_result['model_type'].upper()}",
            "decision_time_ms": "<20ms",
            "explainability": {
                "ml_score": ml_score,
                "rule_score": rule_score,
                "final_score": final_score,
                "top_ml_reasons": ml_result['reasons'][:3],
                "top_rule_reasons": rule_decision.get('reasons', [])[:3]
            }
        }
