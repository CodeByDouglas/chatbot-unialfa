import json
import logging
from datetime import datetime
from database import db


logger = logging.getLogger(__name__)

def processar_webhook_whatsapp(request_body):
    """
    Processa o corpo da requisição do webhook do WhatsApp
    Extrai os dados necessários e salva no banco de dados
    """
    try:
        # Log da requisição recebida
        logger.info(f"Processando webhook do WhatsApp em {datetime.now()}")
        
        # Verifica se há entrada de dados
        if 'entry' in request_body:
            for entry in request_body['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change.get('value') and 'messages' in change['value']:
                            # Extrai metadados da sessão
                            metadata = change['value'].get('metadata', {})
                            phone_number_id = metadata.get('phone_number_id')
                            display_phone_number = metadata.get('display_phone_number')
                            
                            for message in change['value']['messages']:
                                processar_mensagem(message, phone_number_id, display_phone_number)
                                
        logger.info("Webhook processado com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {str(e)}")
        return False

def processar_mensagem(message, phone_number_id=None, display_phone_number=None):
    """
    Processa uma mensagem individual e salva no banco de dados
    """
    try:
        # Extrai informações da mensagem
        message_id = message.get('id')
        from_number = message.get('from')
        timestamp = message.get('timestamp')
        message_type = message.get('type')
        
        logger.info(f"Mensagem recebida - ID: {message_id}, De: {from_number}, Tipo: {message_type}")
        
        # Processa diferentes tipos de mensagem
        if message_type == 'text':
            text_content = message.get('text', {}).get('body', '')
            logger.info(f"Texto da mensagem: {text_content}")
            
            # Salva a mensagem no banco de dados
            if text_content and from_number:
                db.inserir_historico(from_number, text_content)
                logger.info(f"Mensagem salva no banco para número {from_number}")
            
        elif message_type == 'image':
            image_data = message.get('image', {})
            logger.info(f"Imagem recebida - ID: {image_data.get('id')}")
            # Salva informação sobre imagem recebida
            if from_number:
                db.inserir_historico(from_number, f"[IMAGEM] ID: {image_data.get('id')}")
            
        elif message_type == 'document':
            document_data = message.get('document', {})
            filename = document_data.get('filename', 'Documento sem nome')
            logger.info(f"Documento recebido - Nome: {filename}")
            # Salva informação sobre documento recebido
            if from_number:
                db.inserir_historico(from_number, f"[DOCUMENTO] {filename}")
            
        # Adicione mais tipos de mensagem conforme necessário
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
