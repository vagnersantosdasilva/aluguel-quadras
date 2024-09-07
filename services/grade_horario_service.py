from models import GradeHorario, Campo
from app import db
from flask import jsonify, request
from datetime import datetime


# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response


def get_all_grades_horario(campo_id):
    try:
        grades = GradeHorario.query.filter_by(campo_id=campo_id).all()
        grades_list = [grade.to_dict() for grade in grades]
        return jsonify(grades_list), 200
    except Exception as e:
        return handle_error(str(e), 500)


def create_grade_horario(campo_id, data):
    try:
        # Verifica se o campo existe
        campo = Campo.query.get(campo_id)
        if not campo:
            return handle_error(f"Campo com ID {campo_id} não encontrado", 404)

        # Converte strings de horário para objetos datetime.time
        data['horario_abertura'] = datetime.strptime(data['horario_abertura'], "%H:%M").time()
        data['horario_fechamento'] = datetime.strptime(data['horario_fechamento'], "%H:%M").time()
        data['campo_id'] = campo_id

        new_grade = GradeHorario(**data)  # Cria um novo objeto GradeHorario
        db.session.add(new_grade)
        db.session.commit()
        return jsonify(new_grade.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


def update_grade_horario(grade_id, data):
    try:
        grade = GradeHorario.query.get(grade_id)
        if not grade:
            return handle_error(f"Grade de Horário com ID {grade_id} não encontrada", 404)

        if 'horario_abertura' in data:
            data['horario_abertura'] = datetime.strptime(data['horario_abertura'], "%H:%M").time()
        if 'horario_fechamento' in data:
            data['horario_fechamento'] = datetime.strptime(data['horario_fechamento'], "%H:%M").time()

        # Atualiza os atributos do objeto GradeHorario
        for key, value in data.items():
            setattr(grade, key, value)

        db.session.commit()
        return jsonify(grade.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


def get_grade_horario(grade_id):
    try:
        grade = GradeHorario.query.get(grade_id)
        if not grade:
            return handle_error(f"Grade de Horário com ID {grade_id} não encontrada", 404)

        return jsonify(grade.to_dict()), 200
    except Exception as e:
        return handle_error(str(e), 500)


def delete_grade_horario(grade_id):
    try:
        grade = GradeHorario.query.get(grade_id)
        if not grade:
            return handle_error(f"Grade de Horário com ID {grade_id} não encontrada", 404)

        db.session.delete(grade)
        db.session.commit()
        return jsonify({'message': f"Grade de Horário com ID {grade_id} deletada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)
