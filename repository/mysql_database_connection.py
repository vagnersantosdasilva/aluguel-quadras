# mysql_database_connection.py
import mysql.connector
import os
from db_connection import DatabaseConnection


class MySQLDatabaseConnection(DatabaseConnection):
    def connect(self):
        local = os.environ.get('DB_SERVER')
        login = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        database = os.environ.get('DB_NAME')
        return mysql.connector.connect(
            user=login,
            password=password,
            host=local,
            database=database
        )

    def close(self, connection):
        connection.close()

    def get_cursor(self, connection):
        return connection.cursor()
