import tkinter as tk
from utility.config import colors,spacing, fonts
from components.CardItem import  CardItem

def  create_section_recommendation(self, parent, titulo, itens):
        
        header_frame = tk.Frame(parent, bg=colors['bg_white'])
        header_frame.pack(fill=tk.X, pady=(spacing['lg'], spacing['sm']))
        
        tk.Label(
            header_frame,
            text=titulo,
            font=fonts['title_medium'],
            bg=colors['bg_white'],
            fg=colors['text_dark']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            header_frame,
            text=f"({len(itens)} {'item' if len(itens) == 1 else 'itens'})",
            font=fonts['body'],
            bg=colors['bg_white'],
            fg=colors['text_secondary']
        ).pack(side=tk.LEFT, padx=(spacing['sm'], 0))
        
        tk.Frame(
            parent,
            bg=colors['primary'],
            height=2
        ).pack(fill=tk.X, pady=(0, spacing['md']))
        
        for item in itens:
            card = CardItem(
                parent,
                item,
                on_edit=None,
                on_delete=None  
            )
            card.pack(fill=tk.X, pady=(0, spacing['md']))