# ===============================
# Imagem base do Python
# ===============================
FROM python:3.11-slim

# ===============================
# Variáveis de ambiente
# ===============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ===============================
# Diretório de trabalho
# ===============================
WORKDIR /app

# ===============================
# Copiar dependências primeiro
# (melhora cache do Docker)
# ===============================
COPY requirements.txt .

# ===============================
# Instalar dependências
# ===============================
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Copiar o restante do projeto
# ===============================
COPY . .

# ===============================
# Expor a porta da API
# ===============================
EXPOSE 5000

# ===============================
# Comando de execução
# ===============================
CMD ["python", "app.py"]
