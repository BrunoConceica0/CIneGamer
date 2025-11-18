import tkinter as tk
from utility.config import colors, fonts, spacing         

class CardItem(tk.Frame):
    #Card para exibir um item da coleção
    
    def __init__(self, parent, item, on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, bg=colors['bg_card'], relief=tk.RAISED, bd=2, **kwargs)
        
        self.item = item
        
        container = tk.Frame(self, bg=colors['bg_card'])
        container.pack(fill=tk.BOTH, expand=True, padx=spacing['md'], pady=spacing['md'])
        
        header = tk.Frame(container, bg=colors['bg_card'])
        header.pack(fill=tk.X, pady=(0, spacing['sm']))
  
        icones_types = {'Filme': '🎬', 'Série': '📺', 'Jogo': '🎮'}
        icone = icones_types.get(item[2], '📁')
        
        tk.Label(
            header,
            text=icone,
            font=('Segoe UI', 20),
            bg=colors['bg_card']
        ).pack(side=tk.LEFT, padx=(0, spacing['sm']))
        
        
        tk.Label(
            header,
            text=item[1],  
            font=fonts['title_small'],
            bg=colors['bg_card'],
            fg=colors['text_dark']
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        info_frame = tk.Frame(container, bg=colors['bg_card'])
        info_frame.pack(fill=tk.X, pady=spacing['xs'])

        info1 = f"{item[2]} • {item[3]}"
        if item[4]:  
            info1 += f" • {item[4]}"
        
        tk.Label(
            info_frame,
            text=info1,
            font=fonts['body'],
            bg=colors['bg_card'],
            fg=colors['text_secondary']
        ).pack(anchor='w')
        

        info2_frame = tk.Frame(info_frame, bg=colors['bg_card'])
        info2_frame.pack(fill=tk.X, pady=(spacing['xs'], 0))

        stars = '⭐' * item[5] if item[5] else 'Sem avaliação'
        tk.Label(
            info2_frame,
            text=stars,
            font=fonts['body'],
            bg=colors['bg_card'],
            fg=colors['alert']
        ).pack(side=tk.LEFT)

        colors_status = {
            'Assistido': colors['success'],
            'Assistindo': colors['info'],
            'Pendente': colors['alert'],
            'Abandonado': colors['erro']
        }
        cor_status = colors_status.get(item[6], colors['text_secondary'])
        
        status_label = tk.Label(
            info2_frame,
            text=item[6],
            font=fonts['small'],
            bg=cor_status,
            fg=colors['text_white'],
            padx=spacing['sm'],
            pady=spacing['xs']
        )
        status_label.pack(side=tk.RIGHT)
        
        # Tempo (se houver)
        if item[7] and item[7] > 0:  
            hours = item[7] // 60
            minutes = item[7] % 60
            time_text = f"{hours}h {minutes}min" if hours > 0 else f"{minutes}min"
            
            tk.Label(
                info2_frame,
                text=f"⏱️ {time_text}",
                font=fonts['body'],
                bg=colors['bg_card'],
                fg=colors['text_secondary']
            ).pack(side=tk.RIGHT, padx=(0, spacing['md']))
        
        if on_edit or on_delete:
            btn_frame = tk.Frame(container, bg=colors['bg_card'])
            btn_frame.pack(fill=tk.X, pady=(spacing['md'], 0))
            
            if on_edit:
                btn_editar = tk.Button(
                    btn_frame,
                    text='✏️ Editar',
                    command=lambda: on_edit(item[0]),
                    bg=colors['info'],
                    fg=colors['text_white'],
                    font=fonts['small'],
                    relief=tk.FLAT,
                    cursor='hand2',
                    padx=spacing['sm'],
                    pady=spacing['xs']
                )
                btn_editar.pack(side=tk.LEFT, padx=(0, spacing['xs']))
            
            if on_delete:
                btn_deletar = tk.Button(
                    btn_frame,
                    text='🗑️ Deletar',
                    command=lambda: on_delete(item[0]),
                    bg=colors['erro'],
                    fg=colors['text_white'],
                    font=fonts['small'],
                    relief=tk.FLAT,
                    cursor='hand2',
                    padx=spacing['sm'],
                    pady=spacing['xs']
                )
                btn_deletar.pack(side=tk.LEFT)