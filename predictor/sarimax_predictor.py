from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
import pandas as pd
import os

def predict_sarimax(train_df, test_df, store_id, dept_id, save_dir="model/SARIMAX", steps=12):
    os.makedirs(save_dir, exist_ok=True)

    exog_vars = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'IsHoliday']
    train = train_df[(train_df['Store'] == store_id) & (train_df['Dept'] == dept_id)]
    test = test_df[(test_df['Store'] == store_id) & (test_df['Dept'] == dept_id)]

    ts = train.set_index('Date')['Weekly_Sales'].asfreq('W-MON').fillna(method='ffill')
    exog_train = train.set_index('Date')[exog_vars].asfreq('W-MON').fillna(method='ffill')
    exog_test = test.set_index('Date')[exog_vars].asfreq('W-MON').fillna(method='ffill')

    try:
        auto_model = auto_arima(ts, exogenous=exog_train, seasonal=True, m=52)
        order = auto_model.order
        seasonal_order = auto_model.seasonal_order

        model = SARIMAX(ts, exog=exog_train, order=order, seasonal_order=seasonal_order)
        model_fit = model.fit(disp=False)

        forecast = model_fit.forecast(steps=steps, exog=exog_test)
        forecast_df = forecast.reset_index(drop=True)
        forecast_df.to_csv(f"{save_dir}/SARIMAX_Store{store_id}_Dept{dept_id}_test.csv", index=False)
        return forecast_df
    except Exception as e:
        print(f"Error Store {store_id} Dept {dept_id}: {e}")
        return None
