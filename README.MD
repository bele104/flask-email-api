# api-email-n8n

API em Flask para envio automatizado de e-mails, integrada com [N8N](https://n8n.io/).  
Permite gerenciar listas de destinatários e templates HTML de forma dinâmica, garantindo disparos centralizados e evitando envio duplicado.

---

## ⚡ Funcionalidades

- Recebe dados via JSON e mantém lista persistente enquanto a API estiver ativa.
- Integração com templates HTML para personalização de e-mails.
- Endpoint dedicado para disparo de e-mails.
- Suporte a múltiplos destinatários agrupados por áreas.
- Compatível com N8N para automação de workflows.
- Previne envio duplicado e controla fluxo de e-mails.

---

## 📂 Estrutura do Projeto

