# Usa uma imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da API para o container
COPY . .

# Instala o wkhtmltopdf para conversão de HTML para PDF
RUN apt-get update && apt-get install -y wkhtmltopdf && apt-get clean

# Expõe a porta que a API usará
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
