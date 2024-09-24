from flask import  request
from app import app
from services.aluguel_service import alugar_campo, cancelar_aluguel_campo,adicionar_usuario_lista_espera


@app.route('/locacao', methods=['POST'])
def alugar_campo_controller():
    with app.app_context():
        data = request.get_json()
        return alugar_campo(data)

@app.route('/locacao/cancelamento', methods=['PUT'])
def cancelar_aluguel_controller():
    with app.app_context():
        data = request.get_json()
        return cancelar_aluguel_campo(data)


@app.route('/locacao/listaespera', methods=['POST'])
def adicionar_lista_espera():
    with app.app_context():
        data = request.get_json()
        return adicionar_usuario_lista_espera(data)
