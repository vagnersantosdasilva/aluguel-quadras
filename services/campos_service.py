from models import Campo
from app import db
from flask import jsonify, request

# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response

def get_all_campo():
    try:
        campos = Campo.query.all()  # Recupera todos os objetos Campo
        campos_list = [campo.to_dict() for campo in campos]  # Converte cada objeto para dicionário
        return jsonify(campos_list), 200
    except Exception as e:
        return handle_error(str(e), 500)

def create_campo(data):
    try:
        new_campo = Campo(**data)  # Cria um novo objeto Campo com os dados do JSON
        db.session.add(new_campo)  # Adiciona o objeto à sessão do SQLAlchemy
        db.session.commit()  # Commita as alterações no banco de dados
        return jsonify(new_campo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

def update_campo(data, id):
    try:
        campo = Campo.query.get(id)  # Busca o campo pelo ID
        if not campo:
            return handle_error(f"Campo com ID {id} não encontrado", 404)

        for key, value in data.items():
            setattr(campo, key, value)  # Atualiza os atributos do objeto Campo
        db.session.commit()  # Commita as alterações no banco de dados

        return jsonify(campo.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

def get_campo(id):
    try:
        campo = Campo.query.get(id)  # Busca o campo pelo ID
        if not campo:
            return handle_error(f"Campo com ID {id} não encontrado", 404)

        return jsonify(campo.to_dict()), 200
    except Exception as e:
        return handle_error(str(e), 500)

def delete_campo(id):
    try:
        campo = Campo.query.get(id)  # Busca o campo pelo ID
        if not campo:
            return handle_error(f"Campo com ID {id} não encontrado", 404)

        db.session.delete(campo)  # Remove o objeto do banco de dados
        db.session.commit()  # Commita as alterações no banco de dados

        return jsonify({'message': f"Campo com ID {id} deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)
