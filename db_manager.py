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
                
                # Verificar se a tabela historico já existe
                cursor.execute("PRAGMA table_info(historico)")
                columns = [column[1] for column in cursor.fetchall()]
                
                # Se a tabela não existe, criar com o novo campo user
                if not columns:
                    cursor.execute('''
                        CREATE TABLE historico (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            numero TEXT NOT NULL,
                            mensagem TEXT NOT NULL,
                            user TEXT NOT NULL DEFAULT 'aluno',
                            horario_data DATETIME DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
                    logger.info("Tabela historico criada com campo user")
                else:
                    # Se a tabela existe mas não tem o campo user, adicionar
                    if 'user' not in columns:
                        cursor.execute('ALTER TABLE historico ADD COLUMN user TEXT NOT NULL DEFAULT "aluno"')
                        logger.info("Campo user adicionado à tabela historico")
                
                # Criar tabela contexto
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS contexto (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        documentacao TEXT NOT NULL
                    )
                ''')
                
                # Recriar view para mensagens por número (incluindo o campo user)
                cursor.execute('DROP VIEW IF EXISTS mensagens_por_numero')
                cursor.execute('''
                    CREATE VIEW mensagens_por_numero AS
                    SELECT 
                        numero,
                        mensagem,
                        user,
                        horario_data
                    FROM historico
                    ORDER BY horario_data DESC
                ''')
                
                conn.commit()
                logger.info("Banco de dados inicializado com sucesso")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
    
    def inserir_historico(self, numero, mensagem, user='aluno'):
        """
        Insere uma nova entrada no histórico
        
        Args:
            numero: Número do telefone
            mensagem: Conteúdo da mensagem
            user: 'aluno' ou 'Bot UNIALFA'
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO historico (numero, mensagem, user, horario_data)
                    VALUES (?, ?, ?, ?)
                ''', (numero, mensagem, user, datetime.now()))
                conn.commit()
                logger.info(f"Histórico inserido para número {numero} - User: {user}")
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
