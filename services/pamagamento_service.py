'''MOCK de interface de pagamento para simular o envio de pagamento para um serviço externo de pagamento'''
from models import Pagamento, Locacao
from app import db
from flask import jsonify
from random import choice

# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response

def acionar_interface_pagamento(data):
    try:
        status_pagamento_possiveis = ['APROVADO','APROVADO','APROVADO','APROVADO','PENDENTE',  'NEGADO']
        # Busca a locação pelo ID


        locacao = get_locacao(data)

        # SIMULA  serviço de pagamento
        status_pagamento = choice(status_pagamento_possiveis)

        pagamento = get_pagamento(data)
        pagamento.status = status_pagamento
        db.session.add(pagamento)

        # Atualiza o status da locação conforme o resultado do pagamento
        if status_pagamento == "APROVADO":
            locacao.status = "EM_ANDAMENTO"
        elif status_pagamento == "NEGADO":
            locacao.status = "CANCELADO"
        elif status_pagamento == "PENDENTE":
            locacao.status = "PENDENTE"

        db.session.commit()


        return jsonify(pagamento.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

def get_locacao(data):
    locacao_id = data.get('locacao_id')
    locacao = Locacao.query.get(locacao_id)
    if not locacao:
        return handle_error("Locação não encontrada.", 404)

    # Verifica se o status da locação é "PENDENTE"
    if locacao.status != "PENDENTE":
        return handle_error(f"Pagamento não pode ser processado. Status atual da locação: " + locacao.status, 400)

    return locacao

def get_pagamento(data):
    locacao_id = data.get('locacao_id')

    # Verifica se já existe um pagamento para a locação
    pagamento = Pagamento.query.filter_by(locacao_id=locacao_id).first()

    if pagamento:
        raise ValueError(f"Já existe um processo de pagamento em andamento para essa locação de id: {pagamento.locacao_id}" )
    else:
        # Cria um novo pagamento
        novo_pagamento = Pagamento(**data)
        return novo_pagamento