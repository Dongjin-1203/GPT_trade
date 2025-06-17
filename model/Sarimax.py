import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error
import numpy as np
import os
from statsmodels.tsa.statespace.sarimax import SARIMAX

# 경고 무시
import warnings
warnings.filterwarnings("ignore")

os.makedirs("model/SARIMAX", exist_ok=True)

class multivar:
    def __init__(self, train_final_data: pd.DataFrame, forecast_steps: int = 12):
        self.data = train_final_data.copy()
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.forecast_steps = forecast_steps

    def sarimax(self):
        grouped = self.data.groupby(['Store', 'Dept'])

        for (store_id, dept_id), group in grouped:
            if group.shape[0] < 50:
                print(f"Skipping Store {store_id}, Dept {dept_id} due to insufficient data.")
                continue

            ts = group.set_index('Date')['Weekly_Sales'].asfreq('W-MON').fillna(method='ffill')

            exog_vars = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'IsHoliday']
            if not all(var in group.columns for var in exog_vars):
                print(f"Skipping Store {store_id}, Dept {dept_id} due to missing exogenous variables.")
                continue

            exog = group.set_index('Date')[exog_vars].asfreq('W-MON').fillna(method='ffill')

            try:
                auto_model = auto_arima(
                    ts,
                    exogenous=exog,
                    seasonal=True,
                    m=52,
                    stepwise=True,
                    suppress_warnings=True,
                    error_action='ignore'
                )

                order = auto_model.order
                seasonal_order = auto_model.seasonal_order

                model = SARIMAX(ts, exog=exog, order=order, seasonal_order=seasonal_order)
                model_fit = model.fit(disp=False)

                future_exog = exog.iloc[-self.forecast_steps:]
                forecast = model_fit.forecast(steps=self.forecast_steps, exog=future_exog)
                forecast_index = pd.date_range(start=ts.index[-1] + pd.Timedelta(weeks=1), 
                                            periods=self.forecast_steps, freq='W-MON')

                forecast_series = pd.Series(forecast, index=forecast_index)

                # Save plot
                plt.figure(figsize=(10, 5))
                ts.plot(label='Observed')
                forecast_series.plot(label='Forecast', linestyle='--')
                plt.title(f"SARIMAX Forecast: Store {store_id}, Dept {dept_id}")
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.savefig(f"model/SARIMAX/SARIMAX_Store{store_id}_Dept{dept_id}.png", dpi=300)
                plt.close()

                # Save CSV
                forecast_series.to_csv(
                    f"model/SARIMAX//SARIMAX_Store{store_id}_Dept{dept_id}.csv",
                    index=True,
                    header=['Forecast']
                )

                print(f"Finished Store {store_id}, Dept {dept_id}")

            except Exception as e:
                print(f"Error in Store {store_id}, Dept {dept_id}: {e}")