class Theme:
    """Modern color themes for the application"""
    
    DARK = {
        'bg_primary': '#1e1e2e',
        'bg_secondary': '#313244',
        'bg_input': '#45475a',
        'text_primary': '#cdd6f4',
        'text_secondary': '#a6adc8',
        'accent_primary': '#89b4fa',
        'accent_secondary': '#74c7ec',
        'success': '#a6e3a1',
        'warning': '#f9e2af',
        'danger': '#f38ba8',
        'border': '#585b70',
        'shadow': '#00000066'
    }
    
    LIGHT = {
        'bg_primary': '#f5f5f7',
        'bg_secondary': '#ffffff',
        'bg_input': '#e8e8ed',
        'text_primary': '#1a1a2e',
        'text_secondary': '#4a4a5e',
        'accent_primary': '#4a7be7',
        'accent_secondary': '#5a9be7',
        'success': '#40a040',
        'warning': '#d4a020',
        'danger': '#d04040',
        'border': '#c0c0c8',
        'shadow': '#00000033'
    }
    
    @classmethod
    def get_theme(cls, is_dark: bool = True):
        return cls.DARK if is_dark else cls.LIGHT