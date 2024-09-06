from flask import  request
from app import app
from services.campos_service import create_campo, update_campo, get_campo, get_all_campo, delete_campo


# Registrando as CRUD para gerenciamento de campos
@app.route('/campo', methods=['GET'])
def get_fields():
    with app.app_context():  # Cria o contexto da aplicação
        return get_all_campo()


@app.route('/campo', methods=['POST'])
def create_fields():
    with app.app_context():
        data = request.get_json()
        return create_campo(data)


@app.route('/campo/<int:id>', methods=['PUT'])
def update_fields(id):
    with app.app_context():
        data = request.get_json()
        return update_campo(data, id)


@app.route('/campo/<int:id>', methods=['DELETE'])
def delete_field(id):
    with app.app_context():
        return delete_campo(id)


@app.route('/campo/<int:id>', methods=['GET'])
def get_field(id):
    with app.app_context():
        return get_campo(id)

