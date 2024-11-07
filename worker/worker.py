import pika
import pdfkit
import os
import json
from flask import Flask
from models import db, Certificado
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/certificados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
QUEUE_NAME = 'certificados_queue'

def process_certificado(data, certificado_id):
    certificado = Certificado.query.get(certificado_id)

    html = render_template(
        'certificado.html',
        nome=data['nome'],
        cpf=data['cpf'],
        nacionalidade=data['nacionalidade'],
        estado=data['estado'],
        curso=data['curso'],
        data=data['data']
    )

    pdf_filename = f"{data['nome']}.pdf"
    pdf_path = f'certificados/{pdf_filename}'
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdfkit.from_string(html, pdf_path)

    certificado.pdf_url = pdf_path
    db.session.commit()

def callback(ch, method, properties, body):
    message = json.loads(body)
    data = message['data']
    certificado_id = message['certificado_id']
    
    with app.app_context():
        process_certificado(data, certificado_id)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    print('Esperando por mensagens. Para sair pressione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
