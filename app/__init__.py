from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    """
    Factory function para criar a aplicação Flask
    Segue o padrão de Application Factory
    """
    # Cria a aplicação Flask
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['JSON_AS_ASCII'] = False  # Suporte a caracteres especiais
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Configuração de logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/chatbot.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('ChatBot UNIALFA startup')
    
    # Registra os blueprints
    from app.controllers.webhook import webhook_bp
    from app.controllers.context import context_bp
    
    app.register_blueprint(webhook_bp)
    app.register_blueprint(context_bp)
    
    return app

# Cria a instância da aplicação
app = create_app()
