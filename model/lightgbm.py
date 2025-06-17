import pandas as pd
import lightgbm as lgb
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error

class LightGBMForecast:
    def __init__(self, train_df: pd.DataFrame, test_df: pd.DataFrame, forecast_dir: str = "model/LightGBM"):
        self.train_df = train_df.copy()
        self.test_df = test_df.copy()
        self.forecast_dir = forecast_dir
        os.makedirs(self.forecast_dir, exist_ok=True)

        self.features = [
            'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'IsHoliday_x', 'IsHoliday_y',
            'Week', 'Month', 'Year', 'DayOfWeek'
        ]

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df['Week'] = df['Date'].dt.isocalendar().week.astype(int)
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        return df

    def train_and_predict(self):
        self.train_df = self.preprocess(self.train_df)
        self.test_df = self.preprocess(self.test_df)

        results = []

        for (store_id, dept_id), train_group in self.train_df.groupby(['Store', 'Dept']):
            test_group = self.test_df[
                (self.test_df['Store'] == store_id) &
                (self.test_df['Dept'] == dept_id)
            ]

            if test_group.empty or train_group.shape[0] < 60:
                print(f"Skipping Store {store_id}, Dept {dept_id} due to insufficient data.")
                continue

            X_train = train_group[self.features].fillna(method='ffill')
            y_train = train_group['Weekly_Sales']
            X_test = test_group[self.features].fillna(method='ffill')

            lgb_train = lgb.Dataset(X_train, label=y_train)
            params = {
                'objective': 'regression',
                'metric': 'rmse',
                'verbosity': -1,
                'boosting_type': 'gbdt',
                'learning_rate': 0.05,
                'num_leaves': 31,
                'seed': 42
            }

            model = lgb.train(params, lgb_train, num_boost_round=100)
            y_pred = model.predict(X_test)

            result = test_group[['Date']].copy()
            result['Forecast'] = y_pred
            result.to_csv(
                os.path.join(self.forecast_dir, f"LightGBM_Store{store_id}_Dept{dept_id}_test.csv"),
                index=False
            )

            print(f"✅ LightGBM 예측 완료: Store {store_id}, Dept {dept_id}")

            # 실제값이 존재한다면 평가 추가
            if 'Weekly_Sales' in test_group.columns:
                y_true = test_group['Weekly_Sales'][:len(y_pred)]
                rmse = mean_squared_error(y_true, y_pred, squared=False)
                mae = mean_absolute_error(y_true, y_pred)
                results.append({'Store': store_id, 'Dept': dept_id, 'RMSE': rmse, 'MAE': mae})

        return pd.DataFrame(results)
