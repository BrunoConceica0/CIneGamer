import  tkinter as tk
from utility.config import fonts, colors
from components import CardItem
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
    