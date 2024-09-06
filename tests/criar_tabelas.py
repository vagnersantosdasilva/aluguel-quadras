from app import db, app   # Importa a instância do banco de dados e a fábrica da aplicação

def create_tables():
    with app.app_context():  # Cria o contexto da aplicação
        db.create_all()  # Cria todas as tabelas
        print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    create_tables()