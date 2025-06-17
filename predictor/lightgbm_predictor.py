import pandas as pd
import lightgbm as lgb
import os

def predict_lightgbm(train_df, test_df, store_id, dept_id, save_dir="model/LightGBM"):
    os.makedirs(save_dir, exist_ok=True)

    features = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'IsHoliday',
                'Week', 'Month', 'Year', 'DayOfWeek']
    
    train = train_df[(train_df['Store'] == store_id) & (train_df['Dept'] == dept_id)]
    test = test_df[(test_df['Store'] == store_id) & (test_df['Dept'] == dept_id)]

    # 결측값 처리
    train = train.fillna(method='ffill')
    test = test.fillna(method='ffill')

    # 라벨 및 특성
    X_train = train[features]
    y_train = train['Weekly_Sales']
    X_test = test[features]

    # LightGBM Dataset 객체로 변환
    lgb_train = lgb.Dataset(X_train, label=y_train)

    # 파라미터 설정
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'learning_rate': 0.05,
        'num_leaves': 31,
        'seed': 42
    }

    # 모델 학습
    model = lgb.train(params, lgb_train, num_boost_round=100)

    # 예측
    y_pred = model.predict(X_test)

    # 저장
    result = test[['Date']].copy()
    result['Forecast'] = y_pred
    result.to_csv(f"{save_dir}/LightGBM_Store{store_id}_Dept{dept_id}_test.csv", index=False)

    print(f"✅ LightGBM 예측 완료: Store {store_id}, Dept {dept_id}")
    return result
