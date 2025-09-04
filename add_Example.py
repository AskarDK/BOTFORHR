# add_Example.py

from datetime import date
from bot import SessionLocal, Employee  # импортируем фабрику сессий и модель

def add_admin():
    # ← ОБРАТИТЕ ВНИМАНИЕ: именно SessionLocal(), а не SessionLocal
    session = SessionLocal()
    try:
        admin = Employee(
            telegram_id=None,
            email="admin@company.com",
            role="Admin",
            name="Иван Иванов",
            birthday=date(1990, 1, 1),
            registered=True,
            greeted=False
        )
        session.add(admin)     # метод .add есть у сессии — не у фабрики!
        session.commit()
        print(f"✅ Admin {admin.email} добавлен")
    finally:
        session.close()       # и закрываем сессию

if __name__ == "__main__":
    add_admin()
