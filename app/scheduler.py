from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.limpar_historico import limpar_historico_inativo
import logging

logger = logging.getLogger(__name__)

def iniciar_scheduler():
    """
    Inicia o scheduler para executar tarefas agendadas
    """
    try:
        # Cria o scheduler
        scheduler = BackgroundScheduler()
        
        # Adiciona a tarefa de limpeza a cada 24 horas
        scheduler.add_job(
            func=limpar_historico_inativo,
            trigger=IntervalTrigger(hours=24),
            id='limpeza_historico',
            name='Limpeza de histórico inativo',
            replace_existing=True
        )
        
        # Inicia o scheduler
        scheduler.start()
        
        logger.info("✅ Scheduler iniciado com sucesso")
        logger.info("📅 Tarefa agendada: Limpeza de histórico a cada 24 horas")
        
        return scheduler
        
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar scheduler: {str(e)}")
        return None

def parar_scheduler(scheduler):
    """
    Para o scheduler de forma segura
    """
    try:
        if scheduler:
            scheduler.shutdown()
            logger.info("🛑 Scheduler parado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao parar scheduler: {str(e)}")

def verificar_status_scheduler(scheduler):
    """
    Verifica o status do scheduler
    """
    try:
        if scheduler and scheduler.running:
            jobs = scheduler.get_jobs()
            logger.info(f"📊 Scheduler ativo com {len(jobs)} tarefas agendadas")
            return True
        else:
            logger.warning("⚠️ Scheduler não está rodando")
            return False
    except Exception as e:
        logger.error(f"❌ Erro ao verificar status do scheduler: {str(e)}")
        return False
