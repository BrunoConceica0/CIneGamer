"""
Módulo de renderização de recomendações

Este módulo contém funções para criar e renderizar
seções de recomendações na interface.
"""

# Importa e renomeia a função principal
from .render_recommendation_cards import render_recommendation_cards as renderRecommendation

# Importa função auxiliar
from .create_section_recommendation import create_section_recommendation

# Define exports públicos
__all__ = [
    'renderRecommendation',
    'create_section_recommendation'
]
