import streamlit as st
import pandas as pd

# 1. 頁面基本設定
st.set_page_config(
    page_title="精準資產計算機", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= 頂級質感 CSS 魔法 (解決手機截斷與佈局) =================
st.markdown("""
<style>
    /* 全局深色底色與字體 */
    [data-testid="stAppViewContainer"] { background-color: #0E1117; }
    * { font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* 自訂數據卡片 */
    .metric-card {
        background-color: #1E1E24;
        border: 1px solid #333333;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-label {
        color: #888888;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #4B8BF5;
        /* 關鍵：使用 clamp 確保手機上數字會縮小不截斷 */
        font-size: clamp(1.2rem, 5vw, 2.2rem);
        font-weight: 700;
        letter-spacing: -1px;
    }

    /* 手機版 2x2 控制面板優化 */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 48% !important;
            flex: 1 1 48% !important;
        }
    }

    /* 按鈕美化 */
    button[kind="secondary"] {
        border-radius: 10px;
        background-color: #262730;
        border: 1px solid #4B8BF5;
        color: white;
        font-weight: bold;
        padding: 10px 0;
        transition: 0.3s;
    }
    button[kind="secondary"]:hover {
        background-color: #4B8BF5;
        box-shadow: 0 0 10px rgba(75, 139, 245, 0.5);
    }

    /* 表格滾動區域鎖定 */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)
# =======================================================================

# 2. 初始化與重設邏輯
if 'init_cap' not in st.session_state: st.session_state.init_cap = 1000000
if 'mon_inv' not in st.session_state: st.session_state.mon_inv = 10000
if 'rate' not in st.session_state: st.session_state.rate = 6.5
if 'yrs' not in st.session_state: st.session_state.yrs = 20

def reset_values():
    st.session_state.init_cap = 1000000
    st.session_state.mon_inv = 10000
    st.session_state.rate = 6.5
    st.session_state.yrs = 20

# 3. 計算邏輯
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

# ================= 頁面配置 =================

st.markdown("<h2 style='text-align:center; color:white; font-size:1.8rem;'>💰 專業資產增長儀表板</h2>", unsafe_allow_html=True)

# --- A. 頂部自訂卡片列 ---
c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
with c_kpi1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">最終預估總資產</div><div class="metric-value">NT$ {final["總資產"]:,}</div></div>', unsafe_allow_html=True)
with c_kpi2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">累積投入本金</div><div class="metric-value">NT$ {final["累積本金"]:,}</div></div>', unsafe_allow_html=True)
with c_kpi3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">預估複利獲利</div><div class="metric-value">NT$ {final["投資獲利"]:,}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- B. 參數控制區 (手動輸入 + 加減按鈕) ---
st.markdown("<p style='color:#888; margin-bottom:0;'>⚙️ 投資參數設定</p>", unsafe_allow_html=True)
ctrl_col1, ctrl_col2 = st.columns(2)
with ctrl_col1:
    st.number_input("初始資金 (NTD)", key='init_cap', step=10000, format="%d")
    st.number_input("預期報酬率 (%)", key='rate', step=0.1, format="%.1f")
with ctrl_col2:
    st.number_input("每月定期定額", key='mon_inv', step=1000, format="%d")
    st.number_input("投資年限 (年)", key='yrs', step=1, format="%d")

st.button("🔄 恢復預設設定", on_click=reset_values, use_container_width=True)

# --- C. 置底報表表格 ---
st.markdown("<p style='color:#888; margin-top:20px; margin-bottom:5px;'>📋 歷年資產增長明細</p>", unsafe_allow_html=True)
styled_df = df.style.format({"累積本金": "{:,}", "投資獲利": "{:,}", "總資產": "{:,}"})
st.dataframe(styled_df, use_container_width=True, hide_index=True, height=300)
