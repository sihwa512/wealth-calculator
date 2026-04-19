import streamlit as st
import pandas as pd

# 將網頁設定為寬版，讓圖表更大更好看
st.set_page_config(page_title="資產增長計算機", layout="wide")

def calculate_wealth_history(initial_capital, monthly_investment, annual_rate, years):
    data = []
    current_principal = initial_capital
    current_total = initial_capital
    monthly_rate = annual_rate / 12
    
    data.append({"年份": 0, "累積本金": current_principal, "投資獲利": 0})
    
    for year in range(1, years + 1):
        for month in range(12):
            current_principal += monthly_investment
            current_total = (current_total + monthly_investment) * (1 + monthly_rate)
            
        profit = current_total - current_principal
        data.append({"年份": year, "累積本金": round(current_principal), "投資獲利": round(profit)})
        
    return pd.DataFrame(data)

st.title("📈 資產增長計算機")

# --- 1. 互動控制區塊 (使用 Slider 達成即時拖曳更新) ---
st.markdown("### ⚙️ 請調整您的投資參數")
col1, col2 = st.columns(2)

with col1:
    # st.slider 讓使用者可以用滑桿拖曳，數值改變會自動觸發下方重新計算
    initial_capital = st.slider("初始資金 (NTD)", min_value=0, max_value=10000000, value=1000000, step=100000)
    monthly_investment = st.slider("每月定期定額 (NTD)", min_value=0, max_value=200000, value=30000, step=5000)

with col2:
    annual_rate_percent = st.slider("預期年化報酬 (%)", min_value=0.0, max_value=20.0, value=6.5, step=0.1)
    years = st.slider("投資年限 (年)", min_value=1, max_value=50, value=20, step=1)

# --- 2. 背景自動計算 (拿掉按鈕，實現即時反應) ---
annual_rate = annual_rate_percent / 100
df = calculate_wealth_history(initial_capital, monthly_investment, annual_rate, years)

final_data = df.iloc[-1]
total_invested = final_data["累積本金"]
profit = final_data["投資獲利"]
total_future_value = total_invested + profit

st.markdown("---")

# --- 3. 顯示大數字儀表板 ---
col3, col4, col5 = st.columns(3)
col3.metric("最終總資產", f"NT$ {int(total_future_value):,}")
col4.metric("總投入本金", f"NT$ {int(total_invested):,}")
col5.metric("投資獲利", f"NT$ {int(profit):,}")

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. 繪製即時動態面積圖 ---
st.subheader("📊 資產成長軌跡")
chart_data = df.set_index("年份")
st.area_chart(chart_data, color=["#4b8bf5", "#85e093"])
