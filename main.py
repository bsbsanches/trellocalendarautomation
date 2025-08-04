from __future__ import print_function
import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Escopo necessário para criar e editar eventos no Google Agenda
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None
    # O arquivo token.json salva as credenciais para reutilizar sem novo login
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Salva as credenciais
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Criar evento de teste
    event = {
        'summary': 'Reunião teste Trello → Google Agenda',
        'start': {
            'dateTime': '2025-08-05T10:00:00-03:00',
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': '2025-08-05T11:00:00-03:00',
            'timeZone': 'America/Sao_Paulo',
        }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Evento criado: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()