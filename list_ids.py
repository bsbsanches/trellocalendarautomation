import os
from dotenv import load_dotenv
from trello import TrelloClient

load_dotenv()
client = TrelloClient(api_key=os.getenv("TRELLO_KEY"), token=os.getenv("TRELLO_TOKEN"))

# 1) Lista todos os quadros
print("Quadros disponíveis:")
for b in client.list_boards():
    print(f"- {b.name} (ID do quadro: {b.id})")

# 2) Defina aqui o ID do quadro que você quer inspecionar
BOARD_ID = "6870569880607a1a544e6698"

board = client.get_board(BOARD_ID)
print(f"\nExplorando o quadro '{board.name}':")

# 3) Para cada lista, imprime ID; para cada cartão, imprime ID
for lst in board.list_lists():
    print(f"Lista: {lst.name}  →  LIST_ID: {lst.id}")
    for card in lst.list_cards():
        print(f"    • {card.name}  →  CARD_ID: {card.id}")
