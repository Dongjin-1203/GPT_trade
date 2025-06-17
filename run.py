import pandas as pd

from etl.test_dataset import test_dataset
from etl.train_dataset import train_dataset
from feature_engineering.Concat import Concat
from eda.sales_anal import sales_analyze
from eda.type_size import type_size
from eda.markdown import markdown

if __name__ == "__main__":
    print("모듈을 성공적으로 불러왔습니다.")
    
    eda = input("전처리부터 시작 하시겠습니까?(y/n) :")
    if eda == 'y' or eda == 'Y' or eda == 'ㅛ':
        # 데이터 불러오기
        train_path = 'data/train.csv'
        train_data = pd.read_csv(train_path)
        test_path = 'data/test.csv'
        test_data = pd.read_csv(test_path)

        # 데이터 확인(주석처리 가능)
        """
        print(data.head())
        print(data.info())

        print(data['Store'].value_counts)   # 매장 번호 확인 코드

        """

        # 특성 합치기
        Concat.feature_plus_store()
        # 분석용 데이터셋 작성
        Concat.concat_data(train_data, test_data)

        train_final_path = 'data/train_final.csv'
        train_final_data = pd.read_csv(train_final_path)
        test_final_path = 'data/test_final.csv'
        test_final_data = pd.read_csv(test_final_path)
        
        # 매장별 데이터 분리
        train_dataset.seperate_store(train_final_data)
        test_dataset.seperate_store(test_final_data)
        # 코너별 데이터 분리
        train_dataset.seperate_dept(train_final_data)
        test_dataset.seperate_dept(test_final_data)
        # 매장 내 코너별 데이터 분리
        train_dataset.seperate_store_dept()
        test_dataset.seperate_store_dept()

    elif eda == 'n' or eda == 'N' or eda == 'ㅜ':
        print("분석/예측을 시작하겠습니다.")

        train_final_path = 'data/train_final.csv'
        train_final_data = pd.read_csv(train_final_path)
        test_final_path = 'data/test_final.csv'
        test_final_data = pd.read_csv(test_final_path)

        # 전체 매장 개별 분석
        #sales_analyze.analyzed_Store(train_final_data)
        # 한개 그래프로 통합(전체 매장에 대해서: store_ids=None, 특정 매장에 대해서: store_ids=[1, 2, 3])
        #sales_analyze.plot_all_stores(train_final_data, store_ids=None)
        # 전체 코너 개별 분석
        #sales_analyze.analyzed_Dept(train_final_data)
        # 한개 그래프로 통합(전체 코너에 대해서: dept_ids=None, 특정 코너에 대해서: dept_ids=[1, 2, 3])
        #sales_analyze.plot_all_deptes(train_final_data, dept_ids=None)
        # 코너별, 매장별 매출 분석(경우의수가 약 3600개 이상인 관계로 상위 데이터만 확인)
        #sales_analyze.analyzed_Store_Dept(train_final_data, top_n=5)

        # Type, Size vs Weekly_Sales
        type_size = type_size(train_final_data)

        type_size.analyze_by_type()
        type_size.analyze_by_size()
        type_size.boxplot_by_type()
        type_size.summarize()

        # MarkDown Correlations
        markdown = markdown(train_final_data)

        markdown.analyze_markdown()
        markdown.analyze_markdown_by_type()
        markdown.analyze_markdown_by_dept()
        markdown.analyze_markdown_by_size()
        markdown.analyze_markdown_by_store()
    
    else:
        print("올바른 값을 입력하세요. ")