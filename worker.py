import pika
import json
import os
import time
from flask import Flask, render_template
from models import db, Certificado
from database import init_db
import pdfkit

# Configura o Flask para acessar templates e banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////certificados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Função para conectar ao RabbitMQ com retentativas
def connect_to_rabbitmq(retries=5, delay=5):
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"Tentativa {i + 1} de conectar ao RabbitMQ falhou. Retentando em {delay} segundos...")
            time.sleep(delay)
    raise Exception("Não foi possível conectar ao RabbitMQ após várias tentativas.")

# Função de callback para processar mensagens
def callback(ch, method, properties, body):
    data = json.loads(body)
    with app.app_context():
        # Renderiza o template HTML do certificado
        html = render_template(
            'certificado.html',
            nome=data['nome'],
            cpf=data['cpf'],
            nacionalidade=data['nacionalidade'],
            estado=data['estado'],
            curso=data['curso'],
            data=data['data']
        )

        # Gera o PDF
        pdf_filename = f"{data['nome']}.pdf"
        pdf_path = f'certificados/{pdf_filename}'
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        pdfkit.from_string(html, pdf_path)
        print(f"Certificado para {data['nome']} gerado e salvo em {pdf_path}")

# Configura a conexão e inicia o worker
def start_worker():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='certificados')
    channel.basic_consume(queue='certificados', on_message_callback=callback, auto_ack=True)
    print('Worker esperando por mensagens...')
    channel.start_consuming()

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Certifique-se de que o banco de dados está inicializado
    start_worker()
