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

class markdown:
    
    def __init__(self, train_final_data: pd.DataFrame):
        # 데이터 준비
        self.df = train_final_data.copy()
        self.df['Date'] = pd.to_datetime(self.df['Date'])

        # MarkDown 컬럼만 필터링
        self.markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']

        # MarkDown 결측치는 0으로 간주 (할인 없음)
        self.df[self.markdown_cols] = self.df[self.markdown_cols].fillna(0)


        os.makedirs("img/markdown_analysis", exist_ok=True)
        os.makedirs("img/markdown_analysis/type", exist_ok=True)
        os.makedirs("img/markdown_analysis/store", exist_ok=True)
        os.makedirs("img/markdown_analysis/dept", exist_ok=True)
        os.makedirs("img/markdown_analysis/size", exist_ok=True)

    def analyze_markdown(self):

        # 상관계수 분석
        correlations = self.df[self.markdown_cols + ['Weekly_Sales']].corr()
        print(correlations['Weekly_Sales'].sort_values(ascending=False))

        plt.figure(figsize=(8, 6))
        sns.heatmap(correlations, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title("MarkDown 변수와 매출의 상관관계")
        plt.tight_layout()
        plt.savefig("img/markdown_analysis/markdown_weekly_sales.png", dpi=300)
        plt.close()
        plt.show()

        for col in self.markdown_cols:
            plt.figure(figsize=(6, 4))
            sns.scatterplot(x=self.df[col], y=self.df['Weekly_Sales'])
            plt.title(f"{col} vs Weekly Sales")
            plt.xlabel(col)
            plt.ylabel("Weekly Sales")
            plt.tight_layout()
            plt.savefig(f"img/markdown_analysis/markdown_{col}_weekly_sales.png", dpi=300)
            plt.close()
            plt.show()

        top_md = correlations['Weekly_Sales'].abs().sort_values(ascending=False).index[1:3]  # 상위 2개
        print(f"상관계수 높은 할인 변수: {list(top_md)}")
    
    def analyze_markdown_by_type(self):
        # 타입 필터
        for store_type in self.df['Type'].unique():
            type_df = self.df[self.df['Type'] == store_type]

            # 상관계수 분석
            correlations = type_df[self.markdown_cols + ['Weekly_Sales']].corr()
            print(f"\n=== Type {store_type} ===")
            print(correlations['Weekly_Sales'].sort_values(ascending=False))

            # 히트맵 저장
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlations, annot=True, fmt=".2f", cmap='coolwarm')
            plt.title(f"MarkDown vs Weekly Sales - Type {store_type}")
            plt.tight_layout()
            plt.savefig(f"img/markdown_analysis/type/markdown_corr_type_{store_type}.png", dpi=300)
            plt.close()

    def analyze_markdown_by_store(self):
        # 타입 필터
        for store_id in self.df['Store'].unique():
            store_df = self.df[self.df['Store'] == store_id]

            # 상관계수 분석
            correlations = store_df[self.markdown_cols + ['Weekly_Sales']].corr()
            print(f"\n=== Store {store_id} ===")
            print(correlations['Weekly_Sales'].sort_values(ascending=False))

            # 히트맵 저장
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlations, annot=True, fmt=".2f", cmap='coolwarm')
            plt.title(f"MarkDown vs Weekly Sales - Store {store_id}")
            plt.tight_layout()
            plt.savefig(f"img/markdown_analysis/store/markdown_corr_Store_{store_id}.png", dpi=300)
            plt.close()

    def analyze_markdown_by_dept(self):
        # 타입 필터
        for store_dept in self.df['Dept'].unique():
            dept_df = self.df[self.df['Dept'] == store_dept]

            # 상관계수 분석
            correlations = dept_df[self.markdown_cols + ['Weekly_Sales']].corr()
            print(f"\n=== Dept {store_dept} ===")
            print(correlations['Weekly_Sales'].sort_values(ascending=False))

            # 히트맵 저장
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlations, annot=True, fmt=".2f", cmap='coolwarm')
            plt.title(f"MarkDown vs Weekly Sales - Dept {store_dept}")
            plt.tight_layout()
            plt.savefig(f"img/markdown_analysis/dept/markdown_corr_Dept_{store_dept}.png", dpi=300)
            plt.close()

    def analyze_markdown_by_size(self):
        # 타입 필터
        for store_size in self.df['Size'].unique():
            size_df = self.df[self.df['Size'] == store_size]

            # 상관계수 분석
            correlations = size_df[self.markdown_cols + ['Weekly_Sales']].corr()
            print(f"\n=== Size {store_size} ===")
            print(correlations['Weekly_Sales'].sort_values(ascending=False))

            # 히트맵 저장
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlations, annot=True, fmt=".2f", cmap='coolwarm')
            plt.title(f"MarkDown vs Weekly Sales - Size {store_size}")
            plt.tight_layout()
            plt.savefig(f"img/markdown_analysis/size/markdown_corr_Size_{store_size}.png", dpi=300)
            plt.close()