import streamlit as st
import pandas as pd

# 1. 頁面基本設定：展開為寬版
st.set_page_config(page_title="資產增長計算機", layout="wide")

# 2. 初始化預設數值 (為「重設按鈕」做準備)
if 'init_cap' not in st.session_state:
    st.session_state.init_cap = 1000000
    st.session_state.mon_inv = 30000
    st.session_state.rate = 6.5
    st.session_state.yrs = 20

# 重設數值的函數
def reset_values():
    st.session_state.init_cap = 1000000
    st.session_state.mon_inv = 30000
    st.session_state.rate = 6.5
    st.session_state.yrs = 20

# 3. 核心計算邏輯
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

# 執行計算
annual_rate = st.session_state.rate / 100
df = calculate_wealth_history(
    st.session_state.init_cap, 
    st.session_state.mon_inv, 
    annual_rate, 
    st.session_state.yrs
)

final_data = df.iloc[-1]
total_invested = final_data["累積本金"]
profit = final_data["投資獲利"]
total_future_value = total_invested + profit

# ================= 網頁排版開始 =================

# --- 頂部區塊：標題與三大指標放在同一列 ---
col_title, col_m1, col_m2, col_m3 = st.columns([1.5, 1, 1, 1])

with col_title:
    st.title("資產增長計算機")
with col_m1:
    st.metric("最終總資產", f"NT$ {int(total_future_value):,}")
with col_m2:
    st.metric("總投入本金", f"NT$ {int(total_invested):,}")
with col_m3:
    st.metric("投資獲利", f"NT$ {int(profit):,}")

# --- 中央區塊：滿版的堆疊面積圖 ---
st.markdown("<br>", unsafe_allow_html=True)
chart_data = df.set_index("年份")
# 為了對齊截圖的顏色，特別指定本金與獲利的顏色
st.area_chart(chart_data, color=["#4b8bf5", "#85e093"], height=400)

st.markdown("---")

# --- 底部區塊：2x2 的控制面板 ---
col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    st.slider("初始資金 (NTD)", min_value=0, max_value=10000000, step=10000, key='init_cap')
    st.slider("預期年化報酬 (%)", min_value=0.0, max_value=20.0, step=0.1, key='rate')

with col_ctrl2:
    st.slider("每月定期定額 (NTD)", min_value=0, max_value=200000, step=1000, key='mon_inv')
    st.slider("投資年限 (年)", min_value=1, max_value=50, step=1, key='yrs')

# --- 最底部：全寬的重設按鈕 ---
st.button("重設數值", on_click=reset_values, use_container_width=True)
