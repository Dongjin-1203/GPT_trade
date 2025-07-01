# ⏱️ Time Series Practice

월마트 매장 판매 데이터를 기반으로 다양한 시계열 모델을 학습하고 예측 성능을 비교하는 프로젝트입니다.  
ARIMA, SARIMAX부터 XGBoost, LightGBM 등 머신러닝 기반의 시계열 예측 모델까지 실험하며, 모델 성능을 평가하고 시각화합니다.

---

## 📌 목차
- [프로젝트 소개](#프로젝트-소개)
- [데이터셋](#데이터셋)
- [모델링 방법](#모델링-방법)
- [폴더 구조](#폴더-구조)
- [실행 방법](#실행-방법)
- [기술 스택](#기술-스택)
- [결과 예시](#결과-예시)
- [향후 계획](#향후-계획)

---

## 📖 프로젝트 소개

- Walmart Store Sales Forecasting 데이터를 활용한 시계열 예측 프로젝트입니다.
- 단일/다중 시계열 모델 성능 비교를 통해 **현실성 있는 예측 시스템 설계**를 목표로 합니다.
- 비정상성을 고려한 ARIMA/SARIMAX와 ML 기반 회귀 모델(XGBoost, LightGBM 등)을 함께 다룹니다.

---

## 📂 데이터셋

- 데이터 출처: [Walmart Store Sales Forecasting](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting)
- 주요 컬럼:
  - `Date`, `Weekly_Sales`, `Store`, `Dept`, `IsHoliday`
  - 외부 요인: `Temperature`, `Fuel_Price`, `CPI`, `Unemployment`

---

## 🔧 모델링 방법

| 모델 유형        | 내용 |
|------------------|------|
| **ARIMA**        | 단일 시계열 기반 기본 모델 |
| **SARIMAX**      | 외생 변수 포함 다중 시계열 모델 |
| **XGBoost**      | 시계열 특화 전처리 + ML 회귀 |
| **LightGBM**     | 시계열 데이터 회귀 실험 및 성능 비교 |
| **예측 대상**    | 특정 매장-부서의 `Weekly_Sales` 예측 |

---

## 🗂️ 폴더 구조

```bash
Time_series_Practice/
├── data/               # 원본 및 전처리된 데이터
├── model/              # ARIMA, SARIMAX, XGBoost 등 모델 구현
├── utils/              # 공통 함수 (평가지표, 시각화 등)
├── run.py              # 모델 실행 메인 파일
└── README.md           # 프로젝트 설명 문서
```

---

## 🚀 실행 방법
```bash
복사
편집
# 1. 프로젝트 클론
git clone https://github.com/Dongjin-1203/Time_series_Practice.git
cd Time_series_Practice

# 2. 가상환경 설정 및 라이브러리 설치
pip install -r requirements.txt

# 3. 모델 실행
python run.py
```

---

## 🛠️ 기술 스택
- 언어/환경: Python 3.10
- 라이브러리:
  - 시계열 모델링: statsmodels, pmdarima
  - 머신러닝: xgboost, lightgbm, scikit-learn
  - 데이터 처리: pandas, numpy
  - 시각화: matplotlib, seaborn

 ---

 ## 📊 결과 예시
 | 모델       | RMSE     | MAE      |
| -------- | -------- | -------- |
| ARIMA    | 12.45    | 9.23     |
| SARIMAX  | 10.78    | 8.02     |
| XGBoost  | 8.92     | 6.35     |
| LightGBM | **8.65** | **6.12** |

✅ LightGBM 모델이 가장 우수한 성능을 보였으며, 다변량 피처 추가가 성능 향상에 기여함을 확인했습니다.
