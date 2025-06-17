import pandas as pd

from etl.dataset import dataset

if __name__ == "__main__":
    print("모듈을 성공적으로 불러왔습니다.")
    # 데이터 불러오기
    path = 'data/train.csv'
    data = pd.read_csv(path)

    # 데이터 확인(주석처리 가능)
    """
    print(data.head())
    print(data.info())

    print(data['Store'].value_counts)   # 매장 번호 확인 코드

    """
    # 매장별 데이터 분리
    dataset.seperate_store(data)
    # 코너별 데이터 분리
    dataset.seperate_dept(data)
    # 매장 내 코너별 데이터 분리
    dataset.seperate_store_dept()