from config.database import Database

def popular_banco():
    db = Database()
    
    # Filmes
    filmes = [
        ('Matrix', 'Filme', 'Ficção Científica', 1999, 5, 'Assistido', 136, 'Clássico da ficção científica'),
        ('O Poderoso Chefão', 'Filme', 'Drama', 1972, 5, 'Assistido', 175, 'Obra-prima do cinema'),
        ('Interestelar', 'Filme', 'Ficção Científica', 2014, 5, 'Assistido', 169, 'Viagem espacial épica'),
        ('Parasita', 'Filme', 'Thriller', 2019, 5, 'Assistido', 132, 'Oscar de Melhor Filme'),
        ('Vingadores: Ultimato', 'Filme', 'Ação', 2019, 4, 'Assistido', 181, 'Final da saga do infinito'),
        ('Dunkirk', 'Filme', 'Guerra', 2017, 4, 'Assistido', 106, 'Christopher Nolan'),
        ('John Wick 4', 'Filme', 'Ação', 2023, 4, 'Pendente', 169, 'Quero assistir em breve'),
    ]
    
    # Séries
    series = [
        ('Breaking Bad', 'Série', 'Drama', 2008, 5, 'Assistido', 3000, 'Uma das melhores séries já feitas'),
        ('Game of Thrones', 'Série', 'Fantasia', 2011, 4, 'Assistido', 4320, 'Temporadas iniciais excelentes'),
        ('Stranger Things', 'Série', 'Ficção Científica', 2016, 4, 'Assistindo', 1200, 'Na 4ª temporada'),
        ('The Last of Us', 'Série', 'Drama', 2023, 5, 'Assistido', 540, 'Adaptação perfeita do jogo'),
        ('The Witcher', 'Série', 'Fantasia', 2019, 3, 'Assistindo', 800, 'Segunda temporada em andamento'),
        ('Dark', 'Série', 'Ficção Científica', 2017, 5, 'Assistido', 1800, 'Complexa e fascinante'),
    ]
    
    # Jogos
    jogos = [
        ('The Last of Us Part II', 'Jogo', 'Ação/Aventura', 2020, 5, 'Assistido', 1500, 'História emocionante'),
        ('Elden Ring', 'Jogo', 'RPG', 2022, 5, 'Assistindo', 8000, 'Ainda explorando o mundo'),
        ('God of War Ragnarök', 'Jogo', 'Ação/Aventura', 2022, 5, 'Assistido', 3000, 'Excelente conclusão'),
        ('Red Dead Redemption 2', 'Jogo', 'Ação/Aventura', 2018, 5, 'Assistido', 6000, 'Obra-prima da Rockstar'),
        ('Cyberpunk 2077', 'Jogo', 'RPG', 2020, 4, 'Assistido', 5000, 'Após updates ficou ótimo'),
        ('Baldurs Gate 3', 'Jogo', 'RPG', 2023, 5, 'Assistindo', 4000, 'RPG do ano'),
        ('Hogwarts Legacy', 'Jogo', 'RPG', 2023, 4, 'Pendente', 0, 'Na lista de desejos'),
        ('Resident Evil 4 Remake', 'Jogo', 'Terror', 2023, 4, 'Pendente', 0, 'Quero jogar'),
    ]
    
    # Adicionar todos os itens
    print("Populando banco de dados...")
    
    for filme in filmes:
        db.add_content(filme)
        print(f"✓ Filme adicionado: {filme[0]}")
    
    for serie in series:
        db.add_content(serie)
        print(f"✓ Série adicionada: {serie[0]}")
    
    for jogo in jogos:
        db.add_content(jogo)
        print(f"✓ Jogo adicionado: {jogo[0]}")
    
    # Exibir estatísticas
    stats = db.set_statistics()
    print("\n" + "="*50)
    print("📊 ESTATÍSTICAS DO BANCO")
    print("="*50)
    print(f"Total de itens: {stats['total_itens']}")
    print(f"Avaliação média: {stats['average_rating']}/5")
    print(f"Tempo total: {stats['time_total_hours']} horas")
    print("\nPor tipo:")
    for tipo, count in stats['per_type'].items():
        print(f"  {tipo}: {count}")
    print("\nPor status:")
    for status, count in stats['per_status'].items():
        print(f"  {status}: {count}")
    
    db.close()
    print("\n✅ Banco populado com sucesso!")

if __name__ == '__main__':
    popular_banco()