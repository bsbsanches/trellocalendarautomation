# Trello → Google Calendar Automation

Automatiza a criação de eventos no Google Calendar sempre que um cartão é criado/movido em uma lista específica do Trello.

---

## Sumário

- [Pré-requisitos](#pré-requisitos)  
- [Instalação](#instalação)  
- [Configuração](#configuração)  
  - [Trello API](#trello-api)  
  - [Google Calendar API](#google-calendar-api)  
  - [Variáveis de Ambiente](#variáveis-de-ambiente)  
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Uso](#uso)  
  - [1. Obter IDs de Lista Trello](#1-obter-ids-de-lista-trello)  
  - [2. Executar o servidor de Webhook](#2-executar-o-servidor-de-webhook)  
  - [3. Expor via Ngrok](#3-expor-via-ngrok)  
  - [4. Registrar Webhook no Trello](#4-registrar-webhook-no-trello)  
  - [5. Executar a Automação](#5-executar-a-automação)  
- [Desenvolvimento](#desenvolvimento)  
- [Licença](#licença)  

---

## Pré-requisitos

- **Python** ≥ 3.8  
- **pip** (gerenciador de pacotes Python)  
- Conta no **Trello** com permissão para criar tokens e webhooks  
- Conta no **Google Cloud** com a **Google Calendar API** habilitada  
- **Ngrok** (para expor o servidor local)  

---

## Instalação

```bash
# 1. Clone o repositório
git clone git@github.com:bsbsanches/trellocalendarautomation.git
cd trellocalendarautomation

# 2. Crie e ative um ambiente virtual
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# 3. Instale as dependências
pip install -r requirements.txt
