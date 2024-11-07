# Use uma imagem oficial do Python como base
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de dependências e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da API para o container
COPY . .

# Instale o wkhtmltopdf para conversão de HTML para PDF
RUN apt-get update && apt-get install -y wkhtmltopdf && apt-get clean

# Expõe a porta que a API usará
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
