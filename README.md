# Gestão de Eventos - API REST

Um sistema completo de gerenciamento de eventos desenvolvido com Django REST Framework, permitindo criar, gerenciar e inscrever participantes em eventos com sistema de pagamento integrado.

---

## 📋 Sumário
- [Visão Geral](#visão-geral)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Requisitos](#requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos de Dados](#modelos-de-dados)
- [Endpoints da API](#endpoints-da-api)
- [Permissões e Autenticação](#permissões-e-autenticação)
- [Fluxo de Funcionamento](#fluxo-de-funcionamento)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Uso e Exemplos](#uso-e-exemplos)

---

## 🎯 Visão Geral

A plataforma **Gestão de Eventos** é uma API REST que permite:
- **Organizadores** criarem e gerenciarem eventos
- **Participantes** se inscreverem em eventos
- **Sistema de pagamentos** para validar inscrições
- **Gerenciamento de emails** para comunicação com participantes
- **Relatórios** com estatísticas de eventos e participantes
- **Controle de lotação** de eventos

O sistema foi construído seguindo os princípios de arquitetura RESTful, com suporte a autenticação baseada em tokens e controle granular de permissões.

---

## ✨ Funcionalidades Principais

### Para Organizadores:
- ✅ Criar e gerenciar eventos
- ✅ Definir título, descrição, data/hora, localização, lotação e preço
- ✅ Visualizar todas as inscrições em seus eventos
- ✅ Confirmar inscrições após pagamento
- ✅ Cancelar inscrições e processar reembolsos
- ✅ Visualizar histórico de emails enviados
- ✅ Acessar relatórios de eventos

### Para Participantes:
- ✅ Se inscrever em eventos
- ✅ Visualizar eventos disponíveis
- ✅ Acompanhar status de inscrições
- ✅ Realizar pagamentos para confirmar inscrição
- ✅ Visualizar eventos em que está inscrito
- ✅ Ver perfil pessoal

### Sistema Geral:
- ✅ Envio automático de emails de confirmação,lembrete,reembolso,cancelamento.
- ✅ Controle de lotação de eventos
- ✅ Validação de datas
- ✅ Sistema de relatórios
- ✅ Transações atômicas para evitar race conditions

---

## 💻 Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|-----------|--------|-----------|
| Django | 6.0 | Framework web Python |
| Django REST Framework | - | Toolkit para construir APIs REST |
| Python | 3.x | Linguagem de programação |
| SQLite | - | Banco de dados (padrão) |
| Django Token Auth | - | Autenticação baseada em tokens |
| python-dotenv | - | Gerenciamento de variáveis de ambiente |

---

## 📦 Requisitos

### Sistema:
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

### Dependências Python:
```
Django==6.0
djangorestframework
python-dotenv
```

---

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone <https://github.com/denysbp/API-Eventos>
cd eventos
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
# No Windows
venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Criar arquivo `.env` na raiz do projeto:
```env
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
EMAIL=seu-email@gmail.com
PASSWORD_EMAIL=sua-senha-de-app-gmail
```

### 5. Executar Migrações
```bash
python manage.py migrate
```

### 6. Criar Superusuário (Admin)
```bash
python manage.py createsuperuser
```

### 7. Iniciar o Servidor
```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`

---

## 📁 Estrutura do Projeto

```
eventos/
├── manage.py                 # Utilitário de linha de comando Django
├── db.sqlite3               # Banco de dados SQLite
├── README.md                # Este arquivo
├── LICENSE                  # Licença do projeto
│
├── eventos/                 # Configuração principal do Django
│   ├── __init__.py
│   ├── settings.py         # Configurações do projeto
│   ├── urls.py             # Rotas principais
│   ├── asgi.py             # ASGI config
│   └── wsgi.py             # WSGI config
│
└── core/                    # App principal da aplicação
    ├── models.py           # Modelos de dados
    ├── views.py            #  APIViews
    ├── serializers.py      # Serializadores DRF
    ├── permissions.py      # Permissões customizadas
    ├── urls.py             # Rotas da API
    ├── admin.py            # Interface admin Django
    ├── apps.py             # Configuração da app
    ├── signals.py          # Sinais Django
    ├── tests.py            # Testes unitários
    │
    ├── migrations/         # Migrações do banco de dados
    │   ├── __init__.py
    │   └── 0001_initial.py
    │
    └── management/         # Comandos customizados
        └── commands/
            ├── __init__.py
            └── atualizar_pagamentos.py
```

---

## 🗄️ Modelos de Dados

### 1. **Organizador**
Estende o modelo User do Django para representar criadores de eventos.

**Campos:**
- `user` (OneToOneField) - Relação com usuário Django
- `nome` (CharField) - Nome do organizador
- `email` (EmailField) - Email único

```python
# Exemplo de relacionamento:
organizador.user.username
organizador.organizador_eventos.all()  # Todos os eventos criados
```

### 2. **Participante**
Estende o modelo User do Django para representar inscritos em eventos.

**Campos:**
- `user` (OneToOneField) - Relação com usuário Django
- `nome` (CharField) - Nome do participante
- `email` (EmailField) - Email único

```python
# Exemplo de relacionamento:
participante.inscritos.all()  # Todas as inscrições do participante
```

### 3. **Eventos**
Representa um evento criado por um organizador.

**Campos:**
- `organizador` (ForeignKey) - Criador do evento
- `titulo` (CharField) - Título do evento
- `descricao` (TextField) - Descrição até 300 caracteres
- `inicio` (DateTimeField) - Data/hora de início
- `fim` (DateTimeField) - Data/hora de término
- `localizacao` (CharField) - Localização do evento
- `Lotacao` (PositiveBigIntegerField) - Capacidade máxima
- `preco` (IntegerField) - Preço da inscrição
- `status` (CharField) - Estado do evento (ATIVO, LOTADO, CONCLUÍDO, CANCELADO)
- `inscritos` (IntegerField) - Número de inscritos confirmados

**Status do Evento:**
- `A` - ATIVO (aceitando inscrições)
- `L` - LOTADO (capacidade máxima atingida)
- `C` - CONCLUÍDO (evento finalizado)
- `X` - CANCELADO

**Validações:**
- Data de término deve ser posterior à data de início

### 4. **Inscricoes**
Representa a inscrição de um participante em um evento.

**Campos:**
- `participante` (ForeignKey) - Participante inscrito
- `evento` (ForeignKey) - Evento em que se inscreveu
- `status` (CharField) - Estado da inscrição
- `data` (DateTimeField) - Data da inscrição (auto)
- `pago` (BooleanField) - Indica se pagou

**Status da Inscrição:**
- `P` - PENDENTE (aguardando pagamento)
- `C` - CONFIRMADA (pagamento confirmado)
- `X` - CANCELADA
- `R` - REEMBOLSADO (reembolso processado)

**Funcionalidades:**
- Validação de lotação automática
- Envio de email de confirmação
- Criação automática de registro de pagamento

### 5. **Pagamentos**
Controla os pagamentos das inscrições.

**Campos:**
- `evento` (ForeignKey) - Evento
- `participante` (ForeignKey) - Participante
- `pago` (IntegerField) - Valor a pagar
- `status` (CharField) - Status do pagamento
- `ativo` (BooleanField) - Indica se está ativo

### 6. **Email**
Registro de todos os emails enviados pelo sistema.

**Campos:**
- `destinatario` (ForeignKey) - Participante
- `evento` (ForeignKey) - Evento relacionado
- `tipo` (CharField) - Tipo de email
- `assunto` (CharField) - Assunto do email
- `mensagem` (TextField) - Corpo do email
- `status` (CharField) - Status de envio
- `data_criacao` (DateTimeField) - Quando foi criado
- `data_envio` (DateTimeField) - Quando foi enviado
- `tentativas` (IntegerField) - Número de tentativas

### 7. **Relatorio**
Mantém estatísticas gerais do sistema (apenas um registro permitido).

**Métodos:**
- `total_evento()` - Total de eventos
- `total_inscritos()` - Total de participantes
- `evento_populares()` - Ranking de eventos mais populares

---

## 🔌 Endpoints da API

### Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/login/` | Fazer login e obter token |
| POST | `/api/auth/logout/` | Fazer logout |

### Usuários
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/criar/participante/` | Registrar novo participante |
| POST | `/criar/organizador/` | Registrar novo organizador |
| GET | `/perfil/` | Ver perfil do usuário logado |

### Eventos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/criar-evento/` | Criar novo evento (Organizador) |
| GET | `/ver-eventos/` | Listar todos os eventos |
| GET | `/ver-evento/<id>/` | Ver detalhes de um evento |
| GET | `/ver-eventos/organizador/` | Ver eventos do organizador logado |

### Inscrições
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/inscrever/evento/<evento_id>/` | Se inscrever em um evento (Participante) |
| GET | `/ver-eventos/inscritos/` | Ver eventos em que está inscrito |
| GET | `/ver-inscricoes/eventos/<evento_id>/` | Ver inscrições de um evento (Organizador) |
| PUT | `/incricao/<inscricao_id>/estado/confirmado/` | Confirmar inscrição (Organizador) |
| PUT | `/incricao/<inscricao_id>/estado/cancelada/` | Cancelar inscrição (Organizador) |
| PUT | `/incricao/<inscricao_id>/estado/reembolso/` | Processar reembolso (Organizador) |

### Pagamentos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/incricao/<inscricao_id>/pagamento/` | Ver status de pagamento |
| PUT | `/pagamento/<pagamento_id>/confirmar/` | Confirmar pagamento (Organizador) |

### Emails
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/emails/evento/<evento_id>/` | Listar emails de um evento (Organizador) |

### Relatórios
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/relatorio/` | Ver relatório geral |
| POST | `/relatorio/` | Criar relatório |

---

## 🔐 Permissões e Autenticação

### Tipos de Permissões

#### 1. **IsOrganizador**
Verifica se o usuário tem relacionamento com modelo `Organizador`.
```python
permission_classes = [IsAuthenticated, IsOrganizador]
```

#### 2. **IsParticipante**
Verifica se o usuário tem relacionamento com modelo `Participante`.
```python
permission_classes = [IsAuthenticated, IsParticipante]
```

#### 3. **AllowAny**
Permite acesso sem autenticação (para registro de novos usuários).

#### 4. **IsAuthenticated**
Requer que o usuário esteja autenticado via token.

### Fluxo de Autenticação

1. Usuário se registra como Organizador ou Participante
2. Sistema cria usuário Django e relacionado (Organizador/Participante)
3. Usuário faz login e recebe token
4. Token é incluído em todas as requisições: `Authorization: Token <seu-token>`

---

## 🔄 Fluxo de Funcionamento

### Fluxo de Inscrição

```
1. Participante se inscreve em evento
   ↓
2. Sistema valida:
   - Evento está ativo?
   - Já está inscrito?
   - Evento tem vagas?
   ↓
3. Inscrição criada com status PENDENTE
   ↓
4. Email de confirmação enviado
   ↓
5. Registro de pagamento criado
   ↓
6. Participante realiza pagamento
   ↓
7. Organizador confirma pagamento
   ↓
8. Inscrição atualizada para CONFIRMADA
   ↓
9. Vagas atualizadas e status do evento verificado
```

### Fluxo de Pagamento

```
1. Inscrição criada (PENDENTE)
   ↓
2. Pagamento registrado (PENDENTE)
   ↓
3. Participante realiza pagamento externo
   ↓
4. Organizador confirma pagamento via API
   ↓
5. Inscrição marcada como PAGA e CONFIRMADA
   ↓
6. Status do evento verificado (ATIVO/LOTADO)
```

### Fluxo de Email

```
1. Inscrição criada
   ↓
2. Evento de sinal (signal) disparado
   ↓
3. Email de confirmação criado no banco
   ↓
4. Email enviado para participante
   ↓
5. Registro mantido no histórico
```

---

## 🔧 Variáveis de Ambiente

Criar arquivo `.env` com as seguintes variáveis:

```env
# Django
DJANGO_SECRET_KEY=sua-chave-secreta-super-segura-aqui

# Email (Gmail)
EMAIL=seu-email@gmail.com
PASSWORD_EMAIL=sua-senha-de-app-especifica-gmail

# Database (opcional para SQLite)
# DATABASE_URL=sqlite:///db.sqlite3

# Debug
# DEBUG=True
```

### Gerando Chave Secreta Django

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Configurando Gmail

1. Ativar autenticação de dois fatores no Gmail
2. Gerar "Senha de App" (não usar senha do Gmail)
3. Usar a "Senha de App" no arquivo `.env`

---

## 💡 Uso e Exemplos

### 1. Registrar Novo Participante

```bash
curl -X POST http://localhost:8000/criar/participante/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao_silva",
    "password": "senha123!",
    "nome": "João Silva",
    "email": "joao@example.com"
  }'
```

**Resposta:**
```json
{
  "nome": "João Silva",
  "email": "joao@example.com"
}
```

### 2. Registrar Novo Organizador

```bash
curl -X POST http://localhost:8000/criar/organizador/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria_org",
    "password": "senha123!",
    "nome": "Maria Oliveira",
    "email": "maria@example.com"
  }'
```

### 3. Criar um Evento (Organizador)

```bash
curl -X POST http://localhost:8000/criar-evento/ \
  -H "Authorization: Token seu-token-aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Workshop Python Avançado",
    "descricao": "Aprenda técnicas avançadas de Python",
    "inicio": "2026-02-15T09:00:00Z",
    "fim": "2026-02-15T17:00:00Z",
    "localizacao": "São Paulo, SP",
    "Lotacao": 50,
    "preco": 150
  }'
```

### 4. Ver Todos os Eventos

```bash
curl -X GET http://localhost:8000/ver-eventos/ \
  -H "Authorization: Token seu-token-aqui"
```

### 5. Se Inscrever em um Evento (Participante)

```bash
curl -X POST http://localhost:8000/inscrever/evento/1/ \
  -H "Authorization: Token seu-token-aqui" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Resposta:**
```json
{
  "status": "P",
  "data": "2026-01-22T10:30:00Z",
  "pago": false
}
```

### 6. Confirmar Inscrição (Organizador)

```bash
curl -X PUT http://localhost:8000/incricao/1/estado/confirmado/ \
  -H "Authorization: Token seu-token-aqui" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 7. Ver Inscrições de um Evento (Organizador)

```bash
curl -X GET http://localhost:8000/ver-inscricoes/eventos/1/ \
  -H "Authorization: Token seu-token-aqui"
```

**Resposta:**
```json
{
  "Evento": "Workshop Python Avançado",
  "total_inscritos": 10,
  "inscritos": [
    {
      "participante": "João Silva",
      "status": "C",
      "pago": true,
      "data": "2026-01-22T10:30:00Z"
    }
  ]
}
```

### 8. Ver Relatório

```bash
curl -X GET http://localhost:8000/relatorio/ \
  -H "Authorization: Token seu-token-aqui"
```

---

## 📊 Transações Atômicas

O projeto utiliza `transaction.atomic()` para garantir integridade de dados em operações críticas:

- Criação de relatório (evitar duplicatas)
- Confirmação de inscrição
- Cancelamento de inscrição
- Listagem de emails

---

## 🧪 Testes

Para executar os testes:

```bash
python manage.py test core
```

---

## 📝 Comandos Customizados

### Atualizar Pagamentos

Comando para atualizar status de pagamentos:

```bash
python manage.py atualizar_pagamentos
```

---

## 🔍 Validações Implementadas

1. **Validação de Datas** - Data fim deve ser posterior à data início
2. **Validação de Lotação** - Não permite inscrição acima da capacidade
3. **Validação de Duplicatas** - Participante não pode se inscrever duas vezes
4. **Validação de Username/Email** - Evita duplicatas no banco de dados
5. **Validação de Status** - Apenas eventos ATIVOS aceitam inscrições
6. **Validação de Permissões** - Apenas organizador do evento pode gerenciar

---

## 📞 Sinais (Signals)

O projeto usa Django Signals para:
- Enviar email ao criar inscrição
- Criar registro de pagamento automaticamente
- Atualizar status de eventos

---

## ⚡ Performance

- **select_related()** em querysets para reduzir N+1 queries
- **Transações atômicas** para operações críticas
- **Índices implícitos** no SQLite para foreign keys

---

## 🛡️ Segurança

- Autenticação baseada em tokens (Django Token Auth)
- Permissões granulares por tipo de usuário
- Variáveis sensíveis em arquivo `.env` (não versionado)
- Validação de entrada em todos os endpoints
- CSRF protection habilitado

---

## 📚 Documentação Adicional

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Docs](https://docs.djangoproject.com/)
- [Django Signals](https://docs.djangoproject.com/en/6.0/topics/signals/)

---

## 📄 Licença

Veja arquivo [LICENSE](LICENSE) para detalhes.

---

## 🤝 Contribuição

Para contribuir com melhorias:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📧 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Django REST Framework**

*Última atualização: 22 de janeiro de 2026*
