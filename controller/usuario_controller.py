from flask import request
from app import app
from services.usuario_service import create_usuario, update_usuario, get_usuario, get_all_usuarios, delete_usuario

# Registrando as CRUD para gerenciamento de usuários
@app.route('/usuario', methods=['GET'])
def get_users():
    with app.app_context():  # Cria o contexto da aplicação
        return get_all_usuarios()


@app.route('/usuario', methods=['POST'])
def create_user():
    with app.app_context():
        data = request.get_json()
        return create_usuario(data)


@app.route('/usuario/<int:id>', methods=['PUT'])
def update_user(id):
    with app.app_context():
        data = request.get_json()
        return update_usuario(data, id)


@app.route('/usuario/<int:id>', methods=['DELETE'])
def delete_user(id):
    with app.app_context():
        return delete_usuario(id)


@app.route('/usuario/<int:id>', methods=['GET'])
def get_user(id):
    with app.app_context():
        return get_usuario(id)
