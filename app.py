from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Inicialize o Flask-Mail
mail = Mail(app)

from controller.campos_controller import *
from controller.usuario_controller import *
from controller.grade_horario_controller import *
from controller.locacao_controller import *
from controller.email_controller import  *
if __name__ == '__main__':
    app.run(debug=True)