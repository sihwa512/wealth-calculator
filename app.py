import streamlit as st
import pandas as pd

# 1. 頁面基本設定 (隱藏預設的選單，讓畫面更像獨立 APP)
st.set_page_config(
    page_title="精準資產計算機", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= 視覺美化 CSS 魔法 =================
st.markdown("""
<style>
    /* 全局字體與背景優化 */
    * { font-family: 'Helvetica Neue', Arial, sans-serif; }
    
    /* 頂部數據卡片美化 */
    div[data-testid="metric-container"] {
        background-color: #1E1E24; /* 深色質感背景 */
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15); /* 立體微陰影 */
        transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px); /* 滑鼠游標移過去會微微浮起 */
    }
    div[data-testid="metric-container"] label {
        color: #A0A5B5 !important;
        font-size: 1.1rem !important;
        font-weight: 500;
        margin-bottom: 5px;
    }
    div[data-testid="metric-container"] div {
        color: #FFFFFF !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }

    /* 重設按鈕美化 */
    button[kind="secondary"] {
        background-color: #2D2F36;
        color: #FFFFFF;
        border: 1px solid #4B8BF5;
        border-radius: 8px;
        font-weight: bold;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    button[kind="secondary"]:hover {
        background-color: #4B8BF5;
        color: white;
        border-color: #4B8BF5;
        box-shadow: 0 0 15px rgba(75, 139, 245, 0.4);
    }
    
    /* 隱藏表格預設的醜醜 index 列，並讓表格更俐落 */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)
# =========================================================

# 2. 初始化預設值與重設邏輯
def init_values():
    if 'init_cap' not in st.session_state: st.session_state.init_cap = 1000000
    if 'mon_inv' not in st.session_state: st.session_state.mon_inv = 10000
    if 'rate' not in st.session_state: st.session_state.rate = 6.5
    if 'yrs' not in st.session_state: st.session_state.yrs = 20

init_values()

def reset_values():
    st.session_state.init_cap = 1000000
    st.session_state.mon_inv = 10000
    st.session_state.rate = 6.5
    st.session_state.yrs = 20

# 3. 核心計算邏輯
def calculate_report(initial_capital, monthly_investment, annual_rate, years):
    data = []
    current_principal = initial_capital
    current_total = initial_capital
    monthly_rate = (annual_rate / 100) / 12
    
    data.append({"年份": "第 0 年", "累積本金": int(current_principal), "投資獲利": 0, "總資產": int(current_principal)})
    
    for year in range(1, years + 1):
        for month in range(12):
            current_principal += monthly_investment
            current_total = (current_total + monthly_investment) * (1 + monthly_rate)
        data.append({"年份": f"第 {year} 年", "累積本金": int(current_principal), "投資獲利": int(current_total - current_principal), "總資產": int(current_total)})
    return pd.DataFrame(data)

df = calculate_report(st.session_state.init_cap, st.session_state.mon_inv, st.session_state.rate, st.session_state.yrs)
final = df.iloc[-1]

# ================= 介面排版 =================

# --- A. 頂部核心指標 ---
st.markdown("<h2 style='text-align: center; color: #4B8BF5; margin-bottom: 30px;'>💰 專業資產增長計算機</h2>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("最終預估總資產", f"NT$ {final['總資產']:,}")
m2.metric("總投入本金累積", f"NT$ {final['累積本金']:,}")
m3.metric("時間複利獲利", f"NT$ {final['投資獲利']:,}")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- B. 中間參數控制區 ---
st.markdown("#### ⚙️ 投資參數設定")
c1, c2 = st.columns(2)
with c1:
    st.number_input("初始資金 (NTD)", key='init_cap', step=10000, format="%d")
    st.number_input("預期年化報酬率 (%)", key='rate', step=0.1, format="%.1f")
with c2:
    st.number_input("每月定期定額 (NTD)", key='mon_inv', step=1000, format="%d")
    st.number_input("投資年限 (年)", key='yrs', step=1, format="%d")

st.markdown("<br>", unsafe_allow_html=True)
st.button("🔄 恢復預設數值", on_click=reset_values, use_container_width=True)

st.markdown("<hr style='border: 1
