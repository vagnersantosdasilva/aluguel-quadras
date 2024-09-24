from decimal import Decimal

from models import Campo, GradeHorario, Usuario, Locacao, ExcecaoHorario, ListaEspera
from app import db
from flask import jsonify, request
from datetime import datetime, time

import locale

from services.pamagamento_service import acionar_interface_pagamento


# PEgar um usuario cliente
# Pegar um campo
# verificar se a data e faixa de horário está disponível
#  Pegar valor hora do campo
# calcular o valor total
# acionar meio de pagamento
# notificar email do usuario de status de pagamento e do aluguel
# atualizar grade de horario de campo para ativo ou ocupado



# Handler para tratar erros e respostas
def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response


def alugar_campo(data):
    try:
        # Valida a locação e calcula o valor total
        validar_locacao(data)
        valor_total = calcular_valor_locacao(data)

        # Cria o objeto Locacao e salva no banco de dados
        new_locacao = Locacao(**data)
        new_locacao.valor_total = valor_total
        db.session.add(new_locacao)
        db.session.commit()

        # # Aciona o serviço de pagamento
        # resultado_pagamento = acionar_interface_pagamento(new_locacao)
        #
        # # Atualiza o status da locação com base no resultado do pagamento
        # if resultado_pagamento['status'] == "APROVADO":
        #     new_locacao.status = "EM_ANDAMENTO"
        # elif resultado_pagamento['status'] == "REJEITADO":
        #     new_locacao.status = "CANCELADO"
        # elif resultado_pagamento['status'] == "PENDENTE":
        #     new_locacao.status = "PENDENTE_PAGAMENTO"

        # Salva a atualização de status da locação no banco de dados
        db.session.commit()

        return jsonify(new_locacao.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


def cancelar_aluguel_campo(data):
    # TODO: Atrelar os pedidos de locacao ao id de usuario que faz a solicitação para evitar que usuarios possam alterar locacoes que não são suas

    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    # Extrair o ID da locação a ser cancelada
    id = data.get('id')

    # Verificar se o ID foi fornecido
    if not id:
        return handle_error("O ID da locação é obrigatório.", 400)

    try:
        # Buscar a locação pelo ID
        locacao = Locacao.query.filter_by(id=id).first()

        # Verificar se a locação foi encontrada
        if not locacao:
            return handle_error(f"Locação com ID {id} não encontrada.", 404)

        # Verificar se a locação já está cancelada
        if locacao.status == 'CANCELADO':
            return handle_error("Essa locação já foi cancelada.", 400)

        # Verificar se a locação está em um estado que permita cancelamento (por exemplo, 'EM_ANDAMENTO')
        if locacao.status not in ['PENDENTE', 'EM_ANDAMENTO']:
            return handle_error("A locação não pode ser cancelada no status atual.", 400)

        # Atualizar o status da locação para 'CANCELADO'
        locacao.status = 'CANCELADO'

        # Salvar as mudanças no banco de dados
        db.session.commit()

        # Retornar uma resposta de sucesso
        return jsonify({"message": "Locação cancelada com sucesso.", "locacao": locacao.to_dict()}), 200

    except Exception as e:
        # Em caso de erro, fazer rollback da transação e retornar erro
        db.session.rollback()
        return handle_error(str(e), 500)


def validar_locacao(data):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    # Extrai os dados do JSON de entrada
    campo_id = data.get('campo_id')
    data_inicio = data.get('data_inicio')  # Data de início em string
    horario_inicio = data.get('horario_inicio')  # Horário de início em string
    horario_fim = data.get('horario_fim')  # Horário de fim em string

    if not campo_id or not data_inicio or not horario_inicio or not horario_fim:
        raise ValueError("Campo, data de início, horário de início e horário de fim são obrigatórios.")

    # Converte as strings de data e hora em objetos datetime e time
    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    horario_inicio = datetime.strptime(horario_inicio, "%H:%M").time()
    horario_fim = datetime.strptime(horario_fim, "%H:%M").time()

    # Verifica se a data solicitada é um dia da semana ativo
    dia_semana = data_inicio.strftime("%A")  # Obtém o dia da semana por extenso

    # Busca o campo no banco de dados
    campo = Campo.query.get(campo_id)
    if not campo:
        raise ValueError(f"O campo com ID {campo_id} não foi encontrado.")

    # Verifica a grade de horários regulares do campo para o dia da semana solicitado
    grade_horario = GradeHorario.query.filter_by(campo_id=campo_id, dia_semana=dia_semana, ativo=True).first()

    if not grade_horario:
        raise ValueError(f"O campo {campo.nome} não possui horário ativo para {dia_semana}.")

    # Verifica se o horário solicitado está dentro do horário de funcionamento regular do campo
    if not (grade_horario.horario_abertura <= horario_inicio < grade_horario.horario_fechamento and
            grade_horario.horario_abertura < horario_fim <= grade_horario.horario_fechamento):
        raise ValueError(
            f"O horário solicitado ({horario_inicio} - {horario_fim}) não está dentro do horário de funcionamento do campo.")

    # Verifica por conflitos com outras locações no mesmo campo e data
    conflito_locacao = Locacao.query.filter(
        Locacao.campo_id == campo_id,
        Locacao.data_inicio == data_inicio,
        Locacao.horario_inicio < horario_fim,
        Locacao.horario_fim > horario_inicio,
        Locacao.status != 'CANCELADO'
    ).first()

    if conflito_locacao:
        raise ValueError("O campo já está alugado para o período solicitado.")

    # Verifica exceções de horários (como feriados ou eventos especiais)
    excecao_horario = ExcecaoHorario.query.filter(
        ExcecaoHorario.campo_id == campo_id,
        ExcecaoHorario.data == data_inicio,
        ExcecaoHorario.horario_abertura < horario_fim,
        ExcecaoHorario.horario_fechamento > horario_inicio
    ).first()

    if excecao_horario:
        raise ValueError(f"O campo está indisponível devido a uma exceção: {excecao_horario.descricao}")

    # Se todas as verificações passaram, o campo está disponível para locação
    return True


def calcular_valor_locacao(data):
    try:
        # Calcula o valor total da locação
        campo_id = data.get('campo_id')
        horario_inicio = datetime.strptime(data.get('horario_inicio'), "%H:%M").time()
        horario_fim = datetime.strptime(data.get('horario_fim'), "%H:%M").time()

        # Busca o campo no banco de dados para obter o preço
        campo = Campo.query.get(campo_id)
        if not campo:
            raise ValueError(f"O campo com ID {campo_id} não foi encontrado.")

        # Calcula o total de horas
        duracao = datetime.combine(datetime.min, horario_fim) - datetime.combine(datetime.min, horario_inicio)
        # Convertendo horas_totais para Decimal
        horas_totais = Decimal(duracao.total_seconds()) / Decimal(3600)

        # Calcula o valor total usando Decimal
        valor_total = horas_totais * campo.preco

        return valor_total
    except Exception as e:
        raise ValueError(f"Ocorreu um erro em calcular o valor :"+str(e))


def adicionar_usuario_lista_espera(data):
    try:
        # Extrai os dados do JSON de entrada
        usuario_id = data.get('usuario_id')
        campo_id = data.get('campo_id')
        data_locacao = data.get('data_locacao')  # Data de início em string
        horario_inicio = data.get('horario_inicio')  # Horário de início em string
        horario_fim = data.get('horario_fim')  # Horário de fim em string

        if not usuario_id or not campo_id or not data_locacao or not horario_inicio or not horario_fim:
            raise ValueError("Usuário, campo, data de início, horário de início e horário de fim são obrigatórios.")

        # Converte as strings de data e hora em objetos datetime e time
        data_locacao = datetime.strptime(data_locacao, "%Y-%m-%d").date()
        horario_inicio = datetime.strptime(horario_inicio, "%H:%M").time()
        horario_fim = datetime.strptime(horario_fim, "%H:%M").time()

        # Verifica se o campo existe
        campo = Campo.query.get(campo_id)
        if not campo:
            raise ValueError(f"O campo com ID {campo_id} não foi encontrado.")

        # Verifica por conflitos com outras locações no mesmo campo e data
        conflito_locacao = Locacao.query.filter(
            Locacao.campo_id == campo_id,
            Locacao.data_inicio == data_locacao,
            Locacao.horario_inicio < horario_fim,
            Locacao.horario_fim > horario_inicio
        ).first()

        # Se não há conflitos, o campo está disponível
        if not conflito_locacao:
            return handle_error("O campo está disponível, não há necessidade de adicionar à lista de espera.", 400)

        # Verifica exceções de horários (como feriados ou eventos especiais)
        excecao_horario = ExcecaoHorario.query.filter(
            ExcecaoHorario.campo_id == campo_id,
            ExcecaoHorario.data == data_locacao,
            ExcecaoHorario.horario_abertura < horario_fim,
            ExcecaoHorario.horario_fechamento > horario_inicio
        ).first()

        if excecao_horario:
            return handle_error(f"O campo está indisponível devido a uma exceção: {excecao_horario.descricao}", 400)

        # Se houve conflitos, adicionar o usuário à lista de espera
        fila_espera = ListaEspera(
            usuario_id=usuario_id,
            campo_id=campo_id,
            data_locacao=data_locacao,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim
        )

        # Salva no banco de dados
        db.session.add(fila_espera)
        db.session.commit()

        return jsonify({"message": "Usuário adicionado à lista de espera com sucesso."}), 201

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)