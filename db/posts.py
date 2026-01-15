from db.config import get_connection


def getAllPosts():
    query = "SELECT * FROM post ORDER BY post.datetime DESC "
    connection = get_connection()
    cur = connection.execute(query)
    res = cur.fetchall()
    cur.close()
    connection.close()
    return res


def getPostById(id):
    query = "SELECT * FROM post WHERE id = ?"
    args = [id]
    connection = get_connection()
    cur = connection.execute(query, args)
    res = cur.fetchone()
    cur.close()
    connection.close()
    return res


def createPost(text, filename, date_time, client_id):
    query = "INSERT INTO post (text, filename, datetime, client_id) VALUES (?, ?, ?, ?)"
    args = [text, filename, date_time, client_id]
    connection = get_connection()
    cur = connection.execute(query, args)
    connection.commit()
    cur.close()
    connection.close()


def deletePostById(id):
    query = "DELETE FROM post WHERE id = ?"
    args = [id]
    connection = get_connection()
    cur = connection.execute(query, args)
    connection.commit()
    cur.close()
    connection.close()