import tkinter as tk
from utility.config import colors, fonts, spacing

class sidebar(tk.Frame):
    
    def __init__(self, parent, icone, text, command, **kwargs):
        super().__init__(parent, bg=colors['bg_sidebar'], cursor='hand2', **kwargs)
        
        self.command = command
        self.selector = False
        
        container = tk.Frame(self, bg=colors['bg_sidebar'])
        container.pack(fill=tk.BOTH, expand=True, padx=spacing['md'], pady=spacing['sm'])
        
        self.icone_label = tk.Label(
            container,
            text=icone,
            font=fonts['menu_icone'],
            bg=colors['bg_sidebar'],
            fg=colors['text_menu']
        )
        self.icone_label.pack(side=tk.LEFT, padx=(spacing['sm'], spacing['md']))
        
        self.text_label = tk.Label(
            container,
            text=text,
            font=fonts['menu'],
            bg=colors['bg_sidebar'],
            fg=colors['text_menu'],
            anchor='w'
        )
        self.text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.bind('<Button-1>', self._on_click)
        container.bind('<Button-1>', self._on_click)
        self.icone_label.bind('<Button-1>', self._on_click)
        self.text_label.bind('<Button-1>', self._on_click)
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        container.bind('<Enter>', self._on_enter)
        container.bind('<Leave>', self._on_leave)
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        if not self.selector:
            self.config(bg=colors['hover_sidebar'])
            for widget in self.winfo_children():
                self._change_bg_recursive(widget, colors['hover_sidebar'])
    
    def _on_leave(self, event):
        if not self.selector:
            self.config(bg=colors['bg_sidebar'])
            for widget in self.winfo_children():
                self._change_bg_recursive(widget, colors['bg_sidebar'])
    
    def _change_bg_recursive(self, widget, cor):
        try:
            widget.config(bg=cor)
        except:
            pass
        for child in widget.winfo_children():
            self._change_bg_recursive(child, cor)
    
    def select(self):
        self.selector = True
        self.config(bg=colors['hover'])
        for widget in self.winfo_children():
            self._change_bg_recursive(widget, colors['hover'])
        self.icone_label.config(fg=colors['accent'])
        self.text_label.config(fg=colors['text_white'], font=fonts['body_negrito'])
    
    def deselect(self):
        self.selector = False
        self.config(bg=colors['bg_sidebar'])
        for widget in self.winfo_children():
            self._change_bg_recursive(widget, colors['bg_sidebar'])
        self.icone_label.config(fg=colors['text_menu'])
        self.text_label.config(fg=colors['text_menu'], font=fonts['menu'])

    def clean(self):
        if isinstance(self.widget, tk.Text):
            self.widget.delete('1.0', tk.END)
        else:
            self.widget.delete(0, tk.END)


