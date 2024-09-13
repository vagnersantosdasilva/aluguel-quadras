'''MOCK de interface de pagamento para simular o envio de pagamento para um serviço externo de pagamento'''
from random import choice
from models import Pagamento
from app import db


def acionar_interface_pagamento(locacao):
    # Status possíveis de um pagamento
    status_pagamento_possiveis = ["APROVADO", "REJEITADO", "PENDENTE"]

    # Seleciona um status aleatório
    status_pagamento = choice(status_pagamento_possiveis)

    # Cria o registro de pagamento
    pagamento = Pagamento(
        locacao_id=locacao.id,
        usuario_id=locacao.usuario_id,
        status=status_pagamento,
        valor_total=locacao.valor_total
    )

    # Salva o pagamento no banco de dados
    db.session.add(pagamento)
    db.session.commit()

    # Simula o retorno de um pagamento fictício
    retorno_pagamento = {
        "locacao_id": locacao.id,
        "usuario_id": locacao.usuario_id,
        "status": status_pagamento,
        "valor_total": str(locacao.valor_total),
        "mensagem": f"Pagamento {status_pagamento} para o valor de R$ {str(locacao.valor_total)}"
    }

    return retorno_pagamento