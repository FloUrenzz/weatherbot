import sqlite3
from config import DB_NAME


def init_db():
    """Инициализация таблицы user_settings, если не создана."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            city TEXT,
            notify_time TEXT
        );
    """)
    conn.commit()
    conn.close()


def get_user_settings(user_id: int):
    """Возвращает (city, notify_time) для данного user_id или (None, None)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT city, notify_time FROM user_settings WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return (row[0], row[1]) if row else (None, None)


def set_city(user_id: int, city: str):
    """Сохраняет или обновляет город пользователя."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_settings (user_id, city) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET city=excluded.city
    """, (user_id, city))
    conn.commit()
    conn.close()


def set_notify_time(user_id: int, notify_time: str):
    """Сохраняет или обновляет время уведомления (формат HH:MM)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_settings (user_id, notify_time) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET notify_time=excluded.notify_time
    """, (user_id, notify_time))
    conn.commit()
    conn.close()


def get_all_users():
    """Возвращает список (user_id, city, notify_time) для всех пользователей."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, city, notify_time FROM user_settings")
    rows = cursor.fetchall()
    conn.close()
    return rows
