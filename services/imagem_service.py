from flask import jsonify
from models import Imagem
from app import db


# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response


def get_all_imagem(campo_id):
    try:
        # Recupera as imagens associadas ao campo_id fornecido
        imagens = Imagem.query.filter_by(campo_id=campo_id).all()

        # Converte as imagens para uma lista de dicionários
        imagens_list = [imagem.to_dict() for imagem in imagens]

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
        # Verifica se já existe uma imagem principal para o campo
        if data.get('tipo') == 'principal':
            imagem_principal_existente = Imagem.query.filter_by(campo_id=data.get('campo_id'), tipo='principal').first()
            if imagem_principal_existente:
                return jsonify({"erro": "Já existe uma imagem principal para este campo."}), 400

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


def update_imagem(data, id, id_campo):
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
