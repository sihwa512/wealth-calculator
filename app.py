import streamlit as st
import pandas as pd

# 1. 頁面基本設定
st.set_page_config(page_title="資產增長計算機", layout="wide")

# 2. 初始化與重設邏輯
def init_values():
    if 'init_cap' not in st.session_state: st.session_state.init_cap = 1000000
    if 'mon_inv' not in st.session_state: st.session_state.mon_inv = 10000 # 初始值設為 10,000
    if 'rate' not in st.session_state: st.session_state.rate = 6.5
    if 'yrs' not in st.session_state: st.session_state.yrs = 20

init_values()

def reset_values():
    st.session_state.init_cap = 1000000
    st.session_state.mon_inv = 10000
    st.session_state.rate = 6.5
    st.session_state.yrs = 20

# 3. 計算邏輯
def calculate_data(initial_capital, monthly_investment, annual_rate, years):
    data = []
    current_principal = initial_capital
    current_total = initial_capital
    monthly_rate = (annual_rate / 100) / 12
    
    data.append({
        "年份": "第 0 年", 
        "累積本金": int(current_principal), 
        "投資獲利": 0,
        "總資產": int(current_principal)
    })
    
    for year in range(1, years + 1):
        for month in range(12):
            current_principal += monthly_investment
            current_total = (current_total + monthly_investment) * (1 + monthly_rate)
        
        data.append({
            "年份": f"第 {year} 年", 
            "累積本金": int(current_principal), 
            "投資獲利": int(current_total - current_principal),
            "總資產": int(current_total)
        })
    return pd.DataFrame(data)

# 執行計算
df = calculate_data(st.session_state.init_cap, st.session_state.mon_inv, st.session_state.rate, st.session_state.yrs)
final = df.iloc[-1]

# ================= 介面排版 =================

# --- A. 頂部核心指標 ---
st.title("💰 資產計算機")
m1, m2, m3 = st.columns(3)
m1.metric("最終總資產", f"NT$ {final['總資產']:,}")
m2.metric("總投入本金", f"NT$ {final['累積本金']:,}")
m3.metric("投資獲利", f"NT$ {final['投資獲利']:,}")

st.markdown("---")

# --- B. 中間參數控制區 (手動輸入 + 加減按鈕) ---
st.subheader("⚙️ 調整投資參數")
c1, c2 = st.columns(2)
with c1:
    st.number_input("初始資金 (NTD)", key='init_cap', step=10000, format="%d")
    st.number_input("預期年化報酬率 (%)", key='rate', step=0.1, format="%.1f")
with c2:
    st.number_input("每月定期定額 (NTD)", key='mon_inv', step=1000, format="%d")
    st.number_input("投資年限 (年)", key='yrs', step=1, format="%d")

st.button("🔄 重設數值", on_click=reset_values, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- C. 最下方年度明細表格 ---
st.subheader("📋 年度資產增長明細")
st.dataframe(df, use_container_width=True, hide_index=True)
