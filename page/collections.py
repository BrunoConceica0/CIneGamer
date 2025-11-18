import tkinter as tk 
from utility.config import colors, fonts
from utility.ui_config import title
from components.Button import button
from utility.config import colors,fonts
from components.TitlePage import TitlePage
from components.CardItem import CardItem

def collections(self):  
    container = tk.Frame(self.area_principal, bg=colors['bg_white'])
    container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
    
    TitlePage(container, title['colecao']).pack(anchor='w', pady=(0, 20))
    
    button(container, '➕ Adicionar', command=self.add_item,
           style='success').pack(anchor='w', pady=(0, 15))
    
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
    
    reload_list(self)


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
                          on_edit=self.edit_item, 
                          on_delete=self.delete_item)
            card.pack(fill=tk.X, pady=(0, 10))