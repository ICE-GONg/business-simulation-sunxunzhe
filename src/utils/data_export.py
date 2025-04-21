import pandas as pd
import json
from datetime import datetime
import streamlit as st
import os

class DataExporter:
    @staticmethod
    def export_game_data(game_data, format='excel'):
        """导出游戏数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'excel':
            # 创建Excel writer
            filename = f'game_data_{timestamp}.xlsx'
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            
            # 导出市场配置
            market_config_df = pd.DataFrame(game_data['market_config'])
            market_config_df.to_excel(writer, sheet_name='Market_Config')
            
            # 导出玩家资产数据
            assets_df = pd.DataFrame(game_data['assets'])
            assets_df.to_excel(writer, sheet_name='Assets')
            
            # 导出市场报告
            market_reports_df = pd.DataFrame(game_data['market_reports'])
            market_reports_df.to_excel(writer, sheet_name='Market_Reports')
            
            # 导出玩家决策
            decisions_df = pd.DataFrame(game_data['player_decisions'])
            decisions_df.to_excel(writer, sheet_name='Player_Decisions')
            
            writer.save()
            return filename
            
        elif format == 'json':
            filename = f'game_data_{timestamp}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, ensure_ascii=False, indent=4)
            return filename

def render_data_export():
    """渲染数据导出界面"""
    st.subheader("数据导出")
    
    export_format = st.selectbox(
        "选择导出格式",
        ["Excel", "JSON"],
        help="选择要导出的文件格式"
    )
    
    if st.button("导出数据"):
        # 收集游戏数据
        game_data = {
            "market_config": st.session_state.get('market_config', {}).markets,
            "assets": st.session_state.get('asset_tracker', {}).player_assets,
            "market_reports": {
                market: market_obj.market_reports
                for market, market_obj in st.session_state.get('markets', {}).items()
            },
            "player_decisions": {
                market: market_obj.players
                for market, market_obj in st.session_state.get('markets', {}).items()
            }
        }
        
        try:
            format = 'excel' if export_format == "Excel" else 'json'
            filename = DataExporter.export_game_data(game_data, format)
            
            # 提供下载链接
            with open(filename, 'rb') as f:
                st.download_button(
                    label="下载数据",
                    data=f,
                    file_name=filename,
                    mime='application/octet-stream'
                )
            
            st.success(f"数据已导出到: {filename}")
            
        except Exception as e:
            st.error(f"导出失败: {str(e)}")
            
        finally:
            # 清理临时文件
            if 'filename' in locals() and os.path.exists(filename):
                os.remove(filename) 