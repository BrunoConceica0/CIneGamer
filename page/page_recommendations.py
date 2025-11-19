import tkinter as tk
from components.TitlePage import TitlePage
from utility.config import colors, fonts
from components.Card import Card
from utility.ui_config import title
from hooks.sectionRecommendation import renderRecommendation

def page_recommendations(parent_app):
    container = tk.Frame(parent_app.principal_area, bg=colors['bg_white'])
    container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    TitlePage(container, title['recomendacoes']).pack(anchor='w', pady=(0, 5))
    
    tk.Label(
        container,
        text='Baseado nos itens que você avaliou com 4⭐ ou 5⭐',
        font=fonts['body'],
        bg=colors['bg_white'],
        fg=colors['text_secondary']
    ).pack(anchor='w', pady=(0, 20))
    
    recomendacoes = parent_app.db.get_recommendations(30)
    
    if not recomendacoes:
        card = Card(container)
        card.pack(fill=tk.BOTH, expand=True)
        
        empty_frame = tk.Frame(card, bg=colors['bg_card'])
        empty_frame.pack(expand=True, pady=80)
        
        tk.Label(
            empty_frame,
            text='⭐',
            font=('Segoe UI', 64),
            bg=colors['bg_card'],
            fg=colors['alert']
        ).pack(pady=(20, 10))
        
        tk.Label(
            empty_frame,
            text='Nenhuma recomendação disponível',
            font=fonts['title_medium'],
            bg=colors['bg_card'],
            fg=colors['text_dark']
        ).pack(pady=5)
        
        tk.Label(
            empty_frame,
            text='Avalie seus filmes, séries e jogos com 4⭐ ou 5⭐\npara receber recomendações personalizadas!',
            font=fonts['body'],
            bg=colors['bg_card'],
            fg=colors['text_secondary'],
            justify='center'
        ).pack(pady=10)
    else:
        stats_frame = tk.Frame(container, bg=colors['bg_white'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        total_rec = len(recomendacoes)
        filmes_count = len([r for r in recomendacoes if r[2] == 'Filme'])
        series_count = len([r for r in recomendacoes if r[2] == 'Série'])
        jogos_count = len([r for r in recomendacoes if r[2] == 'Jogo'])
        
        for i, (icone, texto, valor, cor) in enumerate([
            ('🎯', 'Total', total_rec, colors['primary']),
            ('🎬', 'Filmes', filmes_count, colors['secondary']),
            ('📺', 'Séries', series_count, colors['info']),
            ('🎮', 'Jogos', jogos_count, colors['success'])
        ]):
            mini_card = Card(stats_frame)
            mini_card.grid(row=0, column=i, padx=8, sticky='nsew')
            stats_frame.columnconfigure(i, weight=1)
            
            tk.Label(mini_card, text=f"{icone} {texto}", font=fonts['body'],
                    bg=colors['bg_card'], fg=colors['text_secondary']).pack(pady=(12, 5))
            tk.Label(mini_card, text=str(valor), font=fonts['title_medium'],
                    bg=colors['bg_card'], fg=cor).pack(pady=(0, 12))
        
        scroll_frame = tk.Frame(container, bg=colors['bg_white'])
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(scroll_frame, bg=colors['bg_white'], highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient='vertical', command=canvas.yview)
        
        scrollable = tk.Frame(canvas, bg=colors['bg_white'])
        scrollable.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        filmes = [r for r in recomendacoes if r[2] == 'Filme']
        series = [r for r in recomendacoes if r[2] == 'Série']
        jogos = [r for r in recomendacoes if r[2] == 'Jogo']
        
        if filmes:
            renderRecommendation(scrollable, '🎬 Filmes Recomendados', filmes)
        
        if series:
            renderRecommendation(scrollable, '📺 Séries Recomendadas', series)
        
        if jogos:
            renderRecommendation(scrollable, '🎮 Jogos Recomendados', jogos)