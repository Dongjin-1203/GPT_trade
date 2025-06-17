import pandas as pd
import xgboost as xgb
import os

def predict_xgboost(train_df, test_df, store_id, dept_id, save_dir="model/XGBoost"):
    os.makedirs(save_dir, exist_ok=True)

    exog_vars = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'IsHoliday_x', 'IsHoliday_y']
    train = train_df[(train_df['Store'] == store_id) & (train_df['Dept'] == dept_id)]
    test = test_df[(test_df['Store'] == store_id) & (test_df['Dept'] == dept_id)]

    X_train = train[exog_vars]
    y_train = train['Weekly_Sales']
    X_test = test[exog_vars]

    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    result = test[['Date']].copy()
    result['Forecast'] = y_pred
    result.to_csv(f"{save_dir}/XGBoost_Store{store_id}_Dept{dept_id}_test.csv", index=False)
    return result
