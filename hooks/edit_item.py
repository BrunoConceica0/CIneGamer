import tkinter as tk
from tkinter import messagebox
from components.Button import button
from components.FormField import FormField
from utility.config import colors
from utility.ui_config import types, genres, status, reviews, labels, placeholder

def edit_item(parent_app, item_id):
    item_row = parent_app.db.get_content(item_id)
    if not item_row:
        messagebox.showerror('Erro', 'Item não encontrado.')
        return
    
    item = list(item_row)
    
    window = tk.Toplevel(parent_app.root)
    window.title(f'✏️ Editar: {item[1]}')
    window.geometry('750x700')
    window.transient(parent_app.root)
    window.grab_set()
    window.configure(bg=colors['bg_white'])
    
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
    y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
    window.geometry(f'+{x}+{y}')
    
    canvas = tk.Canvas(window, bg=colors['bg_white'], highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    container = tk.Frame(canvas, bg=colors['bg_white'])
    
    container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=30)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    left_column = tk.Frame(container, bg=colors['bg_white'])
    left_column.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    
    right_column = tk.Frame(container, bg=colors['bg_white'])
    right_column.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
    
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    
    field_name = FormField(left_column, labels['name'], 'entry', required=True,initial_value=item[1])
    field_name.pack(fill=tk.X, pady=(0, 20))
    
    field_genres = FormField(left_column, labels['genres'], 'select', required=True,options=genres, placeholder_text=placeholder['genres'],initial_value=item[3])
    field_genres.pack(fill=tk.X, pady=(0, 20))
    field_reviews = FormField(left_column, labels['reviews'], 'select',options=reviews, placeholder_text=placeholder['reviews'],initial_value=str(item[5]) if item[5] else None)
    field_reviews.pack(fill=tk.X, pady=(0, 20))
    field_time = FormField(left_column, labels['time'], 'number',initial_value=str(item[7]) if item[7] else None)
    field_time.pack(fill=tk.X, pady=(0, 20))
    field_types = FormField(right_column, labels['types'], 'select', required=True,options=types, placeholder_text=placeholder['types'],initial_value=item[2])
    field_types.pack(fill=tk.X, pady=(0, 20))
    
    field_year = FormField(right_column, labels['year'], 'number',initial_value=str(item[4]) if item[4] else None)
    field_year.pack(fill=tk.X, pady=(0, 20))
    
    field_status = FormField(right_column, labels['status'], 'select', required=True,options=status, placeholder_text=placeholder['status'],initial_value=item[6])
    field_status.pack(fill=tk.X, pady=(0, 20))
    
    obs_frame = tk.Frame(container, bg=colors['bg_white'])
    obs_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(20, 0))
    
    field_obs = FormField(obs_frame, labels['observations'], 'textarea',
                         initial_value=item[8])
    field_obs.pack(fill=tk.BOTH, expand=True)
    
    def update():
        # Validação usando os novos nomes
        if not field_name.get() or not field_types.get() or not field_genres.get() or not field_status.get():
            messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
            return
        data = (
            field_name.get(),
            field_types.get(),
            field_genres.get(),
            int(field_year.get()) if field_year.get() else None,
            int(field_reviews.get()) if field_reviews.get() else None,
            field_status.get(),
            int(field_time.get()) if field_time.get() else 0,
            field_obs.get() if field_obs.get() else None
        )
        
        if parent_app.db.update_content(item_id, data):
            messagebox.showinfo('Sucesso', '✅ Item atualizado com sucesso!')
            window.destroy()
            
            if hasattr(parent_app, 'list_current') and parent_app.list_current.winfo_ismapped():
                parent_app.reload_list()
        else:
            messagebox.showerror('Erro', '❌ Falha ao atualizar!')
    
    btn_frame = tk.Frame(container, bg=colors['bg_white'])
    btn_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(30, 0))
    
    button(btn_frame, '💾 Atualizar', command=update, style='success').pack(side=tk.LEFT, padx=(0, 10))
    button(btn_frame, '❌ Cancelar', command=window.destroy, style='erro').pack(side=tk.LEFT)