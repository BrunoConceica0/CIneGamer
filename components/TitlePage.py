import tkinter as tk
from utility.config import colors , fonts
class TitlePage(tk.Label):
    
    def __init__(self, parent, text, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=fonts['title_big'],
            bg=colors['bg_white'],
            fg=colors['text_dark'],
            anchor='w',
            **kwargs
        )
