import pandas as pd

from etl.test_dataset import test_dataset
from etl.train_dataset import train_dataset
from feature_engineering.Concat import Concat
from eda.sales_analyze import sales_analyze
from eda.type_size import type_size
from eda.markdown import markdown
from model.arima import Time_series
from model.Sarimax import multivar
from model.Xgboost import XGBoostForecast
from model.lightgbm import LightGBMForecast
from evaluation.rmse_mea import MultiModelEvaluator
from predictor.xgboost_predictor import predict_xgboost
from predictor.sarimax_predictor import predict_sarimax
from predictor.lightgbm_predictor import predict_lightgbm

def load_final_data():
    train_final_data = pd.read_csv('data/train_final.csv')
    test_final_data = pd.read_csv('data/test_final.csv')
    return train_final_data, test_final_data

def run_preprocessing():
    train_data = pd.read_csv('data/train.csv')
    test_data = pd.read_csv('data/test.csv')
    Concat.feature_plus_store()
    Concat.concat_data(train_data, test_data)
    train_dataset.seperate_store(train_data)
    test_dataset.seperate_store(test_data)
    train_dataset.seperate_dept(train_data)
    test_dataset.seperate_dept(test_data)
    train_dataset.seperate_store_dept()
    test_dataset.seperate_store_dept()

def run_eda(train_final_data):
    sales_analyze.analyzed_Store(train_final_data)
    sales_analyze.plot_all_stores(train_final_data)
    sales_analyze.analyzed_Dept(train_final_data)
    sales_analyze.plot_all_deptes(train_final_data)
    sales_analyze.analyzed_Store_Dept(train_final_data, top_n=5)

    ts = type_size(train_final_data)
    ts.analyze_by_type()
    ts.analyze_by_size()
    ts.boxplot_by_type()
    ts.summarize()

    md = markdown(train_final_data)
    md.analyze_markdown()
    md.analyze_markdown_by_type()
    md.analyze_markdown_by_dept()
    md.analyze_markdown_by_size()
    md.analyze_markdown_by_store()

def run_modeling(train_final_data, test_final_data):
    Time_series(train_final_data).arima()
    Time_series(train_final_data).sarima()
    multivar(train_final_data).sarimax()
    XGBoostForecast(train_final_data).train_predict()
    LightGBMForecast(train_df=train_final_data, test_df=test_final_data).train_and_predict()

def run_evaluation(train_final_data):
    model_dirs = {
        'ARIMA': 'model/(Auto)ARIMA',
        'SARIMA': 'model/SARIMA',
        'XGBoost': 'model/XGBoost',
        'LightGBM': 'model/LightGBM'
    }
    evaluator = MultiModelEvaluator(train_final_data, model_dirs)
    result_df = evaluator.evaluate_models()
    result_df.to_csv("model/all_model_evaluation.csv", index=False)
    print(result_df.sort_values(by="RMSE").head(10))

def run_forecasting(train_final_data, test_final_data):
    for store in train_final_data['Store'].unique():
        for dept in train_final_data[train_final_data['Store'] == store]['Dept'].unique():
            predict_xgboost(train_final_data, test_final_data, store, dept)
            predict_sarimax(train_final_data, test_final_data, store, dept)
            predict_lightgbm(train_final_data, test_final_data, store, dept)

if __name__ == "__main__":
    print("모듈을 성공적으로 불러왔습니다.")

    mode = input("실행 모드 선택: preprocess / eda / model / evaluate / forecast : ").strip().lower()

    if mode == 'preprocess':
        run_preprocessing()

    train_final_data, test_final_data = load_final_data()

    if mode == 'eda':
        run_eda(train_final_data)

    elif mode == 'model':
        run_modeling(train_final_data, test_final_data)

    elif mode == 'evaluate':
        run_evaluation(train_final_data)

    elif mode == 'forecast':
        run_forecasting(train_final_data, test_final_data)

    else:
        print("올바른 모드를 선택해주세요.")
