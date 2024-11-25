from flask import  request
from app import app
from services.grade_horario_service import create_grade_horario, update_grade_horario, delete_grade_horario, \
    get_grade_horario, get_all_grades_horario, create_array_grade_horario


# Registrando as CRUD para gerenciamento de campos
@app.route('/campo/<int:id>/grade', methods=['GET'])
def get_grade(id):
    with app.app_context():  # Cria o contexto da aplicação
        return get_all_grades_horario(id)

@app.route('/campo/<int:id>/grade', methods=['POST'])
def create_grade(id):
    with app.app_context():
        data = request.get_json()
        return create_array_grade_horario(id,data)


@app.route('/campo/<int:id_campo>/grade/<int:id>', methods=['PUT'])
def update_grade(id_campo,id):
    with app.app_context():
        data = request.get_json()
        return update_grade_horario(id_campo, id, data)


@app.route('/grade/<int:id>', methods=['DELETE'])
def delete_grade(id):
    with app.app_context():
        return delete_grade_horario(id)


@app.route('/grade/<int:id>', methods=['GET'])
def get_one_grade(id):
    with app.app_context():
        return get_grade_horario(id)
