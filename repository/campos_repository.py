import mysql.connector
import os
from models import Campo
import exceptions
from dotenv import load_dotenv
load_dotenv()

SQL_CREATE_CAMPO = 'INSERT INTO campo (nome, localizacao, tipo, dimensoes, iluminacao, preco) VALUES (%s, %s, %s, %s, %s, %s)'
SQL_UPDATE_CAMPO = 'UPDATE campo SET nome = %s, localizacao = %s, tipo = %s, dimensoes = %s, iluminacao = %s, preco = %s WHERE id = %s'
SQL_FIND_CAMPO_BY_NAME = 'SELECT * FROM campo WHERE nome = %s'
SQL_FIND_ALL_CAMPO = 'SELECT * FROM campo'
SQL_FIND_CAMPO_BY_ID = 'SELECT * FROM campo WHERE id = %s'


def getConnection():
    """Estabelece uma conexão com o banco de dados."""
    try:
        local = os.environ.get('DB_SERVER')
        login = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        database = os.environ.get('DB_NAME')
        mydb = mysql.connector.connect(
            user=login,
            password=password,
            host=local,
            database=database
        )
        return mydb
    except mysql.connector.Error as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None


def get_list():
    """Recupera todos os registros de 'campo'."""
    mydb = getConnection()
    if mydb is None:
        return []

    try:
        mycursor = mydb.cursor()
        mycursor.execute(SQL_FIND_ALL_CAMPO)
        rows = mycursor.fetchall()
        campos = [make_campo(row) for row in rows]
        return campos
    finally:
        mydb.close()


def make_campo(row):
    """Converte uma tupla do banco de dados em um objeto Campo."""
    return Campo(row[0], row[1], row[2], row[3], row[4], row[5], row[6])


def get_by_id(id):
    """Recupera um registro de 'campo' pelo ID."""
    mydb = getConnection()
    if mydb is None:
        return None

    try:
        mycursor = mydb.cursor()
        mycursor.execute(SQL_FIND_CAMPO_BY_ID, (id,))
        row = mycursor.fetchone()
        if row:
            return make_campo(row)
        return None
    finally:
        mydb.close()


def save(campo):
    """Salva um novo registro de 'campo'."""
    try:
        connection = getConnection()
        if connection is None:
            return None

        cursor = connection.cursor()
        campo_tuple = (campo.nome, campo.localizacao, campo.tipo, campo.dimensoes, campo.iluminacao, campo.preco)
        cursor.execute(SQL_CREATE_CAMPO, campo_tuple)
        campo.id = cursor.lastrowid
        connection.commit()
        return campo.id
    except Exception as error:
        exceptions.handler_error(error)
    finally:
        if connection:
            connection.close()


def update(campo):
    """Atualiza um registro existente de 'campo'."""
    try:
        connection = getConnection()
        if connection is None:
            return False

        cursor = connection.cursor()
        update_tuple = (campo.nome, campo.localizacao, campo.tipo, campo.dimensoes, campo.iluminacao, campo.preco, campo.id)
        cursor.execute(SQL_UPDATE_CAMPO, update_tuple)
        connection.commit()
        return True
    except Exception as error:
        exceptions.handler_error(error)
        return False
    finally:
        if connection:
            connection.close()
