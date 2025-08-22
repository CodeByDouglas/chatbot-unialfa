from flask import Blueprint, request, jsonify
import logging
import sys
import os

# Adiciona o diretório raiz ao path para importar db_manager.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db_manager import db

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria o blueprint
atualizar_contexto_bp = Blueprint('atualizar_contexto', __name__)

@atualizar_contexto_bp.route('/atualizar-contexto', methods=['POST'])
def atualizar_contexto():
    """
    Endpoint para atualizar a documentação no banco de dados
    """
    try:
        # Log da requisição recebida
        logger.info("Requisição para atualizar contexto recebida")
        
        # Obtém os dados da requisição
        data = request.get_json()
        
        if not data:
            logger.warning("Requisição sem dados JSON")
            return jsonify({
                "status": "error", 
                "message": "Dados JSON não fornecidos"
            }), 400
        
        # Verifica se o campo documentação está presente
        if 'documentacao' not in data:
            logger.warning("Campo 'documentacao' não encontrado no body")
            return jsonify({
                "status": "error", 
                "message": "Campo 'documentacao' é obrigatório"
            }), 400
        
        documentacao = data['documentacao']
        
        # Valida se a documentação não está vazia
        if not documentacao or not documentacao.strip():
            logger.warning("Documentação fornecida está vazia")
            return jsonify({
                "status": "error", 
                "message": "Documentação não pode estar vazia"
            }), 400
        
        # Limpa a tabela contexto existente
        db.limpar_contexto()
        logger.info("Tabela contexto limpa com sucesso")
        
        # Insere a nova documentação
        resultado = db.inserir_contexto(documentacao)
        
        if resultado:
            logger.info("Documentação atualizada com sucesso")
            return jsonify({
                "status": "success",
                "message": "Documentação atualizada com sucesso",
                "id": resultado
            }), 200
        else:
            logger.error("Erro ao inserir nova documentação")
            return jsonify({
                "status": "error",
                "message": "Erro ao inserir nova documentação"
            }), 500
        
    except Exception as e:
        logger.error(f"Erro ao atualizar contexto: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Erro interno: {str(e)}"
        }), 500

@atualizar_contexto_bp.route('/contexto', methods=['GET'])
def obter_contexto():
    """
    Endpoint para obter a documentação atual
    """
    try:
        from views import views
        
        # Obtém a documentação do banco
        documentacoes = views.obter_contexto()
        
        if documentacoes:
            return jsonify({
                "status": "success",
                "documentacao": documentacoes[0] if documentacoes else "",
                "total_registros": len(documentacoes)
            }), 200
        else:
            return jsonify({
                "status": "success",
                "documentacao": "",
                "total_registros": 0,
                "message": "Nenhuma documentação encontrada"
            }), 200
            
    except Exception as e:
        logger.error(f"Erro ao obter contexto: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Erro interno: {str(e)}"
        }), 500
