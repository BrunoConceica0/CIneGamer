# main.py - Aplicação Principal CineGamer

import tkinter as tk
from database import Database
from config import cores, fonts
from Siderbar import sidebar
from TitlePage import TitlePage

class CineGamerApp:
    """Aplicação principal do CineGamer"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.db = Database()
        
        self.configurar_janela()
        self.criar_interface()
        self.mostrar_pagina('inicio')
    
    def configurar_janela(self):
        """Configura a janela principal"""
        self.root.title('🎬 CineGamer - Coleção de Entretenimento')
        self.root.geometry('1200x700')
        self.root.minsize(1200, 700)
        
        # Centralizar janela
        self.root.update_idletasks()
        largura = self.root.winfo_width()
        altura = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f'{largura}x{altura}+{x}+{y}')
        
        # Configurar grid
        self.root.columnconfigure(0, weight=0)  # Sidebar
        self.root.columnconfigure(1, weight=1)  # Área principal
        self.root.rowconfigure(0, weight=1)
    
    def criar_interface(self):
        """Cria a interface principal"""
        # SIDEBAR (Menu Lateral)
        self.criar_sidebar()
        
        # ÁREA PRINCIPAL
        self.area_principal = tk.Frame(self.root, bg=cores['bg_white'])
        self.area_principal.grid(row=0, column=1, sticky='nsew')
    
    def criar_sidebar(self):
        """Cria o menu lateral"""
        frame_sidebar = tk.Frame(
            self.root, 
            bg=cores['bg_sidebar'],
            width=200
        )
        frame_sidebar.grid(row=0, column=0, sticky='nsew')
        frame_sidebar.grid_propagate(False)
        
        # Logo/Título
        header = tk.Frame(frame_sidebar, bg=cores['bg_sidebar'])
        header.pack(fill=tk.X, pady=(20, 30))
        
        tk.Label(
            header,
            text='🎬',
            font=('Segoe UI', 32),
            bg=cores['bg_sidebar'],
            fg=cores['text_white']
        ).pack()
        
        tk.Label(
            header,
            text='CINEGAMER',
            font=('Segoe UI', 20, 'bold'),
            bg=cores['bg_sidebar'],
            fg=cores['text_white']
        ).pack()
        
        # Separador
        tk.Frame(
            frame_sidebar, 
            bg=cores['hover'], 
            height=2
        ).pack(fill=tk.X, padx=15)
        
        # Menu de navegação
        self.menu_botoes = {}
        
        menus = [
            ('inicio', '🏠', 'Início'),
            ('colecao', '📚', 'Coleção'),
            ('estatisticas', '📊', 'Estatísticas'),
            ('recomendacoes', '⭐', 'Recomendações'),
            ('configuracoes', '⚙️', 'Configurações'),
        ]
        
        nav_frame = tk.Frame(frame_sidebar, bg=cores['bg_sidebar'])
        nav_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        for id_pagina, icone, texto in menus:
            botao = sidebar(
                nav_frame,
                icone,
                texto,
                lambda p=id_pagina: self.mostrar_pagina(p)
            )
            botao.pack(fill=tk.X, pady=(0, 5))
            self.menu_botoes[id_pagina] = botao
    
    def mostrar_pagina(self, pagina):
        """Mostra uma página específica"""
        # Limpar área principal
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        
        # Desselecionar todos os botões
        for botao in self.menu_botoes.values():
            botao.desselecionar()
        
        # Selecionar botão atual
        if pagina in self.menu_botoes:
            self.menu_botoes[pagina].selecionar()
        
        # Criar página de teste
        self.criar_pagina_teste(pagina)
    
    def criar_pagina_teste(self, pagina):
        """Cria uma página de teste simples"""
        container = tk.Frame(self.area_principal, bg=cores['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Título
        titulos = {
            'inicio': '🏠 Início - Dashboard',
            'colecao': '📚 Minha Coleção',
            'estatisticas': '📊 Estatísticas',
            'recomendacoes': '⭐ Recomendações',
            'configuracoes': '⚙️ Configurações',
        }
        
        TitlePage(container, titulos.get(pagina, 'CineGamer')).pack(
            anchor='w', pady=(0, 20)
        )
        
        # Conteúdo de teste
        from Card import Card
        card = Card(container)
        card.pack(fill=tk.BOTH, expand=True)
        
        info_frame = tk.Frame(card, bg=cores['bg_card'])
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            info_frame,
            text=f'Página: {pagina.upper()}',
            font=fonts['titulo_medium'],
            bg=cores['bg_card'],
            fg=cores['text_dark']
        ).pack(pady=10)
        
        tk.Label(
            info_frame,
            text='✅ A aplicação está funcionando!',
            font=fonts['body'],
            bg=cores['bg_card'],
            fg=cores['success']
        ).pack(pady=5)
        
        # Testar banco de dados
        stats = self.db.set_statistics()
        tk.Label(
            info_frame,
            text=f'📊 Itens no banco: {stats["total_itens"]}',
            font=fonts['body'],
            bg=cores['bg_card'],
            fg=cores['text_dark']
        ).pack(pady=5)
        
        # Botão de teste
        from Button import button
        button(
            info_frame,
            'Botão de Teste',
            command=lambda: print(f'Clicou na página: {pagina}'),
            style='primary'
        ).pack(pady=20)
    
    def executar(self):
        """Inicia o loop principal da aplicação"""
        self.root.mainloop()


if __name__ == '__main__':
    app = CineGamerApp()
    app.executar()