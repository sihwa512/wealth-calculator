import streamlit as st
import pandas as pd

# 1. 頁面基本設定
st.set_page_config(page_title="資產增長計算機", layout="wide")

# 2. 初始化預設數值 (每月定期定額預設為 10000)
if 'init_cap' not in st.session_state:
    st.session_state.init_cap = 1000000
if 'mon_inv' not in st.session_state:
    st.session_state.mon_inv = 10000
if 'rate' not in st.session_state:
    st.session_state.rate = 6.5
if 'yrs' not in st.session_state:
    st.session_state.yrs = 20

def reset_values():
    st.session_state.init_cap = 1000000
    st.session_state.mon_inv = 10000
    st.session_state.rate = 6.5
    st.session_state.yrs = 20

# 3. 核心計算邏輯 (加入「總資產」欄位供表格顯示)
def calculate_wealth_history(initial_capital, monthly_investment, annual_rate, years):
    data = []
    current_principal = initial_capital
    current_total = initial_capital
    monthly_rate = (annual_rate / 100) / 12
    
    # 紀錄第 0 年狀態
    data.append({
        "年份": "第 0 年", 
        "累積本金": current_principal, 
        "投資獲利": 0,
        "總資產": current_principal
    })
    
    # 逐年計算
    for year in range(1, years + 1):
        for month in range(12):
            current_principal += monthly_investment
            current_total = (current_total + monthly_investment) * (1 + monthly_rate)
        
        profit = current_total - current_principal
        
        data.append({
            "年份": f"第 {year} 年", 
            "累積本金": int(current_principal), 
            "投資獲利": int(profit),
            "總資產": int(current_total)
        })
        
    return pd.DataFrame(data)

# 4. 取得計算結果
df = calculate_wealth_history(
    st.session_state.init_cap, 
    st.session_state.mon_inv, 
    st.session_state.rate, 
    st.session_state.yrs
)

# 取得最後一年的數據供頂部指標使用
final_data = df.iloc[-1]
total_invested = final_data["累積本金"]
profit = final_data["投資獲利"]
total_future_value = final_data["總資產"]

# ================= 網頁排版開始 =================

# --- 頂部：標題與核心指標 ---
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

# --- 中央：詳細數據表格 ---
st.subheader("📋 年度資產增長明細")
# 使用 st.dataframe 顯示漂亮的互動表格，hide_index=True 可隱藏左側多餘的序號
st.dataframe(
    df, 
    use_container_width=True, 
    hide_index=True,
    height=350 # 固定高度，讓表格出現滾動條，不會讓網頁變得太長
)

st.markdown("---")

# --- 底部：參數控制面板 (直接輸入 + 加減按鈕) ---
col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    st.number_input("初始資金 (NTD)", value=None, key='init_cap', step=10000, format="%d")
    st.number_input("預期年化報酬率 (%)", value=None, key='rate', step=0.1, format="%.1f")

with col_ctrl2:
    st.number_input("每月定期定額 (NTD)", value=None, key='mon_inv', step=1000, format="%d")
    st.number_input("投資年限 (年)", value=None, key='yrs', step=1, format="%d")

st.markdown("<br>", unsafe_allow_html=True)
st.button("🔄 重設數值", on_click=reset_values, use_container_width=True)
