import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Views:
    def __init__(self, db_path='chatbot.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Cria uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)
    
    def obter_mensagens_por_numero(self, numero):
        """Obtém todas as mensagens de um número específico usando a view"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT mensagem, user, horario_data
                    FROM mensagens_por_numero
                    WHERE numero = ?
                    ORDER BY horario_data DESC
                ''', (numero,))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao obter mensagens por número: {str(e)}")
            return []
    
    def obter_todas_mensagens(self):
        """Obtém todas as mensagens usando a view"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT numero, mensagem, user, horario_data
                    FROM mensagens_por_numero
                ''')
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao obter todas as mensagens: {str(e)}")
            return []
    
    def obter_contexto(self):
        """Obtém toda a documentação do contexto"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT documentacao FROM contexto')
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Erro ao obter contexto: {str(e)}")
            return []

# Instância global das views
views = Views()
