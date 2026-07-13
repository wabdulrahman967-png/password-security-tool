import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gui.styles import Theme
from gui.widgets import ModernButton, ModernEntry, ModernText
from core.password_checker import PasswordStrengthChecker
from core.breach_checker import BreachChecker
from core.encryption import CaesarCipher
from core.report_generator import ReportGenerator

class MainWindow:
    """Main application window with modern design"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Password Security Suite v2.0")
        self.root.geometry("750x650")
        self.root.minsize(600, 500)
        
        # Initialize components
        self.checker = PasswordStrengthChecker()
        self.breach_checker = BreachChecker()
        self.report_gen = ReportGenerator()
        self.theme = Theme.get_theme()
        
        self._setup_ui()
        self._apply_theme()
        
        # Track state
        self.current_password = ""
        self.is_dark_mode = True
    
    def _setup_ui(self):
        """Setup all UI components"""
        # Main container with padding
        self.main_frame = tk.Frame(self.root, padx=30, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self._create_header()
        
        # Password input section
        self._create_password_section()
        
        # Action buttons
        self._create_action_buttons()
        
        # Tabs for results
        self._create_result_tabs()
        
        # Status bar
        self._create_status_bar()
    
    def _create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(
            header_frame,
            text="🔐 Password Security Suite",
            font=('Segoe UI', 20, 'bold')
        )
        title.pack(side=tk.LEFT)
        
        # Theme toggle
        self.theme_btn = tk.Button(
            header_frame,
            text="🌙 Dark",
            font=('Segoe UI', 10),
            command=self._toggle_theme,
            relief=tk.FLAT,
            padx=10
        )
        self.theme_btn.pack(side=tk.RIGHT)
    
    def _create_password_section(self):
        """Create password input section"""
        input_frame = tk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Label
        tk.Label(
            input_frame,
            text="Enter Password:",
            font=('Segoe UI', 12, 'bold')
        ).pack(anchor=tk.W)
        
        # Entry with show/hide
        entry_frame = tk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.password_entry = ModernEntry(entry_frame)
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.password_entry.bind('<Return>', lambda e: self._analyze_password())
        
        # Show/Hide button
        self.show_btn = tk.Button(
            entry_frame,
            text="👁️",
            font=('Segoe UI', 12),
            command=self._toggle_password_visibility,
            relief=tk.FLAT,
            padx=8
        )
        self.show_btn.pack(side=tk.RIGHT)
        
        # Password strength meter (visual)
        self.strength_meter = ttk.Progressbar(
            input_frame,
            length=200,
            mode='determinate',
            style='TProgressbar'
        )
        self.strength_meter.pack(fill=tk.X, pady=(5, 0))
        self._update_strength_meter(0, "No password")
    
    def _create_action_buttons(self):
        """Create main action buttons"""
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Main buttons
        analyze_btn = ModernButton(
            btn_frame,
            text="🔍 Analyze Password",
            command=self._analyze_password
        )
        analyze_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = ModernButton(
            btn_frame,
            text="🗑️ Clear",
            command=self._clear_fields
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = ModernButton(
            btn_frame,
            text="💾 Save Report",
            command=self._save_report
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Encryption section (compact)
        enc_frame = tk.Frame(btn_frame)
        enc_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            enc_frame,
            text="Encrypt:",
            font=('Segoe UI', 10)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.encrypt_entry = ModernEntry(enc_frame, width=15)
        self.encrypt_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.encrypt_entry.insert(0, "shift 3")
        
        enc_btn = tk.Button(
            enc_frame,
            text="🔐",
            font=('Segoe UI', 12),
            command=self._encrypt_password,
            relief=tk.FLAT,
            padx=8
        )
        enc_btn.pack(side=tk.LEFT)
    
    def _create_result_tabs(self):
        """Create tabbed results view"""
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: Analysis Results
        self.analysis_tab = tk.Frame(notebook)
        notebook.add(self.analysis_tab, text="📊 Analysis")
        
        self.result_text = ModernText(self.analysis_tab)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
        # Tab 2: Encryption Tools
        self.encrypt_tab = tk.Frame(notebook)
        notebook.add(self.encrypt_tab, text="🔐 Encryption")
        self._setup_encryption_tab()
        
        # Tab 3: History
        self.history_tab = tk.Frame(notebook)
        notebook.add(self.history_tab, text="📜 History")
        self._setup_history_tab()
    
    def _setup_encryption_tab(self):
        """Setup encryption tool tab"""
        frame = tk.Frame(self.encrypt_tab, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Input
        tk.Label(
            frame,
            text="Text to Encrypt:",
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor=tk.W)
        
        self.encrypt_input = ModernText(frame, height=3)
        self.encrypt_input.pack(fill=tk.X, pady=(5, 10))
        
        # Shift control
        shift_frame = tk.Frame(frame)
        shift_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(shift_frame, text="Shift:").pack(side=tk.LEFT, padx=(0, 10))
        self.shift_spinbox = tk.Spinbox(
            shift_frame,
            from_=1,
            to=25,
            width=5,
            font=('Segoe UI', 11)
        )
        self.shift_spinbox.pack(side=tk.LEFT)
        self.shift_spinbox.delete(0, tk.END)
        self.shift_spinbox.insert(0, "3")
        
        # Buttons
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        enc_btn = ModernButton(
            btn_frame,
            text="Encrypt",
            command=self._encrypt_text
        )
        enc_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        dec_btn = ModernButton(
            btn_frame,
            text="Decrypt",
            command=self._decrypt_text
        )
        dec_btn.pack(side=tk.LEFT, padx=5)
        
        brute_btn = ModernButton(
            btn_frame,
            text="Brute Force",
            command=self._brute_force_text
        )
        brute_btn.pack(side=tk.LEFT, padx=5)
        
        # Output
        tk.Label(
            frame,
            text="Result:",
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor=tk.W, pady=(10, 0))
        
        self.encrypt_output = ModernText(frame, height=5)
        self.encrypt_output.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    def _setup_history_tab(self):
        """Setup history tab"""
        frame = tk.Frame(self.history_tab, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text="Analysis History",
            font=('Segoe UI', 14, 'bold')
        ).pack()
        
        # History listbox
        self.history_list = tk.Listbox(frame, height=8, font=('Segoe UI', 10))
        self.history_list.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Clear history button
        clear_history_btn = ModernButton(
            frame,
            text="Clear History",
            command=self._clear_history
        )
        clear_history_btn.pack()
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=('Segoe UI', 9),
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _apply_theme(self):
        """Apply current theme to all widgets"""
        bg = self.theme['bg_primary']
        fg = self.theme['text_primary']
        
        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)
        
        # Apply to all child widgets (simplified)
        for widget in self.main_frame.winfo_children():
            self._apply_theme_to_widget(widget)
    
    def _apply_theme_to_widget(self, widget):
        """Recursively apply theme to widget and children"""
        try:
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.theme['bg_primary'])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.theme['bg_primary'], fg=self.theme['text_primary'])
            elif isinstance(widget, tk.Button):
                if widget not in [self.theme_btn, self.show_btn]:
                    widget.configure(bg=self.theme['accent_primary'], fg='#1e1e2e')
        except:
            pass
        
        for child in widget.winfo_children():
            self._apply_theme_to_widget(child)
    
    def _toggle_theme(self):
        """Toggle between dark and light theme"""
        self.is_dark_mode = not self.is_dark_mode
        self.theme = Theme.get_theme(self.is_dark_mode)
        self.theme_btn.config(text="☀️ Light" if not self.is_dark_mode else "🌙 Dark")
        self._apply_theme()
    
    def _toggle_password_visibility(self):
        """Toggle password visibility in entry field"""
        current = self.password_entry['show']
        self.password_entry.config(show='' if current == '•' else '•')
        self.show_btn.config(text='🔒' if current == '•' else '👁️')
    
    def _update_strength_meter(self, score, label):
        """Update the strength progress bar"""
        max_score = 8
        percentage = (score / max_score) * 100
        
        self.strength_meter['value'] = percentage
        
        # Color based on strength (using progressbar style)
        if percentage < 40:
            self.strength_meter['style'] = 'red.Horizontal.TProgressbar'
        elif percentage < 70:
            self.strength_meter['style'] = 'yellow.Horizontal.TProgressbar'
        else:
            self.strength_meter['style'] = 'green.Horizontal.TProgressbar'
    
    def _analyze_password(self):
        """Main password analysis function"""
        password = self.password_entry.get()
        
        if not password:
            messagebox.showwarning("Warning", "Please enter a password first")
            return
        
        self.current_password = password
        self.status_bar.config(text="Analyzing password...")
        self.root.update()
        
        # Get strength analysis
        strength_result = self.checker.check_strength(password)
        
        # Check for breaches
        breach_result = self.breach_checker.check_password(password)
        
        # Update strength meter
        self._update_strength_meter(strength_result['score'], strength_result['strength'])
        
        # Display results
        self._display_results(strength_result, breach_result)
        
        # Add to history
        self._add_to_history(password, strength_result['strength'])
        
        self.status_bar.config(text="Analysis complete")
    
    def _display_results(self, strength_result, breach_result):
        """Display results in the text area"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Header
        self.result_text.insert(tk.END, "=" * 55 + "\n")
        self.result_text.insert(tk.END, "   PASSWORD SECURITY ANALYSIS\n")
        self.result_text.insert(tk.END, "=" * 55 + "\n\n")
        
        # Strength
        self.result_text.insert(
            tk.END,
            f"📊 Strength: {strength_result['strength']}\n",
            ('bold',)
        )
        self.result_text.insert(tk.END, f"📈 Score: {strength_result['score']}/{strength_result['max_score']}\n")
        self.result_text.insert(tk.END, f"🔑 Entropy: {strength_result['entropy']} bits\n\n")
        
        # Criteria
        self.result_text.insert(tk.END, "📋 Criteria Check:\n")
        for key, value in strength_result['criteria'].items():
            icon = "✅" if value else "❌"
            display = key.replace('_', ' ').title()
            self.result_text.insert(tk.END, f"   {icon} {display}\n")
        
        # Recommendations
        if strength_result['feedback']:
            self.result_text.insert(tk.END, "\n💡 Recommendations:\n")
            for f in strength_result['feedback']:
                self.result_text.insert(tk.END, f"   {f}\n")
        
        # Breach check
        self.result_text.insert(tk.END, "\n" + "-" * 40 + "\n")
        self.result_text.insert(tk.END, "🔍 Breach Check:\n")
        
        if breach_result:
            if breach_result[0] is None:
                self.result_text.insert(tk.END, f"⚠️ {breach_result[1]}\n")
            elif breach_result[0]:
                self.result_text.insert(
                    tk.END,
                    f"🚨 PASSWORD BREACHED! Found {breach_result[1]} times\n",
                    ('danger',)
                )
            else:
                self.result_text.insert(tk.END, "✅ No breaches found\n")
        
        self.result_text.insert(tk.END, "\n" + "=" * 55 + "\n")
        self.result_text.config(state=tk.DISABLED)
    
    def _save_report(self):
        """Save analysis report to file"""
        if not self.current_password:
            messagebox.showwarning("Warning", "No analysis to save")
            return
        
        # Get analysis data
        strength_result = self.checker.check_strength(self.current_password)
        breach_result = self.breach_checker.check_password(self.current_password)
        
        data = {
            **strength_result,
            'breach_info': {
                'is_breached': breach_result[0] if breach_result else None,
                'count': breach_result[1] if breach_result and breach_result[0] else 0
            }
        }
        
        try:
            filename = self.report_gen.save_report(data, 'txt')
            messagebox.showinfo("Success", f"Report saved: {filename}")
            self.status_bar.config(text=f"Report saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
    
    def _encrypt_password(self):
        """Encrypt the current password using Caesar cipher"""
        if not self.current_password:
            messagebox.showwarning("Warning", "No password to encrypt")
            return
        
        try:
            shift = int(self.encrypt_entry.get().replace('shift', '').strip())
        except:
            shift = 3
        
        encrypted = CaesarCipher.encrypt(self.current_password, shift)
        messagebox.showinfo("Encrypted", f"Encrypted password:\n\n{encrypted}")
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(encrypted)
        self.status_bar.config(text="Encrypted password copied to clipboard")
    
    def _encrypt_text(self):
        """Encrypt text in encryption tab"""
        text = self.encrypt_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text to encrypt")
            return
        
        try:
            shift = int(self.shift_spinbox.get())
        except:
            shift = 3
        
        result = CaesarCipher.encrypt(text, shift)
        self.encrypt_output.config(state=tk.NORMAL)
        self.encrypt_output.delete(1.0, tk.END)
        self.encrypt_output.insert(1.0, result)
        self.encrypt_output.config(state=tk.DISABLED)
    
    def _decrypt_text(self):
        """Decrypt text in encryption tab"""
        text = self.encrypt_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text to decrypt")
            return
        
        try:
            shift = int(self.shift_spinbox.get())
        except:
            shift = 3
        
        result = CaesarCipher.decrypt(text, shift)
        self.encrypt_output.config(state=tk.NORMAL)
        self.encrypt_output.delete(1.0, tk.END)
        self.encrypt_output.insert(1.0, result)
        self.encrypt_output.config(state=tk.DISABLED)
    
    def _brute_force_text(self):
        """Brute force decryption"""
        text = self.encrypt_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text to brute force")
            return
        
        results = CaesarCipher.brute_force(text)
        
        # Display results
        self.encrypt_output.config(state=tk.NORMAL)
        self.encrypt_output.delete(1.0, tk.END)
        for r in results[:10]:  # Show first 10
            self.encrypt_output.insert(tk.END, f"Shift {r['shift']}: {r['text']}\n")
        self.encrypt_output.config(state=tk.DISABLED)
    
    def _add_to_history(self, password, strength):
        """Add analysis to history"""
        entry = f"{password[:10]}... | {strength}"
        self.history_list.insert(0, entry)
        if self.history_list.size() > 50:  # Limit history
            self.history_list.delete(50)
    
    def _clear_history(self):
        """Clear history list"""
        self.history_list.delete(0, tk.END)
        self.status_bar.config(text="History cleared")
    
    def _clear_fields(self):
        """Clear all fields"""
        self.password_entry.delete(0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self._update_strength_meter(0, "No password")
        self.current_password = ""
        self.status_bar.config(text="Fields cleared")