

from models import GradeHorario, Campo
from app import db
from flask import jsonify, request
from datetime import datetime, time


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

            # Verifica se já existe uma grade com o mesmo dia da semana para o campo
        dia_existente = GradeHorario.query.filter_by(campo_id=campo_id, dia_semana=data['dia_semana']).first()
        if dia_existente:
            return handle_error(f"Já existe um horário cadastrado para o dia {data['dia_semana']} neste campo", 400)

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


def create_array_grade_horario(campo_id, array_data):
    try:
        # Verifica se o campo existe
        campo = Campo.query.get(campo_id)
        if not campo:
            return handle_error(f"Campo com ID {campo_id} não encontrado", 404)

        processed_grades = []  # Lista para armazenar as grades processadas

        for data in array_data:

            def parse_time(value):
                try:
                    return datetime.strptime(value, "%H:%M").time()
                except ValueError:
                    try:
                        return datetime.strptime(value, "%H:%M:%S").time()
                    except (ValueError, TypeError):
                        return time(0, 0)  # Valor padrão: 00:00 em caso de erro

            data['horario_abertura'] = parse_time(data.get('horario_abertura'))
            data['horario_fechamento'] = parse_time(data.get('horario_fechamento'))

                #return handle_error(f"Erro ao converter horários: {str(ve)}", 400)

            if data.get('id') and data.get('campo_id'):
                # Atualiza o objeto existente
                grade_existente = GradeHorario.query.filter_by(id=data['id'], campo_id=campo_id).first()
                if grade_existente:
                    grade_existente.dia_semana = data['dia_semana']
                    grade_existente.horario_abertura = data['horario_abertura']
                    grade_existente.horario_fechamento = data['horario_fechamento']
                    processed_grades.append(grade_existente)
                else:
                    return handle_error(f"Grade com ID {data['id']} não encontrada para o campo {campo_id}", 404)
            else:
                # Cria um novo objeto
                data['campo_id'] = campo_id
                new_grade = GradeHorario(**data)
                db.session.add(new_grade)
                processed_grades.append(new_grade)

        db.session.commit()  # Salva todas as alterações no banco de dados

        # Retorna as grades processadas (criadas ou atualizadas) como JSON
        return jsonify([grade.to_dict() for grade in processed_grades]), 201

    except Exception as e:
        db.session.rollback()  # Reverte as alterações no banco em caso de erro
        return handle_error(str(e), 500)


def update_grade_horario(id_campo, grade_id, data):
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
