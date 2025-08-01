#!/usr/bin/env python3
import os
import asyncio
import logging
import html
from datetime import datetime, date
from math import radians, sin, cos, sqrt, atan2

from dotenv import load_dotenv

from aiogram.types import ChatMemberUpdated
from aiogram import Bot, Dispatcher, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message, CallbackQuery,
    KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardButton, InlineKeyboardMarkup,
    FSInputFile
)
from aiogram.utils.chat_action import ChatActionSender

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sqlalchemy import (
    create_engine, Column, Integer, String, Date, Boolean,
    ForeignKey, func, Time, Text, DateTime
)
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from contextlib import contextmanager

import random

# — Загрузка .env —
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
COMMON_CHAT_ID = int(os.getenv("COMMON_CHAT_ID", "-1001234567890"))
OFFICE_LAT = float(os.getenv("OFFICE_LAT", "51.1282"))
OFFICE_LON = float(os.getenv("OFFICE_LON", "71.4304"))
OFFICE_RADIUS_METERS = int(os.getenv("OFFICE_RADIUS_METERS", "300"))

# — Логирование —
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# — Инициализация бота и диспетчера —
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


# — FSM States —
class Reg(StatesGroup):
    waiting_code = State()


class Training(StatesGroup):
    waiting_ack = State()


class Quiz(StatesGroup):
    waiting_answer = State()


class AdminAdd(StatesGroup):
    email = State()
    role = State()
    name = State()
    birthday = State()


class AdminFindID(StatesGroup):
    waiting_id = State()


class AdminAttendance(StatesGroup):
    waiting_employee_id = State()
    waiting_date = State()


# FSM для новых функций
class AddEvent(StatesGroup):
    waiting_title = State()
    waiting_description = State()
    waiting_date = State()


class SubmitIdea(StatesGroup):
    waiting_for_idea = State()


# — SQLAlchemy setup —
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


# — Модели —
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


# НОВЫЕ ТАБЛИЦЫ ДЛЯ ИВЕНТОВ И ИДЕЙ
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
    idea_text = Column(Text, nullable=False)
    submission_date = Column(DateTime, default=datetime.utcnow)


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True)
    role = Column(String, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image_path = Column(String, nullable=True) # <-- ДОБАВИТЬ ЭТУ СТРОКУ


class RoleOnboarding(Base):
    __tablename__ = "role_onboarding"
    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True, nullable=False)
    text = Column(String, nullable=False)
    file_path = Column(String, nullable=True)


class TrainingMaterial(Base):
    __tablename__ = "training_material"
    id = Column(Integer, primary_key=True)
    role = Column(String, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    file_path = Column(String, nullable=True)


class GroupChat(Base):
    __tablename__ = "group_chats"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    chat_id = Column(Integer, nullable=False)


Base.metadata.create_all(engine)

# — Кнопки и клавиатуры —
BACK_BTN = KeyboardButton(text="🔙 Назад")

# --- ИЗМЕНЕНИЕ: Добавлена кнопка "Наши сотрудники" ---
employee_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Я на месте", request_location=True),
         KeyboardButton(text="👋 Я ухожу", request_location=True)],
        [KeyboardButton(text="🎉 Посмотреть ивенты"), KeyboardButton(text="💡 Поделиться идеей")],
        [KeyboardButton(text="👥 Наши сотрудники"), KeyboardButton(text="🧠 База знаний")],
        [KeyboardButton(text="📊 Мой профиль")]
    ],
    resize_keyboard=True
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 База знаний"), KeyboardButton(text="📊 Мой профиль")]
    ],
    resize_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить сотрудника"), KeyboardButton(text="Список сотрудников")],
        [KeyboardButton(text="Добавить ивент"), KeyboardButton(text="🎉 Посмотреть ивенты")],
        [KeyboardButton(text="Просмотр идей"), KeyboardButton(text="Посещаемость сотрудника")],
        [KeyboardButton(text="👥 Наши сотрудники"), KeyboardButton(text="🧠 База знаний")],
        [KeyboardButton(text="📊 Мой профиль")],
        [BACK_BTN],
    ],
    resize_keyboard=True
)

training_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О компании"), KeyboardButton(text="🏃‍♂️ Пройти тренинг"),
         KeyboardButton(text="Контакты")],
        [BACK_BTN],
    ],
    resize_keyboard=True
)

quiz_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Готовы", callback_data="quiz_start")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")],
    ]
)

ack_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ознакомился", callback_data="training_done")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")],
    ]
)

PAGE_SIZE = 5


# --- Функции для геолокации ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


@dp.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()

    if emp and emp.registered:
        if not emp.is_active:
            await msg.answer("❌ Ваш аккаунт деактивирован. Обратитесь к администратору.", reply_markup=None)
            return
        if not emp.training_passed:
            await msg.answer(
                f"👋 Привет, {emp.name}! Чтобы продолжить работу, пройдите, пожалуйста, тренинг 🏃‍♂️",
                reply_markup=training_kb
            )
        else:
            kb = admin_kb if emp.role == "Admin" else employee_main_kb
            await msg.answer(
                f"👋 С возвращением, {emp.name}! Тренинг уже пройден 😊",
                reply_markup=kb
            )
    else:
        await msg.answer(
            "📝 Пожалуйста, введите ваш 8-значный регистрационный код:",
            reply_markup=ReplyKeyboardMarkup(keyboard=[[BACK_BTN]], resize_keyboard=True)
        )
        await state.set_state(Reg.waiting_code)


@dp.message(Reg.waiting_code)
async def process_code(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        with get_session() as db:
            emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        kb = admin_kb if emp and emp.role == "Admin" else main_kb
        await msg.answer("🔙 Возвращаемся в главное меню.", reply_markup=kb)
        return
    if not msg.text or not msg.text.isdigit() or len(msg.text) != 8:
        await msg.answer("❌ Неверный формат кода. Введите 8 цифр или «🔙 Назад».")
        return

    code = msg.text.strip()
    with get_session() as db:
        rc = db.query(RegCode).filter_by(code=code, used=False).first()
        if not rc:
            await msg.answer("❌ Код не найден или уже использован. Пожалуйста, попробуйте ещё раз.")
            return
        emp = db.query(Employee).filter_by(email=rc.email).first()
        if not emp.is_active:
            await msg.answer("❌ Ваш аккаунт был деактивирован. Регистрация невозможна.")
            await state.clear()
            return

        emp.telegram_id = msg.from_user.id
        emp.registered = True
        rc.used = True
        db.commit()

    await state.clear()
    if emp.training_passed:
        kb = admin_kb if emp.role == "Admin" else employee_main_kb
        await msg.answer(f"🎉 Ура, {emp.name}! Вы — {emp.role}. Тренинг уже пройден ✅", reply_markup=kb)
    else:
        await msg.answer(
            f"🎉 Ура, {emp.name}! Вы — {emp.role}. Чтобы продолжить работу, пройдите, пожалуйста, тренинг 🏃‍♂️",
            reply_markup=training_kb
        )


@dp.message(F.location)
async def handle_location(msg: Message):
    user_location = msg.location
    distance = haversine(user_location.latitude, user_location.longitude, OFFICE_LAT, OFFICE_LON)

    if distance > OFFICE_RADIUS_METERS:
        await msg.answer(
            f"❌ Вы находитесь слишком далеко от офиса ({int(distance)} м). "
            f"Допустимый радиус: {OFFICE_RADIUS_METERS} м. Попробуйте подойти ближе."
        )
        return

    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id, is_active=True).first()
        if not emp:
            await msg.answer("Не удалось идентифицировать вас как активного сотрудника.")
            return

        today_date = date.today()
        now_time = datetime.now().time()
        attendance_record = db.query(Attendance).filter_by(employee_id=emp.id, date=today_date).first()

        if not attendance_record:
            attendance_record = Attendance(employee_id=emp.id, date=today_date, arrival_time=now_time)
            db.add(attendance_record)
            db.commit()
            await msg.answer(f"✅ Отлично, {emp.name}! Ваш приход в {now_time.strftime('%H:%M:%S')} зафиксирован.")
        else:
            if attendance_record.departure_time:
                await msg.answer(
                    f"🤔 Вы уже отмечали уход сегодня в {attendance_record.departure_time.strftime('%H:%M:%S')}. Повторная отметка не требуется.")
            else:
                attendance_record.departure_time = now_time
                db.commit()
                await msg.answer(
                    f"👋 Хорошего вечера, {emp.name}! Ваш уход в {now_time.strftime('%H:%M:%S')} зафиксирован.")


@dp.callback_query(F.data == "back")
async def inline_back(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.clear()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=cb.from_user.id).first()

    if emp and emp.is_active:
        if emp.role == "Admin":
            kb = admin_kb
        elif emp.training_passed:
            kb = employee_main_kb
        else:
            kb = main_kb
        # Изменено для отправки нового сообщения вместо редактирования
        await cb.message.answer("🔙 Возвращаемся в главное меню.", reply_markup=kb)
    await cb.answer()


# --- БЛОК ИВЕНТОВ ---
@dp.message((F.text == "🎉 Посмотреть ивенты") | (F.text == "Посмотреть ивенты"))
async def view_events(msg: Message):
    with get_session() as db:
        upcoming_events = db.query(Event).filter(Event.event_date >= datetime.now()).order_by(Event.event_date).all()

    if not upcoming_events:
        await msg.answer("😢 Пока нет предстоящих ивентов.")
        return

    response = "<b>🎉 Предстоящие ивенты:</b>\n\n"
    for event in upcoming_events:
        event_date_str = event.event_date.strftime("%d.%m.%Y в %H:%M")
        response += (f"<b>{html.escape(event.title)}</b>\n"
                     f"<i>{html.escape(event.description)}</i>\n"
                     f"<b>Когда:</b> {event_date_str}\n\n")

    await msg.answer(response)


@dp.message(F.text == "Добавить ивент")
async def admin_add_event_start(msg: Message, state: FSMContext):
    with get_session() as db:
        me = db.query(Employee).filter_by(telegram_id=msg.from_user.id, role="Admin", is_active=True).first()
    if not me: return
    await msg.answer("Введите название ивента:",
                     reply_markup=ReplyKeyboardMarkup(keyboard=[[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AddEvent.waiting_title)


@dp.message(AddEvent.waiting_title)
async def event_add_title(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Вы в админ-панели.", reply_markup=admin_kb)
        return
    await state.update_data(title=msg.text)
    await msg.answer("Теперь введите описание ивента:")
    await state.set_state(AddEvent.waiting_description)


@dp.message(AddEvent.waiting_description)
async def event_add_description(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer("И наконец, введите дату и время ивента в формате ГГГГ-ММ-ДД ЧЧ:ММ (например, 2025-08-15 19:00):")
    await state.set_state(AddEvent.waiting_date)


@dp.message(AddEvent.waiting_date)
async def event_add_date(msg: Message, state: FSMContext):
    try:
        event_dt = datetime.strptime(msg.text, "%Y-%m-%d %H:%M")
    except ValueError:
        await msg.answer("❌ Неверный формат. Пожалуйста, используйте формат ГГГГ-ММ-ДД ЧЧ:ММ.")
        return

    data = await state.get_data()
    with get_session() as db:
        new_event = Event(
            title=data['title'],
            description=data['description'],
            event_date=event_dt
        )
        db.add(new_event)
        db.commit()

    await msg.answer(f"✅ Ивент «{html.escape(data['title'])}» успешно добавлен!", reply_markup=admin_kb)
    await state.clear()


@dp.message(F.text == "💡 Поделиться идеей")
async def share_idea_start(msg: Message, state: FSMContext):
    await msg.answer("Напишите вашу идею или предложение. Администрация обязательно рассмотрит его.",
                     reply_markup=ReplyKeyboardMarkup(keyboard=[[BACK_BTN]], resize_keyboard=True))
    await state.set_state(SubmitIdea.waiting_for_idea)


@dp.message(SubmitIdea.waiting_for_idea)
async def process_idea(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        with get_session() as db:
            emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        kb = admin_kb if emp and emp.role == "Admin" else employee_main_kb
        await msg.answer("Главное меню.", reply_markup=kb)
        return

    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id, is_active=True).first()
        if not emp: return

        new_idea = Idea(employee_id=emp.id, idea_text=msg.text)
        db.add(new_idea)
        db.commit()
    kb = admin_kb if emp.role == "Admin" else employee_main_kb
    await msg.answer("Спасибо! Ваша идея принята.", reply_markup=kb)
    await state.clear()


@dp.message(F.text == "Просмотр идей")
async def view_ideas(msg: Message):
    with get_session() as db:
        me = db.query(Employee).filter_by(telegram_id=msg.from_user.id, role="Admin", is_active=True).first()
        if not me: return

    await send_ideas_page(msg.chat.id, page=0)


async def send_ideas_page(chat_id: int, page: int, message_id: int | None = None):
    with get_session() as db:
        total = db.query(Idea).count()
        ideas = (db.query(Idea)
                 .join(Employee, Idea.employee_id == Employee.id)
                 .order_by(Idea.submission_date.desc())
                 .add_columns(Employee.name)
                 .offset(page * PAGE_SIZE).limit(PAGE_SIZE).all())

    if not ideas:
        await bot.send_message(chat_id, "Пока никто не подавал идей.")
        return

    response = "<b>💡 Последние идеи от сотрудников:</b>\n\n"
    for idea, emp_name in ideas:
        date_str = idea.submission_date.strftime("%d.%m.%Y %H:%M")
        response += (f"<b>От:</b> {html.escape(emp_name)}\n"
                     f"<b>Когда:</b> {date_str}\n"
                     f"<b>Идея:</b> <i>{html.escape(idea.idea_text)}</i>\n\n")

    buttons = []
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"idea_page:{page - 1}"))
    if (page + 1) * PAGE_SIZE < total:
        nav.append(InlineKeyboardButton(text="Вперед ▶️", callback_data=f"idea_page:{page + 1}"))
    if nav:
        buttons.append(nav)

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message_id:
        # --- FIX: Using keyword arguments ---
        await bot.edit_message_text(
            text=response,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=kb
        )
    else:
        await bot.send_message(chat_id, response, reply_markup=kb)

@dp.callback_query(F.data.startswith("idea_page:"))
async def idea_page_callback(cb: CallbackQuery):
    page = int(cb.data.split(":", 1)[1])
    await send_ideas_page(cb.message.chat.id, page, cb.message.message_id)
    await cb.answer()


# --- НОВЫЙ БЛОК: ПРОСМОТР СОТРУДНИКОВ ДЛЯ ВСЕХ ---
@dp.message(F.text == "👥 Наши сотрудники")
async def show_employee_roles(msg: Message):
    with get_session() as db:
        # Проверяем, что пользователь является активным сотрудником
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id, is_active=True).first()
        if not emp:
            await msg.answer("Эта функция доступна только для зарегистрированных сотрудников.")
            return

    await send_roles_page(msg.chat.id)


async def send_roles_page(chat_id: int, message_id: int | None = None):
    with get_session() as db:
        roles = db.query(Employee.role).filter(Employee.is_active == True).distinct().all()

    if not roles:
        text = "В компании пока нет сотрудников."
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 В меню", callback_data="back")]])
    else:
        text = "Выберите отдел, чтобы посмотреть список сотрудников:"
        buttons = [
            [InlineKeyboardButton(text=role[0], callback_data=f"role_select:{role[0]}:0")]
            for role in roles if role[0]
        ]
        buttons.append([InlineKeyboardButton(text="🔙 В меню", callback_data="back")])
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message_id:
        # --- FIX: Using keyword arguments ---
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=kb
        )
    else:
        await bot.send_message(chat_id, text, reply_markup=kb)

async def send_employees_by_role_page(chat_id: int, role: str, page: int, message_id: int | None = None):
    with get_session() as db:
        query = db.query(Employee).filter(Employee.is_active == True, Employee.role == role)
        total = query.count()
        emps = query.order_by(Employee.name).offset(page * PAGE_SIZE).limit(PAGE_SIZE).all()

    text = f"<b>Сотрудники отдела «{html.escape(role)}»</b> (Страница {page + 1}):"

    buttons = []
    if not emps:
        text = f"В отделе «{html.escape(role)}» пока нет сотрудников."
    else:
        for e in emps:
            buttons.append([InlineKeyboardButton(text=e.name or f"ID {e.id}", callback_data=f"view_emp_details:{e.id}")])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"role_select:{role}:{page - 1}"))
    if (page + 1) * PAGE_SIZE < total:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"role_select:{role}:{page + 1}"))
    if nav:
        buttons.append(nav)

    buttons.append([InlineKeyboardButton(text="🔙 К отделам", callback_data="back_to_roles")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message_id:
        # --- FIX: Using keyword arguments ---
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=kb
        )
    else:
        await bot.send_message(chat_id, text, reply_markup=kb)

@dp.callback_query(F.data.startswith("role_select:"))
async def select_role_callback(cb: CallbackQuery):
    _, role, page_str = cb.data.split(":", 2)
    await send_employees_by_role_page(cb.message.chat.id, role, int(page_str), cb.message.message_id)
    await cb.answer()


@dp.callback_query(F.data.startswith("view_emp_details:"))
async def view_employee_details_callback(cb: CallbackQuery):
    eid = int(cb.data.split(":", 1)[1])
    with get_session() as db:
        e = db.query(Employee).get(eid)

    if not e:
        await cb.answer("Сотрудник не найден.", show_alert=True)
        return

    text = (f"<b>Профиль сотрудника:</b>\n\n"
            f"<b>Имя:</b> {html.escape(e.name or 'Не указано')}\n"
            f"<b>Должность:</b> {html.escape(e.role)}\n"
            f"<b>Контакт:</b> {html.escape(e.contact_info or 'Не указан')}")

    buttons = []
    if e.telegram_id:
        buttons.append([InlineKeyboardButton(text="💬 Связаться в Telegram", url=f"tg://user?id={e.telegram_id}")])
    buttons.append([InlineKeyboardButton(text="🔙 К списку сотрудников", callback_data=f"role_select:{e.role}:0")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    # --- FIX: Using keyword arguments ---
    await bot.edit_message_text(
        text=text,
        chat_id=cb.message.chat.id,
        message_id=cb.message.message_id,
        reply_markup=kb
    )
    await cb.answer()

@dp.callback_query(F.data == "back_to_roles")
async def back_to_roles_callback(cb: CallbackQuery):
    await send_roles_page(cb.message.chat.id, cb.message.message_id)
    await cb.answer()


# — Админ: добавление сотрудника —
@dp.message(F.text == "Добавить сотрудника")
async def admin_start_add(msg: Message, state: FSMContext):
    with get_session() as db:
        me = db.query(Employee).filter_by(telegram_id=msg.from_user.id, role="Admin", registered=True,
                                          is_active=True).first()
    if not me: return
    await msg.answer("Введите email нового сотрудника:",
                     reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AdminAdd.email)


@dp.message(AdminAdd.email)
async def admin_add_email(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Вы в админ-панели.", reply_markup=admin_kb)
        return
    email = msg.text.strip()
    with get_session() as db:
        if db.query(Employee).filter_by(email=email).first():
            await msg.answer("⚠️ Такой email уже есть. Отмена.", reply_markup=admin_kb)
            await state.clear()
            return
    await state.update_data(email=email)
    await msg.answer("Укажите роль (Hunter, Pusher, Trainer, TL, Admin):",
                     reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AdminAdd.role)


@dp.message(AdminAdd.role)
async def admin_add_role(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Вы в админ-панели.", reply_markup=admin_kb)
        return
    role = msg.text.strip()
    if role not in ["Hunter", "Pusher", "Trainer", "TL", "Admin"]:
        await msg.answer("Неправильная роль. Повторите.",
                         reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
        return
    await state.update_data(role=role)
    await msg.answer("Введите полное имя:", reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AdminAdd.name)


@dp.message(AdminAdd.name)
async def admin_add_name(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Вы в админ-панели.", reply_markup=admin_kb)
        return
    await state.update_data(name=msg.text.strip())
    await msg.answer("Введите дату рождения (YYYY-MM-DD):",
                     reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AdminAdd.birthday)


@dp.message(AdminAdd.birthday)
async def admin_add_birthday(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Вы в админ-панели.", reply_markup=admin_kb)
        return
    text = msg.text.strip()
    try:
        bday = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        await msg.answer("❌ Ошибка формата, используйте YYYY-MM-DD.",
                         reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
        return

    data = await state.get_data()
    with get_session() as db:
        emp = Employee(email=data["email"], role=data["role"], name=data["name"], birthday=bday, is_active=True)
        db.add(emp)
        db.flush()
        # Генерируем уникальный код, которого еще нет в базе
        while True:
            code = "".join(str(random.randint(0, 9)) for _ in range(8))
            if not db.query(RegCode).filter_by(code=code).first():
                break
        db.add(RegCode(code=code, email=data["email"], used=False))
        db.commit()

    await msg.answer(f"✅ Сотрудник {html.escape(data['name'])} добавлен.\n"
                     f"❗️ Выдайте ему этот код для регистрации: <code>{code}</code>",
                     reply_markup=admin_kb)
    await state.clear()


# — Админ: пагинированный список сотрудников —
@dp.message(F.text == "Список сотрудников")
async def admin_list(msg: Message, state: FSMContext):
    with get_session() as db:
        me = db.query(Employee).filter_by(telegram_id=msg.from_user.id, role="Admin", registered=True,
                                          is_active=True).first()
    if not me: return
    await send_employees_page(msg, page=0)


async def send_employees_page(msg: Message, page: int):
    with get_session() as db:
        query = db.query(Employee).filter(Employee.is_active == True)
        total = query.count()
        emps = (query.order_by(Employee.role, Employee.name).offset(page * PAGE_SIZE).limit(PAGE_SIZE).all())

    if not emps:
        await msg.answer("Активных сотрудников нет.", reply_markup=admin_kb)
        return

    buttons: list[list[InlineKeyboardButton]] = []
    for e in emps:
        buttons.append([InlineKeyboardButton(text=e.name or f"ID {e.id}", callback_data=f"emp_select:{e.id}")])

    nav: list[InlineKeyboardButton] = []
    if page > 0: nav.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"emp_page:{page - 1}"))
    if (page + 1) * PAGE_SIZE < total: nav.append(
        InlineKeyboardButton(text="Вперед ▶️", callback_data=f"emp_page:{page + 1}"))
    if nav: buttons.append(nav)

    buttons.append([InlineKeyboardButton(text="🔍 По ID", callback_data="emp_find")])
    buttons.append([InlineKeyboardButton(text="🔙 В меню", callback_data="back")])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    # Исправлено: используется cb.message.chat.id
    if isinstance(msg, CallbackQuery):
        await bot.edit_message_text(
            f"Список активных сотрудников (страница {page + 1} из {((total - 1) // PAGE_SIZE) + 1}):",
            chat_id=msg.message.chat.id,
            message_id=msg.message.message_id,
            reply_markup=kb)
    else:
        await msg.answer(f"Список активных сотрудников (страница {page + 1} из {((total - 1) // PAGE_SIZE) + 1}):",
                         reply_markup=kb)


@dp.callback_query(F.data.startswith("emp_page:"))
async def emp_page_callback(cb: CallbackQuery):
    page = int(cb.data.split(":", 1)[1])
    await send_employees_page(cb, page)
    await cb.answer()


@dp.callback_query(F.data.startswith("emp_select:"))
async def emp_select_callback(cb: CallbackQuery, page: int = 0):
    eid = int(cb.data.split(":", 1)[1])
    with get_session() as db:
        e = db.query(Employee).get(eid)
    if not e:
        await cb.answer("Сотрудник не найден.", show_alert=True)
        return

    status = '✅ Активен' if e.is_active else '❌ Уволен'
    text = (f"• <b>{html.escape(e.name or '')}</b> ({html.escape(e.role)})\n"
            f"  • ID: <code>{e.id}</code>\n"
            f"  • Статус: {status}\n"
            f"  • email: <code>{html.escape(e.email)}</code>\n"
            f"  • Зарегистрирован: {'✅' if e.registered else '❌'}\n"
            f"  • Telegram ID: <code>{html.escape(str(e.telegram_id or '—'))}</code>\n"
            f"  • ДР: {e.birthday.strftime('%d.%m.%Y') if e.birthday else ''}")

    buttons = [
        [InlineKeyboardButton(text="📊 Посещаемость", callback_data=f"emp_attendance:{e.id}")],
        [InlineKeyboardButton(text="🔄 Сбросить телеграм", callback_data=f"emp_reset_tg:{e.id}:{page}")],
        [InlineKeyboardButton(text="🔥 Уволить", callback_data=f"emp_dismiss:{e.id}:{page}")],
        [InlineKeyboardButton(text="🔙 К списку", callback_data=f"emp_page:{page}")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await cb.message.edit_text(text, parse_mode="HTML", reply_markup=kb)
    await cb.answer()


@dp.callback_query(F.data == "emp_list_back")
async def emp_list_back_callback(cb: CallbackQuery):
    await send_employees_page(cb, page=0)
    await cb.answer()


@dp.callback_query(F.data.startswith("emp_reset_tg:"))
async def emp_reset_telegram_callback(cb: CallbackQuery):
    _, eid_str, page_str = cb.data.split(":", 2)
    eid = int(eid_str)
    page = int(page_str)
    with get_session() as db:
        emp = db.query(Employee).get(eid)
        if not emp:
            await cb.answer("Сотрудник не найден.", show_alert=True)
            return

        emp.telegram_id = None
        emp.registered = False
        db.commit()

        await cb.answer("✅ Telegram-аккаунт сотрудника сброшен.", show_alert=True)
        # Обновляем сообщение, чтобы отразить изменения
        cb.data = f"emp_select:{eid}"  # Обновляем данные для вызова
        await emp_select_callback(cb, page=page)


@dp.callback_query(F.data.startswith("emp_dismiss:"))
async def emp_dismiss_callback(cb: CallbackQuery):
    _, eid_str, page_str = cb.data.split(":", 2)
    eid = int(eid_str)
    page = int(page_str)
    with get_session() as db:
        emp = db.query(Employee).get(eid)
        if not emp:
            await cb.answer("Сотрудник не найден.", show_alert=True)
            return
        if not emp.is_active:
            await cb.answer("Сотрудник уже уволен.", show_alert=True)
            return

        emp_name = html.escape(emp.name or f"ID {emp.id}")
        emp.is_active = False
        db.commit()

        # await cb.message.edit_text(f"✅ Сотрудник {emp_name} был уволен.")
        try:
            await bot.send_message(COMMON_CHAT_ID,
                                   f"❗️Внимание: сотрудник {emp_name} ({html.escape(emp.role)}) был уволен.")
        except Exception as e:
            logger.error(f"Could not send dismissal notification to common chat: {e}")
            await bot.send_message(cb.message.chat.id, "Не удалось отправить уведомление в общий чат.")
    await cb.answer(f"Сотрудник {emp_name} уволен.")
    await send_employees_page(cb, page=page)


@dp.message(F.text == "Посещаемость сотрудника")
async def admin_attendance_start(msg: Message, state: FSMContext):
    with get_session() as db:
        me = db.query(Employee).filter_by(telegram_id=msg.from_user.id, role="Admin", is_active=True).first()
    if not me: return
    await msg.answer("Введите ID сотрудника для проверки посещаемости:",
                     reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AdminAttendance.waiting_employee_id)


@dp.callback_query(F.data.startswith("emp_attendance:"))
async def emp_attendance_callback(cb: CallbackQuery, state: FSMContext):
    eid = int(cb.data.split(":", 1)[1])
    await state.update_data(employee_id=eid)
    await cb.message.delete()
    await cb.message.answer(f"Введите дату для проверки посещаемости сотрудника ID {eid} (в формате ГГГГ-ММ-ДД):",
                            reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AdminAttendance.waiting_date)
    await cb.answer()


@dp.message(AdminAttendance.waiting_employee_id)
async def process_attendance_id(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Вы в админ-панели.", reply_markup=admin_kb)
        return
    if not msg.text or not msg.text.isdigit():
        await msg.answer("Пожалуйста, введите числовой ID или «🔙 Назад».")
        return
    eid = int(msg.text)
    with get_session() as db:
        if not db.query(Employee).get(eid):
            await msg.answer("Сотрудник с таким ID не найден.", reply_markup=admin_kb)
            await state.clear()
            return
    await state.update_data(employee_id=eid)
    await msg.answer("Введите дату для проверки (в формате ГГГГ-ММ-ДД):",
                     reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AdminAttendance.waiting_date)


@dp.message(AdminAttendance.waiting_date)
async def process_attendance_date(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Вы в админ-панели.", reply_markup=admin_kb)
        return

    try:
        check_date = datetime.strptime(msg.text.strip(), "%Y-%m-%d").date()
    except ValueError:
        await msg.answer("❌ Неверный формат даты. Введите дату как ГГГГ-ММ-ДД или «🔙 Назад».")
        return

    data = await state.get_data()
    eid = data['employee_id']
    with get_session() as db:
        emp = db.query(Employee).get(eid)
        record = db.query(Attendance).filter_by(employee_id=eid, date=check_date).first()
        emp_name = html.escape(emp.name or f"ID {emp.id}")
        date_str = check_date.strftime('%d.%m.%Y')
        response_text = f"<b>Посещаемость {emp_name} за {date_str}</b>\n\n"

        if record:
            arrival = record.arrival_time.strftime('%H:%M:%S') if record.arrival_time else "не отмечен"
            departure = record.departure_time.strftime('%H:%M:%S') if record.departure_time else "не отмечен"
            response_text += f" • Приход: <b>{arrival}</b>\n • Уход: <b>{departure}</b>"
        else:
            response_text += "❌ Сотрудник не приходил на работу в этот день."
    await msg.answer(response_text, reply_markup=admin_kb)
    await state.clear()


@dp.callback_query(F.data == "emp_find")
async def emp_find_callback(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await cb.message.answer("Введите ID сотрудника:",
                            reply_markup=ReplyKeyboardMarkup([[BACK_BTN]], resize_keyboard=True))
    await state.set_state(AdminFindID.waiting_id)
    await cb.answer()


@dp.message(AdminFindID.waiting_id)
async def process_find_id(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Вы в админ-панели.", reply_markup=admin_kb)
        return
    if not msg.text or not msg.text.isdigit():
        await msg.answer("Пожалуйста, введите числовой ID или «🔙 Назад».")
        return
    eid = int(msg.text)
    with get_session() as db:
        e = db.query(Employee).get(eid)
    if not e:
        await msg.answer("Сотрудник не найден.", reply_markup=admin_kb)
    else:
        status = '✅ Активен' if e.is_active else '❌ Уволен'
        text = (
            f"• <b>{html.escape(e.name or '')}</b> ({html.escape(e.role)})\n"
            f"  • ID: <code>{e.id}</code>\n"
            f"  • Статус: {status}\n"
            f"  • email: <code>{html.escape(e.email)}</code>\n"
            f"  • Зарегистрирован: {'✅' if e.registered else '❌'}\n"
            f"  • Telegram ID: <code>{html.escape(str(e.telegram_id or '—'))}</code>\n"
            f"  • ДР: {e.birthday.strftime('%d.%m.%Y') if e.birthday else ''}"
        )
        await msg.answer(text, parse_mode="HTML", reply_markup=admin_kb)
    await state.clear()


# Остальной код без изменений (тренинг, квиз, база знаний и т.д.)
# ...
@dp.message(F.text == "🏃‍♂️ Пройти тренинг")
async def start_training(msg: Message, state: FSMContext):
    await state.clear()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        if not emp or not emp.is_active: return
        onboarding = db.query(RoleOnboarding).filter_by(role=emp.role).first()
    if onboarding:
        await msg.answer(f"📚 {onboarding.text}")
        if onboarding.file_path:
            try:
                await ChatActionSender.upload_video(chat_id=msg.chat.id)
                await msg.answer_video(FSInputFile(onboarding.file_path))
            except Exception as e:
                logger.error(f"Failed to send video {onboarding.file_path}: {e}")
                await msg.answer("Не удалось загрузить видео-материал.")
    else:
        await msg.answer("📚 Материалы для вашего тренинга пока не добавлены. Обратитесь к HR 😊")
    await msg.answer("Нажмите «✅ Ознакомился» когда будете готовы начать квиз 💡", reply_markup=ack_kb)
    await state.set_state(Training.waiting_ack)


@dp.callback_query(F.data == "training_done")
async def training_done(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await cb.message.answer("✨ Отлично! Теперь давайте проверим знания в квизе. Готовы?", reply_markup=quiz_start_kb)
    await cb.answer()
    await state.clear()


@dp.callback_query(F.data == "quiz_start")
async def on_quiz_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=cb.from_user.id).first()
        if not emp or not emp.is_active:
            await cb.answer("Аккаунт неактивен.", show_alert=True)
            return
        qs = db.query(QuizQuestion).filter_by(role=emp.role).all()
        if not qs:
            emp.training_passed = True
            db.commit()
            kb = admin_kb if emp.role == "Admin" else employee_main_kb
            await cb.message.answer("🎉 Поздравляем! Для вашей роли квиза нет — тренинг пройден.", reply_markup=kb)
            await cb.answer()
            return
    quiz_kb = ReplyKeyboardMarkup(keyboard=[[BACK_BTN]], resize_keyboard=True)
    await cb.message.answer("📝 Начинаем квиз:", reply_markup=quiz_kb)
    await cb.message.answer(f"1. {qs[0].question}")
    await state.update_data(quiz_questions=qs, quiz_index=0, correct=0)
    await state.set_state(Quiz.waiting_answer)
    await cb.answer()


@dp.chat_member()
async def on_user_join(event: ChatMemberUpdated):
    if not event.old_chat_member:
        return
    user = event.new_chat_member.user
    old_status = event.old_chat_member.status
    if old_status in ("left", "kicked") and event.new_chat_member.status == "member":
        with get_session() as db:
            emp = db.query(Employee).filter_by(telegram_id=user.id).first()
            if emp and emp.is_active and emp.training_passed and not emp.greeted:
                await bot.send_message(event.chat.id,
                                       f"🎉 Привет, {html.escape(emp.name)}! Добро пожаловать в нашу группу 😊")
                emp.greeted = True
                db.commit()


@dp.message(Quiz.waiting_answer)
async def process_quiz(msg: Message, state: FSMContext):
    data = await state.get_data()
    qs, idx, correct = data["quiz_questions"], data["quiz_index"], data["correct"]
    if msg.text.strip().lower() == qs[idx].answer.lower(): correct += 1
    idx += 1
    if idx < len(qs):
        await state.update_data(quiz_index=idx, correct=correct)
        await msg.answer(f"{idx + 1}. {qs[idx].question}")
    else:
        total = len(qs)
        with get_session() as db:
            emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
            kb = admin_kb if emp.role == "Admin" else employee_main_kb
            if correct >= total * 0.7:
                emp.training_passed = True
                db.commit()
                await msg.answer(f"🎉 Поздравляем! Вы успешно прошли квиз ({correct}/{total}).", reply_markup=kb)
            else:
                await msg.answer(f"😔 Вы не прошли квиз ({correct}/{total}). Предлагаем пройти тренинг снова 🏃‍♂️",
                                 reply_markup=training_kb)
        await state.clear()


@dp.message(F.text == "🧠 База знаний")
async def show_topics(msg: Message):
    with get_session() as db:
        topics = db.query(Topic).all()
    if not topics:
        await msg.answer("База знаний пока пуста.")
        return
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t.title, callback_data=f"topic:{t.id}")] for t in topics] + [
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]])
    await msg.answer("📚 Выберите тему:", reply_markup=kb)


@dp.callback_query(F.data.startswith("topic:"))
async def send_topic(cb: CallbackQuery):
    """
    Этот обработчик отправляет пользователю содержимое выбранной темы из Базы Знаний.
    Он умеет отправлять как простой текст, так и фото с подписью, если в БД указан путь к файлу.
    """
    # 1. Получаем ID темы из callback-данных
    tid = int(cb.data.split(":")[1])

    # 2. Достаем тему из базы данных
    with get_session() as db:
        t = db.query(Topic).get(tid)

    # 3. Проверяем, найдена ли тема
    if not t:
        await cb.answer("Тема не найдена.", show_alert=True)
        return

    # 4. Удаляем предыдущее сообщение со списком тем, чтобы избежать "зависания"
    await cb.message.delete()

    # 5. Проверяем, есть ли у темы прикрепленное изображение
    if t.image_path:
        # Если да - отправляем фото с текстом в качестве подписи
        try:
            await bot.send_photo(
                chat_id=cb.from_user.id,
                photo=FSInputFile(t.image_path), # Загружаем фото с диска
                caption=t.content # Используем основной контент как подпись
            )
        except Exception as e:
            # Обработка ошибки, если файл не найден или возникла другая проблема
            logger.error(f"Не удалось отправить фото {t.image_path} для темы '{t.title}': {e}")
            await bot.send_message(cb.from_user.id, f"Произошла ошибка при загрузке изображения для темы «{t.title}». Обратитесь к администратору.")
            # Все равно покажем кнопку "Назад"
    else:
        # Если изображения нет - просто отправляем текст
        await bot.send_message(
            chat_id=cb.from_user.id,
            text=t.content
        )

    # 6. Отправляем новое сообщение с кнопкой для возврата к списку тем
    await bot.send_message(
        chat_id=cb.from_user.id,
        text="Выберите следующее действие:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 К темам", callback_data="back_to_topics")]
            ]
        )
    )

    # 7. Отвечаем на callback, чтобы у пользователя пропали "часики" на кнопке
    await cb.answer()


@dp.callback_query(F.data == "back_to_topics")
async def back_to_topics(cb: CallbackQuery):
    with get_session() as db:
        topics = db.query(Topic).all()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t.title, callback_data=f"topic:{t.id}")] for t in topics] + [
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]])
    await cb.message.edit_text("📚 Выберите тему:", reply_markup=kb)
    await cb.answer()


scheduler = AsyncIOScheduler(timezone="Asia/Almaty")


@scheduler.scheduled_job("cron", hour=9, minute=0)
async def birthday_jobs():
    today_date = datetime.now().date()
    with get_session() as db:
        emps = db.query(Employee).filter(func.strftime("%m-%d", Employee.birthday) == today_date.strftime("%m-%d"),
                                         Employee.is_active == True).all()
    for emp in emps:
        try:
            await bot.send_message(chat_id=COMMON_CHAT_ID,
                                   text=f"🎂 Сегодня у {html.escape(emp.name)} ({html.escape(emp.role)}) день рождения! Поздравляем! 🎉")
        except Exception as e:
            logger.error(f"Failed to send birthday greeting for {emp.name}: {e}")


# ...

# — Запуск —
async def main():
    scheduler.start()
    logger.info("Bot starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())