# db_connection.py
from abc import ABC, abstractmethod


class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        pass

    @abstractmethod
    def close(self, connection):
        """Fecha a conexão com o banco de dados."""
        pass

    @abstractmethod
    def get_cursor(self, connection):
        """Obtém um cursor para a execução de consultas."""
        pass
