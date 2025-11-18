import tkinter as tk
from page.ChartWidget import ChartWidget 
from components.TitlePage import TitlePage
from utility.config import colors, fonts
from components.Card import Card
from utility.ui_config import title

def page_statistics(self):
    
    container = tk.Frame(self.area_principal, bg=colors['bg_white'])
    container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
    
    TitlePage(container, title['estatisticas']).pack(anchor='w', pady=(0, 20))
    
    stats = self.db.get_statistics()
    rating_dist = self.db.get_rating_distribution()
    
    canvas_scroll = tk.Canvas(container, bg=colors['bg_white'], highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas_scroll.yview)
    scrollable = tk.Frame(canvas_scroll, bg=colors['bg_white'])
    
    scrollable.bind('<Configure>', lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all')))
    canvas_scroll.create_window((0, 0), window=scrollable, anchor='nw')
    canvas_scroll.configure(yscrollcommand=scrollbar.set)
    
    canvas_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    if stats['per_type']:
        card1 = Card(scrollable)
        card1.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(card1, text='📊 Distribuição por Tipo', font=fonts['title_medium'],
                 bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        chart1 = ChartWidget(card1)
        chart1.pack(fill=tk.BOTH, expand=True)
        chart1.create_pie_chart(stats['per_type'], 'Filmes vs Séries vs Jogos')

    
    if stats['top_genres']:
        card2 = Card(scrollable)
        card2.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(card2, text='🎭 Top 5 Gêneros', font=fonts['title_medium'],
                 bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        chart2 = ChartWidget(card2)
        chart2.pack(fill=tk.BOTH, expand=True)
        top_genres_dict = {genre: count for genre, count in stats['top_genres']}
        chart2.create_bar_chart(top_genres_dict, 'Gêneros Mais Populares')

    if stats['per_status']:
        card3 = Card(scrollable)
        card3.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(card3, text='📋 Distribuição por Status', font=fonts['title_medium'],
                 bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        chart3 = ChartWidget(card3)
        chart3.pack(fill=tk.BOTH, expand=True)
        chart3.create_horizontal_bar_chart(stats['per_status'], 'Status dos Itens')

    if stats['by_year']:
        card4 = Card(scrollable)
        card4.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(card4, text='📅 Itens por Ano', font=fonts['title_medium'],
                 bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        chart4 = ChartWidget(card4)
        chart4.pack(fill=tk.BOTH, expand=True)
        chart4.create_line_chart(stats['by_year'], 'Lançamentos ao Longo dos Anos')

    if rating_dist:
        card5 = Card(scrollable)
        card5.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(card5, text='⭐ Distribuição de Avaliações', font=fonts['title_medium'],
                 bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        chart5 = ChartWidget(card5)
        chart5.pack(fill=tk.BOTH, expand=True)
        chart5.create_rating_chart(rating_dist, 'Quantas estrelas você deu?')