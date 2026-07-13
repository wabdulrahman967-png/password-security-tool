#!/usr/bin/env python3
"""
Password Security Suite v2.0
A comprehensive password security analysis tool
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def setup_styles():
    """Configure custom ttk styles"""
    style = ttk.Style()
    
    # Custom progressbar styles
    style.theme_use('clam')
    
    style.configure('green.Horizontal.TProgressbar', 
                   background='#a6e3a1',
                   troughcolor='#313244',
                   bordercolor='#313244',
                   lightcolor='#a6e3a1',
                   darkcolor='#a6e3a1')
    
    style.configure('yellow.Horizontal.TProgressbar', 
                   background='#f9e2af',
                   troughcolor='#313244',
                   bordercolor='#313244',
                   lightcolor='#f9e2af',
                   darkcolor='#f9e2af')
    
    style.configure('red.Horizontal.TProgressbar', 
                   background='#f38ba8',
                   troughcolor='#313244',
                   bordercolor='#313244',
                   lightcolor='#f38ba8',
                   darkcolor='#f38ba8')
    
    # Notebook style
    style.configure('TNotebook', background='#1e1e2e', borderwidth=0)
    style.configure('TNotebook.Tab', background='#313244', foreground='#cdd6f4', padding=[10, 5])
    style.map('TNotebook.Tab', background=[('selected', '#45475a')])

def main():
    """Main application entry point"""
    try:
        root = tk.Tk()
        setup_styles()
        
        # Set application icon (optional)
        # root.iconbitmap('icon.ico')
        
        app = MainWindow(root)
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()