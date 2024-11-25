from models import Campo, Endereco
from app import db
from flask import jsonify, request
from models import Campo
from app import db
from flask import jsonify


# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response


def get_all_campo_filter(request):
    try:
        # Pega os parâmetros de consulta da requisição
        tipo = request.args.get('tipo')
        dimensoes = request.args.get('dimensoes')
        iluminacao = request.args.get('iluminacao')  # Pode ser 'True' ou 'False'
        preco_min = request.args.get('preco_min', type=float)
        preco_max = request.args.get('preco_max', type=float)

        # Inicia a query
        query = Campo.query

        # Aplica os filtros conforme os parâmetros recebidos
        if tipo:
            query = query.filter(Campo.tipo.ilike(f"%{tipo}%"))
        if dimensoes:
            query = query.filter(Campo.dimensoes.ilike(f"%{dimensoes}%"))
        if iluminacao is not None:
            query = query.filter(Campo.iluminacao == (iluminacao.lower() == 'true'))
        if preco_min is not None:
            query = query.filter(Campo.preco >= preco_min)
        if preco_max is not None:
            query = query.filter(Campo.preco <= preco_max)

        # Executa a query e obtém os resultados
        campos = query.all()
        campos_list = [campo.to_dict() for campo in campos]

        return jsonify(campos_list), 200
    except Exception as e:
        return handle_error(str(e), 500)


def get_all_campo():
    try:
        campos = Campo.query.all()  # Recupera todos os objetos Campo
        campos_list = [campo.to_dict() for campo in campos]  # Converte cada objeto para dicionário
        return jsonify(campos_list), 200
    except Exception as e:
        return handle_error(str(e), 500)


def create_campo(data):
    try:
        # Cria o objeto Campo com as informações recebidas
        new_campo = Campo(
            nome=data.get('nome'),
            tipo=data.get('tipo'),
            dimensoes=data.get('dimensoes'),
            iluminacao=data.get('iluminacao', False),
            preco=data.get('preco'),
            descricao=data.get('descricao')
        )

        # Adiciona o novo campo à sessão
        db.session.add(new_campo)
        db.session.commit()  # Commita as alterações no banco de dados

        return jsonify(new_campo.to_dict()), 201
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return handle_error(str(e), 500)


def update_campo(data, id):
    try:
        campo = Campo.query.get(id)  # Busca o campo pelo ID
        if not campo:
            return handle_error(f"Campo com ID {id} não encontrado", 404)

        # Atualiza os atributos do campo
        for key, value in data.items():
            if key != 'endereco':  # Ignora a chave 'endereco' aqui, pois não estamos mais lidando com esse relacionamento
                setattr(campo, key, value)

        db.session.commit()  # Commita as alterações no banco de dados
        return jsonify(campo.to_dict()), 200

    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
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

            # Verifica e remove o Endereço relacionado
            # Remove relacionamentos associados
        if campo.endereco:
            db.session.delete(campo.endereco)

        for imagem in campo.imagens:
            db.session.delete(imagem)

        for horario in campo.horarios:
            db.session.delete(horario)

        for excecao in campo.excecoes:
            db.session.delete(excecao)

        db.session.delete(campo)  # Remove o objeto do banco de dados
        db.session.commit()  # Commita as alterações no banco de dados

        return jsonify({'message': f"Campo com ID {id} deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return handle_error(str(e), 500)
