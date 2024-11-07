# Dockerfile para o Worker
FROM python:3.9-slim

WORKDIR /app

# Copiar o arquivo de requisitos
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta, embora o worker não precise de porta exposta
EXPOSE 5000

# Definir o comando para rodar o worker
CMD ["python", "worker.py"]
