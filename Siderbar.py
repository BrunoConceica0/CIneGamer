import tkinter as tk
from config import cores, fonts, spacing

class sidebar(tk.Frame):
    #Botão do menu lateral com ícone e text
    
    def __init__(self, parent, icone, text, command, **kwargs):
        super().__init__(parent, bg=cores['bg_sidebar'], cursor='hand2', **kwargs)
        
        self.command = command
        self.selector = False
        
        # Container interno
        container = tk.Frame(self, bg=cores['bg_sidebar'])
        container.pack(fill=tk.BOTH, expand=True, padx=spacing['md'], pady=spacing['sm'])
        
        # Ícone
        self.icone_label = tk.Label(
            container,
            text=icone,
            font=fonts['menu_icone'],
            bg=cores['bg_sidebar'],
            fg=cores['text_menu']
        )
        self.icone_label.pack(side=tk.LEFT, padx=(spacing['sm'], spacing['md']))
        
        # text
        self.text_label = tk.Label(
            container,
            text=text,
            font=fonts['menu'],
            bg=cores['bg_sidebar'],
            fg=cores['text_menu'],
            anchor='w'
        )
        self.text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Eventos
        self.bind('<Button-1>', self._on_click)
        container.bind('<Button-1>', self._on_click)
        self.icone_label.bind('<Button-1>', self._on_click)
        self.text_label.bind('<Button-1>', self._on_click)
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        container.bind('<Enter>', self._on_enter)
        container.bind('<Leave>', self._on_leave)
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        if not self.selector:
            self.config(bg=cores['hover_sidebar'])
            for widget in self.winfo_children():
                self._mudar_bg_recursivo(widget, cores['hover_sidebar'])
    
    def _on_leave(self, event):
        if not self.selector:
            self.config(bg=cores['bg_sidebar'])
            for widget in self.winfo_children():
                self._mudar_bg_recursivo(widget, cores['bg_sidebar'])
    
    def _mudar_bg_recursivo(self, widget, cor):
        try:
            widget.config(bg=cor)
        except:
            pass
        for child in widget.winfo_children():
            self._mudar_bg_recursivo(child, cor)
    
    def selecionar(self):
        """Marca este botão como selector"""
        self.selector = True
        self.config(bg=cores['hover'])
        for widget in self.winfo_children():
            self._mudar_bg_recursivo(widget, cores['hover'])
        self.icone_label.config(fg=cores['acento'])
        self.text_label.config(fg=cores['text_white'], font=fonts['body_negrito'])
    
    def desselecionar(self):
        """Desmarca este botão"""
        self.selector = False
        self.config(bg=cores['bg_sidebar'])
        for widget in self.winfo_children():
            self._mudar_bg_recursivo(widget, cores['bg_sidebar'])
        self.icone_label.config(fg=cores['text_menu'])
        self.text_label.config(fg=cores['text_menu'], font=fonts['menu'])



    
    def clean(self):
        #Limpa o campo
        if isinstance(self.widget, tk.Text):
            self.widget.delete('1.0', tk.END)
        else:
            self.widget.delete(0, tk.END)


