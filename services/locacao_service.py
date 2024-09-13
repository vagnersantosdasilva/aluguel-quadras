from datetime import datetime, time
from models import Locacao, Usuario, Campo, GradeHorario, ExcecaoHorario
from app import db
from flask import jsonify, request


def handle_error(error_message, status_code=400):
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response


def create_locacao(data):
    try:
        # Valida a existência do usuário e do campo
        usuario_id = data.get('usuario_id')
        campo_id = data.get('campo_id')
        horario_inicio_str = data.get('horario_inicio')
        horario_fim_str = data.get('horario_fim')

        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return handle_error(f"Usuário com ID {usuario_id} não encontrado", 404)

        campo = Campo.query.get(campo_id)
        if not campo:
            return handle_error(f"Campo com ID {campo_id} não encontrado", 404)

        # Convertendo strings de horário para objetos datetime.time
        horario_inicio = datetime.strptime(horario_inicio_str, "%H:%M").time()
        horario_fim = datetime.strptime(horario_fim_str, "%H:%M").time()
        data_inicio = datetime.strptime(data.get('data_inicio'), "%Y-%m-%d")

        # Verifica a disponibilidade do campo
        if not is_campo_disponivel(campo_id, data_inicio, horario_inicio, horario_fim):
            return handle_error("Campo não está disponível no horário solicitado", 400)

        # Calcula o valor total com base na duração
        duracao = (datetime.combine(datetime.min, horario_fim) - datetime.combine(datetime.min,
                                                                                  horario_inicio)).seconds / 3600
        valor_total = duracao * float(campo.preco)

        # Cria a nova locação
        locacao = Locacao(
            usuario_id=usuario_id,
            campo_id=campo_id,
            valor_total=valor_total,
            data_inicio=data_inicio,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim
        )

        db.session.add(locacao)
        db.session.commit()
        return jsonify(locacao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


def is_campo_disponivel(campo_id, data_inicio, horario_inicio, horario_fim):
    # Verifica se existe alguma exceção para a data especificada
    excecao = ExcecaoHorario.query.filter_by(campo_id=campo_id, data=data_inicio.date()).first()
    if excecao:
        if horario_inicio >= excecao.horario_abertura and horario_fim <= excecao.horario_fechamento:
            return False

    # Verifica a disponibilidade nas grades de horário regulares
    dia_semana = data_inicio.strftime('%A')  # Dia da semana por extenso
    grade_horario = GradeHorario.query.filter_by(campo_id=campo_id, dia_semana=dia_semana, ativo=True).first()
    if grade_horario:
        if not (horario_inicio >= grade_horario.horario_abertura and horario_fim <= grade_horario.horario_fechamento):
            return False

    # Verifica se já existem locações no mesmo horário
    locacoes_existentes = Locacao.query.filter_by(campo_id=campo_id, data_inicio=data_inicio).all()
    for locacao in locacoes_existentes:
        # Regra: Checar se a nova locação se sobrepõe a alguma locação existente
        if not (horario_fim <= locacao.horario_inicio or horario_inicio >= locacao.horario_fim):
            # Existe uma sobreposição de horário
            return False

    return True
