import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from config import Config
from db_manager import db

logger = logging.getLogger(__name__)

class CleanupService:
    """Serviço para limpeza automática do histórico"""
    
    def __init__(self):
        self.scheduler = None
    
    def limpar_historico_inativo(self):
        """
        Remove mensagens do histórico de usuários inativos
        """
        try:
            mensagens_removidas = db.limpar_historico_inativo(Config.INACTIVE_USER_HOURS)
            logger.info(f"🧹 Limpeza automática concluída: {mensagens_removidas} mensagens removidas")
            return mensagens_removidas
        except Exception as e:
            logger.error(f"❌ Erro na limpeza automática: {str(e)}")
            return 0
    
    def iniciar_scheduler(self):
        """
        Inicia o scheduler para executar a limpeza automaticamente
        """
        try:
            # Cria o scheduler
            self.scheduler = BackgroundScheduler()
            
            # Adiciona a tarefa de limpeza
            self.scheduler.add_job(
                func=self.limpar_historico_inativo,
                trigger=IntervalTrigger(hours=Config.CLEANUP_INTERVAL_HOURS),
                id='limpeza_historico',
                name='Limpeza de histórico inativo',
                replace_existing=True
            )
            
            # Inicia o scheduler
            self.scheduler.start()
            
            logger.info("✅ Scheduler de limpeza iniciado com sucesso")
            logger.info(f"📅 Tarefa agendada: Limpeza de histórico a cada {Config.CLEANUP_INTERVAL_HOURS} horas")
            
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
    
    def verificar_status(self):
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

# Instância global do serviço de limpeza
cleanup_service = CleanupService()

def iniciar_cleanup_service():
    """Função para iniciar o serviço de limpeza"""
    return cleanup_service.iniciar_scheduler()

def parar_cleanup_service():
    """Função para parar o serviço de limpeza"""
    cleanup_service.parar_scheduler()

def verificar_status_cleanup():
    """Função para verificar o status do serviço de limpeza"""
    return cleanup_service.verificar_status()

def executar_limpeza_manual():
    """Função para executar limpeza manual"""
    return cleanup_service.executar_limpeza_manual()
