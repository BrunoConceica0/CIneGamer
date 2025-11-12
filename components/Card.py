import tkinter as tk
from tkinter import ttk
from utility.config import colors, fonts, spacing

class Card(tk.Frame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=colors['bg_card'],
            relief=tk.RAISED,
            bd=1,
            **kwargs
        )
