import tkinter as tk
from components.TitlePage import TitlePage
from utility.config import colors, fonts
from components.Card import Card
from utility.ui_config import title

def page_settings(self):  

    container = tk.Frame(self.

principal_area, bg=colors['bg_white'])
    container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
    
    TitlePage(container, title['configuracoes']).pack(anchor='w', pady=(0, 20))
    
    card = Card(container)
    card.pack(fill=tk.X, pady=10)
    
    tk.Label(card, text='ℹ️ Informações', font=fonts['title_medium'],
            bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
    
    stats = self.db.get_statistics()
    for label, value in [('Versão', '1.0.0'), ('Banco', 'cineGamer.db'),
                        ('Registros', stats['total_itens'])]:
        row = tk.Frame(card, bg=colors['bg_card'])
        row.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(row, text=label, font=fonts['body'],
                bg=colors['bg_card'], fg=colors['text_dark']).pack(side=tk.LEFT)
        tk.Label(row, text=str(value), font=fonts['body_bold'],
                bg=colors['bg_card'], fg=colors['text_secondary']).pack(side=tk.RIGHT)
    
    tk.Frame(card, bg=colors['bg_card'], height=15).pack()