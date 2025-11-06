import tkinter as tk
from config import cores, fonts, spacing
from tkinter import ttk

class InputComposition(tk.Frame):
    #Campo de entrada com label
    
    def __init__(self, parent, label, types='entry', values=None, **kwargs):
        super().__init__(parent, bg=cores['bg_white'])
        
        # Label
        tk.Label(
            self,
            text=label,
            font=fonts['body_negrito'],
            bg=cores['bg_white'],
            fg=cores['text_dark']
        ).pack(anchor='w', pady=(0, spacing['xs']))
        
        # Widget de entrada
        if types == 'entry':
            self.widget = tk.Entry(self, font=fonts['body'], **kwargs)
            self.widget.pack(fill=tk.X)
        
        elif types == 'combo':
            self.widget = ttk.Combobox(
                self,
                font=fonts['body'],
                values=values or [],
                state='readonly',
                **kwargs
            )
            self.widget.pack(fill=tk.X)
            if values:
                self.widget.current(0)
        
        elif types == 'text':
            self.widget = tk.Text(self, font=fonts['body'], height=4, **kwargs)
            self.widget.pack(fill=tk.BOTH, expand=True)
        
        elif types == 'spinbox':
            self.widget = tk.Spinbox(self, font=fonts['body'], **kwargs)
            self.widget.pack(fill=tk.X)
    
    def get(self):
        #Obtém o value do campo
        if isinstance(self.widget, tk.Text):
            return self.widget.get('1.0', tk.END).strip()
        return self.widget.get()
    
    def set(self, value):
        
        #Define o value do campo
        if isinstance(self.widget, tk.Text):
            self.widget.delete('1.0', tk.END)
            self.widget.insert('1.0', value)
        elif isinstance(self.widget, ttk.Combobox):
            self.widget.set(value)
        else:
            self.widget.delete(0, tk.END)
            self.widget.insert(0, value)