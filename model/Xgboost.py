import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import os
import matplotlib.pyplot as plt

class XGBoostForecast:
    def __init__(self, train_final_data: pd.DataFrame, forecast_lags: int = 3):
        self.df = train_final_data.copy()
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.lags = forecast_lags
        os.makedirs("model/XGBoost", exist_ok=True)

    def create_features(self, df):
        df = df.copy()
        df = df.sort_values('Date')

        # 날짜 기반 특징 생성
        df['Week'] = df['Date'].dt.isocalendar().week
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['DayOfWeek'] = df['Date'].dt.dayofweek

        # 시차 특성 (lag features)
        for lag in range(1, self.lags + 1):
            df[f'lag_{lag}'] = df['Weekly_Sales'].shift(lag)

        df = df.dropna()
        return df

    def train_predict(self):
        for (store_id, dept_id), group in self.df.groupby(['Store', 'Dept']):
            if group.shape[0] < 50:
                print(f"Skipping Store {store_id}, Dept {dept_id} due to insufficient data")
                continue

            data = self.create_features(group)

            X = data[['Week', 'Month', 'Year', 'DayOfWeek'] + [f'lag_{i}' for i in range(1, self.lags + 1)] +
                     ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'IsHoliday_x', 'IsHoliday_y']]
            y = data['Weekly_Sales']

            try:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

                model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1)
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)

                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                print(f"Store {store_id}, Dept {dept_id} - RMSE: {rmse:.2f}")

                # 결과 저장
                plt.figure(figsize=(10, 4))
                plt.plot(y_test.values, label='Actual')
                plt.plot(y_pred, label='Forecast', linestyle='--')
                plt.title(f"XGBoost Forecast: Store {store_id}, Dept {dept_id}")
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.savefig(f"model/XGBoost/XGB_Store{store_id}_Dept{dept_id}.png", dpi=300)
                plt.close()

            except Exception as e:
                print(f"Error on Store {store_id}, Dept {dept_id}: {e}")
