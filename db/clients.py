import sqlite3

from db.config import get_connection, query_db


def getUserById(id):
    query = "SELECT * FROM client'' WHERE id = (?)"
    args = (id,)
    cur = get_connection().execute(query, args)
    res = cur.fetchone()
    cur.close()
    return res


def getUserByEmail(email):
    query = "SELECT * FROM client WHERE email = (?)"
    args = (email,)
    cur = get_connection().execute(query, args)
    res = cur.fetchone()
    cur.close()
    return res

def check_password(password,checkPassword):
    if password==checkPassword:
        return True
    else: return False

def createUser(email, password):
    query = "INSERT INTO client (email, password) VALUES (?, ?)"
    args = (email, password)
    connection = get_connection()
    cur = connection.execute(query, args)
    connection.commit()
    cur.close()
