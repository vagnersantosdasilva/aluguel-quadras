from flask import request
from app import app
from services.endereco_service import create_endereco, update_endereco, get_endereco, get_all_enderecos, delete_endereco, get_endereco_by_campo


# Recuperar todos os endereços associados a um campo
@app.route('/endereco', methods=['GET'])
def get_all_enderecos_():
    with app.app_context():
        return get_all_enderecos()


# Criar um novo endereço associado a um campo
@app.route('/campo/<int:id>/endereco', methods=['POST'])
def create_endereco_(id):
    with app.app_context():
        data = request.get_json()
        return create_endereco(id, data)


# Atualizar um endereço específico
@app.route('/campo/<int:id_campo>/endereco/<int:endereco_id>', methods=['PUT'])
def update_endereco_(endereco_id,id_campo):
    with app.app_context():
        data = request.get_json()
        return update_endereco(data, endereco_id, id_campo)


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

@app.route('/campo/<int:campo_id>/endereco', methods=['GET'])
def get_endereco_by_campo_id(campo_id):
    with app.app_context():
        return get_endereco_by_campo(campo_id)
