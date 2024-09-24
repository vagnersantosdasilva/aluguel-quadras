from models import Campo, Endereco
from app import db
from flask import jsonify, request

# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response

def get_all_campo_filter(request):
    try:
        # Pega os parâmetros de consulta da requisição
        localizacao = request.args.get('localizacao')
        tipo = request.args.get('tipo')
        dimensoes = request.args.get('dimensoes')
        iluminacao = request.args.get('iluminacao')  # Pode ser 'True' ou 'False'
        preco_min = request.args.get('preco_min', type=float)
        preco_max = request.args.get('preco_max', type=float)

        # Inicia a query
        query = Campo.query

        # Aplica os filtros conforme os parâmetros recebidos
        if localizacao:
            query = query.filter(Campo.localizacao.ilike(f"%{localizacao}%"))
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
        # Extraindo dados do endereço do JSON
        endereco_data = data.get('endereco', {})

        # Cria o objeto Endereco
        new_endereco = Endereco(
            rua=endereco_data.get('rua'),
            cidade=endereco_data.get('cidade'),
            estado=endereco_data.get('estado'),
            cep=endereco_data.get('cep'),
            numero=endereco_data.get('numero'),
            complemento=endereco_data.get('complemento'),
            bairro=endereco_data.get('bairro')
        )

        # Adiciona o novo endereço à sessão
        db.session.add(new_endereco)
        db.session.flush()  # "Flush" aqui para obter o ID do endereço

        # Agora cria o objeto Campo, referenciando o endereço recém-criado
        new_campo = Campo(
            nome=data.get('nome'),
            tipo=data.get('tipo'),
            dimensoes=data.get('dimensoes'),
            iluminacao=data.get('iluminacao'),
            preco=data.get('preco'),
            endereco_id=new_endereco.id  # Usando o ID do endereço recém-criado
        )

        # Adiciona o novo campo à sessão
        db.session.add(new_campo)
        db.session.commit()  # Commita ambos, campo e endereço
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
