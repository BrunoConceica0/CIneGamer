import tkinter as tk
from tkinter import ttk
from config import cores, fonts, spacing

class Card(tk.Frame):
    #Card branco com sombra (simulada) para conteúdo
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=cores['bg_card'],
            relief=tk.RAISED,
            bd=1,
            **kwargs
        )





