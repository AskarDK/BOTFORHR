# migrate_add_avatar.py
import sqlite3
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
DATABASE_FILE = DATABASE_URL.replace("sqlite:///", "")


def migrate():
    """Добавляет колонку photo_file_id в таблицу employees, если её нет."""
    if not os.path.exists(DATABASE_FILE):
        print("Файл базы данных не найден.")
        return

    print(f"Подключение к базе данных '{DATABASE_FILE}'...")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA table_info(employees)")
        columns = [info[1] for info in cursor.fetchall()]

        if 'photo_file_id' not in columns:
            print("Добавление колонки 'photo_file_id' в таблицу 'employees'...")
            cursor.execute("ALTER TABLE employees ADD COLUMN photo_file_id VARCHAR")
            print(" -> Колонка успешно добавлена.")
        else:
            print("Колонка 'photo_file_id' уже существует.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    conn.commit()
    conn.close()
    print("\nМиграция для аватаров завершена!")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    migrate()