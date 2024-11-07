from flask import Flask, request, send_file, render_template
from models import db, Certificado
from database import init_db
import pdfkit
import os
import pika
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////certificados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'certificados_queue'

with app.app_context():
    init_db()


def send_task_to_queue(data, certificado_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    message = json.dumps({'data': data, 'certificado_id': certificado_id})

    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=message)

    # Fechar a conexão
    connection.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emitir_certificado', methods=['POST'])
def emitir_certificado():
    data = request.json
    certificado = Certificado(
        nome=data['nome'],
        cpf=data['cpf'],
        nacionalidade=data['nacionalidade'],
        estado=data['estado'],
        curso=data['curso'],
        data=data['data']
    )
    db.session.add(certificado)
    db.session.commit()

    send_task_to_queue(data, certificado.id)

    return {'nome': certificado.nome, 'status': 'Certificado em processamento'}

    html = render_template(
        'certificado.html',
        nome=data['nome'],
        cpf=data['cpf'],
        nacionalidade=data['nacionalidade'],
        estado=data['estado'],
        curso=data['curso'],
        data=data['data']
    )

    # Gera o PDF a partir do HTML
    pdf_filename = f"{data['nome']}.pdf"  # Nome do arquivo PDF
    pdf_path = f'certificados/{pdf_filename}'
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdfkit.from_string(html, pdf_path)

    # Retorne a URL correta para download
    return {'nome': certificado.nome, 'pdf_url': f'/certificado/{certificado.nome}'}

@app.route('/certificado/<string:nome>', methods=['GET'])
def get_certificado(nome):
    pdf_path = f'certificados/{nome}.pdf'
    if os.path.exists(pdf_path):
        return send_file(pdf_path)
    return {'message': 'Certificado não encontrado'}, 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

