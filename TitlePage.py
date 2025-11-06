import tkinter as tk
from config import cores , fonts
class TitlePage(tk.Label):
    #Título padrão para páginas
    
    def __init__(self, parent, text, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=fonts['title_big'],
            bg=cores['bg_white'],
            fg=cores['text_dark'],
            anchor='w',
            **kwargs
        )
