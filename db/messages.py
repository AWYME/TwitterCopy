from db.config import get_connection


def getMessagesByChatId(id):
    query = "SELECT * FROM message WHERE chat_id = ?"
    args = [id]
    connection = get_connection()
    cur = connection.execute(query, args)
    res = cur.fetchall()
    cur.close()
    connection.close()
    return res

def createMessage(text, datetime, chat_id, sender_id):
    query = "INSERT INTO message (text, datetime, chat_id, sender_id) VALUES (?, ?, ?, ?)"
    args = [text, datetime, chat_id, sender_id]
    connection = get_connection()
    cur = connection.execute(query, args)
    connection.commit()
    cur.close()
    connection.close()
