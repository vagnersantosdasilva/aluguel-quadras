from flask import  request
from app import app
from services.imagem_service import create_imagem, update_imagem, get_imagem, get_all_imagem, delete_imagem


# Registrando as CRUD para gerenciamento de campos
@app.route('/campo/<int:id>/imagem', methods=['GET'])
def get_imagem_(id):
    with app.app_context():  # Cria o contexto da aplicação
        return get_all_imagem(id)


@app.route('/campo/<int:id>/imagem', methods=['POST'])
def create_imagem_(id):
    with app.app_context():
        data = request.get_json()
        return create_imagem(data)


@app.route('/campo/<int:id_campo>/imagem<int:id>', methods=['PUT'])
def update_imagem_(id_campo,id):
    with app.app_context():
        data = request.get_json()
        return update_imagem(data, id,id_campo)


@app.route('/campo/imagem/<int:id>', methods=['DELETE'])
def delete_imagem_(id):
    with app.app_context():
        return delete_imagem(id)


@app.route('/campo/<int:id_campo>/imagem/<int:id>', methods=['GET'])
def get_on_imagem_(id_campo,id):
    with app.app_context():
        return get_imagem(id)