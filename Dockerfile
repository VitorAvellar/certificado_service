FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y wkhtmltopdf && apt-get clean

EXPOSE 5000

CMD ["python", "app.py"]
