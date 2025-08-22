from flask import Flask

# Cria a aplicação Flask
app = Flask(__name__)

# Configurações da aplicação
app.config['JSON_AS_ASCII'] = False  # Suporte a caracteres especiais

# Importa as rotas
from app.controler.Webhook import webhook_bp
from app.controler.atualizar_contexto import atualizar_contexto_bp

# Registra os blueprints
app.register_blueprint(webhook_bp)
app.register_blueprint(atualizar_contexto_bp)
