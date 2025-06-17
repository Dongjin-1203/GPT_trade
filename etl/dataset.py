import pandas as pd
import os
import glob

output_dir = "data/sorted_store"
dept_path = "data/sorted_store_dept"
os.makedirs(output_dir, exist_ok=True)  # 폴더 없으면 생성
os.makedirs(dept_path, exist_ok=True)

class dataset():
    # 매장 번호별 데이터 저장
    def seperate_store(data):

        store_nums = data['Store'].unique()

        for store_num in store_nums:
            store_data = data[data['Store'] == store_num]
            file_path = os.path.join(output_dir, f'store_{store_num}.csv')
            store_data.to_csv(file_path, index=False)
            print(f"{store_num}번 매장 데이터:\n", store_data)
        
        return
    # 매장내 코너 별 데이터 분리
    def seperate_dept():
        
        store = glob.glob(os.path.join(output_dir, "store_*.csv"))    # 특정 조건을 만족하는 데이터셋 불러오기
        for file in store:
            sorted_data = pd.read_csv(file)

            # store 번호 추출
            store_id = int(os.path.basename(file).split('_')[1].split('.')[0])

            dept_groups = sorted_data['Dept'].unique()

            for dept in dept_groups:
                dept_data = sorted_data[sorted_data['Dept'] == dept]

                result_path = f"data/sorted_store_dept/store_{store_id}"
                os.makedirs(result_path, exist_ok=True)  # 폴더 없으면 생성

                file_path = os.path.join(result_path, f'store_{store_id}_dept_{dept}.csv')
                dept_data.to_csv(file_path, index=False)
                print(f"{store_id}번 매장 {dept}번 코너 데이터:\n", dept_data)
        return
