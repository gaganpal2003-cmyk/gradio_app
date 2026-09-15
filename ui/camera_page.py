import gradio as gr
from services.camera_service import CameraService
from services.detection_service import DetectionService

def create_camera_tab(camera_service: CameraService, detection_service: DetectionService):
    with gr.Tab("Cameras", id="cameras_tab"):
        
        with gr.Row():
            # Left panel: Camera List & Controls
            with gr.Column(scale=1):
                gr.Markdown("### Camera Management")
                
                # Fetch cameras for dropdown
                def get_cam_choices():
                    cams = camera_service.get_all_cameras()
                    if not cams:
                        return gr.update(choices=[], value=None)
                    choices = [(f"{c['name']} (ID:{c['id']})", c['id']) for c in cams]
                    return gr.update(choices=choices, value=choices[0][1] if choices else None)
                
                camera_selector = gr.Dropdown(label="Select Camera", interactive=True)
                
                with gr.Row():
                    start_btn = gr.Button("▶ Start Stream", variant="primary", size="sm")
                    stop_btn = gr.Button("⏹ Stop Stream", size="sm")
                
                gr.Markdown("---")
                with gr.Accordion("Add New Camera", open=False):
                    new_cam_name = gr.Textbox(label="Camera Name", placeholder="e.g. Warehouse Cam 1")
                    new_cam_source = gr.Textbox(label="Source (RTSP / USB index / file)", placeholder="0 or rtsp://...")
                    new_cam_loc = gr.Textbox(label="Location", placeholder="e.g. Zone A")
                    new_cam_model = gr.Dropdown(label="Detection Model", choices=["ppe.pt", "yolov8n.pt"], value="ppe.pt")
                    add_btn = gr.Button("➕ Add Camera", variant="primary")
                    add_status = gr.Markdown("")

            # Right panel: Live Viewer
            with gr.Column(scale=3):
                # The live view image
                video_feed = gr.Image(label="Live Feed", interactive=False, streaming=True)
                
                # We use a Gradio Timer that triggers periodically to fetch the latest frame
                # Gradio 4.x supports gr.Timer
                try:
                    timer = gr.Timer(value=0.1, active=False)
                except AttributeError:
                    # Fallback if gr.Timer is not in this gradio version, we can just use every= in event listener or alternative
                    timer = None

        # Logic
        def on_add(name, source, loc, model):
            success = camera_service.add_camera(name, source, loc, model)
            if success:
                return "✅ Camera added successfully.", get_cam_choices()
            return "❌ Failed to add camera.", gr.update()
            
        add_btn.click(on_add, [new_cam_name, new_cam_source, new_cam_loc, new_cam_model], [add_status, camera_selector])
        
        # Stream loop function
        def get_latest_frame(cam_id):
            if cam_id is None:
                return None
            frame, fps = detection_service.process_latest_frame(cam_id)
            if frame is not None:
                import cv2
                # Convert BGR to RGB for Gradio Image
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame

        # Start / Stop logic
        if timer is not None:
            def on_start(cam_id):
                if cam_id:
                    detection_service.start_detection(cam_id)
                return gr.update(active=True)
                
            def on_stop(cam_id):
                if cam_id:
                    detection_service.stop_detection(cam_id)
                return gr.update(active=False), None
                
            start_btn.click(on_start, inputs=[camera_selector], outputs=[timer])
            stop_btn.click(on_stop, inputs=[camera_selector], outputs=[timer, video_feed])
            
            # The tick event fetches the frame
            timer.tick(get_latest_frame, inputs=[camera_selector], outputs=[video_feed])
        else:
            # Fallback for Gradio < 4
            gr.Markdown("**Note**: Real-time streaming requires Gradio 4+ with `gr.Timer`. Please update Gradio if streaming fails.")

        # Load choices on startup
        def init_tab():
            return get_cam_choices()
            
        # We can trigger init on load or just leave it empty and let the user refresh
