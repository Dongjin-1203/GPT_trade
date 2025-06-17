import pandas as pd
import os

class Concat:

    def feature_plus_store():
        features_path = "data/features.csv"
        features = pd.read_csv(features_path)

        stores_path = "data/stores.csv"
        stores = pd.read_csv(stores_path)

        features_full = features.merge(stores, on='Store', how="left")
        save_path = 'data/feature_plus_store.csv'
        features_full.to_csv(save_path, index=False)
        return
    
    def concat_data(train_data, test_data):
        features_full_path = 'data/feature_plus_store.csv'
        features_full_data = pd.read_csv(features_full_path)

        train_data['Date'] = pd.to_datetime(train_data['Date'])
        test_data['Date'] = pd.to_datetime(test_data['Date'])
        features_full_data['Date'] = pd.to_datetime(features_full_data['Date'])

        train_data = train_data.merge(features_full_data, on=['Store', 'Date'], how="left")
        train_final_path = 'data/train_final.csv'
        train_data.to_csv(train_final_path, index=False)

        test_data = test_data.merge(features_full_data, on=['Store', 'Date'], how="left")
        test_final_path = 'data/test_final.csv'
        test_data.to_csv(test_final_path, index=False)
        return