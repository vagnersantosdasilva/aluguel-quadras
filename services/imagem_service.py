from flask import jsonify
from models import Imagem
from app import db

# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response


def get_all_imagem():
    try:
        imagens = Imagem.query.all()  # Recupera todas as imagens
        imagens_list = [imagem.to_dict() for imagem in imagens]  # Converte para dicionário
        return jsonify(imagens_list), 200
    except Exception as e:
        return handle_error(str(e), 500)


def get_imagem(id):
    try:
        imagem = Imagem.query.get(id)  # Busca a imagem pelo ID
        if not imagem:
            return handle_error(f"Imagem com ID {id} não encontrada", 404)

        return jsonify(imagem.to_dict()), 200
    except Exception as e:
        return handle_error(str(e), 500)


def create_imagem(data):
    try:
        # Cria o objeto Imagem com os dados recebidos
        nova_imagem = Imagem(
            campo_id=data.get('campo_id'),
            tipo=data.get('tipo'),
            dados=data.get('dados').encode('utf-8')  # Certifique-se de que 'dados' seja codificado em binário
        )

        # Adiciona à sessão do banco de dados
        db.session.add(nova_imagem)
        db.session.commit()  # Salva as alterações no banco

        return jsonify(nova_imagem.to_dict()), 201
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return handle_error(str(e), 500)


def update_imagem(data, id):
    try:
        imagem = Imagem.query.get(id)  # Busca a imagem pelo ID
        if not imagem:
            return handle_error(f"Imagem com ID {id} não encontrada", 404)

        # Atualiza os atributos da imagem
        if 'campo_id' in data:
            imagem.campo_id = data.get('campo_id')
        if 'tipo' in data:
            imagem.tipo = data.get('tipo')
        if 'dados' in data:
            imagem.dados = data.get('dados').encode('utf-8')  # Certifique-se de que 'dados' seja codificado em binário

        db.session.commit()  # Salva as alterações no banco
        return jsonify(imagem.to_dict()), 200
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return handle_error(str(e), 500)


def delete_imagem(id):
    try:
        imagem = Imagem.query.get(id)  # Busca a imagem pelo ID
        if not imagem:
            return handle_error(f"Imagem com ID {id} não encontrada", 404)

        db.session.delete(imagem)  # Remove do banco de dados
        db.session.commit()  # Salva as alterações no banco

        return jsonify({'message': f"Imagem com ID {id} deletada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return handle_error(str(e), 500)
