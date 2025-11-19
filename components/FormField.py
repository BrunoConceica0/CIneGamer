import tkinter as tk
from tkinter import ttk
from utility.config import colors, fonts
from utility.ui_config import placeholder as PLACEHOLDERS

class FormField(tk.Frame):
    
    def __init__(self, parent, label, field_type='entry', required=False, 
                 options=None, placeholder_text='', initial_value=None, **kwargs):
        super().__init__(parent, bg=colors['bg_white'])
        
        self.field_type = field_type
        self.required = required
        self.widget = None
        self.placeholder_text = placeholder_text
        
        label_text = f"{label} *" if required else label
        self.label = tk.Label(
            self,
            text=label_text,
            font=fonts['body'],
            bg=colors['bg_white'],
            fg=colors['text_dark'],
            anchor='w'
        )
        self.label.pack(fill=tk.X, pady=(0, 8))
        
        if field_type == 'entry':
            self._create_entry(placeholder_text, initial_value, **kwargs)
        elif field_type == 'select':
            self._create_select(options, placeholder_text, initial_value, **kwargs)
        elif field_type == 'textarea':
            self._create_textarea(placeholder_text, initial_value, **kwargs)
        elif field_type == 'number':
            self._create_number(placeholder_text, initial_value, **kwargs)
    
    def _create_entry(self, placeholder_text, initial_value, **kwargs):
        self.widget = tk.Entry(
            self,
            font=fonts['body'],
            bg=colors['bg_white'],
            fg=colors['text_dark'],
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=colors['gray'],
            highlightcolor=colors['primary']
        )
        self.widget.pack(fill=tk.X, ipady=8, ipadx=12)
        
        if placeholder_text and not initial_value:
            self.widget.insert(0, placeholder_text)
            self.widget.config(fg=colors['text_secondary'])
            self.widget.bind('<FocusIn>', self._on_entry_focus_in)
            self.widget.bind('<FocusOut>', self._on_entry_focus_out)
        
        if initial_value:
            self.widget.insert(0, initial_value)
    
    def _create_select(self, options, placeholder_text, initial_value, **kwargs):
        self.var = tk.StringVar()
        select_options = [placeholder_text] + (options if options else [])
        self.widget = ttk.Combobox(
            self,
            textvariable=self.var,
            values=select_options,
            state='readonly',
            font=fonts['body']
        )
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'TCombobox',
            fieldbackground=colors['bg_white'],
            background=colors['bg_white'],
            foreground=colors['text_dark'],
            arrowcolor=colors['text_dark'],
            bordercolor='#E5E7EB',
            lightcolor=colors['bg_white'],
            darkcolor=colors['bg_white']
        )
        
        style.map('TCombobox', 
                 fieldbackground=[('readonly', colors['bg_white'])],
                 selectbackground=[('readonly', colors['bg_white'])],
                 selectforeground=[('readonly', colors['text_dark'])])
        
        self.widget.pack(fill=tk.X, ipady=8)
        
        if initial_value and initial_value in options:
            self.widget.set(initial_value)
            self.widget.config(foreground=colors['text_dark'])
        else:
            self.widget.set(placeholder_text)
    
    def _create_textarea(self, placeholder_text, initial_value, **kwargs):
        frame = tk.Frame(self, bg=colors['bg_white'])
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.widget = tk.Text(
            frame,
            font=fonts['body'],
            bg=colors['bg_white'],
            fg=colors['text_dark'],
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground='#E5E7EB',
            highlightcolor=colors['primary'],
            wrap=tk.WORD,
            height=5
        )
        self.widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        scrollbar = tk.Scrollbar(frame, command=self.widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.widget.config(yscrollcommand=scrollbar.set)
        
        if placeholder_text and not initial_value:
            self.widget.insert('1.0', placeholder_text)
            self.widget.config(fg=colors['text_secondary'])
            self.widget.bind('<FocusIn>', self._on_text_focus_in)
            self.widget.bind('<FocusOut>', self._on_text_focus_out)
        
        if initial_value:
            self.widget.insert('1.0', initial_value)
    
    def _create_number(self, placeholder_text, initial_value, **kwargs):
        self.widget = tk.Entry(
            self,
            font=fonts['body'],
            bg=colors['bg_white'],
            fg=colors['text_dark'],
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground='#E5E7EB',
            highlightcolor=colors['primary']
        )
        self.widget.pack(fill=tk.X, ipady=8, ipadx=12)
        
        vcmd = (self.widget.register(self._validate_number), '%P')
        self.widget.config(validate='key', validatecommand=vcmd)
        
        if initial_value:
            self.widget.insert(0, str(initial_value))
        elif placeholder_text:
            self.widget.insert(0, placeholder_text)
            self.widget.config(fg=colors['text_secondary'])
            self.widget.bind('<FocusIn>', self._on_entry_focus_in)
            self.widget.bind('<FocusOut>', self._on_entry_focus_out)
    
    def _validate_number(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def _on_entry_focus_in(self, event):
        if self.widget.cget('fg') == colors['text_secondary']:
            self.widget.delete(0, tk.END)
            self.widget.config(fg=colors['text_dark'])
    
    def _on_entry_focus_out(self, event):
        if not self.widget.get():
            self.widget.insert(0, self.placeholder_text)
            self.widget.config(fg=colors['text_secondary'])
    
    def _on_text_focus_in(self, event):
        content = self.widget.get('1.0', 'end-1c')
        if content == self.placeholder_text:
            self.widget.delete('1.0', tk.END)
            self.widget.config(fg=colors['text_dark'])
    
    def _on_text_focus_out(self, event):
        if not self.widget.get('1.0', 'end-1c').strip():
            self.widget.insert('1.0', self.placeholder_text)
            self.widget.config(fg=colors['text_secondary'])
    
    def get(self):
        if self.field_type == 'textarea':
            value = self.widget.get('1.0', 'end-1c').strip()
            if value == self.placeholder_text:
                return ''
        elif self.field_type == 'select':
            value = self.var.get()
            if value == self.placeholder_text:
                return ''
        else:
            value = self.widget.get().strip()
            if value == self.placeholder_text:
                return ''
        
        return value if value else ''
    
    def set(self, value):
        if self.field_type == 'textarea':
            self.widget.delete('1.0', tk.END)
            if value:
                self.widget.insert('1.0', value)
                self.widget.config(fg=colors['text_dark'])
        elif self.field_type == 'select':
            if value in self.widget.cget('values'):
                self.var.set(value)
                self.widget.config(foreground=colors['text_dark'])
            else:
                self.var.set(self.widget.cget('values')[0])
        else:
            self.widget.delete(0, tk.END)
            if value:
                self.widget.insert(0, value)
                self.widget.config(fg=colors['text_dark'])