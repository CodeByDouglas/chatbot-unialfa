import sqlite3
import logging
from datetime import datetime, timedelta
from config import Config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
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
                
                # Se a tabela não existe
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
    
    def limpar_historico_inativo(self, horas_inativo=24):
        """
        Remove mensagens do histórico de usuários inativos
        
        Args:
            horas_inativo: Número de horas para considerar usuário inativo
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                limite_tempo = datetime.now() - timedelta(hours=horas_inativo)
                
                cursor.execute('''
                    DELETE FROM historico 
                    WHERE horario_data < ?
                ''', (limite_tempo,))
                
                mensagens_removidas = cursor.rowcount
                conn.commit()
                
                logger.info(f"Limpeza concluída: {mensagens_removidas} mensagens removidas de usuários inativos há mais de {horas_inativo}h")
                return mensagens_removidas
                
        except Exception as e:
            logger.error(f"Erro ao limpar histórico inativo: {str(e)}")
            return 0
    
    # ===== MÉTODOS DE VIEW =====
    
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

# Instância global do banco de dados unificado
db = Database()
