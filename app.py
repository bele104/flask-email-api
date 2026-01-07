from flask import Flask, Response, request, jsonify, render_template_string
from pathlib import Path
from src.Emails import enviar_email

app = Flask(__name__)

# ===============================
# ESTADO GLOBAL DA APLICAÇÃO
# ===============================

# Lista em memória que recebe os itens enviados pelo n8n
JSON = []

# Flag para evitar envio duplicado de e-mails
EMAIL_ENVIADO = False

# Template HTML base do e-mail
email_template = Path("assets/email.html").read_text(encoding="utf-8")


# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def integrarEmail(template_html):
    """
    Injeta os dados do JSON no template HTML
    e retorna o HTML final renderizado.
    """
    return render_template_string(
        template_html,
        lista=JSON
    )


# ===============================
# ROTAS DA API
# ===============================

@app.route("/lista", methods=["GET"])
def ver_lista():
    """
    Retorna a lista atual de itens recebidos.
    """
    return jsonify(JSON)


@app.route("/lista", methods=["POST"])
def adicionar_item():
    """
    Recebe um item JSON e adiciona à lista.
    Também libera o envio de e-mail novamente.
    """
    global EMAIL_ENVIADO

    novo = request.get_json()

    # Validação simples do payload
    if not isinstance(novo, dict):
        return jsonify({"erro": "Envie um objeto JSON"}), 400

    # Adiciona item na lista
    JSON.append(novo)

    # Sempre que algo novo entra, permite novo envio
    EMAIL_ENVIADO = False

    return jsonify({
        "mensagem": "Item adicionado",
        "total": len(JSON)
    })


@app.route("/email", methods=["POST"])
def disparar_email():
    """
    Dispara o envio do e-mail apenas UMA vez
    por ciclo de dados.
    """
    global EMAIL_ENVIADO

    # Se já enviou, ignora chamadas repetidas
    if EMAIL_ENVIADO:
        return jsonify({
            "status": "ignorado",
            "motivo": "email já enviado"
        }), 409

    # Ativa a trava ANTES de enviar
    EMAIL_ENVIADO = True

    # Gera HTML final com os dados atuais
    html = integrarEmail(email_template)
    
    # Envia o e-mail
    enviar_email("Contatos", html)


    """
    # Envia o e-mail para teste
    enviar_email("teste", html)"""

    # Limpa a lista após envio
    JSON.clear()

    return jsonify({
        "mensagem": "email enviado com sucesso"
    })


@app.route("/", methods=["GET"])
def home():
    """
    Exibe o HTML renderizado no navegador
    para conferência visual.
    """
    html = integrarEmail(email_template)
    return Response(html, content_type="text/html; charset=utf-8")


# ===============================
# START DA APLICAÇÃO
# ===============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
