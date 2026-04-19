import streamlit as st
import pandas as pd

# 1. 頁面基本設定
st.set_page_config(
    page_title="精準資產計算機", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= 手機版與視覺美化 CSS =================
st.markdown("""
<style>
    /* 全局字體設定 */
    * { font-family: 'Helvetica Neue', Arial, sans-serif; }
    
    /* 1. 響應式主標題 (手機上自動縮小) */
    .main-title {
        text-align: center;
        color: #4B8BF5;
        margin-bottom: 20px;
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        font-weight: bold;
    }

    /* 2. 自訂響應式數據卡片 (解決手機版垂直堆疊與截斷問題) */
    .dashboard-container {
        display: grid;
        /* 在手機上會盡量擠在同一排，並允許換行 */
        grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
        gap: 10px;
        margin-bottom: 25px;
    }
    .kpi-card {
        background-color: #1E1E24;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 15px 5px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .kpi-label {
        color: #A0A5B5;
        font-size: clamp(0.7rem, 2.5vw, 1rem); /* 字體自動縮放 */
        font-weight: 500;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #FFFFFF;
        font-size: clamp(1.1rem, 4vw, 2rem); /* 數字自動縮放，絕不截斷 */
        font-weight: 700;
        word-wrap: break-word;
    }

    /* 3. 強制手機版輸入框變成 2x2 網格 (節省垂直空間) */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        /* 讓左右兩欄在手機上強制各佔 48% 寬度 */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 48% !important;
            flex: 1 1 48% !important;
        }
    }

    /* 按鈕與表格美化 */
    button[kind="secondary"] {
        background-color: #2D2F36; color: #FFFFFF; border: 1px solid #4B8BF5;
        border-radius: 8px; font-weight: bold; padding: 10px; margin-top: 5px;
    }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)
# =========================================================

# 2. 初始化與重設邏輯
def init_values():
    if 'init_cap' not in st.session_state: st.session_state.init_cap = 1000000
    if 'mon_inv' not in st.session_state: st.session_state.mon_inv = 10000
    if 'rate' not in st.session_state: st.session_state.rate = 6.5
    if 'yrs' not in st.session_state: st.session_state.yrs = 20

init_values()

def reset_values():
    st.session_state.init_cap = 1000000
    st.session_state.mon_inv = 10000
    st.session_state.rate = 10
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

# --- A. 頂部自訂響應式數據卡片 (取代原本會截斷的 st.metric) ---
metrics_html = f"""
<div class="main-title">💰 專業資產增長計算機</div>
<div class="dashboard-container">
    <div class="kpi-card">
        <div class="kpi-label">最終預估總資產</div>
        <div class="kpi-value">NT$ {final['總資產']:,}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">總投入本金累積</div>
        <div class="kpi-value">NT$ {final['累積本金']:,}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">時間複利獲利</div>
        <div class="kpi-value">NT$ {final['投資獲利']:,}</div>
    </div>
</div>
"""
st.markdown(metrics_html, unsafe_allow_html=True)

# --- B. 中間參數控制區 ---
c1, c2 = st.columns(2)
with c1:
    st.number_input("初始資金", key='init_cap', step=10000, format="%d")
    st.number_input("年化報酬率 (%)", key='rate', step=0.1, format="%.1f")
with c2:
    st.number_input("每月投入", key='mon_inv', step=1000, format="%d")
    st.number_input("投資年限 (年)", key='yrs', step=1, format="%d")

st.button("🔄 恢復預設數值", on_click=reset_values, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- C. 最下方年度明細表格 ---
st.markdown("#### 📋 歷年資產增長明細")

styled_df = df.style.format({
    "累積本金": "{:,}",
    "投資獲利": "{:,}",
    "總資產": "{:,}"
})

# 設定表格高度，防止它在手機上過長
st.dataframe(styled_df, use_container_width=True, hide_index=True, height=350)
