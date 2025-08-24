import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configurações da aplicação"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configurações do banco de dados
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'chatbot.db')
    
    # Configurações da API Groq
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
    GROQ_MODEL = 'llama-3.3-70b-versatile'
    
    # Configurações do servidor
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Configurações de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/chatbot.log'
    
    # Configurações de limpeza automática
    CLEANUP_INTERVAL_HOURS = float(os.environ.get('CLEANUP_INTERVAL_HOURS', 1))  
    INACTIVE_USER_HOURS = float(os.environ.get('INACTIVE_USER_HOURS', 1))       

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    DATABASE_PATH = ':memory:'
    DEBUG = True

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
