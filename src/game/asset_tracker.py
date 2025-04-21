import streamlit as st
import plotly.graph_objects as go
import pandas as pd

class AssetTracker:
    def __init__(self):
        self.player_assets = {}  # {player_id: {round: asset}}
        self.rankings = {}  # {round: {player_id: rank}}
        
    def update_player_asset(self, player_id, round_num, asset):
        """更新玩家资产"""
        if player_id not in self.player_assets:
            self.player_assets[player_id] = {}
        self.player_assets[player_id][round_num] = asset
        
        # 更新排名
        if round_num not in self.rankings:
            self.rankings[round_num] = {}
            
        # 获取当前轮次所有玩家的资产
        round_assets = {
            pid: assets.get(round_num, 0)
            for pid, assets in self.player_assets.items()
        }
        
        # 按资产排序
        sorted_players = sorted(
            round_assets.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 更新排名
        for rank, (pid, _) in enumerate(sorted_players, 1):
            self.rankings[round_num][pid] = rank
    
    def get_player_ranking(self, player_id, round_num):
        """获取玩家排名"""
        return self.rankings.get(round_num, {}).get(player_id)
    
    def create_asset_chart(self):
        """创建资产折线图"""
        fig = go.Figure()
        
        # 为每个玩家创建一条线
        for player_id, rounds_data in self.player_assets.items():
            rounds = list(rounds_data.keys())
            assets = list(rounds_data.values())
            
            fig.add_trace(go.Scatter(
                x=rounds,
                y=assets,
                name=f"Player {player_id}",
                mode='lines+markers'
            ))
        
        fig.update_layout(
            title="玩家资产走势",
            xaxis_title="回合",
            yaxis_title="资产",
            hovermode='x unified'
        )
        
        return fig
    
    def get_rankings_table(self, round_num):
        """获取排名表格"""
        if round_num not in self.rankings:
            return pd.DataFrame()
            
        data = []
        for player_id in self.rankings[round_num]:
            data.append({
                "玩家ID": player_id,
                "资产": self.player_assets[player_id][round_num],
                "排名": self.rankings[round_num][player_id]
            })
            
        return pd.DataFrame(data).sort_values("排名")

def render_asset_tracking():
    """渲染资产追踪界面"""
    st.subheader("资产追踪")
    
    # 初始化资产追踪器
    if "asset_tracker" not in st.session_state:
        st.session_state.asset_tracker = AssetTracker()
    
    tracker = st.session_state.asset_tracker
    current_round = st.session_state.current_round
    
    # 显示资产折线图
    st.plotly_chart(tracker.create_asset_chart())
    
    # 显示当前轮次排名
    st.subheader(f"第 {current_round} 轮排名")
    rankings_df = tracker.get_rankings_table(current_round)
    if not rankings_df.empty:
        st.dataframe(rankings_df)
    else:
        st.info("暂无排名数据") 