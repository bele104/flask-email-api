import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

# ===============================
# 🔐 Carregar credenciais (.env)
# ===============================
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# ===============================
# 📧 Configuração de e-mail
# ===============================
REMETENTE = "vinicius.silva@srna.co"

DESTINATARIOS = {
    "Contatos": os.getenv("DESTINATARIOS_CONTATOS", "").split(","),
    "teste": os.getenv("DESTINATARIOS_TESTE", "").split(",")
}

# ===============================
# 🔑 Obter token Microsoft Graph
# ===============================
def obter_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )

    token = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    return token.get("access_token")


# ===============================
# ✉️ Enviar e-mail (HTML)
# ===============================
def enviar_email(area, html):
    token = obter_token()
    destinatarios = DESTINATARIOS.get(area)

    if not destinatarios:
        raise ValueError(f"Área '{area}' não encontrada.")

    payload = {
        "message": {
            "subject": f"Tarefas da Área: {area}",
            "body": {
                "contentType": "HTML",
                "content": html
            },
            "toRecipients": [
                {"emailAddress": {"address": email}}
                for email in destinatarios
            ]
        },
        "saveToSentItems": True
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{REMETENTE}/sendMail",
        headers=headers,
        json=payload
    )

    if response.status_code == 202:
        print(f"[OK] E-mail enviado para a área '{area}'")
    else:
        print(f"[ERRO] {response.status_code} - {response.text}")
