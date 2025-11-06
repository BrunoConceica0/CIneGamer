import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name="cineGamer.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
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
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings(
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        self.conn.commit()

    # CRUD DOS CONTEÚDOS 

    def add_content(self, data):
        """Adiciona novo conteúdo"""
        cursor = self.conn.cursor()
        date_current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO content(
                name, types, genre, year, avalible, status, timer_minutes, observations, date_register
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*data, date_current))
        self.conn.commit()
        return cursor.lastrowid

    def list_content(self, filter=None):
        """Lista conteúdos com filtros opcionais"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM content WHERE 1=1"
        params = []

        if filter:
            if filter.get('types'):
                query += " AND types = ?"
                params.append(filter["types"])

            if filter.get('genre'):
                query += " AND genre = ?"
                params.append(filter['genre'])

            if filter.get('year'):
                query += " AND year = ?"
                params.append(filter['year'])

            if filter.get('status'):
                query += " AND status = ?"
                params.append(filter['status'])

            if filter.get('search'):
                query += " AND name LIKE ?"
                params.append(f"%{filter['search']}%")

        query += " ORDER BY date_register DESC"
        cursor.execute(query, params)
        return cursor.fetchall()

    def set_content(self, id):
        """Obtém um conteúdo específico por ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM content WHERE id = ?", (id,))
        return cursor.fetchone()

    def update_content(self, id, data):
        """Atualiza um conteúdo existente"""
        cursor = self.conn.cursor()
        date_current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            UPDATE content
            SET name = ?, types = ?, genre = ?, year = ?, avalible = ?, status = ?, timer_minutes = ?, observations = ?, date_update = ?
            WHERE id = ?
        ''', (*data, date_current, id))

        self.conn.commit()
        return cursor.rowcount

    def delete_content(self, id):
        """Deleta um conteúdo"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM content WHERE id=?", (id,))
        self.conn.commit()

    # ========== ESTATÍSTICAS ==========

    def set_statistics(self):
        """Retorna estatísticas gerais da coleção"""
        cursor = self.conn.cursor()

        # Total items
        cursor.execute("SELECT COUNT(*) FROM content")
        total_itens = cursor.fetchone()[0] or 0

        # Items per type
        cursor.execute("SELECT types, COUNT(*) FROM content GROUP BY types")
        per_type = dict(cursor.fetchall())

        # Top genres
        cursor.execute("SELECT genre, COUNT(*) FROM content GROUP BY genre ORDER BY COUNT(*) DESC LIMIT 5")
        top_genres = cursor.fetchall()

        # Count by status
        cursor.execute("SELECT status, COUNT(*) FROM content GROUP BY status")
        per_status = dict(cursor.fetchall())

        # Average rating
        cursor.execute("SELECT AVG(avalible) FROM content WHERE avalible > 0")
        average_rating = cursor.fetchone()[0] or 0

        # Total time (in hours)
        cursor.execute("SELECT SUM(timer_minutes) FROM content")
        time_total = cursor.fetchone()[0] or 0
        time_hours = time_total / 60

        # Items per year
        cursor.execute("""
            SELECT year, COUNT(*)
            FROM content
            WHERE year IS NOT NULL
            GROUP BY year
            ORDER BY year DESC
            LIMIT 10
        """)
        per_year = cursor.fetchall()

        return {
            'total_itens': total_itens,
            'per_type': per_type,
            'top_genres': top_genres,
            'per_status': per_status,
            'average_rating': round(average_rating, 2),
            'time_total_hours': round(time_hours, 1),
            'per_year': per_year
        }

    def get_recommendations(self, limite=10):
        """Retorna recomendações baseadas nas melhores avaliações"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM content 
            WHERE avalible >= 4 AND status = 'Assistido'
            ORDER BY avalible DESC, date_register DESC
            LIMIT ?
        ''', (limite,))
        return cursor.fetchall()
    
    def get_available_years(self):
        """Retorna lista de anos disponíveis"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT year FROM content WHERE year IS NOT NULL ORDER BY year DESC")
        return [row[0] for row in cursor.fetchall()]
    
    
    def save_configuration(self, key, value):
        """Salva uma configuração"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, value))
        self.conn.commit()
    
    def get_configuration(self, key, default=None):
        """Obtém uma configuração"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else default
    
    def close(self):
        """Fecha a conexão com o banco"""
        self.conn.close()