import gradio as gr
import pandas as pd
from services.alert_service import AlertService
import config
from pathlib import Path
from PIL import Image

def create_alerts_tab(alert_service: AlertService):
    with gr.Tab("Alerts History", id="alerts_tab"):
        
        with gr.Row():
            # Filters
            with gr.Column(scale=1):
                gr.Markdown("### Filters")
                severity_filter = gr.Dropdown(choices=["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"], value="ALL", label="Severity")
                status_filter = gr.Dropdown(choices=["ALL", "UNRESOLVED", "ACKNOWLEDGED", "RESOLVED"], value="ALL", label="Status")
                refresh_btn = gr.Button("🔄 Apply Filters / Refresh", variant="primary")
            
            # Data table
            with gr.Column(scale=3):
                alerts_table = gr.Dataframe(
                    headers=["ID", "Time", "Camera", "Violation", "Severity", "Conf.", "Status", "Snapshot"],
                    datatype=["number", "str", "str", "str", "str", "number", "str", "str"],
                    interactive=False
                )
                
                with gr.Row():
                    alert_id_input = gr.Number(label="Alert ID to Update", precision=0)
                    new_status = gr.Dropdown(choices=["ACKNOWLEDGED", "RESOLVED"], label="New Status")
                    update_btn = gr.Button("Update Status", size="sm")
                    update_msg = gr.Markdown("")
        
        gr.Markdown("---")
        gr.Markdown("### Snapshot Viewer")
        with gr.Row():
            snapshot_path_input = gr.Textbox(label="Paste Snapshot Path to View", placeholder="data/alerts/...")
            view_btn = gr.Button("View Snapshot", size="sm")
        
        snapshot_image = gr.Image(label="Violation Snapshot", interactive=False)
        
        def load_alerts(sev, stat):
            s = None if sev == "ALL" else sev
            st = None if stat == "ALL" else stat
            
            raw_alerts = alert_service.get_recent_alerts(limit=100, severity=s, status=st)
            
            # Convert to list of lists for Gradio Dataframe
            data = []
            for a in raw_alerts:
                data.append([
                    a['id'],
                    str(a['timestamp']),
                    a['camera_name'],
                    a['violation_type'],
                    a['severity'],
                    round(a['confidence'], 2),
                    a['status'],
                    a['snapshot_path'] or "N/A"
                ])
            return pd.DataFrame(data, columns=["ID", "Time", "Camera", "Violation", "Severity", "Conf.", "Status", "Snapshot"])
            
        def update_status(a_id, stat):
            if not a_id or not stat:
                return "Please provide both ID and Status."
            success = alert_service.update_alert_status(int(a_id), stat)
            return "✅ Updated successfully." if success else "❌ Failed to update."
            
        def view_snapshot(path):
            if not path or path == "N/A":
                return None
            full_path = config.BASE_DIR / path
            if full_path.exists():
                return Image.open(full_path)
            return None

        refresh_btn.click(load_alerts, inputs=[severity_filter, status_filter], outputs=[alerts_table])
        update_btn.click(update_status, inputs=[alert_id_input, new_status], outputs=[update_msg])
        view_btn.click(view_snapshot, inputs=[snapshot_path_input], outputs=[snapshot_image])
