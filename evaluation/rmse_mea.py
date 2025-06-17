import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

class MultiModelEvaluator:
    def __init__(self, ground_truth_df: pd.DataFrame, model_dirs: dict, forecast_steps: int = 12):
        """
        model_dirs: {'ARIMA': 'model/(Auto)ARIMA', 'SARIMA': 'model/SARIMA', ...}
        """
        self.ground_truth_df = ground_truth_df.copy()
        self.ground_truth_df['Date'] = pd.to_datetime(self.ground_truth_df['Date'])
        self.model_dirs = model_dirs
        self.forecast_steps = forecast_steps

    def evaluate_models(self):
        all_results = []

        for model_name, forecast_dir in self.model_dirs.items():
            print(f"Evaluating model: {model_name}")

            for file in os.listdir(forecast_dir):
                if not file.endswith(".csv"):
                    continue

                try:
                    path = os.path.join(forecast_dir, file)
                    forecast_df = pd.read_csv(path, index_col=0)
                    forecast_df.index = pd.to_datetime(forecast_df.index)
                    forecast_df.columns = ['Forecast']

                    # 파일명에서 store, dept 추출
                    parts = file.replace('.csv', '').split('_')
                    store_id = int([s for s in parts if 'Store' in s][0].replace("Store", ""))
                    dept_id = int([s for s in parts if 'Dept' in s][0].replace("Dept", ""))

                    actual_df = self.ground_truth_df[
                        (self.ground_truth_df['Store'] == store_id) &
                        (self.ground_truth_df['Dept'] == dept_id)
                    ].set_index('Date')

                    actual_series = actual_df['Weekly_Sales'].asfreq('W-MON').iloc[-self.forecast_steps:]

                    # 날짜 일치하는 것만 평가
                    forecast_series = forecast_df['Forecast']
                    common_dates = actual_series.index.intersection(forecast_series.index)

                    if len(common_dates) == 0:
                        continue

                    actual = actual_series.loc[common_dates]
                    predicted = forecast_series.loc[common_dates]

                    rmse = np.sqrt(mean_squared_error(actual, predicted))
                    mae = mean_absolute_error(actual, predicted)

                    all_results.append({
                        'Model': model_name,
                        'Store': store_id,
                        'Dept': dept_id,
                        'RMSE': rmse,
                        'MAE': mae
                    })

                except Exception as e:
                    print(f"Error in {model_name} file {file}: {e}")

        return pd.DataFrame(all_results)
