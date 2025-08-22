import requests
import json
import logging

logger = logging.getLogger(__name__)

def enviar_para_groq(historico_mensagens, documentacao, mensagem_atual):
    """
    Envia requisição para API do Groq com histórico de mensagens, documentação e mensagem atual
    
    Args:
        historico_mensagens: Lista de mensagens do histórico
        documentacao: Texto com a documentação
        mensagem_atual: Mensagem atual que a IA deve responder
    
    Returns:
        Resposta da API do Groq
    """
    try:
        # Chave da API do Groq
        api_key = "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"
        
        # URL da API do Groq
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Headers da requisição
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prompt fixo
        prompt_fixo = "Você é um assistente virtual da unialfa você deve ser responsavel em auxiliar os alunos seguindo as informações que você tem logo a baixo e levando o contexto do historico de mensagens:"
        
        # Monta o conteúdo completo incluindo a mensagem atual
        conteudo_completo = f"{prompt_fixo}\n\ndocumentação:\n{documentacao}\n\nhistorico:\n{historico_mensagens}\n\nmensagem atual do usuário:\n{mensagem_atual}"
        
        # Dados da requisição
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": conteudo_completo
                }
            ]
        }
        
        # Faz a requisição para a API do Groq
        response = requests.post(url, headers=headers, json=data)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            response_data = response.json()
            resposta_groq = response_data['choices'][0]['message']['content']
            logger.info("Requisição para Groq realizada com sucesso")
            return resposta_groq
        else:
            logger.error(f"Erro na requisição para Groq: {response.status_code} - {response.text}")
            return f"Erro na API: {response.status_code}"
            
    except Exception as e:
        logger.error(f"Erro ao enviar requisição para Groq: {str(e)}")
        return f"Erro interno: {str(e)}"
