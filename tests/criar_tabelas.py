from app import db, app   # Importa a instância do banco de dados e a fábrica da aplicação

def recreate_tables():
    with app.app_context():  # Cria o contexto da aplicação
        db.drop_all()  # Destroi todas as tabelas
        print("Tabelas destruídas com sucesso!")

        db.create_all()  # Cria todas as tabelas
        print("Tabelas criadas com sucesso!")

def create_tables():
    with app.app_context():  # Cria o contexto da aplicação
        db.create_all()  # Cria todas as tabelas
        print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    recreate_tables()
    #create_tables()