SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='estudo',
        senha='Abc%401234',  # '@' é codificado como '%40'
        servidor='localhost',
        database='aluguel_campos'
    )