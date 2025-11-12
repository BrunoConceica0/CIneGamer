import tkinter as tk
from utility.config import colors, fonts

class button(tk.Button):

    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        styles = {
            'primary': {'bg': colors['secund'], 'fg': colors['text_white'], 'hover': '#2980B9'},
            'success': {'bg': colors['success'], 'fg': colors['text_white'], 'hover': '#229954'},
            'erro': {'bg': colors['erro'], 'fg': colors['text_white'], 'hover': '#C0392B'},
            'alert': {'bg': colors['alert'], 'fg': colors['text_white'], 'hover': '#D68910'},
            'secund': {'bg': colors['bg_white'], 'fg': colors['text_dark'], 'hover': '#D5DBDB'},
        }

        selected_style = styles.get(style, styles["primary"])

        super().__init__(
            parent,
            text=text,
            command=command,
            bg=selected_style['bg'],
            fg=selected_style['fg'],
            font=fonts['body_bold'],
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10,
            **kwargs
        )

        self.cor_normal = selected_style['bg']
        self.cor_hover = selected_style['hover']

        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def _on_enter(self, e):
        self.config(bg=self.cor_hover)

    def _on_leave(self, e):
        self.config(bg=self.cor_normal)