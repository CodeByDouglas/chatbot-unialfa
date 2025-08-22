#!/usr/bin/env python3
"""
Script de teste para verificar se a função extrair_dados_whatsapp funciona
com o formato JSON real do webhook do WhatsApp
"""

import json
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.whatsapp_utils import extrair_dados_whatsapp

def test_webhook_extraction():
    """Testa a extração de dados do webhook"""
    
    print("🧪 Testando extração de dados do webhook...")
    print("=" * 50)
    
    # Teste 1: Formato real do WhatsApp
    print("\n📱 TESTE 1: Formato real do WhatsApp")
    print("-" * 30)
    
    with open('test_real_webhook.json', 'r', encoding='utf-8') as f:
        webhook_data_real = json.load(f)
    
    resultado_real = extrair_dados_whatsapp(webhook_data_real)
    
    if resultado_real:
        print("✅ Dados extraídos com sucesso!")
        print(f"📱 Número: {resultado_real.get('numero', 'N/A')}")
        print(f"💬 Mensagem: {resultado_real.get('mensagem', 'N/A')}")
        print(f"⏰ Timestamp: {resultado_real.get('timestamp', 'N/A')}")
        print(f"🆔 Phone Number ID: {resultado_real.get('phone_number_id', 'N/A')}")
        print(f"📞 Display Phone Number: {resultado_real.get('display_phone_number', 'N/A')}")
        print(f"👤 Nome do Contato: {resultado_real.get('nome_contato', 'N/A')}")
    else:
        print("❌ Falha ao extrair dados do formato real")
        return False
    
    # Teste 2: Formato antigo/teste
    print("\n📱 TESTE 2: Formato antigo/teste")
    print("-" * 30)
    
    with open('test_old_format.json', 'r', encoding='utf-8') as f:
        webhook_data_old = json.load(f)
    
    resultado_old = extrair_dados_whatsapp(webhook_data_old)
    
    if resultado_old:
        print("✅ Dados extraídos com sucesso!")
        print(f"📱 Número: {resultado_old.get('numero', 'N/A')}")
        print(f"💬 Mensagem: {resultado_old.get('mensagem', 'N/A')}")
        print(f"⏰ Timestamp: {resultado_old.get('timestamp', 'N/A')}")
    else:
        print("❌ Falha ao extrair dados do formato antigo")
        return False
    
    print("\n🎉 Todos os testes passaram!")
    return True

if __name__ == "__main__":
    success = test_webhook_extraction()
    sys.exit(0 if success else 1)
