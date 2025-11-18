import tkinter as tk
from tkinter import messagebox
from config.database import Database
from utility.config import colors, fonts, spacing
from components.Siderbar import sidebar 
from components.TitlePage import TitlePage
from components.Card import Card
from components.CardItem import CardItem
from components.Button import button
from components.InputComposition import InputComposition
from utility.ui_config import menu, title

class CineGamerApp:
    
    def __init__(self):
        self.root = tk.Tk()
        self.db = Database()
        self.configure_window()
        self.create_interface()
        self.show_page('inicio')
    
    def configure_window(self):
        """Configura a janela principal"""
        self.root.title(title["title"])
        self.root.geometry('1200x700')
        self.root.minsize(1200, 700)
        
        self.root.update_idletasks()
        largura = self.root.winfo_width()
        altura = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def create_interface(self):
        self.create_sidebar()
        self.area_principal = tk.Frame(self.root, bg=colors['bg_white'])
        self.area_principal.grid(row=0, column=1, sticky='nsew')
    
    def create_sidebar(self):
        frame_sidebar = tk.Frame(self.root, bg=colors['bg_sidebar'], width=200)
        frame_sidebar.grid(row=0, column=0, sticky='nsew')
        frame_sidebar.grid_propagate(False)
        
        header = tk.Frame(frame_sidebar, bg=colors['bg_sidebar'])
        header.pack(fill=tk.X, pady=(20, 30))
        
        tk.Label(header, text='🎬', font=('Segoe UI', 32),
                bg=colors['bg_sidebar'], fg=colors['text_white']).pack()
        tk.Label(header, text='CINEGAMER', font=('Segoe UI', 20, 'bold'),
                bg=colors['bg_sidebar'], fg=colors['text_white']).pack()
        
        tk.Frame(frame_sidebar, bg=colors['hover'], height=2).pack(fill=tk.X, padx=15)
        
        self.menu_botoes = {}
        nav_frame = tk.Frame(frame_sidebar, bg=colors['bg_sidebar'])
        nav_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        for id_page, icone, text in menu:
            btn = sidebar(nav_frame, icone, text, lambda p=id_page: self.show_page(p))
            btn.pack(fill=tk.X, pady=(0, 5))
            self.menu_botoes[id_page] = btn
    
    def show_page(self, page):
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        
        for btn in self.menu_botoes.values():
            btn.desselecionar()
        
        if page in self.menu_botoes:
            self.menu_botoes[page].selecionar()
        
        if page == 'inicio':
            self.page()
        elif page == 'colecao':
            self.page_colection()
        elif page == 'estatisticas':
            self.page_estatisticas()
        elif page == 'recomendacoes':
            self.page_recommendations()
        elif page == 'configuracoes':
            self.page_configuracoes()
    
    def page(self):
        container = tk.Frame(self.area_principal, bg=colors['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['inicio']).pack(anchor='w', pady=(0, 20))
        
        stats = self.db.get_statistics()
        
        # Cards de estatísticas
        stats_frame = tk.Frame(container, bg=colors['bg_white'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        for i, (titulo, valor, cor) in enumerate([
            ('📚 Total', stats['total_itens'], colors['primary']),
            ('⭐ Média', f"{stats['average_rating']}/5", colors['alert']),
            ('⏱️ Horas', f"{stats['time_total_hours']}h", colors['info'])
        ]):
            card = Card(stats_frame)
            card.grid(row=0, column=i, padx=10, sticky='nsew')
            stats_frame.columnconfigure(i, weight=1)
            
            tk.Label(card, text=titulo, font=fonts['body'],
                    bg=colors['bg_card'], fg=colors['text_secondary']).pack(pady=(15, 5))
            tk.Label(card, text=str(valor), font=fonts['title_big'],
                    bg=colors['bg_card'], fg=cor).pack(pady=(0, 15))
        
        # Distribuição
        card_tipos = Card(container)
        card_tipos.pack(fill=tk.X, pady=10)
        
        tk.Label(card_tipos, text='📊 Distribuição', font=fonts['title_small'],
                bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        for tipo, count in stats['per_type'].items():
            row = tk.Frame(card_tipos, bg=colors['bg_card'])
            row.pack(fill=tk.X, padx=20, pady=5)
            icones = {'Filme': '🎬', 'Série': '📺', 'Jogo': '🎮'}
            tk.Label(row, text=f"{icones.get(tipo, '📄')} {tipo}", font=fonts['body'],
                    bg=colors['bg_card'], fg=colors['text_dark']).pack(side=tk.LEFT)
            tk.Label(row, text=str(count), font=fonts['body_bold'],
                    bg=colors['bg_card'], fg=colors['secondary']).pack(side=tk.RIGHT)
        
        tk.Frame(card_tipos, bg=colors['bg_card'], height=15).pack()
        
        # Botões
        button(container, '➕ Adicionar Novo', command=self.add_item_dialog,
               style='primary').pack(anchor='w', pady=10)
    
    def page_colection(self):
        container = tk.Frame(self.area_principal, bg=colors['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['colecao']).pack(anchor='w', pady=(0, 20))
        
        button(container, '➕ Adicionar', command=self.add_item_dialog,
               style='success').pack(anchor='w', pady=(0, 15))
        
        # list com scroll
        list_frame = tk.Frame(container, bg=colors['bg_white'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(list_frame, bg=colors['bg_white'], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.list_current = tk.Frame(canvas, bg=colors['bg_white'])
        
        self.list_current.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.list_current, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.reload_list()
    
    def reload_list(self):
        for widget in self.list_current.winfo_children():
            widget.destroy()
        
        itens = self.db.list_content()
        
        if not itens:
            tk.Label(self.list_current, text='📭 Nenhum item',
                    font=fonts['title_medium'], bg=colors['bg_white'],
                    fg=colors['text_secondary']).pack(pady=50)
        else:
            for item in itens:
                card = CardItem(self.list_current, item,
                              on_edit=self.edit_item, on_delete=self.delete_item)
                card.pack(fill=tk.X, pady=(0, 10))
    
    def add_item_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('➕ Adicionar')
        dialog.geometry('500x700')
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        container = tk.Frame(dialog, bg=colors['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Campos
        name = InputComposition(container, 'name:*', types='entry')
        name.pack(fill=tk.X, pady=(0, 10))
        
        tipo = InputComposition(container, 'Tipo:*', types='combo',
                               values=['Filme', 'Série', 'Jogo'])
        tipo.pack(fill=tk.X, pady=(0, 10))
        
        genero = InputComposition(container, 'Gênero:*', types='entry')
        genero.pack(fill=tk.X, pady=(0, 10))
        
        ano = InputComposition(container, 'Ano:', types='spinbox', from_=1900, to=2030)
        ano.pack(fill=tk.X, pady=(0, 10))
        
        aval = InputComposition(container, 'Avaliação:', types='spinbox', from_=1, to=5)
        aval.pack(fill=tk.X, pady=(0, 10))
        
        status = InputComposition(container, 'Status:*', types='combo',
                                 values=['Assistido', 'Assistindo', 'Pendente', 'Abandonado'])
        status.pack(fill=tk.X, pady=(0, 10))
        
        time = InputComposition(container, 'time (min):', types='spinbox', from_=0, to=10000)
        time.pack(fill=tk.X, pady=(0, 10))
        
        obs = InputComposition(container, 'Obs:', types='text')
        obs.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        def save():
            if not name.get() or not tipo.get() or not genero.get() or not status.get():
                messagebox.showerror('Erro', 'Preencha campos obrigatórios (*)')
                return
            
            data = (name.get(), tipo.get(), genero.get(),
                   int(ano.get()) if ano.get() else None,
                   int(aval.get()) if aval.get() else None,
                   status.get(), int(time.get()) if time.get() else 0,
                   obs.get() if obs.get() else None)
            
            self.db.add_content(data)
            messagebox.showinfo('Sucesso', 'Item adicionado!')
            dialog.destroy()
            if hasattr(self, 'list_current'):
                self.reload_list()
        
        btn_frame = tk.Frame(container, bg=colors['bg_white'])
        btn_frame.pack(fill=tk.X)
        
        button(btn_frame, '💾 save', command=save, style='success').pack(side=tk.LEFT, padx=(0, 10))
        button(btn_frame, '❌ Cancelar', command=dialog.destroy, style='erro').pack(side=tk.LEFT)
    
    def edit_item(self, item_id):
            item_row = self.db.get_content(item_id)
            if not item_row:
                messagebox.showerror('Erro', 'Item não encontrado.')
                return
            
            # Converter para lista para acesso por índice/nome
            item = list(item_row) 
            
            dialog = tk.Toplevel(self.root)
            dialog.title(f'✏️ Editar: {item[1]}')
            dialog.geometry('500x700')
            dialog.transient(self.root)
            dialog.grab_set()
            
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
            y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
            dialog.geometry(f'+{x}+{y}')
            
            container = tk.Frame(dialog, bg=colors['bg_white'])
            container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            name = InputComposition(container, 'name:*', types='entry', initial_value=item[1])
            name.pack(fill=tk.X, pady=(0, 10))
            
            tipo = InputComposition(container, 'Tipo:*', types='combo',
                                values=['Filme', 'Série', 'Jogo'], initial_value=item[2])
            tipo.pack(fill=tk.X, pady=(0, 10))
            
            genero = InputComposition(container, 'Gênero:*', types='entry', initial_value=item[3])
            genero.pack(fill=tk.X, pady=(0, 10))
            
            ano = InputComposition(container, 'Ano:', types='spinbox', from_=1900, to=2030, initial_value=item[4])
            ano.pack(fill=tk.X, pady=(0, 10))
            
            aval = InputComposition(container, 'Avaliação:', types='spinbox', from_=1, to=5, initial_value=item[5])
            aval.pack(fill=tk.X, pady=(0, 10))
            
            status = InputComposition(container, 'Status:*', types='combo',
                                    values=['Assistido', 'Assistindo', 'Pendente', 'Abandonado'], initial_value=item[6])
            status.pack(fill=tk.X, pady=(0, 10))
            
            time = InputComposition(container, 'time (min):', types='spinbox', from_=0, to=10000, initial_value=item[7])
            time.pack(fill=tk.X, pady=(0, 10))
            
            obs = InputComposition(container, 'Obs:', types='text', initial_value=item[8])
            obs.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            def update():
                # Mesma validação do 'add'
                if not name.get() or not tipo.get() or not genero.get() or not status.get():
                    messagebox.showerror('Erro', 'Preencha campos obrigatórios (*)')
                    return
                
                # Dados para a função update_content
                data = (name.get(), tipo.get(), genero.get(),
                    int(ano.get()) if ano.get() else None,
                    int(aval.get()) if aval.get() else None,
                    status.get(), int(time.get()) if time.get() else 0,
                    obs.get() if obs.get() else None)
                
                # Chama o novo método de atualização do DB
                if self.db.update_content(item_id, data):
                    messagebox.showinfo('Sucesso', 'Item atualizado!')
                    dialog.destroy()
                    # Recarrega a lista se estiver na página de Coleção
                    if hasattr(self, 'list_current') and self.list_current.winfo_ismapped(): 
                        self.reload_list()
                    # Também recarrega as estatísticas se estiver nas páginas afetadas
                    if self.menu_botoes.get('inicio') and self.menu_botoes['inicio'].is_selected():
                        self.show_page('inicio')
                    elif self.menu_botoes.get('estatisticas') and self.menu_botoes['estatisticas'].is_selected():
                        self.show_page('estatisticas')
                    elif self.menu_botoes.get('recomendacoes') and self.menu_botoes['recomendacoes'].is_selected():
                        self.show_page('recomendacoes')
                else:
                    messagebox.showerror('Erro', 'Falha ao atualizar o item no banco de dados.')


            btn_frame = tk.Frame(container, bg=colors['bg_white'])
            btn_frame.pack(fill=tk.X)
            
            button(btn_frame, '💾 update', command=update, style='success').pack(side=tk.LEFT, padx=(0, 10))
            button(btn_frame, '❌ Cancelar', command=dialog.destroy, style='erro').pack(side=tk.LEFT)
    
    def delete_item(self, item_id):
        """Deletar item"""
        if messagebox.askyesno('Confirmar', 'Deletar este item?'):
            self.db.delete_content(item_id)
            messagebox.showinfo('Sucesso', 'Deletado!')
            self.reload_list()
    
    
    def page_estatisticas(self):
        """Página de Estatísticas com Gráficos"""
        container = tk.Frame(self.area_principal, bg=colors['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['estatisticas']).pack(anchor='w', pady=(0, 20))
        
        # Buscar estatísticas
        stats = self.db.get_statistics()
        rating_dist = self.db.get_rating_distribution()
        
        # Área com scroll
        canvas_scroll = tk.Canvas(container, bg=colors['bg_white'], highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas_scroll.yview)
        scrollable = tk.Frame(canvas_scroll, bg=colors['bg_white'])
        
        scrollable.bind('<Configure>', lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all')))
        canvas_scroll.create_window((0, 0), window=scrollable, anchor='nw')
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        canvas_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        from ChartWidget import ChartWidget
        
        # GRÁFICO 1: Pizza - Tipos
        if stats['per_type']:
            card1 = Card(scrollable)
            card1.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(card1, text='📊 Distribuição por Tipo', font=fonts['title_medium'],
                    bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
            
            chart1 = ChartWidget(card1)
            chart1.pack(fill=tk.BOTH, expand=True)
            chart1.create_pie_chart(stats['per_type'], 'Filmes vs Séries vs Jogos')
        
        # GRÁFICO 2: Barras - Top Gêneros
        if stats['top_genres']:
            card2 = Card(scrollable)
            card2.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(card2, text='🎭 Top 5 Gêneros', font=fonts['title_medium'],
                    bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
            
            chart2 = ChartWidget(card2)
            chart2.pack(fill=tk.BOTH, expand=True)
            top_genres_dict = {genre: count for genre, count in stats['top_genres']}
            chart2.create_bar_chart(top_genres_dict, 'Gêneros Mais Populares')
        
        # GRÁFICO 3: Barras Horizontal - Status
        if stats['per_status']:
            card3 = Card(scrollable)
            card3.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(card3, text='📋 Distribuição por Status', font=fonts['title_medium'],
                    bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
            
            chart3 = ChartWidget(card3)
            chart3.pack(fill=tk.BOTH, expand=True)
            chart3.create_horizontal_bar_chart(stats['per_status'], 'Status dos Itens')
        
        # GRÁFICO 4: Linhas - Por Ano
        if stats['by_year']:
            card4 = Card(scrollable)
            card4.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(card4, text='📅 Itens por Ano', font=fonts['title_medium'],
                    bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
            
            chart4 = ChartWidget(card4)
            chart4.pack(fill=tk.BOTH, expand=True)
            chart4.create_line_chart(stats['by_year'], 'Lançamentos ao Longo dos Anos')
        
        # GRÁFICO 5: Avaliações
        if rating_dist:
            card5 = Card(scrollable)
            card5.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(card5, text='⭐ Distribuição de Avaliações', font=fonts['title_medium'],
                    bg=colors['bg_card'], fg=colors['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
            
            chart5 = ChartWidget(card5)
            chart5.pack(fill=tk.BOTH, expand=True)
            chart5.create_rating_chart(rating_dist, 'Quantas estrelas você deu?')
    
    def page_recommendations(self):
        """Página de Recomendações"""
        container = tk.Frame(self.area_principal, bg=colors['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['recomendacoes']).pack(anchor='w', pady=(0, 5))
        
        # Subtítulo explicativo
        tk.Label(
            container,
            text='Baseado nos itens que você avaliou com 4⭐ ou 5⭐',
            font=fonts['body'],
            bg=colors['bg_white'],
            fg=colors['text_secondary']
        ).pack(anchor='w', pady=(0, 20))
        
        # Buscar recomendações
        recomendacoes = self.db.get_recommendations(20)
        
        if not recomendacoes:
            # Estado vazio - sem recomendações
            card = Card(container)
            card.pack(fill=tk.BOTH, expand=True)
            
            empty_frame = tk.Frame(card, bg=colors['bg_card'])
            empty_frame.pack(expand=True, pady=50)
            
            # Ícone
            tk.Label(
                empty_frame,
                text='⭐',
                font=('Segoe UI', 64),
                bg=colors['bg_card'],
                fg=colors['alert']
            ).pack(pady=(20, 10))
            
            # Título
            tk.Label(
                empty_frame,
                text='Nenhuma recomendação disponível',
                font=fonts['title_medium'],
                bg=colors['bg_card'],
                fg=colors['text_dark']
            ).pack(pady=5)
            
            # Mensagem
            tk.Label(
                empty_frame,
                text='Avalie seus filmes, séries e jogos com 4⭐ ou 5⭐\npara receber recomendações personalizadas!',
                font=fonts['body'],
                bg=colors['bg_card'],
                fg=colors['text_secondary'],
                justify='center'
            ).pack(pady=10)
            
            # Botão
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
            
            # Agrupar por tipo
            filmes = [r for r in recomendacoes if r[2] == 'Filme']
            series = [r for r in recomendacoes if r[2] == 'Série']
            jogos = [r for r in recomendacoes if r[2] == 'Jogo']
            
            # Mostrar cada tipo
            if filmes:
                self._criar_secao_recomendacao(scrollable, '🎬 Filmes Recomendados', filmes)
            
            if series:
                self._criar_secao_recomendacao(scrollable, '📺 Séries Recomendadas', series)
            
            if jogos:
                self._criar_secao_recomendacao(scrollable, '🎮 Jogos Recomendados', jogos)

    def _criar_secao_recomendacao(self, parent, titulo, itens):
        """Cria uma seção de recomendações por tipo"""
        
        # Header da seção
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
        
        # Linha separadora
        tk.Frame(
            parent,
            bg=colors['primary'],
            height=2
        ).pack(fill=tk.X, pady=(0, spacing['md']))
        
        # Cards dos itens
        for item in itens:
            card = CardItem(
                parent,
                item,
                on_edit=self.edit_item,
                on_delete=None  # Sem deletar em recomendações
            )
            card.pack(fill=tk.X, pady=(0, spacing['md']))
    
    def page_configuracoes(self):
        container = tk.Frame(self.area_principal, bg=colors['bg_white'])
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
    
    def executar(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = CineGamerApp()
    app.executar()
    
    def executar(self):
        self.root.mainloop()