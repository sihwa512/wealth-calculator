import streamlit as st
import pandas as pd

def calculate_wealth_history(initial_capital, monthly_investment, annual_rate, years):
    """
    逐年計算累積本金與投資獲利，用來繪製圖表
    """
    data = []
    current_principal = initial_capital
    current_total = initial_capital
    monthly_rate = annual_rate / 12
    
    # 紀錄第 0 年 (初始狀態)
    data.append({
        "年份": 0,
        "累積本金": current_principal,
        "投資獲利": 0
    })
    
    # 逐年計算
    for year in range(1, years + 1):
        for month in range(12):
            # 每月投入本金
            current_principal += monthly_investment
            # 計算當月總資產 (本月期初資產 + 本月投入) * 月報酬
            current_total = (current_total + monthly_investment) * (1 + monthly_rate)
            
        profit = current_total - current_principal
        
        # 紀錄每年年底的狀態
        data.append({
            "年份": year,
            "累積本金": round(current_principal),
            "投資獲利": round(profit)
        })
        
    return pd.DataFrame(data)

# --- 網頁介面設計開始 ---
st.title("📈 資產複利與定期定額計算機")
st.write("輸入您的資金狀況，看看經過時間的複利，未來能累積多少資產！")

# 建立輸入區塊
st.subheader("請輸入您的資訊：")
col1, col2 = st.columns(2)

with col1:
    initial_capital = st.number_input("目前的金錢部位 (元)", min_value=0, value=1000000, step=10000)
    monthly_investment = st.number_input("每月可投入金額 (元)", min_value=0, value=30000, step=1000)

with col2:
    annual_rate_percent = st.number_input("預期年化報酬率 (%)", value=6.5, step=0.1)
    years = st.number_input("投資年限 (年)", min_value=1, value=20, step=1)

# 按下按鈕後進行計算與繪圖
if st.button("開始計算"):
    annual_rate = annual_rate_percent / 100
    
    # 取得逐年數據表
    df = calculate_wealth_history(initial_capital, monthly_investment, annual_rate, years)
    
    # 取得最後一年的最終數據來顯示大數字
    final_data = df.iloc[-1]
    total_invested = final_data["累積本金"]
    profit = final_data["投資獲利"]
    total_future_value = total_invested + profit
    
    st.markdown("---")
    
    # 1. 顯示大數字儀表板
    col3, col4, col5 = st.columns(3)
    col3.metric("最終總資產", f"NT$ {int(total_future_value):,}")
    col4.metric("總投入本金", f"NT$ {int(total_invested):,}")
    col5.metric("投資獲利", f"NT$ {int(profit):,}")
    
    st.markdown("<br>", unsafe_allow_html=True) # 增加一點空行
    
    # 2. 繪製面積圖
    st.subheader("📊 資產成長軌跡")
    # 設定 X 軸為年份，並畫出堆疊面積圖
    chart_data = df.set_index("年份")
    st.area_chart(chart_data, color=["#4b8bf5", "#85e093"]) # 設定本金與獲利的顏色
    
    st.success("持續投資，時間就是最好的朋友！")
