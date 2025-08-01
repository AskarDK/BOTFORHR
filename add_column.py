#!/usr/bin/env python3
# migrate_add_training_passed.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

# берём URL вашей базы из .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")

def add_training_passed_column():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    with engine.connect() as conn:
        # читаем список колонок в таблице employees
        res = conn.execute(text("PRAGMA table_info(employees);")).fetchall()
        cols = [row[1] for row in res]  # row[1] — имя колонки
        if "training_passed" in cols:
            print("✅ Колонка training_passed уже существует в таблице employees.")
        else:
            try:
                # добавляем колонку BOOLEAN DEFAULT 0 (FALSE)
                conn.execute(text(
                    "ALTER TABLE employees ADD COLUMN training_passed BOOLEAN NOT NULL DEFAULT 0;"
                ))
                print("✅ Колонка training_passed успешно добавлена.")
            except OperationalError as e:
                print("❌ Не удалось добавить колонку:", e)

if __name__ == "__main__":
    add_training_passed_column()
