import sqlite3
from datetime import datetime

class Database:
    
    def __init__(self, db_name='cineGamer.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row # Retorna resultados como dicionários (acesso por nome da coluna)
            self.cursor = self.conn.cursor()

    def create_tables(self):
        self.connect()
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS content(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    types TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    year INTEGER,
                    avalible INTEGER CHECK(avalible >= 1 AND avalible <= 5),
                    status TEXT NOT NULL,
                    timer_minutes INTEGER DEFAULT 0,
                    observations TEXT,
                    date_register TEXT NOT NULL,
                    date_update TEXT
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")

    def add_content(self, data):
        """Adiciona um novo item à coleção"""
        self.connect()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO content (name, types, genre, year, avalible, status, timer_minutes, observations, date_register)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            # O 'data' tem 8 elementos. Adicionamos 'now' para o date_register
            self.cursor.execute(sql, data + (now,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao adicionar conteúdo: {e}")
            return False

    def list_content(self):
        """Retorna todos os itens da coleção"""
        self.connect()
        self.cursor.execute("SELECT * FROM content ORDER BY date_register DESC")
        return self.cursor.fetchall()
    
    def get_content(self, item_id):
        """Retorna um item pelo ID"""
        self.connect()
        self.cursor.execute("SELECT * FROM content WHERE id = ?", (item_id,))
        return self.cursor.fetchone()

    def delete_content(self, item_id):
        """Deleta um item pelo ID"""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM content WHERE id = ?", (item_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao deletar conteúdo: {e}")
            return False
            
    def get_statistics(self):
        """
        Calcula e retorna estatísticas resumidas.
        CORREÇÃO APLICADA: 'type' foi trocado por 'types'.
        """
        self.connect()
        stats = {
            'total_itens': 0,
            'average_rating': 0,
            'time_total_hours': 0,
            'per_type': {}
        }

        # 1. Total de itens
        self.cursor.execute("SELECT COUNT(*) FROM content")
        stats['total_itens'] = self.cursor.fetchone()[0]

        # 2. Média de avaliação (apenas itens avaliados)
        self.cursor.execute("SELECT AVG(avalible) FROM content WHERE avalible IS NOT NULL")
        avg = self.cursor.fetchone()[0]
        stats['average_rating'] = f"{avg:.1f}" if avg else 'N/A'
        
        # 3. Tempo total em horas (em minutos na tabela)
        self.cursor.execute("SELECT SUM(timer_minutes) FROM content")
        total_minutes = self.cursor.fetchone()[0]
        stats['time_total_hours'] = round((total_minutes / 60), 1) if total_minutes else 0


        self.cursor.execute("SELECT types, COUNT(*) FROM content GROUP BY types")
        for types, count in self.cursor.fetchall():
            stats['per_type'][types] = count
            
        return stats
    
    def get_recommendations(self, limit=5):
        """Retorna itens com avaliação 4 ou 5 e status 'Assistido'"""
        self.connect()
        sql = """
            SELECT * FROM content 
            WHERE avalible >= 4 AND status = 'Assistido' 
            ORDER BY avalible DESC, date_register DESC 
            LIMIT ?
        """
        self.cursor.execute(sql, (limit,))
        return self.cursor.fetchall()
    
    def update_content(self, item_id, data):
        self.connect()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      
        sql = """
            UPDATE content 
            SET name = ?, types = ?, genre = ?, year = ?, avalible = ?, 
                status = ?, timer_minutes = ?, observations = ?, date_update = ?
            WHERE id = ?
        """
        try:
            self.cursor.execute(sql, data + (now, item_id,)) 
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar conteúdo: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    db = Database()
    
    stats = db.get_statistics()
    print(stats)
    
    db.close()