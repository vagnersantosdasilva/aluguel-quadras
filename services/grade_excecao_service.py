from models import ExcecaoHorario
from app import db
from flask import jsonify

# Handler para erros
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response


# Recupera todas as exceções
def get_all_excecoes():
    try:
        excecoes = ExcecaoHorario.query.all()
        excecoes_list = [excecao.to_dict() for excecao in excecoes]
        return jsonify(excecoes_list), 200
    except Exception as e:
        return handle_error(str(e), 500)


# Recupera uma exceção pelo ID
def get_excecao(id):
    try:
        excecao = ExcecaoHorario.query.get(id)
        if not excecao:
            return handle_error(f"Exceção com ID {id} não encontrada", 404)

        return jsonify(excecao.to_dict()), 200
    except Exception as e:
        return handle_error(str(e), 500)

def get_excecoes_by_campo_id(campo_id):
    try:
        excecoes = ExcecaoHorario.query.filter_by(campo_id=campo_id).all()  # Filtra exceções pelo campo_id
        if not excecoes:
            return handle_error(f"Nenhuma exceção encontrada para o campo com ID {campo_id}", 404)

        excecoes_list = [excecao.to_dict() for excecao in excecoes]  # Converte cada exceção em dicionário
        return jsonify(excecoes_list), 200
    except Exception as e:
        return handle_error(str(e), 500)


# Cria uma nova exceção
def create_excecao(data):
    try:
        campo_id = data.get('campo_id')
        data_excecao = data.get('data')

        # Verifica se já existe uma exceção no mesmo dia para o mesmo campo
        excecao_existente = ExcecaoHorario.query.filter_by(campo_id=campo_id, data=data_excecao).first()
        if excecao_existente:
            return handle_error(f"Já existe uma exceção para o campo com ID {campo_id} na data {data_excecao}", 400)

        nova_excecao = ExcecaoHorario(
            campo_id=data.get('campo_id'),
            data=data.get('data'),
            horario_abertura=data.get('horario_abertura'),
            horario_fechamento=data.get('horario_fechamento'),
            descricao=data.get('descricao')
        )
        db.session.add(nova_excecao)
        db.session.commit()

        return jsonify(nova_excecao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


# Atualiza uma exceção existente
def update_excecao(data, id):
    try:
        excecao = ExcecaoHorario.query.get(id)
        if not excecao:
            return handle_error(f"Exceção com ID {id} não encontrada", 404)

        for key, value in data.items():
            setattr(excecao, key, value)

        db.session.commit()
        return jsonify(excecao.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


# Deleta uma exceção pelo ID
def delete_excecao(id):
    try:
        excecao = ExcecaoHorario.query.get(id)
        if not excecao:
            return handle_error(f"Exceção com ID {id} não encontrada", 404)

        db.session.delete(excecao)
        db.session.commit()

        return jsonify({'message': f"Exceção com ID {id} deletada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)
