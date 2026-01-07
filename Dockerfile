# 1. Escolher a imagem base do Python
FROM python:3.11-slim

# 2. Criar pasta de trabalho dentro do container
WORKDIR /app

# 3. Copiar os arquivos da API para dentro do container
COPY requirements.txt .
COPY app.py .

# 4. Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expor a porta que a API vai usar
EXPOSE 5000

# 6. Comando para rodar a API
CMD ["python", "app.py"]
