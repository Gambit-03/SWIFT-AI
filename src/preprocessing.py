import pandas as pd
import numpy as np
import gc
import pickle
from typing import List, Tuple, Any
from sklearn.preprocessing import StandardScaler
from scipy.stats import ks_2samp

def detect_feature_drift(X_train: pd.DataFrame, X_test: pd.DataFrame, threshold: float = 0.05) -> Tuple[List[Tuple[str, float, float]], List[Tuple[str, float]]]:
    """
    Use Kolmogorov-Smirnov Test to detect data drift.
    
    High p-value (>0.05) = Feature distribution is similar in Train & Test
    Low p-value  (<0.05) = Feature distribution DRIFTED (may cause problems)
    
    This prevents your model from failing in production due to data shift.
    """
    print("\n[KS-Test] Detecting Feature Drift...")
    print("   (Comparing Train vs Test distributions)")
    
    drift_features: List[Tuple[str, float, float]] = []
    passed_features: List[Tuple[str, float]] = []
    
    for col in X_train.columns:
        ks_stat, p_value = ks_2samp(X_train[col], X_test[col])
        
        if p_value < threshold: # type: ignore
            drift_features.append((col, p_value, ks_stat)) # type: ignore
            print(f"   ⚠ DRIFT: {col:30s} | p-value: {p_value:.6f} | KS: {ks_stat:.4f}")
        else:
            passed_features.append((col, p_value)) # type: ignore
    
    print(f"\n   Summary: {len(passed_features)} features OK, {len(drift_features)} DRIFTED")
    
    # Save drift report
    if drift_features:
        drift_df = pd.DataFrame(drift_features, columns=['Feature', 'p_value', 'ks_stat'])
        drift_df.to_csv('drift_report.csv', index=False)
        print(f"   [Saved] drift_report.csv (for investigation)")
    
    return drift_features, passed_features

def perform_preprocessing() -> None:
    print("STEP 3: PREPROCESSING (STRICT PIPELINE + DRIFT DETECTION)")
    print("="*70)

    # --- 1. LOAD ENGINEERED DATA ---
    print("\n[Action] Loading Engineered Data...")
    train: pd.DataFrame = pd.read_pickle('train_engineered.pkl')
    test: pd.DataFrame = pd.read_pickle('test_engineered.pkl')
    
    # Isolate Target
    y: pd.Series = train['isFraud']
    
    # Save TransactionIDs for the final Dashboard/Submission
    train_ids: pd.Series = train['TransactionID']
    test_ids: pd.Series = test['TransactionID']

    # --- 2. FEATURE SELECTION & CLEANING ---
    # We drop columns that models can't handle (Strings, Dates)
    print("[Action] Dropping non-numeric columns...")
    
    # We drop 'uid' (it was a string for grouping) and 'TransactionDT' (time delta)
    # We keep the extracted features like 'Transaction_hour', 'uid_TransactionAmt_mean', etc.
    drop_cols = ['isFraud', 'TransactionDT', 'TransactionID', 'uid', 
                 'P_emaildomain', 'R_emaildomain', 'card1', 'addr1', 'dist1']
    
    # Handle columns that might have been created but are strings
    extra_drops: List[str] = [c for c in train.columns if train[c].dtype == 'object']
    final_drops: List[str] = list(set(drop_cols + extra_drops))
    
    X: pd.DataFrame = train.drop(columns=final_drops, errors='ignore')
    X_test: pd.DataFrame = test.drop(columns=final_drops, errors='ignore')
    
    # Garbage collection
    del train, test
    gc.collect()

    # --- 3. NO NANs (Strict Pipeline Rule) ---
    print("\n[Strict Pipeline] Handling NaNs (Filling with -999)...")
    nan_count_train: int = int(X.isna().sum().sum())
    nan_count_test: int = int(X_test.isna().sum().sum())
    print(f"   NaNs in Train: {nan_count_train}, NaNs in Test: {nan_count_test}")
    
    X = X.fillna(-999)
    X_test = X_test.fillna(-999)
    print(f"   ✓ All NaNs filled")
    
    # --- 4. SCALING / NORMALIZATION (Strict Pipeline Rule) ---
    # "The features shouldn’t have too much variability... use standardscaler"
    print("\n[Strict Pipeline] Scaling Data (StandardScaler)...")
    print("   (Using same scaler weights for Train and Test)")
    
    scaler: StandardScaler = StandardScaler()
    
    # FIT on Train, TRANSFORM Train
    # We use float32 to save memory (StandardScaler defaults to float64)
    X_scaled_array: np.ndarray = scaler.fit_transform(X)
    X = pd.DataFrame(X_scaled_array, columns=X.columns).astype('float32')
    
    # TRANSFORM Test (Use the SAME weights - this is CRITICAL)
    X_test_scaled_array: np.ndarray = scaler.transform(X_test)
    X_test = pd.DataFrame(X_test_scaled_array, columns=X_test.columns).astype('float32')
    
    print(f"   ✓ StandardScaler fit on {len(X)} training samples")
    print(f"   ✓ Same scaler applied to {len(X_test)} test samples")
    
    del X_scaled_array, X_test_scaled_array
    gc.collect()

    # --- 4.5 DRIFT DETECTION (NEW - CRITICAL FOR PRODUCTION) ---
    drift_features, passed_features = detect_feature_drift(X, X_test, threshold=0.05)
    
    if drift_features:
        print("\n   ⚠ IMPORTANT: These features have drifted.")
        print("   This is normal in production, but monitor model performance.")

    # --- 5. SPLIT DATA (80/20 Time-Series Split) ---
    # We split by TIME, not random shuffle, to respect the "Future" prediction goal.
    print("\n[Strict Pipeline] Splitting Data (80% Train / 20% Validation)...")
    
    split_index: int = int(len(X) * 0.8)
    
    X_train: pd.DataFrame = X.iloc[:split_index]
    y_train: pd.Series = y.iloc[:split_index]
    
    X_val: pd.DataFrame = X.iloc[split_index:]
    y_val: pd.Series = y.iloc[split_index:]
    
    print(f"   Train Shape: {X_train.shape}")
    print(f"   Val Shape:   {X_val.shape}")
    
    # Check class balance in train and val
    train_fraud_pct: float = float((y_train.sum() / len(y_train)) * 100)
    val_fraud_pct: float = float((y_val.sum() / len(y_val)) * 100)
    print(f"   Fraud % in Train: {train_fraud_pct:.2f}%")
    print(f"   Fraud % in Val:   {val_fraud_pct:.2f}%")

    # --- 6. SAVE ---
    print("\n[Action] Saving Preprocessed Data...")
    X_train.to_pickle('X_train.pkl')
    y_train.to_pickle('y_train.pkl')
    X_val.to_pickle('X_val.pkl')
    y_val.to_pickle('y_val.pkl')
    X_test.to_pickle('X_test.pkl')
    test_ids.to_pickle('test_ids.pkl')
    
    # Also save the scaler for production use
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("   ✓ scaler.pkl saved (for production inference)")

    print("\n" + "="*70)
    print("SUCCESS: Preprocessing Complete!")
    print("="*70)

if __name__ == "__main__":
    perform_preprocessing()