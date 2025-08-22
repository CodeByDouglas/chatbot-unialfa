import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path='chatbot.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Cria uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa o banco de dados criando as tabelas e views"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Criar tabela historico
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS historico (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero TEXT NOT NULL,
                        mensagem TEXT NOT NULL,
                        horario_data DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Criar tabela contexto
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS contexto (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        documentacao TEXT NOT NULL
                    )
                ''')
                
                # Criar view para mensagens por número
                cursor.execute('''
                    CREATE VIEW IF NOT EXISTS mensagens_por_numero AS
                    SELECT 
                        numero,
                        mensagem,
                        horario_data
                    FROM historico
                    ORDER BY horario_data DESC
                ''')
                
                conn.commit()
                logger.info("Banco de dados inicializado com sucesso")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
    
    def inserir_historico(self, numero, mensagem):
        """Insere uma nova entrada no histórico"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO historico (numero, mensagem, horario_data)
                    VALUES (?, ?, ?)
                ''', (numero, mensagem, datetime.now()))
                conn.commit()
                logger.info(f"Histórico inserido para número {numero}")
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Erro ao inserir histórico: {str(e)}")
            return None
    
    def inserir_contexto(self, documentacao):
        """Insere nova documentação no contexto"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO contexto (documentacao)
                    VALUES (?)
                ''', (documentacao,))
                conn.commit()
                logger.info("Contexto inserido com sucesso")
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Erro ao inserir contexto: {str(e)}")
            return None
    
    def limpar_historico(self):
        """Limpa toda a tabela de histórico"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM historico')
                conn.commit()
                logger.info("Histórico limpo com sucesso")
        except Exception as e:
            logger.error(f"Erro ao limpar histórico: {str(e)}")
    
    def limpar_contexto(self):
        """Limpa toda a tabela de contexto"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM contexto')
                conn.commit()
                logger.info("Contexto limpo com sucesso")
        except Exception as e:
            logger.error(f"Erro ao limpar contexto: {str(e)}")

# Instância global do banco de dados
db = Database()
