# migrate.py
import sqlite3
import os

DATABASE_FILE = "bot.db"

def migrate():
    if not os.path.exists(DATABASE_FILE):
        print(f"Файл базы данных {DATABASE_FILE} не найден. Миграция не требуется, база будет создана с нуля.")
        return

    print(f"Подключаюсь к {DATABASE_FILE} для миграции...")
    try:
        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()

        # --- Миграция 1: Проверяем и добавляем is_active в employees ---
        cur.execute("PRAGMA table_info(employees)")
        employees_columns = [info[1] for info in cur.fetchall()]
        if 'is_active' not in employees_columns:
            print("Колонка 'is_active' в 'employees' отсутствует. Добавляю...")
            cur.execute("ALTER TABLE employees ADD COLUMN is_active BOOLEAN DEFAULT 1 NOT NULL")
            print(" -> Колонка 'is_active' успешно добавлена.")
        else:
            print(" -> Колонка 'is_active' в 'employees' уже существует.")

        # --- Миграция 2: Создаем таблицу attendance, если ее нет ---
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attendance'")
        if cur.fetchone() is None:
            print("Таблица 'attendance' отсутствует. Создаю...")
            cur.execute("""
            CREATE TABLE attendance (
                id INTEGER NOT NULL,
                employee_id INTEGER NOT NULL,
                attendance_date DATE NOT NULL,
                check_in_time DATETIME,
                check_out_time DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY(employee_id) REFERENCES employees (id),
                UNIQUE (employee_id, attendance_date)
            )
            """)
            print(" -> Таблица 'attendance' успешно создана.")
        else:
            print(" -> Таблица 'attendance' уже существует.")

        con.commit()
        con.close()
        print("\nМиграция завершена успешно.")

    except Exception as e:
        print(f"\nПроизошла ошибка при миграции: {e}")

if __name__ == "__main__":
    migrate()