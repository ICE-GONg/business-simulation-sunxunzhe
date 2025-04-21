import streamlit as st
import pandas as pd
from datetime import datetime

class Finance:
    def __init__(self, initial_balance=0):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.transactions = []
        self.expenses = {
            "engineer_salary": 0,
            "material_cost": 0,
            "agent_fees": 0,
            "management_investment": 0,
            "quality_investment": 0,
            "market_investment": 0,
            "market_report": 0
        }
        self.revenue = 0
        
    def add_expense(self, category, amount, description=""):
        """添加支出"""
        if self.current_balance >= amount:
            self.current_balance -= amount
            self.expenses[category] += amount
            self.transactions.append({
                "timestamp": datetime.now(),
                "type": "expense",
                "category": category,
                "amount": amount,
                "balance": self.current_balance,
                "description": description
            })
            return True
        return False
        
    def add_revenue(self, amount, description=""):
        """添加收入"""
        self.current_balance += amount
        self.revenue += amount
        self.transactions.append({
            "timestamp": datetime.now(),
            "type": "revenue",
            "amount": amount,
            "balance": self.current_balance,
            "description": description
        })
        
    def get_financial_report(self):
        """获取财务报告"""
        return {
            "initial_balance": self.initial_balance,
            "current_balance": self.current_balance,
            "total_expenses": sum(self.expenses.values()),
            "total_revenue": self.revenue,
            "expenses_breakdown": self.expenses,
            "transactions": self.transactions
        }

def render_finance_report(player_id):
    """渲染财务报告界面"""
    st.subheader("财务报告")
    
    # 初始化财务数据
    if f"finance_{player_id}" not in st.session_state:
        st.session_state[f"finance_{player_id}"] = Finance(initial_balance=10000)  # 示例初始资金
    
    finance = st.session_state[f"finance_{player_id}"]
    report = finance.get_financial_report()
    
    # 显示当前余额
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("当前余额", f"¥{report['current_balance']:,.2f}")
    with col2:
        st.metric("总支出", f"¥{report['total_expenses']:,.2f}")
    with col3:
        st.metric("总收入", f"¥{report['total_revenue']:,.2f}")
    
    # 支出明细
    st.subheader("支出明细")
    expenses_df = pd.DataFrame([
        {"类别": k, "金额": v}
        for k, v in report["expenses_breakdown"].items()
    ])
    st.dataframe(expenses_df)
    
    # 交易历史
    st.subheader("交易历史")
    if report["transactions"]:
        transactions_df = pd.DataFrame(report["transactions"])
        transactions_df["timestamp"] = pd.to_datetime(transactions_df["timestamp"])
        transactions_df = transactions_df.sort_values("timestamp", ascending=False)
        st.dataframe(transactions_df) 