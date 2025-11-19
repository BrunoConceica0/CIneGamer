import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utility.config import colors

class ChartWidget(tk.Frame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=colors['bg_card'], **kwargs)
        
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
        except:
            try:
                plt.style.use('seaborn')
            except:
                plt.style.use('default')
        
        self.figure = Figure(figsize=(6, 4), dpi=100, facecolor=colors['bg_card'])
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def clear(self):
        self.figure.clear()
    
    def draw(self):
        self.canvas.draw()
    
    def create_pie_chart(self, data, title='Distribuição'):
        self.clear()
        ax = self.figure.add_subplot(111)
        
        labels = list(data.keys())
        values = list(data.values())
        chart_colors = [colors['info'], colors['success'], colors['alert']]
        
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=90,
            colors=chart_colors,
            textprops={'fontsize': 10, 'weight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
        
        ax.set_title(title, fontsize=14, weight='bold', color=colors['text_dark'], pad=20)
        ax.axis('equal')
        
        self.draw()
    
    def create_bar_chart(self, data, title='Gráfico de Barras', xlabel='', ylabel='Quantidade'):
        self.clear()
        ax = self.figure.add_subplot(111)
        
        labels = list(data.keys())
        values = list(data.values())
        
        bars = ax.bar(labels, values, color=colors['secondary'], alpha=0.8, edgecolor=colors['primary'])
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, weight='bold')
        
        ax.set_title(title, fontsize=14, weight='bold', color=colors['text_dark'], pad=20)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        
        if len(labels) > 0 and any(len(str(l)) > 8 for l in labels):
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        self.figure.tight_layout()
        self.draw()
    
    def create_horizontal_bar_chart(self, data, title='Status', xlabel='Quantidade', ylabel=''):
        self.clear()
        ax = self.figure.add_subplot(111)
        
        labels = list(data.keys())
        values = list(data.values())
        
        color_map = {
            'Assistido': colors['success'],
            'Assistindo': colors['info'],
            'Pendente': colors['alert'],
            'Abandonado': colors['erro']
        }
        
        bar_colors = [color_map.get(label, colors['secondary']) for label in labels]
        
        bars = ax.barh(labels, values, color=bar_colors, alpha=0.8, edgecolor=colors['primary'])
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f' {int(width)}',
                   ha='left', va='center', fontsize=10, weight='bold')
        
        ax.set_title(title, fontsize=14, weight='bold', color=colors['text_dark'], pad=20)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(axis='x', alpha=0.3)
        
        self.figure.tight_layout()
        self.draw()
    
    def create_line_chart(self, data, title='Itens por Ano', xlabel='Ano', ylabel='Quantidade'):
        self.clear()
        ax = self.figure.add_subplot(111)
        
        if isinstance(data, dict):
            x_values = list(data.keys())
            y_values = list(data.values())
        else:  # list of tuples
            x_values = [item[0] for item in data]
            y_values = [item[1] for item in data]
        
        ax.plot(x_values, y_values, 
               color=colors['secondary'], 
               marker='o', 
               linewidth=2, 
               markersize=8,
               markerfacecolor=colors['accent'],
               markeredgecolor=colors['primary'],
               markeredgewidth=2)
        
        for x, y in zip(x_values, y_values):
            ax.text(x, y, f' {int(y)}', 
                   ha='left', va='bottom', 
                   fontsize=9, weight='bold')
        
        ax.set_title(title, fontsize=14, weight='bold', color=colors['text_dark'], pad=20)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(True, alpha=0.3)
        
        if len(x_values) > 8:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        self.figure.tight_layout()
        self.draw()
    
    def create_rating_chart(self, data, title='Distribuição de Avaliações'):
        self.clear()
        ax = self.figure.add_subplot(111)
        
        ratings = [1, 2, 3, 4, 5]
        counts = [data.get(r, 0) for r in ratings]
        labels = [f'{r} estrelas' for r in ratings]
        
        rating_colors = [
            colors['erro'],    # 1 star
            colors['alert'],   # 2 stars
            colors['info'],    # 3 stars
            colors['accent'],  # 4 stars
            colors['success']  # 5 stars
        ]
        
        bars = ax.bar(labels, counts, color=rating_colors, alpha=0.8, edgecolor=colors['primary'])
        
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=10, weight='bold')
        
        ax.set_title(title, fontsize=14, weight='bold', color=colors['text_dark'], pad=20)
        ax.set_xlabel('Avaliação', fontsize=11)
        ax.set_ylabel('Quantidade', fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        
        self.figure.tight_layout()
        self.draw()