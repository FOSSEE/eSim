"""
Tab Color Configuration for eSim
This file allows easy customization of tab colors for both dark and light themes.
"""

# Dark Theme Tab Colors
DARK_TAB_COLORS = {
    # Normal tab state
    'background': {
        'start': '#2d3748',  # Top gradient color
        'end': '#1a202c'     # Bottom gradient color
    },
    'text': '#e2e8f0',       # Tab text color
    'border': '#4a5568',     # Tab border color
    
    # Selected tab state
    'selected_background': '#667eea',  # Selected tab background (purple)
    'selected_text': '#1a202c',        # Selected tab text
    'selected_border': '#667eea',      # Selected tab border
    
    # Hover state
    'hover_background': '#4a5568',     # Hover background
    'hover_text': '#f7fafc'            # Hover text color
}

# Light Theme Tab Colors
LIGHT_TAB_COLORS = {
    # Normal tab state
    'background': {
        'start': '#ffffff',  # Top gradient color
        'end': '#f8f9fa'     # Bottom gradient color
    },
    'text': '#2c3e50',       # Tab text color
    'border': '#e1e4e8',     # Tab border color
    
    # Selected tab state
    'selected_background': '#1976d2',  # Selected tab background (blue)
    'selected_text': '#ffffff',        # Selected tab text
    'selected_border': '#1976d2',      # Selected tab border
    
    # Hover state
    'hover_background': '#f1f4f9',     # Hover background
    'hover_text': '#1976d2'            # Hover text color
}

# Alternative Color Schemes (you can uncomment and use these)

# Purple Theme
PURPLE_TAB_COLORS = {
    'background': {'start': '#553c9a', 'end': '#b794f4'},
    'text': '#e9d8fd',
    'border': '#9f7aea',
    'selected_background': '#d53f8c',
    'selected_text': '#fed7e2',
    'selected_border': '#d53f8c',
    'hover_background': '#9f7aea',
    'hover_text': '#faf5ff'
}

# Green Theme
GREEN_TAB_COLORS = {
    'background': {'start': '#22543d', 'end': '#38a169'},
    'text': '#c6f6d5',
    'border': '#48bb78',
    'selected_background': '#38a169',
    'selected_text': '#f0fff4',
    'selected_border': '#38a169',
    'hover_background': '#48bb78',
    'hover_text': '#f0fff4'
}

# Orange Theme
ORANGE_TAB_COLORS = {
    'background': {'start': '#744210', 'end': '#ed8936'},
    'text': '#fed7aa',
    'border': '#f6ad55',
    'selected_background': '#dd6b20',
    'selected_text': '#fffaf0',
    'selected_border': '#dd6b20',
    'hover_background': '#f6ad55',
    'hover_text': '#fffaf0'
}

def get_tab_stylesheet(colors, theme_type='dark'):
    """
    Generate CSS stylesheet for tabs based on color configuration.
    
    Args:
        colors (dict): Color configuration dictionary
        theme_type (str): 'dark' or 'light' theme
    
    Returns:
        str: CSS stylesheet string
    """
    return f"""
        QTabBar::tab {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['background']['start']}, stop:1 {colors['background']['end']});
            color: {colors['text']};
            border: 1px solid {colors['border']};
            border-bottom: none;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            padding: 12px 28px;
            margin-right: 4px;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.3px;
        }}
        QTabBar::tab:selected {{
            background: {colors['selected_background']};
            color: {colors['selected_text']};
            border: 1px solid {colors['selected_border']};
            border-bottom: 3px solid {colors['selected_border']};
            font-weight: 700;
        }}
        QTabBar::tab:hover:!selected {{
            background: {colors['hover_background']};
            color: {colors['hover_text']};
        }}
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            border-radius: 0 12px 12px 12px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['background']['start']}, stop:1 {colors['background']['end']});
        }}
    """

def apply_custom_tab_colors(application, dark_colors=None, light_colors=None):
    """
    Apply custom tab colors to the application.
    
    Args:
        application: The main application instance
        dark_colors (dict): Custom dark theme colors (optional)
        light_colors (dict): Custom light theme colors (optional)
    """
    if dark_colors is None:
        dark_colors = DARK_TAB_COLORS
    if light_colors is None:
        light_colors = LIGHT_TAB_COLORS
    
    # Store the custom colors in the application for later use
    application.custom_dark_tab_colors = dark_colors
    application.custom_light_tab_colors = light_colors
    
    # Apply the current theme
    if hasattr(application, 'is_dark_theme') and application.is_dark_theme:
        application.apply_dark_theme()
    else:
        application.apply_light_theme()

# Example usage:
# To use purple theme for dark mode:
# apply_custom_tab_colors(app, dark_colors=PURPLE_TAB_COLORS)

# To use green theme for light mode:
# apply_custom_tab_colors(app, light_colors=GREEN_TAB_COLORS)

# To use both:
# apply_custom_tab_colors(app, dark_colors=PURPLE_TAB_COLORS, light_colors=GREEN_TAB_COLORS) 