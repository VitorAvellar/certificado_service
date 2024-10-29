from flask import Flask, request, send_file, render_template
from models import db, Certificado
from database import init_db
import pdfkit
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificados.db'
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
    certificado = Certificado(nome=data['nome'], curso=data['curso'], data=data['data'])
    db.session.add(certificado)
    db.session.commit()

    # Renderize o template HTML do certificado
    html = render_template('certificado.html', nome=data['nome'], curso=data['curso'], data=data['data'])

    # Gera o PDF a partir do HTML
    pdf_path = f'certificados/{certificado.id}.pdf'
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdfkit.from_string(html, pdf_path)

    # Retorne a URL correta para download
    return {'id': certificado.id, 'pdf_url': f'/certificado/{certificado.id}'}


@app.route('/certificado/<int:id>', methods=['GET'])
def get_certificado(id):
    pdf_path = f'certificados/{id}.pdf'
    if os.path.exists(pdf_path):
        return send_file(pdf_path)
    return {'message': 'Certificado não encontrado'}, 404

if __name__ == '__main__':
    app.run(debug=True)
