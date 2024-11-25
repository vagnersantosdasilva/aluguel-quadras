from flask import request
from app import app
from services.grade_excecao_service import (
    get_all_excecoes,
    get_excecao,
    create_excecao,
    update_excecao,
    delete_excecao,
    get_excecoes_by_campo_id
)

# Rota para listar todas as exceções
@app.route('/campo/excecoes', methods=['GET'])
def get_excecoes():
    with app.app_context():
        return get_all_excecoes()

# Rota para criar uma nova exceção
@app.route('/campo/excecoes', methods=['POST'])
def create_excecao_route():
    with app.app_context():
        data = request.get_json()
        return create_excecao(data)

# Rota para recuperar uma exceção por ID
@app.route('/campo/<int:id>/excecoes', methods=['GET'])
def get_excecao_route(id):
    with app.app_context():
        return get_excecoes_by_campo_id(id)

# Rota para atualizar uma exceção
@app.route('/campo/excecoes/<int:id>', methods=['PUT'])
def update_excecao_route(id):
    with app.app_context():
        data = request.get_json()
        return update_excecao(data, id)

# Rota para deletar uma exceção
@app.route('/campo/excecoes/<int:id>', methods=['DELETE'])
def delete_excecao_route(id):
    with app.app_context():
        return delete_excecao(id)
