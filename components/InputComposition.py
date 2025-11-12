
import tkinter as tk
from tkinter import ttk 
from utility.config import colors, fonts # Assumindo estas importações

class InputComposition(tk.Frame):
    
    def __init__(self, master, label_text, **kwargs):
        # 1. EXTRAIR ARGUMENTOS PERSONALIZADOS DE kwargs
        # Usamos .pop() para remover a chave do dicionário antes de usá-lo 
        # para configurar os widgets Tkinter.
        self.widget_type = kwargs.pop('types', 'entry')
        self.initial_value = kwargs.pop('initial_value', None)
        self.combo_values = kwargs.pop('values', [])
        
        super().__init__(master, bg=colors['bg_white'])
        
        # Criação da Label
        tk.Label(self, text=label_text, font=fonts['body'], 
                 bg=colors['bg_white'], fg=colors['text_dark']).pack(anchor='w')

        # Configuração do Widget
        if self.widget_type == 'entry':
            self.value = tk.StringVar(value=self.initial_value if self.initial_value is not None else '')
            self.widget = tk.Entry(self, font=fonts['body'], textvariable=self.value, **kwargs)
        
        elif self.widget_type == 'combo':
            self.value = tk.StringVar(value=self.initial_value if self.initial_value else self.combo_values[0] if self.combo_values else '')
            # O Combobox precisa de 'values'
            self.widget = ttk.Combobox(self, font=fonts['body'], state="readonly", 
                                      values=self.combo_values, textvariable=self.value, **kwargs)
        
        elif self.widget_type == 'spinbox':
            # Spinbox não tem textvariable por padrão, usamos um 'get' manual
            self.widget = tk.Spinbox(self, font=fonts['body'], **kwargs)
            if self.initial_value is not None:
                self.widget.delete(0, 'end')
                self.widget.insert(0, self.initial_value)

        elif self.widget_type == 'text':
            self.widget = tk.Text(self, font=fonts['body'], height=5, **kwargs)
            if self.initial_value is not None:
                self.widget.insert(tk.END, self.initial_value)
                
        # Empacota o widget
        self.widget.pack(fill=tk.X, expand=True)
        
    def get(self):
        """Método unificado para obter o valor do widget"""
        if self.widget_type in ['entry', 'combo']:
            return self.value.get()
        elif self.widget_type == 'spinbox':
            return self.widget.get()
        elif self.widget_type == 'text':
            # Retorna o texto, ignorando a última linha/quebra de linha
            return self.widget.get("1.0", tk.END).strip()
        return None
    def clear(self):
 
        if isinstance(self.widget, tk.Text):
            self.widget.delete('1.0', tk.END)
        else:
            self.widget.delete(0, tk.END)