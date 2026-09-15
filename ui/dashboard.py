import gradio as gr
from services.statistics_service import StatisticsService
from services.alert_service import AlertService

def fetch_metrics(stats_service: StatisticsService):
    metrics = stats_service.get_dashboard_metrics()
    
    html = f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px;">
        <div class="metric-card">
            <div class="metric-title">Active Cameras</div>
            <div class="metric-value">{metrics['active_cameras']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Alerts Today</div>
            <div class="metric-value">{metrics['today_alerts']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Unresolved Critical</div>
            <div class="metric-value critical">{metrics['critical_alerts']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Safety Compliance</div>
            <div class="metric-value good">{metrics['compliance_pct']}%</div>
        </div>
    </div>
    """
    return html

def fetch_recent_alerts(alert_service: AlertService):
    alerts = alert_service.get_recent_alerts(limit=5)
    if not alerts:
        return "<div style='padding:20px; text-align:center; color:#94a3b8;'>No recent alerts. System is clear.</div>"
        
    html = "<div style='display:flex; flex-direction:column; gap:10px;'>"
    for a in alerts:
        severity_class = "alert-tag-high" if a['severity'] in ['HIGH', 'CRITICAL'] else ""
        color = "#ef4444" if a['severity'] == 'CRITICAL' else "#f59e0b" if a['severity'] == 'HIGH' else "#3b82f6"
        html += f"""
        <div style="background: rgba(30,41,59,0.5); border-left: 4px solid {color}; padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="color: #e2e8f0; font-size: 14px;">{a['camera_name']}</strong>
                <span style="color: #94a3b8; font-size: 13px; margin-left: 10px;">{a['timestamp']}</span>
                <div style="margin-top: 4px; color: #cbd5e1; font-size: 15px;">Violation: {a['violation_type'].replace('_', ' ').title()}</div>
            </div>
            <div>
                <span class="{severity_class}">{a['severity']}</span>
            </div>
        </div>
        """
    html += "</div>"
    return html

def create_dashboard_tab(stats_service: StatisticsService, alert_service: AlertService):
    with gr.Tab("Dashboard", id="dashboard_tab"):
        gr.HTML("""
        <div class="app-header">
            <h1 class="app-title">BOTHERA AI</h1>
            <div style="color: #94a3b8; font-size: 14px;">Enterprise Vision System</div>
        </div>
        """)
        
        metrics_html = gr.HTML(value=fetch_metrics(stats_service))
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### Recent Incident Feed")
                alerts_html = gr.HTML(value=fetch_recent_alerts(alert_service))
            with gr.Column(scale=1):
                gr.Markdown("### System Status")
                gr.Markdown(
                    "- **Database**: Online\n"
                    "- **Engine**: YOLO Dual-Loader Ready\n"
                    "- **Storage**: OK\n"
                )

        # Refresh button to update the dashboard
        refresh_btn = gr.Button("Refresh Dashboard", variant="secondary", size="sm")
        
        def update_all():
            return fetch_metrics(stats_service), fetch_recent_alerts(alert_service)
            
        refresh_btn.click(
            fn=update_all,
            inputs=None,
            outputs=[metrics_html, alerts_html]
        )
