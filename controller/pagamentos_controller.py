from flask import  request
from app import app
from services.pamagamento_service import acionar_interface_pagamento


# Registrando as CRUD para gerenciamento de campos
@app.route('/pagamento', methods=['POST'])
def criar_pagamento():
    with app.app_context():  # Cria o contexto da aplicação
        data = request.get_json()
        return acionar_interface_pagamento(data)