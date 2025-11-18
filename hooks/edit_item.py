import tkinter as tk
from tkinter import messagebox
from components.Button import button
from components.InputComposition import InputComposition
from utility.config import colors

def edit_item(parent_app, item_id):
    item_row = parent_app.db.get_content(item_id)
    if not item_row:
        messagebox.showerror('Erro', 'Item não encontrado.')
        return
    
    item = list(item_row)
    
    dialog = tk.Toplevel(parent_app.root)
    dialog.title(f'✏️ Editar: {item[1]}')
    dialog.geometry('500x700')
    dialog.transient(parent_app.root)
    dialog.grab_set()
    
    # Centralizar
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f'+{x}+{y}')
    
    container = tk.Frame(dialog, bg=colors['bg_white'])
    container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    name = InputComposition(container, 'Nome:*', types='entry', initial_value=item[1])
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
                             values=['Assistido', 'Assistindo', 'Pendente', 'Abandonado'],
                             initial_value=item[6])
    status.pack(fill=tk.X, pady=(0, 10))
    
    time = InputComposition(container, 'Tempo (min):', types='spinbox', from_=0, to=10000, initial_value=item[7])
    time.pack(fill=tk.X, pady=(0, 10))
    
    obs = InputComposition(container, 'Obs:', types='text', initial_value=item[8])
    obs.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    def update():
        """Valida e atualiza o item"""
        # Validação
        if not name.get() or not tipo.get() or not genero.get() or not status.get():
            messagebox.showerror('Erro', 'Preencha campos obrigatórios (*)')
            return
        
        data = (
            name.get(),
            tipo.get(),
            genero.get(),
            int(ano.get()) if ano.get() else None,
            int(aval.get()) if aval.get() else None,
            status.get(),
            int(time.get()) if time.get() else 0,
            obs.get() if obs.get() else None
        )
        
        if parent_app.db.update_content(item_id, data):
            messagebox.showinfo('Sucesso', 'Item atualizado!')
            dialog.destroy()
            
            if hasattr(parent_app, 'list_current') and parent_app.list_current.winfo_ismapped():
                parent_app.reload_list()
        else:
            messagebox.showerror('Erro', 'Falha ao atualizar!')
    
    btn_frame = tk.Frame(container, bg=colors['bg_white'])
    btn_frame.pack(fill=tk.X)
    
    button(btn_frame, '💾 Atualizar', command=update, style='success').pack(side=tk.LEFT, padx=(0, 10))
    button(btn_frame, '❌ Cancelar', command=dialog.destroy, style='erro').pack(side=tk.LEFT)