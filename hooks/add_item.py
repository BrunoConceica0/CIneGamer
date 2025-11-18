import tkinter as tk
from tkinter import messagebox
from components.Button import button
from components.InputComposition import InputComposition
from utility.config import colors

def add_item(parent_app):
    """
    Mostra dialog para adicionar novo item
    
    Args:
        parent_app: Instância da CineGamerApp (self)
    """
    # ========== CRIAR DIALOG ==========
    dialog = tk.Toplevel(parent_app.root)
    dialog.title('➕ Adicionar')
    dialog.geometry('500x700')
    dialog.transient(parent_app.root)
    dialog.grab_set()
    
    # Centralizar
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f'+{x}+{y}')
    
    # Container principal
    container = tk.Frame(dialog, bg=colors['bg_white'])
    container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # ========== CAMPOS ==========
    name = InputComposition(container, 'Nome:*', types='entry')
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
    
    time = InputComposition(container, 'Tempo (min):', types='spinbox', from_=0, to=10000)
    time.pack(fill=tk.X, pady=(0, 10))
    
    obs = InputComposition(container, 'Obs:', types='text')
    obs.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    # ========== FUNÇÃO SALVAR (DENTRO!) ==========
    def save():
        """Valida e salva o novo item"""
        # Validação
        if not name.get() or not tipo.get() or not genero.get() or not status.get():
            messagebox.showerror('Erro', 'Preencha campos obrigatórios (*)')
            return
        
        # Preparar dados
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
        
        # Salvar no banco
        if parent_app.db.add_content(data):
            messagebox.showinfo('Sucesso', 'Item adicionado!')
            dialog.destroy()
            
            # Recarregar lista se estiver na página de coleção
            if hasattr(parent_app, 'list_current'):
                parent_app.reload_list()
        else:
            messagebox.showerror('Erro', 'Falha ao adicionar item!')
    
    # ========== BOTÕES ==========
    btn_frame = tk.Frame(container, bg=colors['bg_white'])
    btn_frame.pack(fill=tk.X)
    
    button(btn_frame, '💾 Salvar', command=save, style='success').pack(side=tk.LEFT, padx=(0, 10))
    button(btn_frame, '❌ Cancelar', command=dialog.destroy, style='erro').pack(side=tk.LEFT)