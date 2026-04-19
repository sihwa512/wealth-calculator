import streamlit as st

def calculate_future_wealth(initial_capital, monthly_investment, annual_rate, years):
    months = years * 12
    monthly_rate = annual_rate / 12
    
    principal_growth = initial_capital * (1 + monthly_rate) ** months
    
    if monthly_rate > 0:
        contribution_growth = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        contribution_growth = monthly_investment * months
        
    total_future_value = principal_growth + contribution_growth
    total_invested = initial_capital + (monthly_investment * months)
    profit = total_future_value - total_invested
    
    return total_invested, profit, total_future_value

# --- 網頁介面設計開始 ---
st.title("📈 資產複利與定期定額計算機")
st.write("輸入您的資金狀況，看看經過時間的複利，未來能累積多少資產！")

# 建立輸入區塊 (左側選單或主畫面皆可)
st.subheader("請輸入您的資訊：")
col1, col2 = st.columns(2)

with col1:
    initial_capital = st.number_input("目前的金錢部位 (元)", min_value=0, value=1000000, step=10000)
    monthly_investment = st.number_input("每月可投入金額 (元)", min_value=0, value=30000, step=1000)

with col2:
    annual_rate_percent = st.number_input("預期年化報酬率 (%)", value=6.5, step=0.1)
    years = st.number_input("投資年限 (年)", min_value=1, value=20, step=1)

# 按下按鈕後進行計算
if st.button("開始計算"):
    annual_rate = annual_rate_percent / 100
    total_invested, profit, total_future_value = calculate_future_wealth(
        initial_capital, monthly_investment, annual_rate, years
    )
    
    st.markdown("---")
    st.subheader("📊 計算結果：")
    
    # 使用 metric 元件顯示漂亮的大數字
    col3, col4, col5 = st.columns(3)
    col3.metric("總投入本金", f"${int(total_invested):,}")
    col4.metric("預估投資獲利", f"${int(profit):,}")
    col5.metric("最終總資產", f"${int(total_future_value):,}")
    
    st.success("持續投資，時間就是最好的朋友！")
