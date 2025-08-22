import sqlite3
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

logger = logging.getLogger(__name__)

class EventoLimpezaHistorico:
    def __init__(self, db_path='chatbot.db'):
        self.db_path = db_path
        self.scheduler = None
        
    def limpar_historico_inativo(self):
        """
        Remove mensagens do histórico de usuários que não enviaram mensagens há mais de 24 horas
        """
        try:
            # Conecta ao banco de dados
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calcula o limite de tempo (24 horas atrás)
            limite_tempo = datetime.now() - timedelta(hours=24)
            
            # Busca números de usuários que não enviaram mensagens há mais de 24h
            cursor.execute('''
                SELECT DISTINCT numero 
                FROM historico 
                WHERE horario_data < ?
            ''', (limite_tempo,))
            
            numeros_inativos = cursor.fetchall()
            
            if not numeros_inativos:
                logger.info("Nenhum usuário inativo encontrado para limpeza")
                return 0
            
            # Remove mensagens dos usuários inativos
            cursor.execute('''
                DELETE FROM historico 
                WHERE horario_data < ?
            ''', (limite_tempo,))
            
            # Confirma as alterações
            conn.commit()
            
            # Conta quantas mensagens foram removidas
            mensagens_removidas = cursor.rowcount
            
            logger.info(f"Limpeza concluída: {mensagens_removidas} mensagens removidas de usuários inativos há mais de 24h")
            
            # Fecha a conexão
            conn.close()
            
            return mensagens_removidas
            
        except Exception as e:
            logger.error(f"Erro ao limpar histórico inativo: {str(e)}")
            return 0
    
    def verificar_usuarios_inativos(self):
        """
        Verifica quantos usuários estão inativos há mais de 24 horas
        """
        try:
            # Conecta ao banco de dados
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calcula o limite de tempo (24 horas atrás)
            limite_tempo = datetime.now() - timedelta(hours=24)
            
            # Conta usuários inativos
            cursor.execute('''
                SELECT COUNT(DISTINCT numero) 
                FROM historico 
                WHERE horario_data < ?
            ''', (limite_tempo,))
            
            usuarios_inativos = cursor.fetchone()[0]
            
            # Fecha a conexão
            conn.close()
            
            logger.info(f"Usuários inativos há mais de 24h: {usuarios_inativos}")
            return usuarios_inativos
            
        except Exception as e:
            logger.error(f"Erro ao verificar usuários inativos: {str(e)}")
            return 0
    
    def iniciar_scheduler(self):
        """
        Inicia o scheduler para executar a limpeza a cada 24 horas
        """
        try:
            # Cria o scheduler
            self.scheduler = BackgroundScheduler()
            
            # Adiciona a tarefa de limpeza a cada 24 horas
            self.scheduler.add_job(
                func=self.limpar_historico_inativo,
                trigger=IntervalTrigger(hours=24),
                id='limpeza_historico',
                name='Limpeza de histórico inativo',
                replace_existing=True
            )
            
            # Inicia o scheduler
            self.scheduler.start()
            
            logger.info("✅ Scheduler de limpeza iniciado com sucesso")
            logger.info("📅 Tarefa agendada: Limpeza de histórico a cada 24 horas")
            
            # Registra função de limpeza para quando a aplicação for encerrada
            atexit.register(self.parar_scheduler)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar scheduler: {str(e)}")
            return False
    
    def parar_scheduler(self):
        """
        Para o scheduler de forma segura
        """
        try:
            if self.scheduler:
                self.scheduler.shutdown()
                logger.info("🛑 Scheduler de limpeza parado com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro ao parar scheduler: {str(e)}")
    
    def verificar_status_scheduler(self):
        """
        Verifica o status do scheduler
        """
        try:
            if self.scheduler and self.scheduler.running:
                jobs = self.scheduler.get_jobs()
                logger.info(f"📊 Scheduler ativo com {len(jobs)} tarefas agendadas")
                return True
            else:
                logger.warning("⚠️ Scheduler não está rodando")
                return False
        except Exception as e:
            logger.error(f"❌ Erro ao verificar status do scheduler: {str(e)}")
            return False
    
    def executar_limpeza_manual(self):
        """
        Executa a limpeza manualmente (útil para testes)
        """
        logger.info("🧹 Executando limpeza manual...")
        return self.limpar_historico_inativo()

# Instância global do evento de limpeza
evento_limpeza = EventoLimpezaHistorico()

def iniciar_evento_limpeza():
    """
    Função para iniciar o evento de limpeza
    """
    return evento_limpeza.iniciar_scheduler()

def parar_evento_limpeza():
    """
    Função para parar o evento de limpeza
    """
    evento_limpeza.parar_scheduler()

def verificar_status_evento_limpeza():
    """
    Função para verificar o status do evento de limpeza
    """
    return evento_limpeza.verificar_status_scheduler()

def executar_limpeza_manual():
    """
    Função para executar limpeza manual
    """
    return evento_limpeza.executar_limpeza_manual()
