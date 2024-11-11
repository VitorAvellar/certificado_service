from flask import Flask, request, jsonify
from models import db, Certificado
from database import init_db
import pika
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////certificados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Inicializa o banco de dados
with app.app_context():
    init_db()

# Configura conexão com RabbitMQ
def publish_message_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='certificados')
    channel.basic_publish(exchange='', routing_key='certificados', body=json.dumps(message))
    connection.close()

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

    # Envia a tarefa para a fila do RabbitMQ
    publish_message_to_queue({
        'nome': data['nome'],
        'cpf': data['cpf'],
        'nacionalidade': data['nacionalidade'],
        'estado': data['estado'],
        'curso': data['curso'],
        'data': data['data']
    })

    return jsonify({'status': 'Certificado em processamento', 'nome': certificado.nome})

if __name__ == '__main__':
    app.run(debug=True)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
