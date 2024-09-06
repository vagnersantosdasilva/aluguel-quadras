import json
import pytest
from app import app, db
from models import Campo

@pytest.fixture
def client():
    # Configuração de testes
    app.config['TESTING'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados em memória para testes
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Cria todas as tabelas no banco de dados em memória
        yield client


def test_create_campo(client):
    # Dados para criar um novo Campo
    data = {
        "nome": "Campo 3",
        "localizacao": "rua 1",
        "tipo": "Gramado sintético",
        "dimensoes": "10x10",
        "iluminacao": True,
        "preco": 24.10
    }
    response = client.post('/campo', data=json.dumps(data), content_type='application/json')

    # Verificando se o status code está correto e se os dados são retornados como esperado
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['nome'] == 'Campo 3'
    assert response.json['localizacao'] == 'rua 1'
    assert response.json['tipo'] == 'Gramado sintético'
    assert response.json['dimensoes'] == '10x10'
    assert response.json['iluminacao'] is True
    assert response.json['preco'] == 24.10


def test_get_all_campo(client):
    response = client.get('/campo')

    # Verifica se a resposta contém uma lista de campo
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_campo(client):
    # Criando um Campo para testar o GET
    campo = Campo.query.first()
    # campo = Campo(nome="Campo 3", localizacao="rua 1", tipo="Gramado sintético", dimensoes="10x10", iluminacao=True,
    #               preco=24.10)
    # db.session.add(campo)
    # db.session.commit()

    response = client.get(f'/campo/{campo.id}')

    # Verificando se os dados do Campo estão corretos na resposta
    assert response.status_code == 200
    # assert response.json['nome'] == 'Campo 3'
    # assert response.json['localizacao'] == 'rua 1'
    # assert response.json['tipo'] == 'Gramado sintético'
    # assert response.json['dimensoes'] == '10x10'
    # assert response.json['iluminacao'] is True
    # assert response.json['preco'] == 24.10


def test_update_campo(client):
    # Criando um Campo inicial para testar o UPDATE
    campo = Campo(nome="Campo Antigo", localizacao="rua 2", tipo="Gramado natural", dimensoes="20x20", iluminacao=False,
                  preco=30.00)
    db.session.add(campo)
    db.session.commit()

    # Dados de atualização do Campo
    update_data = {
        "nome": "Campo 3",
        "localizacao": "rua 1",
        "tipo": "Gramado sintético",
        "dimensoes": "10x10",
        "iluminacao": True,
        "preco": 24.10
    }

    response = client.put(f'/campo/{campo.id}', data=json.dumps(update_data), content_type='application/json')

    # Verificando se o status code e os dados atualizados estão corretos
    assert response.status_code == 200
    assert response.json['nome'] == 'Campo 3'
    assert response.json['localizacao'] == 'rua 1'
    assert response.json['tipo'] == 'Gramado sintético'
    assert response.json['dimensoes'] == '10x10'
    assert response.json['iluminacao'] is True
    assert response.json['preco'] == 24.10


def test_delete_campo(client):
    # Criando um Campo para testar o DELETE
    campo = Campo(nome="Campo para Deletar", localizacao="rua Del", tipo="Gramado sintético", dimensoes="10x10",
                  iluminacao=True, preco=24.10)
    db.session.add(campo)
    db.session.commit()

    response = client.delete(f'/campo/{campo.id}')

    # Verificando se o Campo foi deletado corretamente
    assert response.status_code == 200
    assert response.json['message'] == f"Campo com ID {campo.id} deletado com sucesso"