import streamlit as st
import pandas as pd

# 1. 頁面基本設定
st.set_page_config(page_title="資產增長計算機", layout="wide")

# 2. 核心計算邏輯
def calculate_wealth_history(initial_capital, monthly_investment, annual_rate, years):
    data = []
    current_principal = initial_capital
    current_total = initial_capital
    monthly_rate = annual_rate / 12
    
    # 為了讓長條圖顯示更乾淨，我們從第 1 年開始紀錄
    for year in range(1, years + 1):
        for month in range(12):
            current_principal += monthly_investment
            current_total = (current_total + monthly_investment) * (1 + monthly_rate)
        profit = current_total - current_principal
        
        # 將年份轉為字串，長條圖的 X 軸顯示會更漂亮
        data.append({
            "年份": f"第 {year} 年", 
            "累積本金": round(current_principal), 
            "投資獲利": round(profit)
        })
        
    return pd.DataFrame(data)

st.title("💰 資產增長計算機")

# --- 1. 控制面板：改回精確的數字輸入框 ---
st.markdown("### ⚙️ 請輸入您的投資參數")
col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    initial_capital = st.number_input("初始資金 (NTD)", min_value=0, value=1000000, step=10000)
    annual_rate_percent = st.number_input("預期年化報酬 (%)", min_value=0.0, value=6.5, step=0.1)

with col_ctrl2:
    monthly_investment = st.number_input("每月定期定額 (NTD)", min_value=0, value=30000, step=1000)
    years = st.number_input("投資年限 (年)", min_value=1, value=20, step=1)

# --- 2. 執行計算 ---
annual_rate = annual_rate_percent / 100
df = calculate_wealth_history(initial_capital, monthly_investment, annual_rate, years)

final_data = df.iloc[-1]
total_invested = final_data["累積本金"]
profit = final_data["投資獲利"]
total_future_value = total_invested + profit

st.markdown("---")

# --- 3. 顯示大數字儀表板 ---
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("最終總資產", f"NT$ {int(total_future_value):,}")
with col_m2:
    st.metric("總投入本金", f"NT$ {int(total_invested):,}")
with col_m3:
    st.metric("投資獲利", f"NT$ {int(profit):,}")

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. 繪製圖表：改用堆疊長條圖 (Bar Chart) ---
st.subheader("📊 資產成長軌跡 (堆疊圖)")
chart_data = df.set_index("年份")

# 使用 st.bar_chart 保證絕對的堆疊效果，不會有重疊誤判
st.bar_chart(chart_data, color=["#4b8bf5", "#85e093"], height=450)
