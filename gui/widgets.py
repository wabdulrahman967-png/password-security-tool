import tkinter as tk
from tkinter import ttk
from gui.styles import Theme

class ModernButton(tk.Button):
    """Modern styled button with hover effects"""
    
    def __init__(self, parent, **kwargs):
        self.theme = Theme.get_theme()
        super().__init__(
            parent,
            **kwargs,
            font=('Segoe UI', 11, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self._setup_style()
    
    def _setup_style(self):
        self.config(
            bg=self.theme['accent_primary'],
            fg='#1e1e2e',
            activebackground=self._adjust_brightness(self.theme['accent_primary'], 0.8),
            activeforeground='#1e1e2e',
            bd=0
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, e):
        self.config(bg=self._adjust_brightness(self.theme['accent_primary'], 1.1))
    
    def _on_leave(self, e):
        self.config(bg=self.theme['accent_primary'])
    
    @staticmethod
    def _adjust_brightness(color: str, factor: float) -> str:
        """Adjust hex color brightness by factor"""
        # Simplified version - returns same color for now
        return color

class ModernEntry(tk.Entry):
    """Modern styled entry field"""
    
    def __init__(self, parent, **kwargs):
        self.theme = Theme.get_theme()
        kwargs.setdefault('font', ('Segoe UI', 12))
        kwargs.setdefault('bg', self.theme['bg_input'])
        kwargs.setdefault('fg', self.theme['text_primary'])
        kwargs.setdefault('insertbackground', self.theme['text_primary'])
        kwargs.setdefault('relief', tk.FLAT)
        kwargs.setdefault('bd', 2)
        super().__init__(parent, **kwargs)
        self._setup_border()
    
    def _setup_border(self):
        self.config(highlightthickness=2)
        self.config(highlightbackground=self.theme['border'])
        self.config(highlightcolor=self.theme['accent_primary'])

class ModernText(tk.Text):
    """Modern styled text widget"""
    
    def __init__(self, parent, **kwargs):
        self.theme = Theme.get_theme()
        kwargs.setdefault('font', ('Consolas', 11))
        kwargs.setdefault('bg', self.theme['bg_secondary'])
        kwargs.setdefault('fg', self.theme['text_primary'])
        kwargs.setdefault('relief', tk.FLAT)
        kwargs.setdefault('bd', 0)
        super().__init__(parent, **kwargs)