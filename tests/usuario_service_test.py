import unittest
from unittest.mock import patch, MagicMock
from services.usuario_service import (
    create_usuario,
    update_usuario,
    get_usuario,
    get_all_usuarios,
    delete_usuario
)
from models import Usuario

class TestUsuarioService(unittest.TestCase):

    @patch('services.usuario_service.db.session')
    def test_create_usuario(self, mock_db_session):
        # Mock para evitar interações com o banco de dados
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        # Dados de exemplo
        data = {
            'nome': 'João da Silva',
            'email': 'joao@example.com',
            'tipo': 'cliente',
            'login': 'joaosilva',
            'password': 'senha123',
            'apelido': 'joao'
        }

        # Testa a criação do usuário
        response, status_code = create_usuario(data)
        self.assertEqual(status_code, 201)
        self.assertEqual(response.json['nome'], 'João da Silva')
        self.assertEqual(response.json['email'], 'joao@example.com')

    @patch('services.usuario_service.Usuario')
    def test_get_usuario(self, mock_usuario):
        # Mock para simular o retorno do banco de dados
        mock_user_instance = Usuario(
            nome='João da Silva',
            email='joao@example.com',
            tipo='cliente',
            login='joaosilva',
            password_hash='hashed_password',
            apelido='joao'
        )
        mock_usuario.query.get.return_value = mock_user_instance

        # Testa a obtenção do usuário
        response, status_code = get_usuario(1)
        self.assertEqual(status_code, 200)
        self.assertEqual(response.json['nome'], 'João da Silva')

    @patch('services.usuario_service.db.session')
    @patch('services.usuario_service.Usuario')
    def test_update_usuario(self, mock_usuario, mock_db_session):
        # Mock para simular o usuário existente
        mock_user_instance = Usuario(
            nome='João da Silva',
            email='joao@example.com',
            tipo='cliente',
            login='joaosilva',
            password_hash='hashed_password',
            apelido='joao'
        )
        mock_usuario.query.get.return_value = mock_user_instance

        # Dados de atualização
        data = {'nome': 'João Atualizado'}

        # Testa a atualização do usuário
        response, status_code = update_usuario(data, 1)
        self.assertEqual(status_code, 200)
        self.assertEqual(response.json['nome'], 'João Atualizado')

    @patch('services.usuario_service.db.session')
    @patch('services.usuario_service.Usuario')
    def test_delete_usuario(self, mock_usuario, mock_db_session):
        # Mock para simular o usuário existente
        mock_user_instance = Usuario(
            nome='João da Silva',
            email='joao@example.com',
            tipo='cliente',
            login='joaosilva',
            password_hash='hashed_password',
            apelido='joao'
        )
        mock_usuario.query.get.return_value = mock_user_instance

        # Testa a deleção do usuário
        response, status_code = delete_usuario(1)
        self.assertEqual(status_code, 200)
        self.assertEqual(response.json['message'], "Usuário com ID 1 deletado com sucesso")

if __name__ == '__main__':
    unittest.main()
