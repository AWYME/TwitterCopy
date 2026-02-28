import sqlite3

from db.config import get_connection, query_db


def getUserById(id):
    query = "SELECT * FROM users WHERE id = (?)"
    args = (id,)
    cur = get_connection().execute(query, args)
    res = cur.fetchone()
    cur.close()
    return res

def getUserByUsername(username):
    query = "SELECT * FROM users WHERE username = (?)"
    args = (username,)
    cur = get_connection().execute(query, args)
    res = cur.fetchone()
    cur.close()
    return res

def getUserByEmail(email):
    query = "SELECT * FROM users WHERE email = (?)"
    args = (email,)
    cur = get_connection().execute(query, args)
    res = cur.fetchone()
    cur.close()
    return res

def check_password(password,checkPassword):
    if password==checkPassword:
        return True
    else: return False

def createUser(email, username, password_hash):
    query = "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)"
    args = (username, email, password_hash)
    connection = get_connection()
    cur = connection.execute(query, args)
    connection.commit()
    cur.close()