import tkinter as tk
from utility.config import colors, fonts
from components.Card import Card

def render_recommendation_cards(parent, titulo, itens):
    section_frame = tk.Frame(parent, bg=colors['bg_white'])
    section_frame.pack(fill=tk.X, pady=(0, 20))
    
    tk.Label(
        section_frame,
        text=titulo,
        font=fonts['title_small'],
        bg=colors['bg_white'],
        fg=colors['text_dark']
    ).pack(anchor='w', pady=(0, 15))
    
    for idx, item in enumerate(itens):
        if idx % 2 == 0:
            row_frame = tk.Frame(section_frame, bg=colors['bg_white'])
            row_frame.pack(fill=tk.X, pady=(0, 15))
            row_frame.columnconfigure(0, weight=1)
            row_frame.columnconfigure(1, weight=1)
        
        col = idx % 2
        card = Card(row_frame)
        card.grid(row=0, column=col, sticky='nsew', padx=(0, 15) if col == 0 else (0, 0))
        
        card_content = tk.Frame(card, bg=colors['bg_card'])
        card_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        header_frame = tk.Frame(card_content, bg=colors['bg_card'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame,
            text=item[1],
            font=fonts['body_bold'],
            bg=colors['bg_card'],
            fg=colors['text_dark'],
            anchor='w'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tipo_colors = {
            'Filme': colors['primary'],
            'Série': colors['info'],
            'Jogo': colors['success']
        }
        
        tipo_badge = tk.Label(
            header_frame,
            text=item[2],
            font=('Segoe UI', 9),
            bg=tipo_colors.get(item[2], colors['primary']),
            fg=colors['text_white'],
            padx=8,
            pady=2
        )
        tipo_badge.pack(side=tk.RIGHT, padx=(10, 0))
        
        info_frame = tk.Frame(card_content, bg=colors['bg_card'])
        info_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(
            info_frame,
            text=f"📁 {item[3]}",
            font=('Segoe UI', 10),
            bg=colors['bg_card'],
            fg=colors['text_secondary']
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        if item[4]:
            tk.Label(
                info_frame,
                text=f"📅 {item[4]}",
                font=('Segoe UI', 10),
                bg=colors['bg_card'],
                fg=colors['text_secondary']
            ).pack(side=tk.LEFT, padx=(0, 15))
        
        if item[5]:
            stars = '⭐' * item[5]
            tk.Label(
                info_frame,
                text=stars,
                font=('Segoe UI', 10),
                bg=colors['bg_card'],
                fg=colors['alert']
            ).pack(side=tk.LEFT)
        
        tk.Frame(card_content, bg='#E5E7EB', height=1).pack(fill=tk.X, pady=10)
        
        obs_frame = tk.Frame(card_content, bg=colors['bg_card'])
        obs_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        if item[8] and item[8].strip():
            tk.Label(
                obs_frame,
                text="💬 Comentário:",
                font=('Segoe UI', 10, 'bold'),
                bg=colors['bg_card'],
                fg=colors['text_dark'],
                anchor='w'
            ).pack(fill=tk.X, pady=(0, 5))
            
            comment_text = item[8]
            if len(comment_text) > 150:
                comment_text = comment_text[:150] + '...'
            
            tk.Label(
                obs_frame,
                text=comment_text,
                font=('Segoe UI', 10),
                bg=colors['bg_card'],
                fg=colors['text_secondary'],
                anchor='w',
                justify='left',
                wraplength=400
            ).pack(fill=tk.X)
        else:
            tk.Label(
                obs_frame,
                text="💭 Sem comentários",
                font=('Segoe UI', 10),
                bg=colors['bg_card'],
                fg=colors['text_secondary'],
                anchor='w',
                justify='left',
                wraplength=400
            ).pack(fill=tk.X)
        
        footer_frame = tk.Frame(card_content, bg=colors['bg_card'])
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_colors = {
            'Assistido': colors['success'],
            'Assistindo': colors['info'],
            'Pendente': colors['alert'],
            'Abandonado': colors['erro']
        }
        
        tk.Label(
            footer_frame,
            text=f"📊 {item[6]}",
            font=('Segoe UI', 10),
            bg=colors['bg_card'],
            fg=status_colors.get(item[6], colors['text_secondary'])
        ).pack(side=tk.LEFT)
        
        if item[7] and item[7] > 0:
            horas = item[7] // 60
            minutos = item[7] % 60
            
            if horas > 0:
                tempo_text = f"⏱️ {horas}h {minutos}min"
            else:
                tempo_text = f"⏱️ {minutos}min"
            
            tk.Label(
                footer_frame,
                text=tempo_text,
                font=('Segoe UI', 10),
                bg=colors['bg_card'],
                fg=colors['text_secondary']
            ).pack(side=tk.RIGHT)