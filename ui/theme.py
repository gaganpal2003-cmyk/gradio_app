import gradio as gr

# Custom Gradio Theme for Premium Cyberpunk / Enterprise Aesthetic
custom_theme = gr.themes.Base(
    primary_hue="cyan",
    secondary_hue="indigo",
    neutral_hue="slate",
    radius_size=gr.themes.sizes.radius_lg,
    text_size=gr.themes.sizes.text_md,
    font=[gr.themes.GoogleFont("Outfit"), gr.themes.GoogleFont("Inter"), "sans-serif"],
).set(
    # Body Background & Text
    body_background_fill="linear-gradient(135deg, #0f172a 0%, #020617 100%)",
    body_background_fill_dark="linear-gradient(135deg, #0f172a 0%, #020617 100%)",
    body_text_color="*neutral_200",
    body_text_color_dark="*neutral_200",
    
    # Blocks and Panels (Glassmorphism look)
    background_fill_primary="rgba(30, 41, 59, 0.4)",
    background_fill_primary_dark="rgba(30, 41, 59, 0.4)",
    background_fill_secondary="rgba(15, 23, 42, 0.6)",
    background_fill_secondary_dark="rgba(15, 23, 42, 0.6)",
    
    # Borders
    border_color_primary="rgba(56, 189, 248, 0.15)",
    border_color_primary_dark="rgba(56, 189, 248, 0.15)",
    border_color_accent="*primary_500",
    border_color_accent_dark="*primary_500",
    panel_border_color="rgba(139, 92, 246, 0.2)",
    panel_border_color_dark="rgba(139, 92, 246, 0.2)",
    
    # Buttons
    button_primary_background_fill="linear-gradient(90deg, #0ea5e9 0%, #6366f1 100%)",
    button_primary_background_fill_dark="linear-gradient(90deg, #0ea5e9 0%, #6366f1 100%)",
    button_primary_background_fill_hover="linear-gradient(90deg, #38bdf8 0%, #818cf8 100%)",
    button_primary_background_fill_hover_dark="linear-gradient(90deg, #38bdf8 0%, #818cf8 100%)",
    button_primary_text_color="white",
    button_primary_border_color="transparent",
    
    # Accent Colors
    color_accent_soft="rgba(56, 189, 248, 0.1)",
    color_accent_soft_dark="rgba(56, 189, 248, 0.1)",
    
    # Headings & Labels
    block_title_text_color="*primary_400",
    block_label_background_fill="rgba(30, 41, 59, 0.8)",
    block_label_text_color="*neutral_100",
    block_label_margin="0",
    block_label_radius="*radius_md",
)

custom_css = """
body {
    background-attachment: fixed !important;
    background-size: cover !important;
}

/* Glassmorphism Metric Cards */
.metric-card {
    background: rgba(30, 41, 59, 0.5) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
    transition: left 0.5s;
}

.metric-card:hover {
    transform: translateY(-5px) scale(1.02);
    border-color: rgba(99, 102, 241, 0.6);
    box-shadow: 0 10px 40px rgba(99, 102, 241, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.metric-card:hover::before {
    left: 100%;
}

.metric-title {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 12px;
}

.metric-value {
    color: #f8fafc;
    font-size: 38px;
    font-weight: 800;
    margin: 0;
    font-family: 'Outfit', sans-serif;
}

.metric-value.critical {
    background: linear-gradient(to right, #ef4444, #f87171);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}

.metric-value.good {
    background: linear-gradient(to right, #10b981, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}

/* Premium Gradient Header */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 40px;
    background: rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(56, 189, 248, 0.1);
    border-radius: 16px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.3);
}

.app-title {
    margin: 0;
    font-size: 32px;
    font-weight: 900;
    font-family: 'Outfit', sans-serif;
    background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1.5px;
    filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.5));
}

/* Status dots */
.status-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 10px currentColor;
}
.status-indicator.online {
    color: #10b981;
    background-color: #10b981;
}

/* Alert tags */
.alert-tag-high {
    background: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Fix tabs layout to look more premium */
.tabs > div[role='tablist'] {
    background: rgba(15, 23, 42, 0.6) !important;
    border-radius: 12px;
    padding: 6px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 20px;
}
.tabs > div[role='tablist'] > button {
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}
.tabs > div[role='tablist'] > button.selected {
    background: rgba(56, 189, 248, 0.15) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.1);
}
"""
