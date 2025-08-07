import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Date, Boolean,
    ForeignKey, Time, Text, DateTime
)
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from contextlib import contextmanager
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@contextmanager
def get_session():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ОСНОВНЫЕ МОДЕЛИ ---

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    name = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    registered = Column(Boolean, default=False)
    greeted = Column(Boolean, default=False)
    training_passed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    full_name = Column(String(256), nullable=True)
    position = Column(String(128), nullable=True)
    contract_number = Column(String(64), nullable=True)
    employment_date = Column(Date, nullable=True)
    contact_info = Column(String(64), nullable=True)
    branch = Column(String(128), nullable=True)
    cooperation_format = Column(String(64), nullable=True)
    photo_file_id = Column(String, nullable=True) # <-- НОВОЕ ПОЛЕ ДЛЯ АВАТАРА


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    arrival_time = Column(Time, nullable=True)
    departure_time = Column(Time, nullable=True)

class RegCode(Base):
    __tablename__ = "reg_codes"
    code = Column(String(8), primary_key=True)
    email = Column(String, ForeignKey("employees.email"), nullable=False)
    used = Column(Boolean, default=False)


# --- МОДЕЛИ КОНТЕНТА ---

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    text = Column(Text, nullable=False)
    submission_date = Column(DateTime, default=datetime.utcnow)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image_path = Column(String, nullable=True)


# --- МОДЕЛИ ОБУЧЕНИЯ И ОНБОРДИНГА ---

class RoleOnboarding(Base):
    __tablename__ = "role_onboarding"
    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True, nullable=False)
    text = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    file_type = Column(String, default='document', nullable=False) # Поле для типа файла ('document', 'video', 'video_note')

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id             = Column(Integer, primary_key=True)
    role           = Column(String, index=True, nullable=False)
    question       = Column(String, nullable=False)
    answer         = Column(String, nullable=False)
    question_type  = Column(String(20), nullable=False, default="text")  # "text" или "choice"
    options        = Column(String, nullable=True)                       # для choice: "Вариант1;Вариант2;Вариант3"
    order_index    = Column(Integer, nullable=False, default=0)

class TrainingMaterial(Base):
    __tablename__ = "training_material"
    id = Column(Integer, primary_key=True)
    role = Column(String, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    file_path = Column(String, nullable=True)


# --- СИСТЕМНЫЕ МОДЕЛИ ---

class GroupChat(Base):
    __tablename__ = "group_chats"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    chat_id = Column(Integer, nullable=False)


# --- АРХИВНЫЕ МОДЕЛИ ---

class ArchivedEmployee(Base):
    __tablename__ = "archived_employees"

    # ID теперь автоинкрементный и будет генерироваться сам
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Новое поле для хранения ID из основной таблицы
    original_employee_id = Column(Integer, nullable=False, index=True)

    telegram_id = Column(Integer, unique=False, nullable=True)
    email = Column(String, unique=False, nullable=False)
    role = Column(String, nullable=False)
    name = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    registered = Column(Boolean, default=False)
    training_passed = Column(Boolean, default=False)
    dismissal_date = Column(DateTime, default=datetime.utcnow)
    # Примечание: я убрал поля, которых нет в вашей основной модели Employee,
    # чтобы избежать ошибок при копировании. Можете добавить их обратно, если нужно.

class ArchivedAttendance(Base):
    __tablename__ = "archived_attendance"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    arrival_time = Column(Time, nullable=True)
    departure_time = Column(Time, nullable=True)
    # НОВАЯ ТАБЛИЦА: Хранилище всех текстов бота

class BotText(Base):
        __tablename__ = "bot_texts"
        id = Column(String(50), primary_key=True)  # Уникальный ключ (e.g., "welcome_greeting")
        text = Column(Text, nullable=False, default="Текст не задан")
        description = Column(String, nullable=True)  # Пояснение для админа

    # НОВАЯ ТАБЛИЦА: Конструктор вопросов при онбординге
class OnboardingQuestion(Base):
        __tablename__ = "onboarding_questions"
        id = Column(Integer, primary_key=True)
        role = Column(String, index=True, nullable=False)  # Для какой роли этот вопрос
        order_index = Column(Integer, default=0)
        question_text = Column(String, nullable=False)
        data_key = Column(String(50), nullable=False)  # Ключ для сохранения ответа (e.g., "favorite_quote")
        is_required = Column(Boolean, default=True)

    # НОВАЯ ТАБЛИЦА: Хранилище ответов на кастомные вопросы
class EmployeeCustomData(Base):
        __tablename__ = "employee_custom_data"
        id = Column(Integer, primary_key=True)
        employee_id = Column(Integer, ForeignKey("employees.id"), index=True)
        data_key = Column(String(50), nullable=False)
        data_value = Column(Text, nullable=False)

    # НОВАЯ ТАБЛИЦА: Шаги "Знакомства с компанией" после сбора данных
class OnboardingStep(Base):
        __tablename__ = "onboarding_steps"
        id = Column(Integer, primary_key=True)
        role = Column(String, index=True, nullable=False)
        order_index = Column(Integer, default=0)
        message_text = Column(Text, nullable=True)
        file_path = Column(String, nullable=True)
        file_type = Column(String(20), nullable=True)  # 'video_note', 'photo', 'document'

    # FSM States
class Onboarding(StatesGroup):
        awaiting_answer = State()  # Ожидание ответа на кастомный вопрос


class ArchivedIdea(Base):
    __tablename__ = "archived_ideas"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    submission_date = Column(DateTime, default=datetime.utcnow)

