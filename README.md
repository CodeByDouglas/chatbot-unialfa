# 🤖 ChatBot UNIALFA

Um chatbot inteligente desenvolvido para a UNIALFA que utiliza a API do Groq para fornecer assistência aos alunos através do WhatsApp Business API.

## 🚀 Funcionalidades

- **Webhook do WhatsApp**: Recebe mensagens do WhatsApp Business API
- **IA Inteligente**: Integração otimizada com Groq API para respostas contextuais
- **Histórico Completo**: Armazena conversas com identificação de usuário (aluno/bot)
- **Contexto Dinâmico**: Sistema de documentação atualizável via API
- **Limpeza Automática**: Remove histórico de usuários inativos há mais de 24h
- **Logs Detalhados**: Sistema completo de logging para monitoramento
- **Arquitetura Limpa**: Código organizado seguindo melhores práticas
- **Otimização Groq**: Uso correto de roles (system, user, assistant) e parâmetros otimizados

## 🏗️ Arquitetura

```
ChatBot UNIALFA/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── controllers/             # Controllers (Rotas/Endpoints)
│   │   ├── __init__.py
│   │   ├── webhook.py          # Webhook do WhatsApp
│   │   └── context.py          # Gerenciamento de contexto
│   ├── services/               # Serviços de negócio
│   │   ├── __init__.py
│   │   ├── groq_service.py     # Integração Groq API
│   │   └── cleanup_service.py  # Limpeza automática
│   └── utils/                  # Utilitários
│       ├── __init__.py
│       └── whatsapp_utils.py   # Utilitários WhatsApp
├── config.py                   # Configurações centralizadas
├── db_manager.py               # Gerenciamento do banco SQLite
├── run.py                      # Ponto de entrada da aplicação
└── requirements.txt            # Dependências
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
# Crie um arquivo .env
GROQ_API_KEY=sua_chave_aqui
SECRET_KEY=sua_chave_secreta
FLASK_DEBUG=True
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

## ⚙️ Configuração

O projeto usa um sistema de configuração centralizado em `config.py`:

```python
# Configurações disponíveis
GROQ_API_KEY=sua_chave_aqui
SECRET_KEY=sua_chave_secreta
FLASK_DEBUG=True
DATABASE_PATH=chatbot.db
HOST=0.0.0.0
PORT=5000
LOG_LEVEL=INFO
CLEANUP_INTERVAL_HOURS=24
INACTIVE_USER_HOURS=24
```

## 🔧 Configuração WhatsApp Business API

1. Configure o webhook URL no painel do WhatsApp Business
2. Implemente a função `enviar_resposta_whatsapp()` em `webhook.py`
3. Adicione autenticação da API

## 🤖 Otimizações da API Groq

O sistema implementa otimizações avançadas para maximizar a qualidade das respostas da IA:

### Estrutura de Mensagens
- **Role System**: Contém o prompt principal e a base de conhecimento
- **Role User**: Mensagens dos alunos/usuários
- **Role Assistant**: Respostas anteriores do bot

### Parâmetros Otimizados
```python
{
    "temperature": 0.7,    # Criatividade balanceada
    "max_tokens": 800,     # Limite de resposta
    "top_p": 0.9          # Diversidade controlada
}
```

### Processamento de Histórico
- Conversão inteligente do histórico formatado em mensagens individuais
- Identificação automática de roles baseada no usuário
- Remoção de timestamps e formatação desnecessária
- Manutenção do contexto conversacional

### Benefícios
- ✅ Respostas mais contextuais e precisas
- ✅ Melhor compreensão do histórico da conversa
- ✅ Redução de repetições desnecessárias
- ✅ Otimização de tokens e custos
- ✅ Conformidade com as melhores práticas da API Groq

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

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-flask

# Executar testes
pytest
```

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
