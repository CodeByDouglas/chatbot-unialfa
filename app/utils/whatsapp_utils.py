import logging
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)

def extrair_dados_whatsapp(data: List[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    """
    Extrai os dados necessários do webhook do WhatsApp
    
    Args:
        data: Dados JSON do webhook (formato lista padrão do WhatsApp)
        
    Returns:
        dict: Dicionário com numero, mensagem e timestamp ou None se não conseguir extrair
    """
    try:
        # Verifica se data é uma lista válida
        if not isinstance(data, list) or len(data) == 0:
            logger.warning("Dados do webhook não são uma lista válida")
            return None
        
        # Pega o primeiro item da lista
        webhook_data = data[0]
        
        # Verifica se tem mensagens
        if 'messages' not in webhook_data or len(webhook_data['messages']) == 0:
            logger.warning("Nenhuma mensagem encontrada no webhook")
            return None
        
        message = webhook_data['messages'][0]
        
        # Extrai dados essenciais
        numero = message.get('from', '')
        mensagem = extrair_conteudo_mensagem(message)
        timestamp = message.get('timestamp', '')
        
        # Valida se os dados essenciais estão presentes
        if not numero or not mensagem:
            logger.warning("Dados essenciais (numero ou mensagem) não encontrados")
            return None
        
        return {
            'numero': numero,
            'mensagem': mensagem,
            'timestamp': timestamp
        }
        
    except Exception as e:
        logger.error(f"Erro ao extrair dados do WhatsApp: {str(e)}")
        return None

def extrair_conteudo_mensagem(message: Dict[str, Any]) -> str:
    """
    Extrai o conteúdo da mensagem baseado no tipo
    
    Args:
        message: Objeto da mensagem do WhatsApp
        
    Returns:
        str: Conteúdo da mensagem
    """
    message_type = message.get('type', '')
    
    if message_type == 'text':
        return message.get('text', {}).get('body', '')
    elif message_type == 'audio':
        return "[ÁUDIO]"
    elif message_type == 'image':
        return "[IMAGEM]"
    elif message_type == 'document':
        filename = message.get('document', {}).get('filename', 'Documento sem nome')
        return f"[DOCUMENTO] {filename}"
    elif message_type == 'video':
        return "[VÍDEO]"
    elif message_type == 'location':
        return "[LOCALIZAÇÃO]"
    elif message_type == 'contact':
        return "[CONTATO]"
    else:
        return "[MENSAGEM NÃO SUPORTADA]"

def formatar_historico_mensagens(mensagens: list) -> str:
    """
    Formata o histórico de mensagens para envio ao Groq
    
    Args:
        mensagens: Lista de mensagens do histórico
        
    Returns:
        str: Histórico formatado
    """
    if not mensagens:
        return "Nenhuma mensagem anterior"
    
    historico_formatado = ""
    for msg in mensagens:
        mensagem, user, horario = msg
        historico_formatado += f"- {user}: {mensagem} (às {horario})\n"
    
    return historico_formatado

def validar_numero_whatsapp(numero: str) -> bool:
    """
    Valida se o número está no formato correto do WhatsApp
    
    Args:
        numero: Número do WhatsApp
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not numero:
        return False
    
    # Remove caracteres especiais e espaços
    numero_limpo = ''.join(filter(str.isdigit, numero))
    
    # Verifica se tem pelo menos 10 dígitos (formato internacional)
    return len(numero_limpo) >= 10
