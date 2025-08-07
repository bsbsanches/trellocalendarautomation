import os
import json
import datetime
from dotenv import load_dotenv
from trello import TrelloClient
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ─── Carrega variáveis do .env ─────────────────────────────────
load_dotenv()  # Lê o arquivo .env e popula as variáveis de ambiente

# ─── Configurações ────────────────────────────────────────────────
LIST_ID        = os.getenv("TRELLO_LIST_ID")  # ID da lista no Trello
API_KEY        = os.getenv("TRELLO_KEY")       # Chave da API do Trello
TOKEN          = os.getenv("TRELLO_TOKEN")     # Token de acesso ao Trello
STATE_FILE     = "processed_cards.json"         # Onde guardamos os IDs já processados
CREDENTIALS    = "credentials.json"             # Credenciais do Google Cloud
TOKEN_FILE     = "token.json"                   # Arquivo de token gerado pelo OAuth
SCOPES         = ['https://www.googleapis.com/auth/calendar']
TIMEZONE       = 'America/Sao_Paulo'
DEFAULT_DUR_HR = 1                                # Duração padrão do evento (horas)
# ────────────────────────────────────────────────────────────────

# Inicializa cliente Trello
trello = TrelloClient(api_key=API_KEY, token=TOKEN)

# Função para obter serviço do Google Calendar
def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

# Carrega estado anterior (IDs processados)
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        processed = set(json.load(f))
else:
    processed = set()

# Pega os cartões da lista
trello_list = trello.get_list(LIST_ID)
cards = trello_list.list_cards()

calendar_service = get_calendar_service()

# Processa cada cartão não processado
for card in cards:
    if card.id not in processed:
        # Define horário do evento
        if card.due:
            start = datetime.datetime.fromisoformat(card.due)
            end = start + datetime.timedelta(hours=DEFAULT_DUR_HR)
        else:
            start = datetime.datetime.now() + datetime.timedelta(minutes=5)
            end = start + datetime.timedelta(hours=DEFAULT_DUR_HR)

        event = {
            'summary':     card.name,
            'description': card.desc or '',
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': TIMEZONE,
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': TIMEZONE,
            },
        }

        created = calendar_service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        print(f"[+] Evento criado para '{card.name}': {created.get('htmlLink')}")
        processed.add(card.id)

# Salva o estado atualizado com todos os cartões processados
with open(STATE_FILE, 'w') as f:
    json.dump(list(processed), f)

print("✓ Integração concluída.")
