import gradio as gr

# Custom Gradio Theme for Enterprise/Cyberpunk Aesthetic
custom_theme = gr.themes.Monochrome(
    primary_hue="blue",
    secondary_hue="cyan",
    neutral_hue="slate",
    radius_size=gr.themes.sizes.radius_md,
    text_size=gr.themes.sizes.text_md,
).set(
    body_background_fill="*neutral_950",
    body_background_fill_dark="*neutral_950",
    body_text_color="*neutral_200",
    body_text_color_dark="*neutral_200",
    background_fill_primary="*neutral_900",
    background_fill_primary_dark="*neutral_900",
    background_fill_secondary="*neutral_800",
    background_fill_secondary_dark="*neutral_800",
    border_color_primary="*neutral_700",
    border_color_primary_dark="*neutral_700",
    color_accent_soft="*primary_800",
    color_accent_soft_dark="*primary_800",
    button_primary_background_fill="*primary_600",
    button_primary_background_fill_dark="*primary_600",
    button_primary_background_fill_hover="*primary_500",
    button_primary_background_fill_hover_dark="*primary_500",
    button_primary_text_color="white",
    block_title_text_color="*primary_400",
    block_label_background_fill="*neutral_800",
    block_label_text_color="*neutral_200",
    panel_border_color="*neutral_700",
    panel_border_color_dark="*neutral_700",
)

custom_css = """
body {
    font-family: 'Inter', 'Roboto', sans-serif !important;
}

/* Glassmorphism cards for metrics */
.metric-card {
    background: rgba(30, 41, 59, 0.7) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease-in-out;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: rgba(56, 189, 248, 0.5); /* Cyan glow border */
}

.metric-title {
    color: #94a3b8;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.metric-value {
    color: #f8fafc;
    font-size: 32px;
    font-weight: 700;
    margin: 0;
}

.metric-value.critical {
    color: #ef4444; /* Red for critical */
    text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
}

.metric-value.good {
    color: #10b981; /* Green for good */
    text-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}

/* Stylish header */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 30px;
    background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
    border-bottom: 1px solid #334155;
    margin-bottom: 20px;
    border-radius: 8px;
}

.app-title {
    margin: 0;
    font-size: 24px;
    font-weight: 800;
    background: linear-gradient(to right, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1px;
}

/* Alert tags */
.alert-tag-high {
    background: rgba(239, 68, 68, 0.2);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.4);
    padding: 2px 8px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
}

/* Tabs styling override to make it look like a side/top nav menu */
.tabs {
    border: none !important;
    background: transparent !important;
}
.tab-nav {
    border-bottom: 2px solid #334155 !important;
    gap: 10px !important;
}
.tab-nav button {
    border: none !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    transition: all 0.2s !important;
}
.tab-nav button.selected {
    color: #38bdf8 !important;
    background: rgba(56, 189, 248, 0.1) !important;
    border-bottom: 2px solid #38bdf8 !important;
}
.tab-nav button:hover:not(.selected) {
    color: #cbd5e1 !important;
    background: rgba(255, 255, 255, 0.05) !important;
}
"""
