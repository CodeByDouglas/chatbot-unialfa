from app import app
from database.envento_limpar_historico import iniciar_evento_limpeza
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Inicia o evento de limpeza
    logger.info("🚀 Iniciando evento de limpeza...")
    iniciar_evento_limpeza()
    
    # Inicia o servidor
    logger.info("🌐 Iniciando servidor Flask...")
    app.run(
        host='0.0.0.0',  # Aceita conexões de qualquer IP
        port=5000,       # Porta padrão
        debug=False      # Modo produção para servidor
    )
