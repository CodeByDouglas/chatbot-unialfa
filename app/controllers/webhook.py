from flask import Blueprint, request, jsonify
import json
import logging
from datetime import datetime
import sys
import os

# Adiciona o diretório raiz ao path para importar db_manager.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db_manager import db
from app.services.groq_service import enviar_para_groq
from app.utils.whatsapp_utils import extrair_dados_whatsapp, formatar_historico_mensagens, validar_numero_whatsapp

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria o blueprint
webhook_bp = Blueprint('webhook', __name__)

def enviar_resposta_whatsapp(numero, mensagem):
    """
    Envia resposta para o WhatsApp 
    
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
        
        # Extrai dados do WhatsApp usando utilitário
        dados_whatsapp = extrair_dados_whatsapp(data)
        
        
        if not dados_whatsapp:
            logger.warning("Não foi possível extrair dados do webhook")
            return jsonify({"status": "success", "message": "Dados não processados"}), 200
        
        numero = dados_whatsapp['numero']
        mensagem_atual = dados_whatsapp['mensagem']
        timestamp = dados_whatsapp['timestamp']
        
        # Valida o número do WhatsApp
        if not validar_numero_whatsapp(numero):
            logger.warning(f"Número inválido: {numero}")
            return jsonify({"status": "error", "message": "Número inválido"}), 400
        
        logger.info(f"📱 Mensagem de {numero}: {mensagem_atual}")
        
        # Verifica se é o número administrativo
        if numero == "556293977594":
            logger.info(f"🔧 Comando administrativo detectado de {numero}")
            
            # Comando: "admin - contexto atual"
            if mensagem_atual.strip().lower() == "admin - contexto atual":
                logger.info("📋 Comando para obter contexto atual")
                
                # Obtém a documentação do contexto
                documentacoes = db.obter_contexto()
                documentacao = documentacoes[0] if documentacoes else "Documentação não disponível"
                
                # Envia o contexto atual
                sucesso_envio = enviar_resposta_whatsapp(numero, documentacao)
                
                if sucesso_envio:
                    logger.info(f"✅ Contexto atual enviado com sucesso para {numero}")
                else:
                    logger.error(f"❌ Erro ao enviar contexto atual para {numero}")
                
                return jsonify({"status": "success", "message": documentacao, "numero": numero}), 200
            
            # Comando: "admin - novo contexto contexto: [novo contexto]"
            elif mensagem_atual.strip().lower().startswith("admin - novo contexto:"):
                logger.info("🔄 Comando para atualizar contexto")
                
                # Extrai o novo contexto (tudo após os dois pontos)
                partes = mensagem_atual.split(":", 1)
                if len(partes) >= 2:
                    novo_contexto = partes[1].strip()
                    
                    if novo_contexto:
                        # Limpa a tabela contexto existente
                        db.limpar_contexto()
                        logger.info("🗑️ Tabela contexto limpa com sucesso")
                        
                        # Insere o novo contexto
                        resultado = db.inserir_contexto(novo_contexto)
                        
                        if resultado:
                            logger.info("✅ Contexto atualizado com sucesso")
                            
                            # Envia confirmação
                            mensagem_sucesso = "✅ Contexto atualizado com sucesso!"
                            sucesso_envio = enviar_resposta_whatsapp(numero, mensagem_sucesso)
                            
                            if sucesso_envio:
                                logger.info(f"✅ Confirmação de atualização enviada para {numero}")
                            else:
                                logger.error(f"❌ Erro ao enviar confirmação para {numero}")
                            
                            return jsonify({"status": "success", "message": "Contexto atualizado", "numero": numero}), 200
                        else:
                            logger.error("❌ Erro ao inserir novo contexto")
                            mensagem_erro = "❌ Erro ao atualizar contexto no banco de dados"
                            enviar_resposta_whatsapp(numero, mensagem_erro)
                            return jsonify({"status": "error", "message": "Erro ao atualizar contexto"}), 500
                    else:
                        logger.warning("Novo contexto está vazio")
                        mensagem_erro = "❌ O novo contexto não pode estar vazio"
                        enviar_resposta_whatsapp(numero, mensagem_erro)
                        return jsonify({"status": "error", "message": "Contexto vazio"}), 400
                else:
                    logger.warning("Formato de comando inválido para atualizar contexto")
                    mensagem_erro = "❌ Formato inválido. Use: admin - novo contexto contexto: [seu novo contexto]"
                    enviar_resposta_whatsapp(numero, mensagem_erro)
                    return jsonify({"status": "error", "message": "Formato inválido"}), 400
        
        # Processamento normal para outros números
        # Salva a mensagem atual no histórico (user = 'aluno')
        db.inserir_historico(numero, mensagem_atual, user='aluno')
        logger.info(f"💾 Mensagem do aluno salva no histórico para {numero}")
        
        # Obtém histórico de mensagens do usuário
        historico_mensagens = db.obter_mensagens_por_numero(numero)
        
        # Formata o histórico para envio ao Groq usando utilitário
        historico_formatado = formatar_historico_mensagens(historico_mensagens)
        
        # Obtém a documentação do contexto
        documentacoes = db.obter_contexto()
        documentacao = documentacoes[0] if documentacoes else "Documentação não disponível"
        
        logger.info(f"🤖 Enviando para Groq")
        
        # Chama a API do Groq
        resposta_groq = enviar_para_groq(
            historico_mensagens=historico_formatado,
            documentacao=documentacao,
            mensagem_atual=mensagem_atual
        )
        
        logger.info(f"🤖 Resposta do Groq: {resposta_groq[:100]}...")
        
        # Verifica se a requisição para o Groq foi bem-sucedida
        if resposta_groq.startswith("Erro:") or resposta_groq.startswith("Erro na API:") or resposta_groq.startswith("Erro de conexão:") or resposta_groq.startswith("Erro interno:"):
            logger.error(f"❌ Erro na API do Groq: {resposta_groq}")
            
            # Mensagem de erro para o usuário
            mensagem_erro_usuario = "Serviços indisponíveis no momento, entre em contato com esse número: (62) 993977594"
            
            # Salva a mensagem de erro no histórico (user = 'Bot UNIALFA')
            db.inserir_historico(numero, mensagem_erro_usuario, user='Bot UNIALFA')
            logger.info(f"💾 Mensagem de erro salva no histórico para {numero}")
            
            # Envia mensagem de erro para o usuário
            sucesso_envio = enviar_resposta_whatsapp(numero, mensagem_erro_usuario)
            
            if sucesso_envio:
                logger.info(f"✅ Mensagem de erro enviada com sucesso para {numero}")
            else:
                logger.error(f"❌ Erro ao enviar mensagem de erro para {numero}")
            
            # Envia alerta para o número administrativo
            numero_admin = "556293977594"
            mensagem_alerta_admin = "Chatbot fora de serviço, verificar limites na Groq"
            
            sucesso_alerta_admin = enviar_resposta_whatsapp(numero_admin, mensagem_alerta_admin)
            
            if sucesso_alerta_admin:
                logger.info(f"✅ Alerta administrativo enviado com sucesso para {numero_admin}")
            else:
                logger.error(f"❌ Erro ao enviar alerta administrativo para {numero_admin}")
            
            return jsonify({"status": "error", "message": mensagem_erro_usuario, "numero": numero}), 200
        
        # Fluxo normal - requisição foi bem-sucedida
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
        return jsonify({"status": "success", "message": resposta_groq, "numero": numero}), 200
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

