from app import create_app
from app.services.cleanup_service import iniciar_cleanup_service
from config import Config
import logging

logger = logging.getLogger(__name__)

def main():
    """Função principal para iniciar a aplicação"""
    try:
        # Cria a aplicação Flask
        app = create_app()
        
        # Inicia o serviço de limpeza
        logger.info("🚀 Iniciando serviço de limpeza...")
        iniciar_cleanup_service()
        
        # Inicia o servidor
        logger.info(f"🌐 Iniciando servidor Flask em {Config.HOST}:{Config.PORT}...")
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar aplicação: {str(e)}")
        raise

if __name__ == '__main__':
    main()
