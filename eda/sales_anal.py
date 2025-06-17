import pandas as pd
import matplotlib.pyplot as plt
import os

class sales_analyze:

    def analyzed_Store(train_final_data):
        # 데이터 준비
        df = train_final_data
        df['Date'] = pd.to_datetime(df['Date'])

        # 매장별 주간 매출 합계 산출
        weekly_store_sales = df.groupby(['Store', 'Date'])['Weekly_Sales'].sum().reset_index()

        # 시각화
        store_ids = df['Store'].unique()

        img_path = "img/store_plots"
        os.makedirs(img_path, exist_ok=True)

        for store_id in store_ids:
            store = weekly_store_sales[weekly_store_sales['Store'] == store_id]
            plt.figure(figsize=(12, 5))
            plt.plot(store['Date'], store['Weekly_Sales'])
            plt.title(f"Store {store_id} - Weekly Sales Trend")
            plt.xlabel("Date")
            plt.ylabel("Weekly Sales")
            plt.grid(True)
            plt.tight_layout()

            # 저장
            save_path = os.path.join(img_path, f"store_{store_id}.png")
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()  # 메모리 누수 방지

        print(f"[✓] 모든 매장 그래프 저장 완료 (경로: {img_path})")
        
    def plot_all_stores(train_final_data, store_ids=None):

        df = train_final_data.copy()
        df['Date'] = pd.to_datetime(df['Date'])

        # 주간 매출 집계
        weekly_sales = df.groupby(['Store', 'Date'])['Weekly_Sales'].sum().reset_index()

        # 시각화할 매장 지정 (없으면 전체)
        if store_ids is None:
            store_ids = weekly_sales['Store'].unique()

        plt.figure(figsize=(15, 6))

        # 각 매장 선 추가
        for store_id in store_ids:
            store = weekly_sales[weekly_sales['Store'] == store_id]
            plt.plot(store['Date'], store['Weekly_Sales'], label=f"Store {store_id}")

        plt.title("Weekly Sales Trend - Multiple Stores")
        plt.xlabel("Date")
        plt.ylabel("Weekly Sales")
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fontsize=8)
        plt.grid(True)
        plt.tight_layout()
        
        # 저장
        plt.savefig("img/all_stores_trend.png", dpi=300, bbox_inches='tight')
        plt.show()

    def analyzed_Dept(train_final_data):
        # 데이터 준비
        df = train_final_data
        df['Date'] = pd.to_datetime(df['Date'])

        # 매장별 주간 매출 합계 산출
        weekly_Dept_sales = df.groupby(['Dept', 'Date'])['Weekly_Sales'].sum().reset_index()

        # 시각화
        dept_ids = df['Dept'].unique()

        img_path = "img/dept_plots"
        os.makedirs(img_path, exist_ok=True)

        for dept_id in dept_ids:
            dept = weekly_Dept_sales[weekly_Dept_sales['Dept'] == dept_id]
            plt.figure(figsize=(12, 5))
            plt.plot(dept['Date'], dept['Weekly_Sales'])
            plt.title(f"Dept {dept_id} - Weekly Sales Trend")
            plt.xlabel("Date")
            plt.ylabel("Weekly Sales")
            plt.grid(True)
            plt.tight_layout()

            # 저장
            save_path = os.path.join(img_path, f"store_{dept_id}.png")
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()  # 메모리 누수 방지

        print(f"[✓] 모든 매장 그래프 저장 완료 (경로: {img_path})")

    def plot_all_deptes(train_final_data, dept_ids=None):

        df = train_final_data.copy()
        df['Date'] = pd.to_datetime(df['Date'])

        # 주간 매출 집계
        weekly_sales = df.groupby(['Dept', 'Date'])['Weekly_Sales'].sum().reset_index()

        # 시각화할 매장 지정 (없으면 전체)
        if dept_ids is None:
            dept_ids = weekly_sales['Dept'].unique()

        plt.figure(figsize=(15, 6))

        # 각 매장 선 추가
        for dept_id in dept_ids:
            dept = weekly_sales[weekly_sales['Dept'] == dept_id]
            plt.plot(dept['Date'], dept['Weekly_Sales'], label=f"Dept {dept_id}")

        plt.title("Weekly Sales Trend - Multiple Stores")
        plt.xlabel("Date")
        plt.ylabel("Weekly Sales")
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fontsize=8)
        plt.grid(True)
        plt.tight_layout()
        
        # 저장
        plt.savefig("img/all_depts_trend.png", dpi=300, bbox_inches='tight')
        plt.show()

    
    def analyzed_Store_Dept(train_final_data, top_n=5):
        df = train_final_data.copy()
        df['Date'] = pd.to_datetime(df['Date'])

        # 매장-부서별 주간 매출 집계
        weekly_sales = df.groupby(['Store', 'Dept', 'Date'])['Weekly_Sales'].sum().reset_index()

        # 상위 N개 Store-Dept 조합 추출 (전체 평균 기준)
        top_pairs = (
            weekly_sales.groupby(['Store', 'Dept'])['Weekly_Sales']
            .mean()
            .sort_values(ascending=False)
            .head(top_n)
            .index
        )

        # 시각화 폴더 생성
        img_path = "img/store_dept_trend"
        os.makedirs(img_path, exist_ok=True)

        # 상위 조합만 시각화
        for (store_id, dept_id) in top_pairs:
            subset = weekly_sales[(weekly_sales['Store'] == store_id) & (weekly_sales['Dept'] == dept_id)]

            plt.figure(figsize=(12, 5))
            plt.plot(subset['Date'], subset['Weekly_Sales'])
            plt.title(f"Store {store_id} - Dept {dept_id} Weekly Sales")
            plt.xlabel("Date")
            plt.ylabel("Weekly Sales")
            plt.grid(True)
            plt.tight_layout()

            filename = f"store_{store_id}_dept_{dept_id}.png"
            plt.savefig(os.path.join(img_path, filename), dpi=300)
            plt.close()

        print(f"[✓] 상위 {top_n} 매장-부서 조합 그래프 저장 완료! ({img_path})")