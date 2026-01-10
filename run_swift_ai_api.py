"""
SWIFT-AI INFERENCE API RUNNER
==============================
Runs the SWIFT-AI inference API on port 5002.
"""

import sys
import os
from pathlib import Path

# Get SWIFT-AI src directory
current_dir = Path(__file__).parent
swift_ai_src = current_dir / "DA 2" / "SWIFT-AI" / "src"

if not swift_ai_src.exists():
    print(f"❌ Error: SWIFT-AI directory not found at {swift_ai_src}")
    sys.exit(1)

# Add to path
sys.path.insert(0, str(swift_ai_src))

print("\n" + "="*70)
print("SWIFT-AI INFERENCE API (Port 5002)")
print("="*70)
print(f"SWIFT-AI Directory: {swift_ai_src}")
print("="*70)

# Change to SWIFT-AI directory so it can find model files
os.chdir(str(swift_ai_src))

# Now import and modify
try:
    import inference_api
    
    print("\n[INFO] Starting SWIFT-AI API on port 5002...")
    print("[INFO] Fraud Service will connect to this API")
    print("[INFO] Press Ctrl+C to stop\n")
    
    # Run on port 5002
    inference_api.app.run(
        host="0.0.0.0",
        port=5002,
        debug=False,
        threaded=True
    )
except ImportError as e:
    print(f"❌ Error importing inference_api: {e}")
    print("\nNote: SWIFT-AI model may not be trained yet.")
    print("This is OK - fraud service will use local ML model instead.")
    sys.exit(1)
