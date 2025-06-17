import pandas as pd

import os

output_dir = "data/sorted_store"
os.makedirs(output_dir, exist_ok=True)  # 폴더 없으면 생성

class dataset():
    
    def seperate_store(data):

        store_nums = data['Store'].unique()

        for store_num in store_nums:
            store_data = data[data['Store'] == store_num]
            file_path = os.path.join(output_dir, f'store_{store_num}.csv')
            store_data.to_csv(file_path, index=False)
            print(f"{store_num}번 매장 데이터:\n", store_data)
        
        return