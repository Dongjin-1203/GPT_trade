import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os
import platform


# 운영체제별 폰트 경로 설정
if platform.system() == 'Windows':
    font_path = 'C:/Windows/Fonts/malgun.ttf'  # 맑은 고딕

# 폰트 적용
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

class type_size:
    
    def __init__(self, train_final_data: pd.DataFrame):
        # 데이터 준비
        self.df = train_final_data.copy()
        self.df['Date'] = pd.to_datetime(self.df['Date'])

        # 매장 메타정보 불러오기
        self.store_info = self.df[['Store', 'Type', 'Size']].drop_duplicates()

        os.makedirs("img/store_analysis", exist_ok=True)

    def analyze_by_type(self):
        type_weekly = self.df.groupby(['Date', 'Type'])['Weekly_Sales'].sum().reset_index()

        plt.figure(figsize=(12,6))
        sns.lineplot(data=type_weekly, x='Date', y='Weekly_Sales', hue='Type')
        plt.title("매장 타입별 주간 매출 추세")
        plt.xlabel("Date")
        plt.ylabel("Weekly Sales")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("img/store_analysis/type_weekly_trend.png", dpi=300)
        plt.close()

    def analyze_by_size(self):
        store_sales = self.df.groupby('Store')['Weekly_Sales'].sum().reset_index()
        store_sales = store_sales.merge(self.store_info, on='Store', how='left')

        plt.figure(figsize=(10,6))
        sns.scatterplot(data=store_sales, x='Size', y='Weekly_Sales', hue='Type')
        plt.title("매장 크기 vs. 총 매출")
        plt.xlabel("Store Size")
        plt.ylabel("Total Sales")
        plt.tight_layout()
        plt.savefig("img/store_analysis/size_vs_sales.png", dpi=300)
        plt.close()

        corr = store_sales[['Size', 'Weekly_Sales']].corr().iloc[0,1]
        print(f"[✓] 매장 크기와 총 매출 상관계수: {corr:.3f}")

    def boxplot_by_type(self):
        store_sales = self.df.groupby('Store')['Weekly_Sales'].sum().reset_index()
        store_sales = store_sales.merge(self.store_info, on='Store', how='left')

        plt.figure(figsize=(10,6))
        sns.boxplot(data=store_sales, x='Type', y='Weekly_Sales')
        plt.title("매장 타입별 총 매출 분포")
        plt.xlabel("Store Type")
        plt.ylabel("Total Sales")
        plt.tight_layout()
        plt.savefig("img/store_analysis/type_boxplot.png", dpi=300)
        plt.close()

    def summarize(self):
        print("[📊] 매장 수 (타입별):")
        print(self.store_info['Type'].value_counts())
        print("\n[📐] 매장 크기 통계:")
        print(self.store_info['Size'].describe())