from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


from controller.campos_controller import *
from controller.usuario_controller import *
from controller.grade_horario_controller import *
if __name__ == '__main__':
    app.run(debug=True)