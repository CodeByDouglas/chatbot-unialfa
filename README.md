# 🤖 ChatBot UNIALFA

Um chatbot inteligente desenvolvido para a UNIALFA que utiliza a API do Groq para fornecer assistência aos alunos através do WhatsApp Business API.

## 🚀 Funcionalidades

- **Webhook do WhatsApp**: Recebe mensagens do WhatsApp Business API
- **IA Inteligente**: Integração com Groq API para respostas contextuais
- **Histórico Completo**: Armazena conversas com identificação de usuário (aluno/bot)
- **Contexto Dinâmico**: Sistema de documentação atualizável via API
- **Limpeza Automática**: Remove histórico de usuários inativos há mais de 24h
- **Logs Detalhados**: Sistema completo de logging para monitoramento

## 🏗️ Arquitetura

```
ChatBot UNIALFA/
├── app/
│   ├── __init__.py              # Configuração Flask
│   └── controler/
│       ├── Webhook.py           # Endpoints do webhook
│       ├── Request_grooq.py     # Integração Groq API
│       └── atualizar_contexto.py # Gerenciamento de contexto
├── database/
│   ├── __init__.py
│   └── envento_limpar_historico.py # Limpeza automática
├── db_manager.py                # Gerenciamento do banco SQLite
├── views.py                     # Consultas ao banco
├── run.py                       # Servidor Flask
└── requirements.txt             # Dependências
```

## 📋 Pré-requisitos

- Python 3.8+
- Conta no WhatsApp Business API
- Chave da API do Groq

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/CodeByDouglas/ChatBot-UNIALFA.git
cd ChatBot-UNIALFA
```

2. **Crie um ambiente virtual:**
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual:**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente:**
```bash
# Crie um arquivo .env (opcional)
GROQ_API_KEY=sua_chave_aqui
```

## 🚀 Execução

```bash
python run.py
```

O servidor estará disponível em `http://localhost:5000`

## 📡 Endpoints

### Webhook WhatsApp
- **POST** `/webhook` - Recebe mensagens do WhatsApp

### Gerenciamento de Contexto
- **POST** `/atualizar-contexto` - Atualiza documentação
- **GET** `/contexto` - Consulta documentação atual

### Histórico
- **GET** `/historico/<numero>` - Histórico por número
- **GET** `/historico` - Todo o histórico

## 🗄️ Banco de Dados

### Tabela `historico`
- `id` - Identificador único
- `numero` - Número do WhatsApp
- `mensagem` - Conteúdo da mensagem
- `user` - 'aluno' ou 'Bot UNIALFA'
- `horario_data` - Timestamp da mensagem

### Tabela `contexto`
- `id` - Identificador único
- `documentacao` - Texto da documentação

## 🔧 Configuração WhatsApp Business API

1. Configure o webhook URL no painel do WhatsApp Business
2. Implemente a função `enviar_resposta_whatsapp()` em `Webhook.py`
3. Adicione autenticação da API

## 📝 Exemplo de Uso

### Atualizar Contexto
```bash
curl -X POST http://localhost:5000/atualizar-contexto \
  -H "Content-Type: application/json" \
  -d '{"documentacao": "Nova documentação da UNIALFA..."}'
```

### Simular Webhook
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "5511999999999",
            "text": {"body": "Olá, preciso de informações"},
            "timestamp": "1234567890"
          }]
        }
      }]
    }]
  }'
```

## 🔄 Limpeza Automática

O sistema executa automaticamente uma limpeza a cada 24 horas, removendo mensagens de usuários inativos há mais de 24h.

## 📊 Logs

O sistema gera logs detalhados para:
- Recebimento de webhooks
- Processamento de mensagens
- Chamadas à API do Groq
- Operações no banco de dados
- Limpeza automática

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Douglas** - [CodeByDouglas](https://github.com/CodeByDouglas)

## 🙏 Agradecimentos

- UNIALFA pela oportunidade
- Groq pela API de IA
- WhatsApp Business API
