import gradio as gr
from database.connection import init_database
from services.camera_service import CameraService
from services.detection_service import DetectionService
from services.alert_service import AlertService
from services.statistics_service import StatisticsService
from ui import custom_theme, custom_css, create_dashboard_tab, create_camera_tab, create_alerts_tab, create_analytics_tab, create_settings_tab
import config
from app_utils.logger import logger

def main():
    logger.info("Starting Bothera AI Platform...")
    
    # 1. Initialize Database
    init_database()
    
    # 2. Initialize Services
    camera_service = CameraService()
    alert_service = AlertService()
    detection_service = DetectionService(camera_service, alert_service)
    stats_service = StatisticsService()
    
    # 3. Build Gradio Blocks App
    with gr.Blocks(theme=custom_theme, css=custom_css, title="Bothera AI") as app:
        
        with gr.Tabs():
            create_dashboard_tab(stats_service, alert_service)
            camera_selector, get_cam_choices = create_camera_tab(camera_service, detection_service)
            create_alerts_tab(alert_service)
            create_analytics_tab(stats_service)
            create_settings_tab()
            
        app.load(fn=get_cam_choices, inputs=None, outputs=[camera_selector])
            
    # Start the server
    logger.info(f"Launching Gradio app on {config.SERVER_HOST}:{config.SERVER_PORT}")
    try:
        app.launch(
            server_name=config.SERVER_HOST,
            server_port=config.SERVER_PORT,
            debug=config.DEBUG,
            share=False
        )
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Shutting down services...")
        camera_service.stop_all()

if __name__ == "__main__":
    main()
