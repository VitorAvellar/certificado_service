from flask import Flask, request, send_file, render_template
from models import db, Certificado
from database import init_db
import pdfkit
import os
import random

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////certificados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    init_db()

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

    sequencia = ''.join([str(random.randint(0, 9)) for _ in range(10)])

    
    html = render_template(
        'certificado.html',
        nome=data['nome'],
        cpf=data['cpf'],
        nacionalidade=data['nacionalidade'],
        estado=data['estado'],
        curso=data['curso'],
        data=data['data']
    )

    pdf_filename = f"{data['nome']}_{sequencia}.pdf"  
    pdf_path = f'certificados/{pdf_filename}'
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdfkit.from_string(html, pdf_path)

    
    return {'nome': certificado.nome, 'pdf_url': f'/certificado/{pdf_filename}'}

@app.route('/certificado/<path:nome>', methods=['GET'])
def get_certificado(nome):
    pdf_path = f'certificados/{nome}'
    if os.path.exists(pdf_path):
        return send_file(pdf_path)
    return {'message': 'Certificado não encontrado'}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
