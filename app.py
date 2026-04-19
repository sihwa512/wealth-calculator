import streamlit as st
import pandas as pd

# 1. 頁面基本設定
st.set_page_config(page_title="資產增長計算機", layout="wide")

# 2. 初始化預設數值
if 'init_cap' not in st.session_state:
    st.session_state.init_cap = 1000000
if 'mon_inv' not in st.session_state:
    st.session_state.mon_inv = 10000  # 更新初始值為 10,000
if 'rate' not in st.session_state:
    st.session_state.rate = 6.5
if 'yrs' not in st.session_state:
    st.session_state.yrs = 20

def reset_values():
    st.session_state.init_cap = 1000000
    st.session_state.mon_inv = 10000
    st.session_state.rate = 6.5
    st.session_state.yrs = 20

# 3. 核心計算邏輯
def calculate_wealth_history(initial_capital, monthly_investment, annual_rate, years):
    data = []
    current_principal = initial_capital
    current_total = initial_capital
    monthly_rate = (annual_rate / 100) / 12
    
    data.append({"年份": 0, "累積本金": current_principal, "投資獲利": 0})
    
    for year in range(1, years + 1):
        for month in range(12):
            current_principal += monthly_investment
            current_total = (current_total + monthly_investment) * (1 + monthly_rate)
        profit = current_total - current_principal
        data.append({"年份": year, "累積本金": int(current_principal), "投資獲利": int(profit)})
        
    return pd.DataFrame(data)

# 4. 取得計算結果
df = calculate_wealth_history(
    st.session_state.init_cap, 
    st.session_state.mon_inv, 
    st.session_state.rate, 
    st.session_state.yrs
)

final_data = df.iloc[-1]
total_invested = final_data["累積本金"]
profit = final_data["投資獲利"]
total_future_value = total_invested + profit

# --- 介面排版 ---

# 頂部：標題與指標
col_title, col_m1, col_m2, col_m3 = st.columns([1.2, 1, 1, 1])
with col_title:
    st.title("💰 資產計算機")
with col_m1:
    st.metric("最終總資產", f"NT$ {int(total_future_value):,}")
with col_m2:
    st.metric("總投入本金", f"NT$ {int(total_invested):,}")
with col_m3:
    st.metric("投資獲利", f"NT$ {int(profit):,}")

st.markdown("<br>", unsafe_allow_html=True)

# 中央：圖表
chart_data = df.set_index("年份")
st.area_chart(chart_data, color=["#4b8bf5", "#85e093"], height=350)

st.markdown("---")

# 底部：參數控制面板 (手動輸入 + 加減按鈕)
# st.number_input 在 Streamlit 中完美結合了手動輸入與兩側的 +/- 按鈕
col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    st.number_input("初始資金 (NTD)", value=None, key='init_cap', step=10000, format="%d")
    st.number_input("預期年化報酬率 (%)", value=None, key='rate', step=0.1, format="%.1f")

with col_ctrl2:
    st.number_input("每月定期定額 (NTD)", value=None, key='mon_inv', step=1000, format="%d")
    st.number_input("投資年限 (年)", value=None, key='yrs', step=1, format="%d")

st.markdown("<br>", unsafe_allow_html=True)
st.button("🔄 重設數值", on_click=reset_values, use_container_width=True)
