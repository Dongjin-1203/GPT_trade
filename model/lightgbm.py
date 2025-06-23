import pandas as pd
import lightgbm as lgb
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class LightGBMForecast:
    def __init__(self, train_df: pd.DataFrame, test_df: pd.DataFrame, forecast_dir: str = "model/LightGBM"):
        self.train_df = train_df.copy()
        self.test_df = test_df.copy()
        self.forecast_dir = forecast_dir
        os.makedirs(self.forecast_dir, exist_ok=True)

        self.features = [
            'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'IsHoliday_x', 'IsHoliday_y'
        ]

    def lightgbm(self):
        results = []

        for (store_id, dept_id), train_group in self.train_df.groupby(['Store', 'Dept']):
            test_group = self.test_df[
                (self.test_df['Store'] == store_id) &
                (self.test_df['Dept'] == dept_id)
            ]

            if test_group.empty or train_group.shape[0] < 60:
                print(f"Skipping Store {store_id}, Dept {dept_id} due to insufficient data.")
                continue

            X_train = train_group[self.features]
            y_train = train_group['Weekly_Sales']
            X_test = test_group[self.features]

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

            """
            # 실제값이 존재한다면 평가 추가
            if 'Weekly_Sales' in test_group.columns:
                y_true = test_group['Weekly_Sales'][:len(y_pred)]
                rmse = mean_squared_error(y_true, y_pred, squared=False)
                mae = mean_absolute_error(y_true, y_pred)
                results.append({'Store': store_id, 'Dept': dept_id, 'RMSE': rmse, 'MAE': mae})
            """
            
            # 시각화 추가
            plt.figure(figsize=(10, 4))
            #plt.plot(test_group['Date'], y_true, label='Actual')
            plt.plot(pd.to_datetime(test_group['Date']), y_pred, label='Forecast', linestyle='--')

            # x축 날짜 포맷 지정 및 회전
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)

            plt.title(f"LightGBM Forecast: Store {store_id}, Dept {dept_id}")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"{self.forecast_dir}/GBM_Store{store_id}_Dept{dept_id}.png", dpi=300)
            plt.close()

            result.to_csv(
                os.path.join(self.forecast_dir, f"LightGBM_Store{store_id}_Dept{dept_id}_test.csv"),
                index=False
            )

            print(f"✅ LightGBM 예측 완료: Store {store_id}, Dept {dept_id}")

        return pd.DataFrame(results)
