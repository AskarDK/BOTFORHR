# migrate_to_current_schema.py (fixed)
import os
import sqlite3
from contextlib import closing
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
DB_FILE = DATABASE_URL.replace("sqlite:///", "")

# ---------- helpers ----------

def connect():
    if not os.path.exists(DB_FILE):
        print(f"[skip] DB file '{DB_FILE}' not found. Nothing to migrate.")
        raise SystemExit(0)
    # Оставляем управление транзакцией вручную (без автокоммита)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys=OFF;")
    return conn

def table_exists(cur, name: str) -> bool:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (name,))
    return cur.fetchone() is not None

def columns(cur, table: str):
    cur.execute(f"PRAGMA table_info({table});")
    # row = [cid, name, type, notnull, dflt_value, pk]
    return [row[1] for row in cur.fetchall()]

def index_names(cur, table: str):
    cur.execute(f"PRAGMA index_list({table});")
    # row = [seq, name, unique, origin, partial]
    return [(row[1], row[2]) for row in cur.fetchall()]  # (name, unique_flag)

def has_unique_index_on(cur, table: str, cols: tuple) -> bool:
    # Проверяем что есть уникальный индекс точно по заданным колонкам
    for idx_name, unique in index_names(cur, table):
        if unique != 1:
            continue
        cur.execute(f"PRAGMA index_info({idx_name});")
        idx_cols = [r[2] for r in cur.fetchall()]  # [seqno, cid, name]
        if tuple(idx_cols) == cols:
            return True
    return False

def try_alter_rename_column(cur, table: str, old: str, new: str) -> bool:
    try:
        cur.execute(f"ALTER TABLE {table} RENAME COLUMN {old} TO {new};")
        return True
    except Exception as e:
        print(f"[warn] ALTER RENAME COLUMN {table}.{old} -> {new} failed: {e}")
        return False

def recreate_table(cur, table: str, create_sql: str, copy_sql: str, drop_old: bool = True):
    print(f"[recreate] {table} -> {table}_old -> {table}")
    cur.execute(f"ALTER TABLE {table} RENAME TO {table}_old;")
    cur.execute(create_sql)
    cur.execute(copy_sql)
    if drop_old:
        cur.execute(f"DROP TABLE {table}_old;")

# ---------- steps ----------

def migrate_employee_to_employees(cur):
    if table_exists(cur, "employees"):
        cols = columns(cur, "employees")
        if "joined_main_chat" not in cols:
            print("[alter] employees add joined_main_chat")
            cur.execute("ALTER TABLE employees ADD COLUMN joined_main_chat BOOLEAN DEFAULT 0;")
        if "photo_file_id" not in cols:
            print("[alter] employees add photo_file_id")
            cur.execute("ALTER TABLE employees ADD COLUMN photo_file_id TEXT;")
        return

    if table_exists(cur, "employee"):
        print("[rename + create] employee -> employees (with joined_main_chat, photo_file_id)")
        cur.execute("""
        CREATE TABLE employees (
          id INTEGER PRIMARY KEY,
          telegram_id INTEGER UNIQUE,
          email TEXT UNIQUE NOT NULL,
          role TEXT NOT NULL,
          name TEXT,
          birthday DATE,
          registered BOOLEAN DEFAULT 0,
          greeted BOOLEAN DEFAULT 0,
          training_passed BOOLEAN DEFAULT 0,
          onboarding_completed BOOLEAN DEFAULT 0,
          is_active BOOLEAN DEFAULT 1,
          full_name TEXT,
          position TEXT,
          contract_number TEXT,
          employment_date DATE,
          contact_info TEXT,
          branch TEXT,
          cooperation_format TEXT,
          photo_file_id TEXT,
          joined_main_chat BOOLEAN DEFAULT 0
        );
        """)
        cur.execute("""
        INSERT INTO employees (
          id, telegram_id, email, role, name, birthday, registered, greeted, training_passed,
          onboarding_completed, is_active, full_name, position, contract_number, employment_date,
          contact_info, branch, cooperation_format, photo_file_id, joined_main_chat
        )
        SELECT
          id, telegram_id, email, role, name, birthday, registered, greeted, training_passed,
          onboarding_completed, is_active, full_name, position, contract_number, employment_date,
          contact_info, branch, cooperation_format,
          NULL AS photo_file_id, 0 AS joined_main_chat
        FROM employee;
        """)
        cur.execute("DROP TABLE employee;")
    else:
        print("[ok] employees already consistent or nothing to migrate")

def migrate_reg_codes_fk(cur):
    if not table_exists(cur, "reg_codes"):
        print("[skip] reg_codes not found")
        return
    # Всегда пересоздаём для корректного FK
    recreate_table(
        cur,
        "reg_codes",
        """
        CREATE TABLE reg_codes (
          code TEXT PRIMARY KEY,
          email TEXT NOT NULL REFERENCES employees(email),
          used BOOLEAN DEFAULT 0
        );
        """,
        "INSERT INTO reg_codes (code, email, used) SELECT code, email, used FROM reg_codes_old;"
    )

def migrate_ideas_fk(cur):
    if not table_exists(cur, "ideas"):
        print("[skip] ideas not found")
        return
    # Пересоздаём на всякий случай (FK + порядок столбцов)
    recreate_table(
        cur,
        "ideas",
        """
        CREATE TABLE ideas (
          id INTEGER PRIMARY KEY,
          employee_id INTEGER NOT NULL REFERENCES employees(id),
          text TEXT NOT NULL,
          submission_date DATETIME DEFAULT (datetime('now'))
        );
        """,
        "INSERT INTO ideas (id, employee_id, text, submission_date) SELECT id, employee_id, text, submission_date FROM ideas_old;"
    )

def migrate_attendance_unique(cur):
    if not table_exists(cur, "attendance"):
        print("[skip] attendance not found")
        return
    # Пересоздаём, чтобы гарантировать UNIQUE(employee_id,date) и FK
    recreate_table(
        cur,
        "attendance",
        """
        CREATE TABLE attendance (
          id INTEGER PRIMARY KEY,
          employee_id INTEGER NOT NULL REFERENCES employees(id),
          date DATE NOT NULL,
          arrival_time TIME,
          departure_time TIME,
          CONSTRAINT uix_attendance_emp_date UNIQUE (employee_id, date)
        );
        """,
        """
        INSERT OR IGNORE INTO attendance (id, employee_id, date, arrival_time, departure_time)
        SELECT id, employee_id, date, arrival_time, departure_time FROM attendance_old;
        """
    )

def migrate_archived_employees(cur):
    if not table_exists(cur, "archived_employees"):
        print("[skip] archived_employees not found")
        return
    cols = columns(cur, "archived_employees")
    if "original_employee_id" in cols:
        print("[ok] archived_employees already has original_employee_id")
        return
    print("[recreate] archived_employees to add original_employee_id and autoincrement id")
    recreate_table(
        cur,
        "archived_employees",
        """
        CREATE TABLE archived_employees (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          original_employee_id INTEGER NOT NULL,
          telegram_id INTEGER,
          email TEXT NOT NULL,
          role TEXT NOT NULL,
          name TEXT,
          birthday DATE,
          registered BOOLEAN DEFAULT 0,
          training_passed BOOLEAN DEFAULT 0,
          dismissal_date DATETIME DEFAULT (datetime('now'))
        );
        """,
        """
        INSERT INTO archived_employees (
          original_employee_id, telegram_id, email, role, name, birthday, registered, training_passed, dismissal_date
        )
        SELECT
          id AS original_employee_id, telegram_id, email, role, name, birthday, registered, training_passed, dismissal_date
        FROM archived_employees_old;
        """
    )

def migrate_archived_ideas_column(cur):
    if not table_exists(cur, "archived_ideas"):
        print("[skip] archived_ideas not found")
        return
    cols = columns(cur, "archived_ideas")
    if "idea_text" in cols:
        print("[ok] archived_ideas.idea_text already present")
        return
    if "text" in cols:
        print("[alter] archived_ideas RENAME COLUMN text -> idea_text")
        if not try_alter_rename_column(cur, "archived_ideas", "text", "idea_text"):
            print("[fallback] recreate archived_ideas with idea_text")
            recreate_table(
                cur,
                "archived_ideas",
                """
                CREATE TABLE archived_ideas (
                  id INTEGER PRIMARY KEY,
                  employee_id INTEGER NOT NULL,
                  idea_text TEXT NOT NULL,
                  submission_date DATETIME DEFAULT (datetime('now'))
                );
                """,
                """
                INSERT INTO archived_ideas (id, employee_id, idea_text, submission_date)
                SELECT id, employee_id, text, submission_date FROM archived_ideas_old;
                """
            )
    else:
        print("[ok] archived_ideas already migrated (no text col found)")

def ensure_meta_tables(cur):
    # bot_texts
    if not table_exists(cur, "bot_texts"):
        print("[create] bot_texts")
        cur.execute("""
        CREATE TABLE bot_texts (
          id TEXT PRIMARY KEY,
          text TEXT NOT NULL DEFAULT 'Текст не задан',
          description TEXT
        );
        """)

    # onboarding_questions
    if not table_exists(cur, "onboarding_questions"):
        print("[create] onboarding_questions")
        cur.execute("""
        CREATE TABLE onboarding_questions (
          id INTEGER PRIMARY KEY,
          role TEXT NOT NULL,
          order_index INTEGER DEFAULT 0,
          question_text TEXT NOT NULL,
          data_key TEXT NOT NULL,
          is_required BOOLEAN DEFAULT 1
        );
        """)

    # employee_custom_data
    if not table_exists(cur, "employee_custom_data"):
        print("[create] employee_custom_data")
        cur.execute("""
        CREATE TABLE employee_custom_data (
          id INTEGER PRIMARY KEY,
          employee_id INTEGER REFERENCES employees(id),
          data_key TEXT NOT NULL,
          data_value TEXT NOT NULL
        );
        """)

    # onboarding_steps
    if not table_exists(cur, "onboarding_steps"):
        print("[create] onboarding_steps")
        cur.execute("""
        CREATE TABLE onboarding_steps (
          id INTEGER PRIMARY KEY,
          role TEXT NOT NULL,
          order_index INTEGER DEFAULT 0,
          message_text TEXT,
          file_path TEXT,
          file_type TEXT
        );
        """)

    # group_chats + уникальный индекс на chat_id
    if not table_exists(cur, "group_chats"):
        print("[create] group_chats")
        cur.execute("""
        CREATE TABLE group_chats (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          chat_id INTEGER NOT NULL
        );
        """)
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_group_chats_chat_id ON group_chats(chat_id);")

def migrate():
    print(f"== DB migrate start @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ==")
    with closing(connect()) as conn:
        cur = conn.cursor()
        try:
            # один общий транзакционный блок
            cur.execute("BEGIN IMMEDIATE;")

            migrate_employee_to_employees(cur)
            migrate_reg_codes_fk(cur)
            migrate_ideas_fk(cur)
            migrate_attendance_unique(cur)
            migrate_archived_employees(cur)
            migrate_archived_ideas_column(cur)
            ensure_meta_tables(cur)

            cur.execute("COMMIT;")
        except Exception as e:
            print(f"[error] migration failed: {e}")
            try:
                cur.execute("ROLLBACK;")
            except Exception as e2:
                print(f"[warn] rollback failed: {e2}")
            raise
        finally:
            conn.execute("PRAGMA foreign_keys=ON;")
    print("== DB migrate done ==")

if __name__ == "__main__":
    migrate()
