SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='estudo',
        senha='Abc%401234',  # '@' é codificado como '%40'
        servidor='localhost',
        database='aluguel_campos'
    )

# Configurações para Flask-Mail
MAIL_SERVER = 'smtp-relay.sendinblue.com'  # Substitua pelo seu servidor SMTP
MAIL_PORT = 587  # A porta pode variar, 587 é usada para TLS
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'vgrssdasilva@gmail.com'  # Seu e-mail
MAIL_PASSWORD = 'senha_serviço_smpt'  # Sua senha de e-mail
MAIL_DEFAULT_SENDER = ('Sistema de Aluguel de Campos', 'vgrssdasilva@gmail.com')