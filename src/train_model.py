import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import roc_auc_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import KFold
import gc
import warnings
warnings.filterwarnings('ignore')

def calculate_class_weight(y):
    """
    Calculate scale_pos_weight for imbalanced fraud data.
    This tells LightGBM to weight fraud cases more heavily.
    """
    fraud_count = (y == 1).sum()
    normal_count = (y == 0).sum()
    scale_pos_weight = normal_count / fraud_count
    print(f"   [Class Balance] Normal: {normal_count}, Fraud: {fraud_count}")
    print(f"   [Class Weight] scale_pos_weight = {scale_pos_weight:.2f}")
    return scale_pos_weight

def train_model():
    print("STEP 4: MODEL TRAINING (LIGHTGBM WITH K-FOLD CROSS-VALIDATION)")
    print("="*70)

    X_train = pd.read_pickle("X_train.pkl")
    y_train = pd.read_pickle("y_train.pkl")
    X_val = pd.read_pickle("X_val.pkl")
    y_val = pd.read_pickle("y_val.pkl")

    print(f"\nDataset Shapes:")
    print(f"  Training Data: {X_train.shape}")
    print(f"  Validation Data: {X_val.shape}")
    print(f"  Features: {X_train.shape[1]}")

    # --- STEP 1: CALCULATE CLASS WEIGHT ---
    print("\n[STEP 1] Calculating Class Weight for Imbalanced Data...")
    scale_pos_weight = calculate_class_weight(y_train)

    # --- STEP 2: K-FOLD CROSS-VALIDATION ---
    print("\n[STEP 2] Initiating K-Fold Cross-Validation (K=5)...")
    print("-" * 70)
    
    NFOLDS = 5
    kfold = KFold(n_splits=NFOLDS, shuffle=False)

    
    fold_auc_scores = []
    fold_models = []
    fold_predictions = []
    
    for fold_idx, (train_idx, val_idx) in enumerate(kfold.split(X_train)):
        print(f"\n>>> FOLD {fold_idx + 1}/{NFOLDS}")
        
        X_fold_train = X_train.iloc[train_idx]
        y_fold_train = y_train.iloc[train_idx]
        X_fold_val = X_train.iloc[val_idx]
        y_fold_val = y_train.iloc[val_idx]
        
        print(f"    Fold Train: {X_fold_train.shape[0]}, Fold Val: {X_fold_val.shape[0]}")
        
        # --- LightGBM with Class Weight ---
        model = lgb.LGBMClassifier(
            objective="binary",
            metric="auc",
            boosting_type="gbdt",
            n_estimators=5000,
            learning_rate=0.01,  # Lower learning rate = more stable
            num_leaves=256,
            max_depth=-1,
            colsample_bytree=0.7,
            subsample=0.8,
            subsample_freq=1,
            scale_pos_weight=scale_pos_weight,  # CRITICAL: Weight fraud cases
            random_state=42 + fold_idx,  # Vary seed per fold
            n_jobs=-1,
            verbose=-1
        )

        model.fit(
            X_fold_train,
            y_fold_train,
            eval_set=[(X_fold_train, y_fold_train), (X_fold_val, y_fold_val)],
            eval_names=["Train", "Fold Val"],
            eval_metric="auc",
            callbacks=[
                lgb.early_stopping(stopping_rounds=100, verbose=False),
                lgb.log_evaluation(period=100)
            ]
        )

        # Evaluate on this fold
        fold_preds = np.asarray(model.predict_proba(X_fold_val))[:, 1]
        fold_auc = roc_auc_score(y_fold_val, fold_preds)
        fold_auc_scores.append(fold_auc)
        fold_models.append(model)
        fold_predictions.append(fold_preds)
        
        print(f"    Fold AUC: {fold_auc:.4f}")

    # --- STEP 3: CROSS-VALIDATION SUMMARY ---
    print("\n" + "="*70)
    print("[STEP 3] K-Fold Cross-Validation Summary")
    print("="*70)
    print(f"Fold AUC Scores: {[f'{auc:.4f}' for auc in fold_auc_scores]}")
    print(f"Mean AUC: {np.mean(fold_auc_scores):.4f} (+/- {np.std(fold_auc_scores):.4f})")
    
    if np.mean(fold_auc_scores) > 0.90:
        print("✓ EXCELLENT CROSS-VALIDATION (>0.90)")
    elif np.mean(fold_auc_scores) > 0.85:
        print("✓ GOOD CROSS-VALIDATION (>0.85)")
    else:
        print("⚠ MODEL NEEDS IMPROVEMENT (<0.85)")

    # --- STEP 4: RETRAIN ON FULL TRAIN SET ---
    print("\n[STEP 4] Retraining on Full Training Set...")
    print("-" * 70)
    
    final_model = lgb.LGBMClassifier(
        objective="binary",
        metric="auc",
        boosting_type="gbdt",
        n_estimators=5000,
        learning_rate=0.01,
        num_leaves=256,
        max_depth=-1,
        colsample_bytree=0.7,
        subsample=0.8,
        subsample_freq=1,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )

    final_model.fit(
        X_train,
        y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        eval_names=["Train", "Validation"],
        eval_metric="auc",
        callbacks=[
            lgb.early_stopping(stopping_rounds=100, verbose=False),
            lgb.log_evaluation(period=100)
        ]
    )

    val_preds = np.asarray(final_model.predict_proba(X_val))[:, 1]
    val_auc = roc_auc_score(y_val, val_preds)

    print(f"\nFinal Model Validation AUC: {val_auc:.4f}")

    # --- STEP 5: DETAILED EVALUATION METRICS ---
    print("\n[STEP 5] Detailed Evaluation Metrics")
    print("-" * 70)
    
    # Use 0.5 threshold for binary predictions
    val_preds_binary = (val_preds >= 0.5).astype(int)
    
    tn, fp, fn, tp = confusion_matrix(y_val, val_preds_binary).ravel()
    precision, recall, f1, _ = precision_recall_fscore_support(y_val, val_preds_binary, average='binary')
    
    print(f"True Negatives:  {tn}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"True Positives:  {tp}")
    print(f"\nPrecision (Minimize False Positives): {precision:.4f}")
    print(f"Recall (Detect All Fraud):           {recall:.4f}")
    print(f"F1-Score:                            {f1:.4f}")
    
    # --- STEP 6: FEATURE IMPORTANCE ---
    print("\n[STEP 6] Feature Importance Analysis")
    print("-" * 70)
    
    importance = pd.DataFrame({
        "Feature": X_train.columns,
        "Importance": final_model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    print("\nTop 15 Most Important Features:")
    print(importance.head(15).to_string(index=False))
    importance.to_csv("feature_importance.csv", index=False)

    # --- STEP 7: SAVE MODEL ---
    print("\n[STEP 7] Saving Model")
    print("-" * 70)
    
    final_model.booster_.save_model("fraud_model_lgb.txt")
    print("✓ Model saved to fraud_model_lgb.txt")



    # --- FINAL SUMMARY ---
    print("\n" + "="*70)
    print("TRAINING COMPLETE ✓")
    print("="*70)
    print(f"Cross-Val AUC:     {np.mean(fold_auc_scores):.4f} (±{np.std(fold_auc_scores):.4f})")
    print(f"Final Val AUC:     {val_auc:.4f}")
    print(f"Precision:         {precision:.4f} (minimize false fraud alerts)")
    print(f"Recall:            {recall:.4f} (catch real fraud)")
    print(f"\nModels saved:")
    print(f"  - fraud_model_lgb.txt (For predictions)")
    print(f"  - feature_importance.csv (Feature rankings)")
    print("="*70)

    gc.collect()

if __name__ == "__main__":
    train_model()
