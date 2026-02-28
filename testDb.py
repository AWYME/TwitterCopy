import sqlite3
import os

DB_NAME = "my_database.db"

def create_tables():
    """Создаёт таблицы в базе данных SQLite, если они ещё не существуют."""
    # Подключаемся к базе (файл создастся автоматически, если его нет)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Включаем поддержку внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Создаём таблицу users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    # Создаём таблицу posts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            filename TEXT,
            user_id INTEGER NOT NULL,
            datetime TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Создаём таблицу chat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_client_id INTEGER NOT NULL,
            second_client_id INTEGER NOT NULL,
            FOREIGN KEY (first_client_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (second_client_id) REFERENCES users(id) ON DELETE CASCADE,
            CHECK (first_client_id != second_client_id)  -- чтобы не создавать чат с самим собой
        )
    """)

    # Создаём таблицу message
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            datetime TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            FOREIGN KEY (chat_id) REFERENCES chat(id) ON DELETE CASCADE,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print(f"База данных '{DB_NAME}' успешно создана/обновлена.")

if __name__ == "__main__":
    # Если файл базы уже существует, удалим его, чтобы начать с чистого листа (опционально)
    # if os.path.exists(DB_NAME):
    #     os.remove(DB_NAME)
    create_tables()
