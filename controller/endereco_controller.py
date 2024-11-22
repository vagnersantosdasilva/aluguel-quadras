from flask import request
from app import app
from services.endereco_service import create_endereco, update_endereco, get_endereco, get_all_enderecos, delete_endereco


# Recuperar todos os endereços associados a um campo
@app.route('/endereco', methods=['GET'])
def get_all_enderecos_():
    with app.app_context():
        return get_all_enderecos()


# Criar um novo endereço associado a um campo
@app.route('/endereco', methods=['POST'])
def create_endereco_():
    with app.app_context():
        data = request.get_json()
        return create_endereco(data)


# Atualizar um endereço específico
@app.route('/endereco/<int:endereco_id>', methods=['PUT'])
def update_endereco_(endereco_id):
    with app.app_context():
        data = request.get_json()
        return update_endereco(data, endereco_id)


# Deletar um endereço específico
@app.route('/endereco/<int:endereco_id>', methods=['DELETE'])
def delete_endereco_(endereco_id):
    with app.app_context():
        return delete_endereco(endereco_id)


# Recuperar um endereço específico
@app.route('/endereco/<int:endereco_id>', methods=['GET'])
def get_endereco_(endereco_id):
    with app.app_context():
        return get_endereco(endereco_id)
