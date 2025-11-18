    
import tkinter as tk
from page.ChartWidget import ChartWidget 
from components.TitlePage import TitlePage
from utility.config import colors, fonts
from components.Card import Card
from utility.ui_config import title
from components.Button import button

def page_recommendations(self):
        container = tk.Frame(self.area_principal, bg=colors['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['recomendacoes']).pack(anchor='w', pady=(0, 5))
        
        tk.Label(
            container,
            text='Baseado nos itens que você avaliou com 4⭐ ou 5⭐',
            font=fonts['body'],
            bg=colors['bg_white'],
            fg=colors['text_secondary']
        ).pack(anchor='w', pady=(0, 20))
        
        recomendacoes = self.db.get_recommendations(20)
        
        if not recomendacoes:
            card = Card(container)
            card.pack(fill=tk.BOTH, expand=True)
            
            empty_frame = tk.Frame(card, bg=colors['bg_card'])
            empty_frame.pack(expand=True, pady=50)
            
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
            
            button(
                empty_frame,
                '➕ Adicionar Avaliações',
                command=lambda: self.show_page('colecao'),
                style='primary'
            ).pack(pady=(20, 20))
        else:
            # Mostrar recomendações com scroll
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
                self.create_section_recommendation(scrollable, '🎬 Filmes Recomendados', filmes)
            
            if series:
                self.create_section_recommendation(scrollable, '📺 Séries Recomendadas', series)
            
            if jogos:
                self.create_section_recommendation(scrollable, '🎮 Jogos Recomendados', jogos)