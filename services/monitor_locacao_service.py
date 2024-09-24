from datetime import datetime, timedelta
from services.email_service import send_email
from services.pamagamento_service import atualizar_status_pagamento_pendente
from models import Campo, ListaEspera, Locacao, Pagamento
from app import db, mail, app


def verificar_status_pagamento():
    '''Verificar se status de pagamentos pendentes de respostas das operadoras. Caso haja mudanças, atualizar o status do pagamento e da locacao associada'''
    print('Iniciando verificação de status de pagamentos pendentes')
    with app.app_context():
        pagamentos_pendentes = Pagamento.query.filter_by(status='PENDENTE').all()

        for pagamento in pagamentos_pendentes:
            atualizar_status_pagamento_pendente(pagamento)


def verificar_locacoes_expiradas():
    '''Verifica se existem locacoes não pagas . Caso existam, as cancelam automaticamente mudando seu status e liberando
    para outros usuários interessados
    '''

    hoje = datetime.utcnow().date()
    locacoes_pendentes = Locacao.query.filter(
        Locacao.data_inicio == hoje + timedelta(days=0),
        Locacao.status.in_(['PENDENTE'])
    ).all()

    for locacao in locacoes_pendentes:
        pagamento_pendente = Pagamento.query.filter_by(locacao_id=locacao.id, status='PENDENTE').first()

        # Se o pagamento está pendente ou não foi realizado até a véspera
        if pagamento_pendente or locacao.status == 'PENDENTE':
            cancelar_locacao(locacao)


def verificar_fila_de_espera():
    # Verifica a disponibilidade dos campos para os usuários na fila de espera

    print('Iniciando verificação de locacoes')
    with app.app_context():
        lista_espera = ListaEspera.query.filter_by(notificacao_enviada=False).all()
        for membro in lista_espera:
            # Verifica se há locações para o campo e horário desejado
            locacoes = Locacao.query.filter_by(
                campo_id=membro.campo_id,
                data_inicio=membro.data_locacao,
                horario_inicio=membro.horario_inicio,
                status='CANCELADO'
            ).first()

            if locacoes:
                # Se houver locações canceladas, o campo está disponível. Notificar o usuário.

                membro.notificacao_enviada = True
                db.session.commit()

                enviar_email_notificacao(membro.usuario, membro.campo, membro.data_locacao, membro.horario_inicio,
                                         membro.horario_fim, 'Dispnibilidade de Campo')


def enviar_email_notificacao(usuario, campo, data, horario_inicio, horario_fim, subject):
    # Função para enviar e-mail ao usuário informando a disponibilidade do campo
    try:

        body = f"Olá {usuario.nome},\n\nO campo {campo.nome} está disponível para locação no dia {data} das {horario_inicio} às {horario_fim}. Aproveite para reservar!\n\nAtenciosamente,\nEquipe de Reservas"

        send_email(subject, [usuario.email], body)
        print(f"Notificação genérica  enviada para {usuario.email}")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {str(e)}")


def cancelar_locacao(locacao):
    # Função para cancelar uma locação e enviar notificação ao usuário
    locacao.status = 'CANCELADA'

    db.session.commit()

    try:
        body = f"Olá {locacao.usuario.nome},\n\nSua locação do campo {locacao.campo.nome} para o dia {locacao.data_inicio} das {locacao.horario_inicio} às {locacao.horario_fim} foi cancelada devido à falta de pagamento.\n\nAtenciosamente,\nEquipe de Reservas"
        send_email("Aviso de Cancelamento de Aluguel de Campo", locacao.usuario.email, body)
        print(f"Notificação de cancelamento enviada para {locacao.usuario.email}")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {str(e)}")
