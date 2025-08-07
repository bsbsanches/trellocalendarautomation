# webhook_server.py
from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

TARGET_LIST_ID = os.getenv("TRELLO_LIST_ID")

@app.route("/trello-webhook", methods=["HEAD", "POST"])
def trello_webhook():
    # Trello envia um HEAD para validar a URL
    if request.method == "HEAD":
        return "", 200

    payload = request.get_json(force=True)
    action  = payload.get("action", {})
    data    = action.get("data", {})

    # pode vir criação (data["list"]) ou movimento (data["listAfter"])
    list_id = data.get("list", {}).get("id") or \
              data.get("listAfter", {}).get("id")

    # --- DEBUG: veja no terminal do Flask o que chegou ---
    print(">>> WEBHOOK recebido:")
    print("    type   =", action.get("type"))
    print("    list_id=", list_id)

    # só dispara se for a lista que interessa
    if list_id == TARGET_LIST_ID:
        main_py = os.path.abspath("main.py")
        cwd     = os.path.dirname(main_py)
        print(f">>> Disparando main.py em {cwd}")
        # use call em vez de Popen para rodar em primeiro plano
        subprocess.call(["python", main_py], cwd=cwd)

    return "", 200

if __name__ == "__main__":
    # 0.0.0.0 para o ngrok conseguir acessar de fora
    app.run(host="0.0.0.0", port=5000)
