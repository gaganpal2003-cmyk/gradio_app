import gradio as gr
from database.connection import get_db_connection
import config

def test_db_connection():
    db = get_db_connection()
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
        return "✅ Database Connection Successful!"
    except Exception as e:
        return f"❌ Database Connection Failed: {str(e)}"

def create_settings_tab():
    with gr.Tab("Settings", id="settings_tab"):
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### ⚙️ Database Configuration")
                gr.Textbox(label="Host", value=config.DB_HOST, interactive=False)
                gr.Textbox(label="Port", value=str(config.DB_PORT), interactive=False)
                gr.Textbox(label="Database", value=config.DB_NAME, interactive=False)
                
                test_db_btn = gr.Button("Test Connection", size="sm")
                db_status = gr.Markdown("")
                test_db_btn.click(test_db_connection, outputs=[db_status])

            with gr.Column():
                gr.Markdown("### 🧠 Inference Engine")
                gr.Slider(minimum=0.1, maximum=1.0, value=config.CONF_THRESHOLD, label="Confidence Threshold", interactive=True)
                gr.Slider(minimum=0.1, maximum=1.0, value=config.IOU_THRESHOLD, label="IoU Threshold", interactive=True)
                gr.Slider(minimum=1, maximum=60, value=config.ALERT_COOLDOWN_SECONDS, step=1, label="Alert Cooldown (Seconds)", interactive=True)
                
                save_settings_btn = gr.Button("Save Settings", variant="primary")
                gr.Markdown("*Note: Changing these settings in runtime is a mock-up. In production, write back to .env.*")
