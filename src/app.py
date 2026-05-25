import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, jsonify
from database import inicializar_banco
from routes import tarefas_bp

app = Flask(__name__, template_folder='../templates')
app.register_blueprint(tarefas_bp, url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health')
def health():
    return {'status': 'ok', 'sistema': 'TaskFlow', 'versao': '1.1.0'}


# tratamento de erro 404 global
@app.errorhandler(404)
def nao_encontrado(e):
    return jsonify({'erro': 'Recurso não encontrado'}), 404


# tratamento de erro 500 global
@app.errorhandler(500)
def erro_interno(e):
    return jsonify({'erro': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    inicializar_banco()
    print("TaskFlow v1.1.0 rodando em http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
