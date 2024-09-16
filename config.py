import os


SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD=os.getenv('SGBD', 'mysql+mysqlconnector'),
    usuario=os.getenv('DB_USER', 'estudo'),
    senha=os.getenv('DB_PASSWORD', ''),
    servidor=os.getenv('DB_HOST', 'localhost'),
    database=os.getenv('DB_NAME', 'aluguel_campos')
)

# Configurações para Flask-Mail
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp-relay.sendinblue.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
MAIL_DEFAULT_SENDER = (os.getenv('MAIL_DEFAULT_NAME', 'Sistema de Aluguel de Campos'), os.getenv('MAIL_DEFAULT_EMAIL', 'vgrssdasilva@gmail.com'))