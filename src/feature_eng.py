import pandas as pd
import numpy as np
import gc

def frequency_encoding(df, columns):
    for col in columns:
        print(f"   -> Frequency Encoding: {col}")
        
        # --- FIX: Pandas crashes on float16 map lookups ---
        # We temporarily cast to float32 just for this operation
        if df[col].dtype == 'float16':
            print(f"      (Converting {col} from float16 to float32 for safety)")
            df[col] = df[col].astype('float32')
            
        freq_encoding = df[col].value_counts(dropna=False).to_dict()
        df[col + '_fq_enc'] = df[col].map(freq_encoding)
    return df

def aggregate_features(df, uid_col, agg_cols, aggs=['mean', 'std']):
    for col in agg_cols:
        for agg_type in aggs:
            new_col_name = f'{uid_col}_{col}_{agg_type}'
            print(f"   -> Aggregating {col} by {uid_col} ({agg_type})...")
            
            # --- FIX: Ensure aggregation column isn't float16 either ---
            if df[col].dtype == 'float16':
                 df[col] = df[col].astype('float32')

            temp_df = df.groupby([uid_col])[col].transform(agg_type)
            df[new_col_name] = temp_df
            
            del temp_df
            gc.collect()
    return df

def perform_feature_engineering():
    print("STEP 2: FEATURE ENGINEERING (FIXED)")

    print("\nLoading merged data from Pickle files...")
    train = pd.read_pickle('train_merged.pkl')
    test = pd.read_pickle('test_merged.pkl')
    
    len_train = len(train)
    df = pd.concat([train, test], axis=0, ignore_index=True)
    
    del train, test
    gc.collect()
    
    print("\nCreating User IDs (UIDs)...")
    
    # 1. Convert TransactionDT (seconds) to Days
    df['day'] = df['TransactionDT'] / (24*60*60)
    
    # 2. Calculate the "Start Date" (The day this user first appeared)
    # D1 is "Days since client began". TransactionDay - D1 = StartDay.
    # Check D1 type first
    if df['D1'].dtype == 'float16':
        df['D1'] = df['D1'].astype('float32')
        
    df['uid_D1n'] = df['day'] - df['D1']
    
    # 3. Construct the UID String
    df['uid'] = (df['card1'].astype(str) + '_' + 
                 df['addr1'].astype(str) + '_' + 
                 df['uid_D1n'].astype(str))
    
    print(f"   -> Created {df['uid'].nunique()} unique User IDs.")

    print("\nCalculating Aggregations (Mean/Std) per UID...")
    
    agg_columns = ['TransactionAmt', 'C1', 'C2', 'D1', 'D15']
    
    df = aggregate_features(df, 'uid', agg_columns, aggs=['mean', 'std'])

    print("\nPerforming Frequency Encoding...")
    
    encode_cols = ['card1', 'addr1', 'P_emaildomain', 'R_emaildomain', 'dist1']
    
    df = frequency_encoding(df, encode_cols)

    print("\nSplitting Email Domains...")
    for col in ['P_emaildomain', 'R_emaildomain']:
        df[col] = df[col].astype(str)
        df[col + '_prefix'] = df[col].apply(lambda x: x.split('.')[0] if '.' in x else x)

    print("\nCreating Hour of Day features...")
    df['Transaction_hour'] = np.floor((df['TransactionDT'] % 86400) / 3600)

    print("\nSplitting back to Train/Test and Saving...")
    
    train_eng = df.iloc[:len_train].copy()
    test_eng = df.iloc[len_train:].copy()
    
    del df
    gc.collect()
    
    train_eng.to_pickle('train_engineered.pkl')
    test_eng.to_pickle('test_engineered.pkl')

    print("SUCCESS: Feature Engineering Complete!")

if __name__ == "__main__":
    perform_feature_engineering()