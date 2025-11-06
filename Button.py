import tkinter as tk
from config import cores, fonts

class button(tk.Button):

    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        styles = {
            'primary': {'bg': cores['secund'], 'fg': cores['text_white'], 'hover': '#2980B9'},
            'success': {'bg': cores['success'], 'fg': cores['text_white'], 'hover': '#229954'},
            'erro': {'bg': cores['erro'], 'fg': cores['text_white'], 'hover': '#C0392B'},
            'alert': {'bg': cores['alert'], 'fg': cores['text_white'], 'hover': '#D68910'},
            'secund': {'bg': cores['bg_white'], 'fg': cores['text_dark'], 'hover': '#D5DBDB'},
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

        # Efeitos hover
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def _on_enter(self, e):
        self.config(bg=self.cor_hover)

    def _on_leave(self, e):
        self.config(bg=self.cor_normal)