import pandas as pd
import os
import glob

output_dir1 = "data/train/sorted_store"
output_dir2 = "data/train/sorted_dept"
dept_path = "data/train/sorted_store_dept"
os.makedirs(output_dir1, exist_ok=True)  # 폴더 없으면 생성
os.makedirs(output_dir2, exist_ok=True)
os.makedirs(dept_path, exist_ok=True)

class train_dataset():
    # 매장 번호별 데이터 저장
    def seperate_store(data):

        store_nums = data['Store'].unique()

        for store_num in store_nums:
            store_data = data[data['Store'] == store_num]
            file_path = os.path.join(output_dir1, f'store_{store_num}.csv')
            store_data.to_csv(file_path, index=False)
            print(f"{store_num}번 매장 데이터:\n", store_data)
        
        return
    
    # 코너 번호별 데이터 저장
    def seperate_dept(data):

        dept_nums = data['Dept'].unique()

        for dept_num in dept_nums:
            dept_data = data[data['Dept'] == dept_num]
            file_path = os.path.join(output_dir2, f'dept_{dept_num}.csv')
            dept_data.to_csv(file_path, index=False)
            print(f"{dept_num}번 코너 데이터:\n", dept_data)
        
        return
    # 매장내 코너 별 데이터 분리
    def seperate_store_dept():
        
        store = glob.glob(os.path.join(output_dir1, "store_*.csv"))    # 특정 조건을 만족하는 데이터셋 불러오기
        for file in store:
            sorted_data = pd.read_csv(file)

            # store 번호 추출
            store_id = int(os.path.basename(file).split('_')[1].split('.')[0])

            dept_groups = sorted_data['Dept'].unique()

            for dept in dept_groups:
                dept_store_data = sorted_data[sorted_data['Dept'] == dept]

                result_path = f"data/train/sorted_store_dept/store_{store_id}"
                os.makedirs(result_path, exist_ok=True)  # 폴더 없으면 생성

                file_path = os.path.join(result_path, f'store_{store_id}_dept_{dept}.csv')
                dept_store_data.to_csv(file_path, index=False)
                print(f"{store_id}번 매장 {dept}번 코너 데이터:\n", dept_store_data)
        return
