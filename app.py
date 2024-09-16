from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Inicialize o Flask-Mail
mail = Mail(app)

# Configuração do Swagger
#swagger = Swagger(app)



from controller.campos_controller import *
from controller.usuario_controller import *
from controller.grade_horario_controller import *
from controller.locacao_controller import *
from controller.email_controller import  *
from controller.pagamentos_controller import *
if __name__ == '__main__':
    app.run(debug=True)