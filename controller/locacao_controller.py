from flask import  request
from app import app
from services.aluguel_service import alugar_campo


@app.route('/locacao', methods=['POST'])
def alugar_campo_controller():
    with app.app_context():
        data = request.get_json()
        return alugar_campo(data)


