import logging
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

def extrair_dados_whatsapp(data: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    Extrai os dados necessários do webhook do WhatsApp
    
    Args:
        data: Dados JSON do webhook
        
    Returns:
        dict: Dicionário com numero, mensagem e timestamp ou None se não conseguir extrair
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
                    mensagem = extrair_conteudo_mensagem(message)
                    
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
