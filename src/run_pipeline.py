#!/usr/bin/env python3
"""
SWIFT-AI EXECUTION ORCHESTRATOR
=================================
Master script to run the entire pipeline from start to finish.

USAGE:
  python run_pipeline.py [--step START_STEP] [--demo]

EXAMPLES:
  python run_pipeline.py              # Run all steps (1-4)
  python run_pipeline.py --step 3     # Run from step 3 onwards
  python run_pipeline.py --demo       # Run quick demo on subset
"""

import subprocess
import time
from pathlib import Path
import sys
print("PYTHON EXECUTABLE:", sys.executable)


# ============================================================================
# PIPELINE STEPS
# ============================================================================

STEPS = [
    {
        "number": 1,
        "name": "LOAD & MERGE DATA",
        "script": "load_data.py",
        "description": "Load transaction + identity data, merge, reduce memory",
        "outputs": ["train_merged.pkl", "test_merged.pkl"],
        "duration": "~2-3 minutes"
    },
    {
        "number": 2,
        "name": "FEATURE ENGINEERING",
        "script": "feature_eng.py",
        "description": "Create UIDs, aggregations, frequency encoding (THE MAGIC)",
        "outputs": ["train_engineered.pkl", "test_engineered.pkl"],
        "duration": "~3-5 minutes"
    },
    {
        "number": 3,
        "name": "PREPROCESSING & VALIDATION",
        "script": "preprocessing.py",
        "description": "Handle NaNs, scale data, detect drift, split train/val",
        "outputs": ["X_train.pkl", "X_val.pkl", "X_test.pkl", "scaler.pkl", "drift_report.csv"],
        "duration": "~2 minutes"
    },
    {
        "number": 4,
        "name": "MODEL TRAINING",
        "script": "train_model.py",
        "description": "K-Fold CV, hyperparameter tuning, LightGBM training, SHAP values",
        "outputs": ["fraud_model_lgb.txt", "feature_importance.csv", "shap_values.npy"],
        "duration": "~10-15 minutes (depends on hardware)"
    }
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step_info(step: dict):
    """Print information about a step."""
    print(f"\n📍 STEP {step['number']}: {step['name']}")
    print(f"   Script: {step['script']}")
    print(f"   Description: {step['description']}")
    print(f"   Expected Duration: {step['duration']}")
    print(f"   Outputs: {', '.join(step['outputs'][:3])}{'...' if len(step['outputs']) > 3 else ''}")

def check_dependencies():
    """Check if all required packages are installed."""
    required = [
        'pandas',
        'numpy',
        'lightgbm',
        'scikit-learn',
        'shap',
        'scipy',
        'flask'
    ]
    
    print_header("DEPENDENCY CHECK")
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package:20s} installed")
        except ImportError:
            print(f"✗ {package:20s} MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print(f"\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("\n✓ All dependencies satisfied!")
    return True

def check_data_files():
    """Check if input data files exist."""
    print_header("DATA FILE CHECK")
    
    required_files = [
        'train_transaction.csv',
        'train_identity.csv',
        'test_transaction.csv',
        'test_identity.csv'
    ]
    
    missing = []
    for filename in required_files:
        if Path(filename).exists():
            size_mb = Path(filename).stat().st_size / (1024 * 1024)
            print(f"✓ {filename:30s} ({size_mb:.1f} MB)")
        else:
            print(f"✗ {filename:30s} MISSING")
            missing.append(filename)
    
    if missing:
        print(f"\n✗ Missing data files: {', '.join(missing)}")
        print("\nDownload from Kaggle: https://www.kaggle.com/c/ieee-fraud-detection/data")
        return False
    
    print("\n✓ All data files present!")
    return True

def run_step(step: dict, demo_mode: bool = False):
    """Run a single pipeline step."""
    print_step_info(step)
    
    script = step['script']
    
    if not Path(script).exists():
        print(f"\n✗ Script not found: {script}")
        return False
    
    print(f"\n[Action] Running {script}...")
    
    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=False
        )
        elapsed = time.time() - start_time
        
        print(f"\n✓ Step {step['number']} completed in {elapsed:.1f} seconds")
        
        # Check for outputs
        missing_outputs = []
        for output_file in step['outputs']:
            if not Path(output_file).exists():
                missing_outputs.append(output_file)
        
        if missing_outputs:
            print(f"\n⚠ Warning: Expected outputs not found: {missing_outputs}")
            return False
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Step {step['number']} failed with error:")
        print(f"  {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠ Step {step['number']} interrupted by user")
        return False

def run_inference_api():
    """Start the Flask inference API."""
    print_header("STARTING INFERENCE API")
    
    print("\n📌 Flask API Configuration:")
    print("   Host: 0.0.0.0")
    print("   Port: 5000")
    print("   URL: http://localhost:5000")
    
    print("\n🔗 API Endpoints:")
    print("   GET  /                    Health check + API info")
    print("   GET  /health              Detailed health check")
    print("   GET  /model-info          Model metadata")
    print("   POST /predict             Single transaction prediction")
    print("   POST /batch-predict       Batch transaction predictions")
    
    print("\n[Action] Starting API (Press Ctrl+C to stop)...")
    
    try:
        subprocess.run([sys.executable, "inference_api.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n✓ API stopped gracefully")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ API failed: {e}")

def print_summary(steps_completed: int, total_steps: int):
    """Print execution summary."""
    print_header("PIPELINE EXECUTION SUMMARY")
    
    if steps_completed == total_steps:
        print(f"\n✓ SUCCESS! All {total_steps} steps completed.")
        print("\n📊 Generated Files:")
        print("   - fraud_model_lgb.txt       (Trained LightGBM model)")
        print("   - feature_importance.csv    (Feature rankings)")
        print("   - shap_importance.csv       (SHAP-based importance)")
        print("   - shap_values.npy           (SHAP values for test set)")
        print("   - drift_report.csv          (Data drift analysis)")
        print("   - scaler.pkl                (Fitted StandardScaler)")
        
        print("\n🚀 Next Steps:")
        print("   1. Start the API: python inference_api.py")
        print("   2. Test predictions: curl http://localhost:5000")
        print("   3. Create your dashboard (use metadata_hydration.py)")
        print("   4. Present to judges!")
    else:
        print(f"\n⚠ Pipeline incomplete: {steps_completed}/{total_steps} steps done")
        print("\nYou can resume from the next step later.")

def main():
    """Main orchestration function."""
    
    # Parse arguments
    start_step = 1
    demo_mode = False
    run_api = False
    
    for arg in sys.argv[1:]:
        if arg.startswith('--step='):
            start_step = int(arg.split('=')[1])
        elif arg == '--step' and len(sys.argv) > sys.argv.index(arg) + 1:
            start_step = int(sys.argv[sys.argv.index(arg) + 1])
        elif arg == '--demo':
            demo_mode = True
        elif arg == '--api':
            run_api = True
    
    # Print banner
    print("\n" + "="*70)
    print("  SWIFT-AI: FRAUD DETECTION PIPELINE ORCHESTRATOR")
    print("  36-Hour Hackathon Edition")
    print("="*70)
    
    # Pre-flight checks
    if not check_dependencies():
        print("\n⚠ Please install missing dependencies and try again.")
        return 1
    
    if not check_data_files():
        print("\n⚠ Please download data files and try again.")
        return 1
    
    # Main pipeline
    print_header(f"STARTING PIPELINE (Steps {start_step}-{len(STEPS)})")
    
    steps_completed = 0
    for step in STEPS:
        if step['number'] < start_step:
            print(f"\n⏭️  Skipping Step {step['number']} (already completed)")
            steps_completed += 1
            continue
        
        success = run_step(step, demo_mode)
        if success:
            steps_completed += 1
        else:
            print(f"\n⚠ Pipeline stopped at Step {step['number']}")
            print_summary(steps_completed, len(STEPS))
            return 1
    
    # Print summary
    print_summary(steps_completed, len(STEPS))
    
    # Optionally start API
    if run_api or (steps_completed == len(STEPS)):
        response = input("\n🎯 Start the Flask API now? (y/n): ")
        if response.lower() == 'y':
            run_inference_api()
    
    return 0

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
