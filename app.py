import streamlit as st
import pandas as pd

# 1. 頁面基本設定：展開為寬版
st.set_page_config(page_title="資產增長計算機", layout="wide")

# 2. 初始化預設數值
default_values = {
    'init_cap': 1000000, 
    'mon_inv': 10000, 
    'rate': 6.5, 
    'yrs': 20
}

for key, val in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = val

def reset_values():
    for key, val in default_values.items():
        st.session_state[key] = val

# 3. 建立「自訂加減按鈕」的專屬元件
def custom_stepper(label, key, step, is_float=False):
    # 顯示標題
    st.markdown(f"<p style='margin-bottom: 5px; font-size: 15px; color: #888;'>{label}</p>", unsafe_allow_html=True)
    
    # 建立 1:4:1 的三個欄位來放置 [按鈕] [數字] [按鈕]
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        if st.button("－", key=f"minus_{key}", use_container_width=True):
            # 防止數值變成負數
            st.session_state[key] = max(0, st.session_state[key] - step)
            
    with col2:
        # 格式化數字 (加上千分位逗號)
        val = st.session_state[key]
        display_val = f"{val:,.1f}" if is_float else f"{val:,}"
        # 顯示中央的數字區塊 (適應亮/暗模式的微透明背景)
        st.markdown(
            f"<div style='text-align:center; padding:0.35rem; background-color: rgba(128,128,128,0.15); border-radius:4px; font-size: 1.1rem;'>{display_val}</div>", 
            unsafe_allow_html=True
        )
        
    with col3:
        if st.button("＋", key=f"plus_{key}", use_container_width=True):
            st.session_state[key] += step

# 4. 核心計算邏輯
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

# --- 頂部區塊：三大指標 ---
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("最終總資產", f"NT$ {int(total_future_value):,}")
with col_m2:
    st.metric("總投入本金", f"NT$ {int(total_invested):,}")
with col_m3:
    st.metric("投資獲利", f"NT$ {int(profit):,}")

st.markdown("<br>", unsafe_allow_html=True)

# --- 中央區塊：面積圖 ---
chart_data = df.set_index("年份")
# 顏色對應：藍色為本金，綠色為獲利
st.area_chart(chart_data, color=["#4b8bf5", "#85e093"], height=350)

st.markdown("---")

# --- 底部區塊：2x2 自訂微調按鈕網格 ---
col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    custom_stepper("初始資金 (NTD)", "init_cap", step=10000)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # 增加垂直間距
    custom_stepper("預期年化報酬率 (%)", "rate", step=0.1, is_float=True)

with col_ctrl2:
    custom_stepper("每月定期定額 (NTD)", "mon_inv", step=1000)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    custom_stepper("投資年限 (年)", "yrs", step=1)

st.markdown("<br>", unsafe_allow_html=True)

# --- 最底部：重設按鈕 ---
st.button("🔄 重設數值", on_click=reset_values, use_container_width=True)
