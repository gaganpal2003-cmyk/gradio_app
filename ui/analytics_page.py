import gradio as gr
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from services.statistics_service import StatisticsService

def create_analytics_tab(stats_service: StatisticsService):
    with gr.Tab("Analytics", id="analytics_tab"):
        
        with gr.Row():
            refresh_btn = gr.Button("🔄 Refresh Charts", variant="primary")
            
        with gr.Row():
            trend_plot = gr.Plot(label="24h Violation Trends")
            breakdown_plot = gr.Plot(label="Violation Types Breakdown")
            
        def load_charts():
            # 1. Trend Line Chart
            trends_data = stats_service.get_hourly_trends(hours=24)
            if trends_data:
                df_trends = pd.DataFrame(trends_data)
                fig_trend = px.line(
                    df_trends, x="hour", y="count", 
                    title="Alerts Over Time (Last 24h)",
                    template="plotly_dark",
                    line_shape="spline",
                    markers=True
                )
                fig_trend.update_traces(line_color="#38bdf8", fill="tozeroy", fillcolor="rgba(56,189,248,0.1)")
            else:
                fig_trend = go.Figure()
                fig_trend.update_layout(title="No data available", template="plotly_dark")
                
            # 2. Breakdown Donut Chart
            breakdown_data = stats_service.get_violation_breakdown(hours=24)
            if breakdown_data:
                df_breakdown = pd.DataFrame(list(breakdown_data.items()), columns=["Violation", "Count"])
                fig_donut = px.pie(
                    df_breakdown, names="Violation", values="Count", 
                    hole=0.6, title="Violation Distribution",
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.sequential.Agalmati
                )
                fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            else:
                fig_donut = go.Figure()
                fig_donut.update_layout(title="No data available", template="plotly_dark")

            return fig_trend, fig_donut

        refresh_btn.click(load_charts, inputs=None, outputs=[trend_plot, breakdown_plot])
