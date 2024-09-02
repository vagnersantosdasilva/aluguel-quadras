from flask import Flask
#from controllers.campo_controller import campo_blueprint

app = Flask(__name__)

# Registrar blueprints
#app.register_blueprint(campo_blueprint)

if __name__ == '__main__':
    app.run(debug=True)