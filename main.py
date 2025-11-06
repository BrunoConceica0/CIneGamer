import tkinter as tk
from tkinter import messagebox
from database import Database
from config import cores, fonts, spacing
from Siderbar import sidebar 
from TitlePage import TitlePage
from Card import Card
from CardItem import CardItem
from Button import button
from InputComposition import InputComposition
from ui_config import menu, title

class CineGamerApp:
    """Aplicação principal do CineGamer - COMPLETA E FUNCIONAL"""
    
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
        
        # Centralizar janela
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
        """Cria a interface principal"""
        self.create_sidebar()
        self.area_principal = tk.Frame(self.root, bg=cores['bg_white'])
        self.area_principal.grid(row=0, column=1, sticky='nsew')
    
    def create_sidebar(self):
        """Cria o menu lateral"""
        frame_sidebar = tk.Frame(self.root, bg=cores['bg_sidebar'], width=200)
        frame_sidebar.grid(row=0, column=0, sticky='nsew')
        frame_sidebar.grid_propagate(False)
        
        header = tk.Frame(frame_sidebar, bg=cores['bg_sidebar'])
        header.pack(fill=tk.X, pady=(20, 30))
        
        tk.Label(header, text='🎬', font=('Segoe UI', 32),
                bg=cores['bg_sidebar'], fg=cores['text_white']).pack()
        tk.Label(header, text='CINEGAMER', font=('Segoe UI', 20, 'bold'),
                bg=cores['bg_sidebar'], fg=cores['text_white']).pack()
        
        tk.Frame(frame_sidebar, bg=cores['hover'], height=2).pack(fill=tk.X, padx=15)
        
        self.menu_botoes = {}
        nav_frame = tk.Frame(frame_sidebar, bg=cores['bg_sidebar'])
        nav_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        for id_page, icone, text in menu:
            btn = sidebar(nav_frame, icone, text, lambda p=id_page: self.show_page(p))
            btn.pack(fill=tk.X, pady=(0, 5))
            self.menu_botoes[id_page] = btn
    
    def show_page(self, page):
        """Mostra página específica"""
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
            self.page_recomendacoes()
        elif page == 'configuracoes':
            self.page_configuracoes()
    
    def page(self):
        #Dashboard
        container = tk.Frame(self.area_principal, bg=cores['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['inicio']).pack(anchor='w', pady=(0, 20))
        
        stats = self.db.set_statistics()
        
        # Cards de estatísticas
        stats_frame = tk.Frame(container, bg=cores['bg_white'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        for i, (titulo, valor, cor) in enumerate([
            ('📚 Total', stats['total_itens'], cores['primary']),
            ('⭐ Média', f"{stats['average_rating']}/5", cores['alert']),
            ('⏱️ Horas', f"{stats['time_total_hours']}h", cores['info'])
        ]):
            card = Card(stats_frame)
            card.grid(row=0, column=i, padx=10, sticky='nsew')
            stats_frame.columnconfigure(i, weight=1)
            
            tk.Label(card, text=titulo, font=fonts['body'],
                    bg=cores['bg_card'], fg=cores['text_secund']).pack(pady=(15, 5))
            tk.Label(card, text=str(valor), font=fonts['title_big'],
                    bg=cores['bg_card'], fg=cor).pack(pady=(0, 15))
        
        # Distribuição
        card_tipos = Card(container)
        card_tipos.pack(fill=tk.X, pady=10)
        
        tk.Label(card_tipos, text='📊 Distribuição', font=fonts['titulo_small'],
                bg=cores['bg_card'], fg=cores['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        for tipo, count in stats['per_type'].items():
            row = tk.Frame(card_tipos, bg=cores['bg_card'])
            row.pack(fill=tk.X, padx=20, pady=5)
            icones = {'Filme': '🎬', 'Série': '📺', 'Jogo': '🎮'}
            tk.Label(row, text=f"{icones.get(tipo, '📄')} {tipo}", font=fonts['body'],
                    bg=cores['bg_card'], fg=cores['text_dark']).pack(side=tk.LEFT)
            tk.Label(row, text=str(count), font=fonts['body_bold'],
                    bg=cores['bg_card'], fg=cores['secund']).pack(side=tk.RIGHT)
        
        tk.Frame(card_tipos, bg=cores['bg_card'], height=15).pack()
        
        # Botões
        button(container, '➕ Adicionar Novo', command=self.add_item_dialog,
               style='primary').pack(anchor='w', pady=10)
    
    def page_colection(self):
        """Coleção completa"""
        container = tk.Frame(self.area_principal, bg=cores['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['colecao']).pack(anchor='w', pady=(0, 20))
        
        button(container, '➕ Adicionar', command=self.add_item_dialog,
               style='success').pack(anchor='w', pady=(0, 15))
        
        # list com scroll
        list_frame = tk.Frame(container, bg=cores['bg_white'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(list_frame, bg=cores['bg_white'], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.list_current = tk.Frame(canvas, bg=cores['bg_white'])
        
        self.list_current.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.list_current, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.reload_list()
    
    def reload_list(self):
        """Carrega list"""
        for widget in self.list_current.winfo_children():
            widget.destroy()
        
        itens = self.db.list_content()
        
        if not itens:
            tk.Label(self.list_current, text='📭 Nenhum item',
                    font=fonts['titulo_medium'], bg=cores['bg_white'],
                    fg=cores['text_secund']).pack(pady=50)
        else:
            for item in itens:
                card = CardItem(self.list_current, item,
                              on_edit=self.edit_item, on_delete=self.delete_item)
                card.pack(fill=tk.X, pady=(0, 10))
    
    def add_item_dialog(self):
        """Adicionar item"""
        dialog = tk.Toplevel(self.root)
        dialog.title('➕ Adicionar')
        dialog.geometry('500x550')
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        container = tk.Frame(dialog, bg=cores['bg_white'])
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
        
        btn_frame = tk.Frame(container, bg=cores['bg_white'])
        btn_frame.pack(fill=tk.X)
        
        button(btn_frame, '💾 save', command=save, style='success').pack(side=tk.LEFT, padx=(0, 10))
        button(btn_frame, '❌ Cancelar', command=dialog.destroy, style='erro').pack(side=tk.LEFT)
    
    def edit_item(self, item_id):
        """Editar item"""
        item = self.db.set_content(item_id)
        if item:
            messagebox.showinfo('Editar', f'Editar: {item[1]}')
    
    def delete_item(self, item_id):
        """Deletar item"""
        if messagebox.askyesno('Confirmar', 'Deletar este item?'):
            self.db.delete_content(item_id)
            messagebox.showinfo('Sucesso', 'Deletado!')
            self.reload_list()
    
    def page_estatisticas(self):
        """Estatísticas"""
        container = tk.Frame(self.area_principal, bg=cores['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['estatisticas']).pack(anchor='w', pady=(0, 20))
        
        stats = self.db.set_statistics()
        
        # Visão geral
        card = Card(container)
        card.pack(fill=tk.X, pady=10)
        
        tk.Label(card, text='📊 Visão Geral', font=fonts['titulo_medium'],
                bg=cores['bg_card'], fg=cores['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        for label, value in [('Total', stats['total_itens']),
                            ('Média', f"{stats['average_rating']}/5"),
                            ('Horas', stats['time_total_hours'])]:
            row = tk.Frame(card, bg=cores['bg_card'])
            row.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(row, text=f"📌 {label}", font=fonts['body'],
                    bg=cores['bg_card'], fg=cores['text_dark']).pack(side=tk.LEFT)
            tk.Label(row, text=str(value), font=fonts['body_bold'],
                    bg=cores['bg_card'], fg=cores['secund']).pack(side=tk.RIGHT)
        
        tk.Frame(card, bg=cores['bg_card'], height=15).pack()
        
        # Por tipo
        card2 = Card(container)
        card2.pack(fill=tk.X, pady=10)
        
        tk.Label(card2, text='🎬 Por Tipo', font=fonts['titulo_medium'],
                bg=cores['bg_card'], fg=cores['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        icones = {'Filme': '🎬', 'Série': '📺', 'Jogo': '🎮'}
        for tipo, count in stats['per_type'].items():
            row = tk.Frame(card2, bg=cores['bg_card'])
            row.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(row, text=f"{icones.get(tipo, '📄')} {tipo}", font=fonts['body'],
                    bg=cores['bg_card'], fg=cores['text_dark']).pack(side=tk.LEFT)
            tk.Label(row, text=str(count), font=fonts['body_bold'],
                    bg=cores['bg_card'], fg=cores['info']).pack(side=tk.RIGHT)
        
        tk.Frame(card2, bg=cores['bg_card'], height=15).pack()
    
    def page_recomendacoes(self):
        """Recomendações"""
        container = tk.Frame(self.area_principal, bg=cores['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['recomendacoes']).pack(anchor='w', pady=(0, 20))
        
        recomendacoes = self.db.get_recommendations(10)
        
        if not recomendacoes:
            card = Card(container)
            card.pack(fill=tk.BOTH, expand=True)
            tk.Label(card, text='⭐', font=('Segoe UI', 48),
                    bg=cores['bg_card'], fg=cores['alert']).pack(pady=(50, 20))
            tk.Label(card, text='Sem recomendações', font=fonts['titulo_medium'],
                    bg=cores['bg_card'], fg=cores['text_dark']).pack()
        else:
            for item in recomendacoes:
                card = CardItem(container, item, on_edit=self.edit_item)
                card.pack(fill=tk.X, pady=(0, 10))
    
    def page_configuracoes(self):
        """Configurações"""
        container = tk.Frame(self.area_principal, bg=cores['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['configuracoes']).pack(anchor='w', pady=(0, 20))
        
        card = Card(container)
        card.pack(fill=tk.X, pady=10)
        
        tk.Label(card, text='ℹ️ Informações', font=fonts['titulo_medium'],
                bg=cores['bg_card'], fg=cores['text_dark']).pack(anchor='w', padx=20, pady=(15, 10))
        
        stats = self.db.set_statistics()
        for label, value in [('Versão', '1.0.0'), ('Banco', 'cineGamer.db'),
                            ('Registros', stats['total_itens'])]:
            row = tk.Frame(card, bg=cores['bg_card'])
            row.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(row, text=label, font=fonts['body'],
                    bg=cores['bg_card'], fg=cores['text_dark']).pack(side=tk.LEFT)
            tk.Label(row, text=str(value), font=fonts['body_bold'],
                    bg=cores['bg_card'], fg=cores['text_secund']).pack(side=tk.RIGHT)
        
        tk.Frame(card, bg=cores['bg_card'], height=15).pack()
    
    def executar(self):
        """Inicia aplicação"""
        self.root.mainloop()


if __name__ == '__main__':
    app = CineGamerApp()
    app.executar()
