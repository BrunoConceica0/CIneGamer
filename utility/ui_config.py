import datetime

menu = [
    ('inicio', '🏠', 'Início'),
    ('colecao', '📚', 'Coleção'),
    ('estatisticas', '📊', 'Estatísticas'),
    ('recomendacoes', '⭐', 'Recomendações'),
    ('configuracoes', '⚙️', 'Configurações'),
]

title = {
    "title": "🎬 CineGamer - Coleção de Entretenimento", 
    'inicio': '🏠 Início - Dashboard',
    'colecao': '📚 Minha Coleção',
    'estatisticas': '📊 Estatísticas',
    'recomendacoes': '⭐ Recomendações',
    'configuracoes': '⚙️ Configurações',
}

types = ['Filme', 'Série', 'Jogo']

genres = [
    'Ação',
    'Aventura',
    'Comédia',
    'Drama',
    'Ficção Científica',
    'Terror',
    'Romance',
    'Suspense',
    'Animação',
    'Documentário',
    'Musical',
    'Fantasia'
]

status = [
    'Assistido',
    'Assistindo',
    'Pendente',
    'Abandonado'
]

reviews = ['1', '2', '3', '4', '5']

year_current = datetime.datetime.now().year
years = [str(ano) for ano in range(1900, year_current + 1)]
years.reverse() 

labels = {
    'name': 'Nome',     
    'types': 'Tipo',
    'genres': 'Gênero',
    'year': 'Ano',
    'reviews': 'Avaliação',
    'status': 'Status',
    'time': 'Tempo (minutos)',
    'observations': 'Observações'
}

placeholder = {
    'name': 'Digite o nome do filme, série ou jogo',
    'types': 'Selecione o tipo',
    'genres': 'Selecione o gênero',
    'year': 'Digite o ano',
    'reviews': 'Selecione a avaliação',
    'status': 'Selecione o status',
    'time': 'Digite quantidade de minutos',
    'observations': 'Adicione suas anotações pessoais sobre este item...'
}