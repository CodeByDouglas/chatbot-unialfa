from flask import Blueprint, request, jsonify
import json
import logging
from datetime import datetime
import sys
import os

# Adiciona o diretório raiz ao path para importar db_manager.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db_manager import db
from views import views
from app.controler.Request_grooq import enviar_para_groq

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria o blueprint
webhook_bp = Blueprint('webhook', __name__)

def extrair_dados_whatsapp(data):
    """
    Extrai os dados necessários do webhook do WhatsApp
    
    Args:
        data: Dados JSON do webhook
        
    Returns:
        dict: Dicionário com numero, mensagem e timestamp
    """
    try:
        # Estrutura típica do webhook do WhatsApp Business API
        if 'entry' in data and len(data['entry']) > 0:
            entry = data['entry'][0]
            
            if 'changes' in entry and len(entry['changes']) > 0:
                change = entry['changes'][0]
                
                if 'value' in change and 'messages' in change['value']:
                    message = change['value']['messages'][0]
                    
                    # Extrai número do telefone
                    numero = message.get('from', '')
                    
                    # Extrai mensagem (pode ser texto, áudio, imagem, etc.)
                    mensagem = ""
                    if 'text' in message:
                        mensagem = message['text'].get('body', '')
                    elif 'audio' in message:
                        mensagem = "[ÁUDIO]"
                    elif 'image' in message:
                        mensagem = "[IMAGEM]"
                    elif 'document' in message:
                        mensagem = "[DOCUMENTO]"
                    else:
                        mensagem = "[MENSAGEM NÃO SUPORTADA]"
                    
                    # Extrai timestamp
                    timestamp = message.get('timestamp', '')
                    
                    return {
                        'numero': numero,
                        'mensagem': mensagem,
                        'timestamp': timestamp
                    }
        
        # Se não conseguir extrair, retorna None
        return None
        
    except Exception as e:
        logger.error(f"Erro ao extrair dados do WhatsApp: {str(e)}")
        return None

def enviar_resposta_whatsapp(numero, mensagem):
    """
    Envia resposta para o WhatsApp (implementação básica)
    
    Args:
        numero: Número do telefone
        mensagem: Mensagem a ser enviada
        
    Returns:
        bool: True se enviado com sucesso
    """
    try:
        # TODO: Implementar envio real para WhatsApp Business API
        # Por enquanto, apenas log da resposta
        logger.info(f"📤 Resposta para {numero}: {mensagem}")
        
        # Aqui você implementaria a chamada para a API do WhatsApp
        # para enviar a mensagem de volta ao usuário
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar resposta WhatsApp: {str(e)}")
        return False

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint para receber webhooks do WhatsApp
    """
    try:
        # Log da requisição recebida
        logger.info(f"📥 Webhook recebido em {datetime.now()}")
        
        # Obtém os dados da requisição
        data = request.get_json()
        
        if not data:
            logger.warning("Requisição sem dados JSON")
            return jsonify({"status": "error", "message": "Dados JSON não fornecidos"}), 400
        
        # Log dos dados recebidos
        logger.info(f"Dados recebidos: {json.dumps(data, indent=2)}")
        
        # Extrai dados do WhatsApp
        dados_whatsapp = extrair_dados_whatsapp(data)
        
        if not dados_whatsapp:
            logger.warning("Não foi possível extrair dados do webhook")
            return jsonify({"status": "success", "message": "Dados não processados"}), 200
        
        numero = dados_whatsapp['numero']
        mensagem_atual = dados_whatsapp['mensagem']
        timestamp = dados_whatsapp['timestamp']
        
        logger.info(f"📱 Mensagem de {numero}: {mensagem_atual}")
        
        # Salva a mensagem atual no histórico (user = 'aluno')
        db.inserir_historico(numero, mensagem_atual, user='aluno')
        logger.info(f"💾 Mensagem do aluno salva no histórico para {numero}")
        
        # Obtém histórico de mensagens do usuário
        historico_mensagens = views.obter_mensagens_por_numero(numero)
        
        # Formata o histórico para envio ao Groq (incluindo user)
        historico_formatado = ""
        if historico_mensagens:
            for msg in historico_mensagens:
                mensagem, user, horario = msg
                historico_formatado += f"- {user}: {mensagem} (às {horario})\n"
        else:
            historico_formatado = "Nenhuma mensagem anterior"
        
        # Obtém a documentação do contexto
        documentacoes = views.obter_contexto()
        documentacao = documentacoes[0] if documentacoes else "Documentação não disponível"
        
        logger.info(f"🤖 Enviando para Groq: histórico={len(historico_mensagens)} msgs, doc={len(documentacao)} chars")
        
        # Chama a API do Groq
        resposta_groq = enviar_para_groq(
            historico_mensagens=historico_formatado,
            documentacao=documentacao,
            mensagem_atual=mensagem_atual
        )
        
        logger.info(f"🤖 Resposta do Groq: {resposta_groq[:100]}...")
        
        # Salva a resposta do bot no histórico (user = 'Bot UNIALFA')
        db.inserir_historico(numero, resposta_groq, user='Bot UNIALFA')
        logger.info(f"💾 Resposta do bot salva no histórico para {numero}")
        
        # Envia resposta para o WhatsApp
        sucesso_envio = enviar_resposta_whatsapp(numero, resposta_groq)
        
        if sucesso_envio:
            logger.info(f"✅ Resposta enviada com sucesso para {numero}")
        else:
            logger.error(f"❌ Erro ao enviar resposta para {numero}")
        
        # Resposta de sucesso para o WhatsApp
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@webhook_bp.route('/historico/<numero>', methods=['GET'])
def obter_historico_numero(numero):
    """
    Endpoint para obter histórico de mensagens de um número específico
    """
    try:
        mensagens = views.obter_mensagens_por_numero(numero)
        return jsonify({
            "numero": numero,
            "mensagens": [
                {
                    "mensagem": msg[0],
                    "user": msg[1],
                    "horario_data": msg[2]
                } for msg in mensagens
            ]
        }), 200
    except Exception as e:
        logger.error(f"Erro ao obter histórico: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@webhook_bp.route('/historico', methods=['GET'])
def obter_todo_historico():
    """
    Endpoint para obter todo o histórico de mensagens
    """
    try:
        mensagens = views.obter_todas_mensagens()
        return jsonify({
            "mensagens": [
                {
                    "numero": msg[0],
                    "mensagem": msg[1],
                    "user": msg[2],
                    "horario_data": msg[3]
                } for msg in mensagens
            ]
        }), 200
    except Exception as e:
        logger.error(f"Erro ao obter todo histórico: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

 