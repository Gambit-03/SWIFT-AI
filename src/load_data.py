from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"

import pandas as pd
import numpy as np
import gc

def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2    
    
    for col in df.columns:
        col_type = df[col].dtypes
        
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float32)    
                    
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose: 
        print(f'Mem. usage decreased to {end_mem:5.2f} Mb ({100 * (start_mem - end_mem) / start_mem:.1f}% reduction)')
    return df

def load_and_merge():
    print("STEP 1: LOADING AND MERGING DATA")

    print("\nLoading Train Transaction...")
    train_trans = pd.read_csv(RAW_DIR / "train_transaction.csv")
    
    print("Loading Train Identity...")
    train_id = pd.read_csv(RAW_DIR / "train_identity.csv")

    print("Merging Train Data on TransactionID...")
    train_df = pd.merge(train_trans, train_id, on='TransactionID', how='left')
    
    if train_df.duplicated('TransactionID').sum() > 0:
        print(f"Removing {train_df.duplicated('TransactionID').sum()} duplicates...")
        train_df = train_df.drop_duplicates('TransactionID')
    
    print(f"Merged Train Shape: {train_df.shape}")
    
    print("Reducing Memory Usage for Train...")
    train_df = reduce_mem_usage(train_df)

    del train_trans, train_id
    gc.collect()

    print("\nLoading Test Transaction...")
    test_trans  = pd.read_csv(RAW_DIR / "test_transaction.csv")

    print("Loading Test Identity...")
    test_id    = pd.read_csv(RAW_DIR / "test_identity.csv")

    print("Merging Test Data on TransactionID...")
    test_df = pd.merge(test_trans, test_id, on='TransactionID', how='left')
    print(f"Merged Test Shape: {test_df.shape}")

    print("Reducing Memory Usage for Test...")
    test_df = reduce_mem_usage(test_df)

    del test_trans, test_id
    gc.collect()

    print("\nSaving merged dataframes to .pkl files...")
    train_df.to_pickle('train_merged.pkl')
    test_df.to_pickle('test_merged.pkl')
    
    print("SUCCESS: Data loaded, merged, shrunk, and saved!")

if __name__ == "__main__":
    load_and_merge()