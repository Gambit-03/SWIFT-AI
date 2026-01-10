import random
from datetime import datetime

# Import ML-powered hybrid decision engine
try:
    from ml_fraud_detector import MLFraudDetector, HybridDecisionEngine
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("[WARNING] ML fraud detector not available, using rules-only mode")

# Import SWIFT-AI adapter
try:
    from swift_ai_adapter import SwiftAIAdapter
    SWIFT_AI_AVAILABLE = True
except ImportError:
    SWIFT_AI_AVAILABLE = False
    print("[WARNING] SWIFT-AI adapter not available")


class FraudEngine:
    """
    Core engine for determining fraud risk.
    Now powered by SWIFT-AI API + ML + Rule-based decision system.
    Provides fast (<100ms), accurate, and explainable fraud detection.
    """
    
    def __init__(self, use_ml=True, use_swift_ai=True):
        """
        Initialize fraud engine.
        
        Args:
            use_ml: Whether to use ML-powered hybrid engine (default: True)
            use_swift_ai: Whether to use SWIFT-AI API if available (default: True)
        """
        # Rule-based thresholds
        self.risk_thresholds = {
            'critical': 85,
            'high': 65,
            'medium': 40
        }
        
        # Initialize SWIFT-AI adapter
        self.use_swift_ai = use_swift_ai and SWIFT_AI_AVAILABLE
        self.swift_ai = None
        
        if self.use_swift_ai:
            try:
                self.swift_ai = SwiftAIAdapter()
                if self.swift_ai.is_available():
                    print("[FraudEngine] SWIFT-AI API connected ✓")
                else:
                    print("[FraudEngine] SWIFT-AI API not available, using local ML")
                    self.swift_ai = None
            except Exception as e:
                print(f"[FraudEngine] SWIFT-AI init failed: {e}")
                self.swift_ai = None
        
        # Initialize ML components
        self.use_ml = use_ml and ML_AVAILABLE
        
        if self.use_ml:
            try:
                self.ml_detector = MLFraudDetector()
                self.hybrid_engine = HybridDecisionEngine(self.ml_detector)
                print("[FraudEngine] Local ML model initialized ✓")
            except Exception as e:
                print(f"[FraudEngine] ML initialization failed: {e}")
                self.use_ml = False
                print("[FraudEngine] Falling back to rules-only mode")
        else:
            print("[FraudEngine] Running in rules-only mode")

    def decide(self, transaction):
        """
        Analyze a transaction and return a decision.
        Priority: SWIFT-AI API > Local ML > Rules
        
        Args:
            transaction (dict): Transaction data (amount, location, etc.)
            
        Returns:
            dict: Decision object with status, score, reasons, explainability, etc.
        """
        # Add timestamp if not present
        if 'timestamp' not in transaction:
            transaction['timestamp'] = datetime.now().isoformat()
        
        # Priority 1: Try SWIFT-AI API
        if self.swift_ai:
            try:
                swift_result = self.swift_ai.predict(transaction)
                if swift_result:
                    # Convert SWIFT-AI result to our format
                    return self._convert_swift_ai_result(swift_result, transaction)
            except Exception as e:
                print(f"[FraudEngine] SWIFT-AI failed: {e}, falling back to local ML")
        
        # Priority 2: Get rule-based decision
        rule_decision = self._apply_business_rules(transaction)
        
        # Priority 3: Use local ML if available
        if self.use_ml:
            try:
                final_decision = self.hybrid_engine.decide(transaction, rule_decision)
                
                # --- VERIFICATION LOG FOR USER ---
                print(f"\n[FRAUD ENGINE] 🔍 Analyzing Transaction {transaction.get('id', 'Unknown')}")
                print(f"[FRAUD ENGINE] 🤖 ML Model Score: {final_decision['explainability']['ml_score']}/100")
                print(f"[FRAUD ENGINE] 📜 Rule Base Score: {final_decision['explainability']['rule_score']}/100")
                print(f"[FRAUD ENGINE] ⚖️  Final Weighted Score: {final_decision['risk_score']}/100")
                print(f"[FRAUD ENGINE] ✅ Decision: {final_decision['status']} (Reasons: {len(final_decision['reasons'])})\n")
                # ---------------------------------
                
                return final_decision
            except Exception as e:
                print(f"[FraudEngine] ML decision failed: {e}, using rules only")
                print(f"[FRAUD ENGINE] ⚠️ FALLBACK: Using Hardcoded Rules Only")
                return rule_decision
        else:
            print(f"[FRAUD ENGINE] ⚠️ MODE: Rules Only (ML Not Active)")
            return rule_decision
    
    def _convert_swift_ai_result(self, swift_result: dict, transaction: dict) -> dict:
        """Convert SWIFT-AI API result to our decision format."""
        fraud_prob = swift_result.get('fraud_probability', 0.5)
        risk_level = swift_result.get('risk_level', 'UNKNOWN')
        
        # Map risk level to status
        if risk_level in ['CRITICAL', 'HIGH']:
            status = "Blocked"
            action = "deny"
        elif risk_level == 'MEDIUM':
            status = "Review"
            action = "investigate"
        elif risk_level == 'LOW':
            status = "Review"
            action = "monitor"
        else:
            status = "Approved"
            action = "allow"
        
        # Calculate risk score from probability
        risk_score = int(fraud_prob * 100)
        
        # Build reasons
        reasons = [f"SWIFT-AI: Fraud probability {fraud_prob:.1%}"]
        reasons.append(f"SWIFT-AI: Risk level {risk_level}")
        
        # Add fraud indicators
        indicators = swift_result.get('fraud_indicators', [])
        if indicators:
            reasons.append(f"SWIFT-AI: Indicators - {', '.join(indicators[:3])}")
        
        return {
            "status": status,
            "risk_score": risk_score,
            "ml_fraud_probability": fraud_prob,
            "ml_confidence": swift_result.get('confidence', 0.5),
            "reasons": reasons,
            "action": action,
            "primary_engine": "SWIFT-AI",
            "engine_version": "v4.0-SWIFT-AI-API",
            "decision_time_ms": swift_result.get('inference_time_ms', '<20ms'),
            "explainability": {
                "swift_ai_indicators": indicators,
                "risk_level": risk_level
            }
        }
    
        # Rule-based thresholds
        self.risk_thresholds = {
            'critical': 80,
            'high': 60,
            'medium': 40  # Anything above 40 triggers Review
        }
        
    # [ ... omitted ... ]

    def _apply_business_rules(self, transaction):
        """
        Apply traditional business rules for fraud detection.
        """
        # Start with a base score that isn't always 0 to simulate environmental noise
        score = random.randint(5, 15) 
        reasons = []
        
        # Extract features
        amount = float(transaction.get('amount', 0))
        location = transaction.get('location', 'Unknown')
        country = transaction.get('country', 'Unknown')
        merchant = transaction.get('merchant', 'Unknown')
        
        # --- Rule Engine ---
        
        # 1. Amount Checks (Variable weighting)
        if amount > 15000:
            score += 55
            reasons.append(f"Rule: Critical transaction amount (${amount:,.2f})")
        elif amount > 5000:
            score += 30
            reasons.append("Rule: High transaction value")
        elif amount > 1000:
            score += 10 # Slight increase for moderate amounts
            
        # 2. Location Checks
        high_risk_locs = ['High Risk Zone', 'Lagos, Nigeria', 'Unknown']
        if location in high_risk_locs or country in ['NG', 'RU', 'KP']:
            score += 45
            reasons.append(f"Rule: High-risk geographic location: {location}")
        
        # 2.1 Cross-Border / Location Mismatch Check
        # User's 'Home' Country (Simulated logic - in real app, get from user profile)
        home_country = 'IN' # Defaulting to India for this demo user
        txn_country = str(transaction.get('country', 'Unknown')).upper()
        
        # Check if country code is valid and differs from home
        if txn_country not in ['UNKNOWN', 'XX'] and txn_country != home_country:
             score += 40
             reasons.append(f"Rule: Location Mismatch (IP in {txn_country} vs Home {home_country})")
             
        # Check for specific high-risk IPs/Locations
        if transaction.get('location') == 'Unknown' or transaction.get('ip_address') in ['127.0.0.1', 'N/A']:
             # Don't penalize local dev, but note it
             pass 
        elif transaction.get('location') == 'High Risk Zone':
             score += 50
             reasons.append(f"Rule: High Risk Zone Detected")
            
        # 3. Merchant Checks
        suspicious_merchants = ['Crypto', 'Casino', 'Betting', 'Dark']
        if any(x in str(merchant) for x in suspicious_merchants):
            score += 35
            reasons.append(f"Rule: High-risk merchant category")

        # 5. User Profile Checks (New Real Logic)
        avg_spent = float(transaction.get('user_total_spent', 0)) / max(1, transaction.get('user_txn_count', 1))
        
        # New account + High amount
        created_at_str = transaction.get('account_created_at')
        if created_at_str:
            try:
                created_at = datetime.fromisoformat(created_at_str)
                age_hours = (datetime.utcnow() - created_at).total_seconds() / 3600
                if age_hours < 24 and amount > 500: # Stricter check
                    score += 50
                    reasons.append("Rule: High value on new account (<24h)")
            except: pass

        # Velocity / Anomaly Check
        if transaction.get('user_txn_count', 0) > 2 and amount > (avg_spent * 4):
            score += 40
            reasons.append(f"Rule: Spending spike (4x average)")
            
        # Previous High Risk Score
        if transaction.get('user_risk_score', 0) > 50:
             score += 25
             reasons.append("Rule: User has elevated risk profile")

        # Finalize Score
        final_score = min(100, score)
        
        # Determine Status
        if final_score >= self.risk_thresholds['critical']:
            status = "Blocked"
            action = "deny"
        elif final_score >= self.risk_thresholds['high']:
            status = "Review"
            action = "investigate"
        elif final_score >= self.risk_thresholds['medium']:
            status = "Review"
            action = "monitor"
        else:
            status = "Approved"
            action = "allow"
            
        return {
            "status": status,
            "risk_score": final_score,
            "reasons": reasons,
            "action": action,
            "engine_version": "v2.1-Rules" if not self.use_ml else "v3.0-Hybrid"
        }
