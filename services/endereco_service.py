from flask import jsonify
from app import db
from models import Endereco, Campo


# Função para lidar com erros
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response

# Recuperar todos os endereços
def get_all_enderecos():
    try:
        enderecos = Endereco.query.all()  # Recupera todos os endereços
        enderecos_list = [endereco.to_dict() for endereco in enderecos]
        return jsonify(enderecos_list), 200
    except Exception as e:
        return handle_error(str(e), 500)

# Recuperar um endereço específico
def get_endereco(endereco_id):
    try:
        endereco = Endereco.query.get(endereco_id)  # Busca o endereço pelo ID
        if not endereco:
            return handle_error(f"Endereço com ID {endereco_id} não encontrado", 404)

        return jsonify(endereco.to_dict()), 200
    except Exception as e:
        return handle_error(str(e), 500)

# Criar um novo endereço
def create_endereco(id_campo,data):
    try:
        # Cria o objeto Endereco com os dados recebidos
        novo_endereco = Endereco(
            campo_id=id_campo,
            rua=data.get('rua'),
            numero=data.get('numero'),
            bairro=data.get('bairro'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            cep=data.get('cep'),
            complemento=data.get('complemento')
        )

        # Adiciona o novo endereço à sessão
        db.session.add(novo_endereco)
        db.session.commit()  # Salva as alterações no banco

        return jsonify(novo_endereco.to_dict()), 201
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return handle_error(str(e), 500)

# Atualizar um endereço existente
def update_endereco(data, endereco_id,id_campo):
    try:
        endereco = Endereco.query.get(endereco_id)  # Busca o endereço pelo ID
        if not endereco:
            return handle_error(f"Endereço com ID {endereco_id} não encontrado", 404)

        # Atualiza os atributos do endereço
        for key, value in data.items():
            if hasattr(endereco, key):
                setattr(endereco, key, value)

        db.session.commit()  # Salva as alterações no banco
        return jsonify(endereco.to_dict()), 200
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return handle_error(str(e), 500)

# Deletar um endereço existente
def delete_endereco(endereco_id):
    try:
        endereco = Endereco.query.get(endereco_id)  # Busca o endereço pelo ID
        if not endereco:
            return handle_error(f"Endereço com ID {endereco_id} não encontrado", 404)

        db.session.delete(endereco)  # Remove o objeto do banco
        db.session.commit()  # Salva as alterações no banco

        return jsonify({'message': f"Endereço com ID {endereco_id} deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return handle_error(str(e), 500)


def get_endereco_by_campo(id):
    try:
        # Busca o campo pelo ID
        campo = Campo.query.get(id)
        if not campo:
            return handle_error(f"Campo com ID {id} não encontrado", 404)

        # Busca o endereço associado ao campo
        endereco = campo.endereco
        if not endereco:
            return handle_error(f"Endereço associado ao Campo com ID {id} não encontrado", 404)

        # Retorna o endereço em formato JSON
        return jsonify(endereco.to_dict()), 200
    except Exception as e:
        return handle_error(str(e), 500)