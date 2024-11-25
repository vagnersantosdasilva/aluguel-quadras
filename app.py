from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import os
from flask_cors import CORS  # Importando Flask-CORS


load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# Inicialize o Flask-Mail
mail = Mail(app)

# Configuração do Swagger
#swagger = Swagger(app)

from controller.grade_excecao_controller import *
from controller.campos_controller import *
from controller.usuario_controller import *
from controller.grade_horario_controller import *
from controller.locacao_controller import *
from controller.email_controller import  *
from controller.pagamentos_controller import *
from controller.imagem_controller import *
from controller.endereco_controller import *
from services.monitor_locacao_service import verificar_fila_de_espera, verificar_status_pagamento

# Configurando o APScheduler
scheduler = BackgroundScheduler()

# Monitoramento de locações
scheduler.add_job(
    func=verificar_fila_de_espera,
    trigger=IntervalTrigger(seconds=int(os.getenv('LOCACAO_MONITOR_INTERVAL', 15))),
    id='monitor_locacoes',
    name='Monitoramento de Locações Canceladas',
    replace_existing=True
)

# Monitoramento de pagamentos pendentes
scheduler.add_job(
    func=verificar_status_pagamento,  # Remover parênteses
    trigger=IntervalTrigger(seconds=int(os.getenv('PAGAMENTO_MONITOR_INTERVAL', 10))),
    id='monitor_pagamentos_pendentes',
    name='Monitoramento de Pagamentos Pendentes',
    replace_existing=True
)

# Verifique se o script não está sendo executado em modo de recarregamento
if not os.getenv('WERKZEUG_RUN_MAIN'):
    scheduler.start()

# Garantir que o scheduler pare ao fechar a aplicação
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)