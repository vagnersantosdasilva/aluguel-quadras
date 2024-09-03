from flask import Flask, request
from controller.campos_controller import get_all_campo, create_campo, update_campo, get_campo, delete_campo

app = Flask(__name__)

# Registrando as CRUD para gerenciamento de campos
@app.route('/fields', methods=['GET'])
def get_fields():
    with app.app_context():  # Cria o contexto da aplicação
        return get_all_campo()

@app.route('/fields',methods=['POST'])
def create_fields():
    with app.app_context():
        data = request.get_json()
        return create_campo(data)

@app.route('/fields/<int:id>',methods=['PUT'])
def update_fields(id):
    with app.app_context():
        data = request.get_json()
        return update_campo(data,id)

@app.route('/fields/<int:id>', methods=['DELETE'])
def delete_field(id):
    with app.app_context():
        return delete_campo(id)

@app.route('/fields/<int:id>', methods=['GET'])
def get_field(id):
    with app.app_context():
        return get_campo(id)

if __name__ == '__main__':
    app.run(debug=True)