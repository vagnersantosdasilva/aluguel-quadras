from models import Usuario
from app import db
from flask import jsonify, request
import bcrypt


# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response


def get_all_usuarios():
    try:
        usuarios = Usuario.query.all()
        usuarios_list = [usuario.to_dict() for usuario in usuarios]
        return jsonify(usuarios_list), 200
    except Exception as e:
        return handle_error(str(e), 500)


def create_usuario(data):
    try:
        # Criptografar a senha com bcrypt
        password = data.get('password')
        if not password:
            return handle_error("Password é necessário", 400)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Criar novo objeto Usuario
        data['password'] = hashed_password.decode('utf-8')
        new_usuario = Usuario(**data)
        db.session.add(new_usuario)
        db.session.commit()
        return jsonify(new_usuario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


def update_usuario(data, id):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return handle_error(f"Usuario com ID {id} não encontrado", 404)

        # Atualizar senha se estiver presente
        if 'password' in data:
            password = data.get('password')
            if password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                data['password'] = hashed_password.decode('utf-8')

        for key, value in data.items():
            setattr(usuario, key, value)
        db.session.commit()

        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


def get_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return handle_error(f"Usuario com ID {id} não encontrado", 404)

        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        return handle_error(str(e), 500)


def delete_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return handle_error(f"Usuario com ID {id} não encontrado", 404)

        db.session.delete(usuario)
        db.session.commit()

        return jsonify({'message': f"Usuario com ID {id} deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


def check_usuario_password(usuario_id, password):
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return handle_error(f"Usuario com ID {usuario_id} não encontrado", 404)

        if bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
            return jsonify({'message': "Senha correta"}), 200
        else:
            return handle_error("Senha incorreta", 401)
    except Exception as e:
        return handle_error(str(e), 500)
