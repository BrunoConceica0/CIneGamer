import tkinter as tk
from tkinter import messagebox
from config.database import Database
from utility.config import colors,fonts
from components.Siderbar import sidebar 
from components.TitlePage import TitlePage
from components.Card import Card
from components.Button import button
from utility.ui_config import menu, title

from hooks.edit_item import edit_item
from hooks.add_item import add_item
from hooks.create_section_recommendation import create_section_recommendation

import page.page_statistics as statistics
import page.page_recommendations as recommendations
from page.collections import collections, reload_list
from page.settings import  page_settings as settings

class CineGamerApp:
    
    def __init__(self):
        self.root = tk.Tk()
        self.db = Database()
        self.configure_window()
        self.create_interface()
        self.show_page('inicio')
    
    def configure_window(self):
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
            self.page_statistics()
        elif page == 'recomendacoes':
            self.page_recommendations()
        elif page == 'configuracoes':
            self.page_settings()  
    
    def page(self):
        container = tk.Frame(self.area_principal, bg=colors['bg_white'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        TitlePage(container, title['inicio']).pack(anchor='w', pady=(0, 20))
        
        stats = self.db.get_statistics()
        
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
        
        button(container, '➕ Adicionar Novo', command=self.add_item,
               style='primary').pack(anchor='w', pady=10)
    
    def page_colection(self):
        """Mostra página de coleção"""
        collections(self)

    def page_settings(self):
        settings(self)
    
    def reload_list(self):
        """Recarrega lista de itens"""
        reload_list(self)  
    
    def add_item(self):
        add_item(self)
    
    def edit_item(self, item_id):
        edit_item(self, item_id)
    
    def delete_item(self, item_id):
        if messagebox.askyesno('Confirmar', 'Deletar este item?'):
            self.db.delete_content(item_id)
            messagebox.showinfo('Sucesso', 'Deletado!')
            self.reload_list() 
    
    def page_statistics(self):
        statistics.page_statistics(self)

    def page_recommendations(self):
        recommendations.page_recommendations(self)
    
    def create_section_recommendation(self, parent, titulo, itens):
        create_section_recommendation(self, parent, titulo, itens)
    
    def executar(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = CineGamerApp()
    app.executar()