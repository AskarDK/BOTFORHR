#!/usr/bin/env python3
import os
import asyncio
import logging
import html
from datetime import datetime, date
from math import radians, sin, cos, sqrt, atan2
from sqlalchemy.exc import IntegrityError

import aiohttp # <-- ДОБАВЛЕНО
from aiogram import Bot, Dispatcher, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ChatAction
from aiogram.filters import Command, StateFilter
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
from dotenv import load_dotenv
from sqlalchemy import func  # остальное здесь не нужно

from aiogram.enums import ChatType, ChatMemberStatus
from aiogram.types import ChatMemberUpdated
from aiogram.enums import ContentType
from aiogram.types import ReplyKeyboardRemove


# ИЗ models ИМПОРТИРУЕМ GroupChat (лучше не дублировать модель)
from models import (
    Employee, RoleGuide, BotText, OnboardingQuestion, EmployeeCustomData, OnboardingStep,
    Attendance, RegCode, Event, Idea, QuizQuestion, Topic, RoleOnboarding,
    ArchivedEmployee, ArchivedAttendance, ArchivedIdea,
    GroupChat, get_session
)


# — Загрузка .env —
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
DATABASE_FILE = DATABASE_URL.replace("sqlite:///", "")
_common = os.getenv("COMMON_CHAT_ID")
try:
    COMMON_CHAT_ID = int(_common) if _common else None
except ValueError:
    COMMON_CHAT_ID = None
OFFICE_LAT = float(os.getenv("OFFICE_LAT", "43.231518"))
OFFICE_LON = float(os.getenv("OFFICE_LON", "76.882392"))
OFFICE_RADIUS_METERS = int(os.getenv("OFFICE_RADIUS_METERS", "300"))
UPLOAD_FOLDER_ONBOARDING = 'uploads/onboarding'
# -- Переменные для погоды --
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_CITY = os.getenv("WEATHER_CITY", "Almaty") # Город по умолчанию - Алматы

# — Логирование —
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# — Инициализация бота и диспетчера —
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()



def initialize_bot_texts():
    """Проверяет и создает тексты для бота по умолчанию, если они отсутствуют."""
    texts_to_ensure = {
        "quiz_success_message": {
            "text": "🎉 Поздравляем, {name}! Вы успешно прошли квиз ({correct}/{total})!",
            "description": "Сообщение после успешного прохождения квиза. Доступные переменные: {name}, {correct}, {total}."
        },
        "group_join_success_message": {
            "text": "Отлично, мы видим, что вы уже в нашем общем чате! Добро пожаловать в команду, теперь вам доступен весь функционал. 🎉",
            "description": "Сообщение, если пользователь прошел квиз и уже состоит в общем чате."
        },
        "group_join_prompt_message": {
            "text": "Остался последний шаг — вступите в наш основной рабочий чат, чтобы быть в курсе всех событий: {group_link}",
            "description": "Сообщение, если пользователь прошел квиз, но еще не в общем чате. ВАЖНО: вручную замените {group_link} на реальную ссылку-приглашение в чат."
        },
        "welcome_to_common_chat": {
            "text": "👋 Встречайте нового коллегу! {user_mention} ({user_name}) присоединился к нашему чату. Добро пожаловать в команду! 🎉",
            "description": "Сообщение в общем чате при вступлении нового сотрудника. Доступные переменные: {user_mention}, {user_name}."
        }

    }
    # ... (остальная логика)
    with get_session() as db:
        for key, data in texts_to_ensure.items():
            existing = db.get(BotText, key)
            if not existing:
                db.add(BotText(id=key, text=data['text'], description=data['description']))
        db.commit()

# Вызываем функцию инициализации один раз при запуске приложения
initialize_bot_texts()
# --- КОНЕЦ НОВОГО БЛОКА ---

# — FSM States —
class Reg(StatesGroup):
    waiting_code = State()
    waiting_for_status = State() # <-- ДОБАВЛЕНО

class Onboarding(StatesGroup):
    awaiting_answer = State()


class Training(StatesGroup):
    waiting_ack = State()


class Quiz(StatesGroup):
    waiting_answer = State()


class AdminAdd(StatesGroup):
    email = State();
    role = State();
    name = State();
    birthday = State()


class AdminFindID(StatesGroup):
    waiting_id = State()


class AdminAttendance(StatesGroup):
    waiting_employee_id = State();
    waiting_date = State()


class AddEvent(StatesGroup):
    waiting_title = State();
    waiting_description = State();
    waiting_date = State()


class SubmitIdea(StatesGroup):
    waiting_for_idea = State()

class EditProfile(StatesGroup):
    choosing_field = State()      # Ожидание выбора поля для редактирования
    waiting_for_new_value = State() # Ожидание нового значения (текст или фото)

class FindEmployee(StatesGroup):
    waiting_for_name = State()

class TimeTracking(StatesGroup):
    waiting_location = State()

# — Кнопки и клавиатуры —
BACK_BTN = KeyboardButton(text="🔙 Назад")
# ЗАМЕНИТЕ СТАРЫЙ БЛОК КЛАВИАТУР НА ЭТОТ

# Клавиатура для под-меню учета времени
# — Клавиатура для под-меню учета времени (без сразу отправки локации)
time_tracking_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Я на месте"),
            KeyboardButton(text="👋 Я ухожу")
        ],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)


# Обновленная основная клавиатура для сотрудника
employee_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏰ Учет времени")],  # <-- Новая общая кнопка
        [KeyboardButton(text="🎉 Посмотреть ивенты"), KeyboardButton(text="💡 Поделиться идеей")],
        [KeyboardButton(text="👥 Наши сотрудники"), KeyboardButton(text="🧠 База знаний")],
        [KeyboardButton(text="📊 Мой профиль")]
    ],
    resize_keyboard=True
)

# Обновленная клавиатура для админа (для единообразия)
admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить сотрудника"), KeyboardButton(text="Список сотрудников")],
        [KeyboardButton(text="Добавить ивент"), KeyboardButton(text="Просмотр идей")],
        [KeyboardButton(text="⏰ Учет времени"), KeyboardButton(text="Посещаемость сотрудника")], # <-- Добавлена сюда
        [KeyboardButton(text="👥 Наши сотрудники"), KeyboardButton(text="🧠 База знаний")],
        [KeyboardButton(text="📊 Мой профиль")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора статуса сотрудника
employee_status_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Я новенький")],
        [KeyboardButton(text="Я действующий сотрудник")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Остальные клавиатуры (training_kb, quiz_start_kb и т.д.) остаются без изменений
training_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🏃‍♂️ Пройти тренинг")]], resize_keyboard=True
)
quiz_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Готов!", callback_data="quiz_start")]])
ack_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="✅ Ознакомился", callback_data="training_done")]])
PAGE_SIZE = 5


# --- Вспомогательные функции ---

def get_text(key: str, default: str = "Текст не найден") -> str:
    """Получает текст для бота из БД по ключу."""
    with get_session() as db:
        text_obj = db.get(BotText, key)
        return text_obj.text if text_obj else default


def access_check(func):
    """Декоратор, который проверяет, прошел ли пользователь тренинг."""

    async def wrapper(message_or_cb: Message | CallbackQuery, state: FSMContext, *args, **kwargs):
        user_id = message_or_cb.from_user.id
        with get_session() as db:
            emp = db.query(Employee).filter_by(telegram_id=user_id).first()

        if not emp or not emp.is_active:
            await func(message_or_cb, state, *args, **kwargs)
            return

        if emp.training_passed:
            await func(message_or_cb, state, *args, **kwargs)
        else:
            if isinstance(message_or_cb, CallbackQuery):
                await message_or_cb.answer(
                    get_text("access_denied_training_required_alert", "Сначала завершите тренинг!"), show_alert=True)
            else:
                await message_or_cb.answer(
                    get_text("access_denied_training_required",
                             "Пожалуйста, завершите тренинг для доступа к функциям."),
                    reply_markup=training_kb
                )

    return wrapper


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# --- Основная логика: Регистрация и Онбординг ---
# --- НОВЫЙ ХЕНДЛЕР: бот стал админом/покинул чат и т.п. ---

@dp.my_chat_member()
async def on_bot_membership_change(event: ChatMemberUpdated):
    # Интересуют только группы/супергруппы
    if event.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return

    chat_id = event.chat.id
    chat_title = event.chat.title or str(chat_id)
    new_status = event.new_chat_member.status

    with get_session() as db:
        # Если бот стал админом → запоминаем чат
        if new_status == ChatMemberStatus.ADMINISTRATOR:
            gc = db.query(GroupChat).filter_by(chat_id=chat_id).first()
            if not gc:
                db.add(GroupChat(name=chat_title, chat_id=chat_id))
            else:
                gc.name = chat_title  # на случай переименования
            db.commit()

        # Если бот больше не админ/вышел/его кикнули → удаляем из списка
        if new_status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED, ChatMemberStatus.MEMBER):
            # MEMBER = просто участник, нам нужен именно админ
            gc = db.query(GroupChat).filter_by(chat_id=chat_id).first()
            if gc:
                db.delete(gc)
                db.commit()

@dp.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()

    if emp and emp.registered:
        if not emp.is_active:
            await msg.answer(get_text("account_deactivated", "Ваш аккаунт деактивирован."))
            return

        if emp.training_passed:
            kb = admin_kb if emp.role == "Admin" else employee_main_kb
            await msg.answer(get_text("welcome_back", "С возвращением, {name}!").format(name=emp.name), reply_markup=kb)
        elif emp.onboarding_completed:
            await msg.answer(
                get_text("training_not_passed_prompt", "Привет! Остался последний шаг - пройдите тренинг."),
                reply_markup=training_kb
            )
        else:
            await msg.answer(
                get_text("onboarding_not_finished", "Похоже, вы не закончили знакомство. Давайте продолжим!"))
            await run_onboarding(msg.from_user.id, state)
    else:
        await msg.answer(
            get_text("enter_reg_code", "Пожалуйста, введите ваш 8-значный регистрационный код:"),
            reply_markup=ReplyKeyboardMarkup(keyboard=[[BACK_BTN]], resize_keyboard=True)
        )
        await state.set_state(Reg.waiting_code)

@dp.message(Reg.waiting_code)
async def process_code(msg: Message, state: FSMContext):
    if msg.text == "🔙 Назад":
        await state.clear()
        await msg.answer("Регистрация отменена.")
        return

    code = msg.text.strip()
    with get_session() as db:
        rc = db.query(RegCode).filter_by(code=code, used=False).first()
        if not rc:
            await msg.answer("❌ Код не найден или уже использован. Пожалуйста, попробуйте ещё раз.")
            return

        emp = db.query(Employee).filter_by(email=rc.email).first()
        if not emp or not emp.is_active:
            await msg.answer("❌ Ваш аккаунт был деактивирован. Регистрация невозможна.")
            await state.clear()
            return

        emp.telegram_id = msg.from_user.id
        emp.registered = True
        rc.used = True
        db.commit()

    # Задаем вопрос о статусе
    await msg.answer(
        "Код принят! 🎉\n\nПожалуйста, выберите ваш статус:",
        reply_markup=employee_status_kb
    )
    await state.set_state(Reg.waiting_for_status)

@dp.message(Reg.waiting_for_status, F.text.in_({"Я новенький", "Я действующий сотрудник"}))
async def process_employee_status(msg: Message, state: FSMContext):
    if msg.text == "Я новенький":
        await msg.answer(get_text("lets_get_acquainted", "Отлично, давайте познакомимся!"),
                         reply_markup=ReplyKeyboardRemove())
        await run_onboarding(msg.from_user.id, state)
        return

    # "Я действующий сотрудник"
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        emp.onboarding_completed = True
        emp.training_passed = True
        db.commit()

        kb = admin_kb if emp.role == "Admin" else employee_main_kb
        await msg.answer(
            get_text("welcome_existing_employee",
                     "С возвращением! Все функции бота теперь доступны для вас.").format(name=emp.name),
            reply_markup=kb
        )
    await state.clear()


async def run_onboarding(user_id: int, state: FSMContext):
    """Главная функция, управляющая сбором данных при онбординге."""
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=user_id).first()
        answered_keys_rows = db.query(EmployeeCustomData.data_key).filter_by(employee_id=emp.id).all()
        answered_keys = [key for (key,) in answered_keys_rows]

        next_question = db.query(OnboardingQuestion).filter(
            OnboardingQuestion.role == emp.role,
            ~OnboardingQuestion.data_key.in_(answered_keys)
        ).order_by(OnboardingQuestion.order_index).first()

    if next_question:
        await bot.send_message(user_id, next_question.question_text)
        await state.set_state(Onboarding.awaiting_answer)
        await state.update_data(current_question_id=next_question.id)
    else:
        await run_company_introduction(user_id, state)


@dp.message(Onboarding.awaiting_answer)
async def process_onboarding_answer(msg: Message, state: FSMContext):
    """Обрабатывает ответы на кастомные вопросы."""
    data = await state.get_data()
    question_id = data.get("current_question_id")
    answer_text = msg.text

    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        question = db.get(OnboardingQuestion, question_id)

        db.add(EmployeeCustomData(employee_id=emp.id, data_key=question.data_key, data_value=answer_text))

        if question.data_key == 'name':
            emp.name = answer_text
        elif question.data_key == 'birthday':
            try:
                emp.birthday = datetime.strptime(answer_text, "%d.%m.%Y").date()
            except ValueError:
                await msg.answer("Неверный формат даты. Попробуйте еще раз в формате ДД.ММ.ГГГГ.")
                return
        elif question.data_key == 'contact_info':
            emp.contact_info = answer_text

        db.commit()

    await run_onboarding(msg.from_user.id, state)


async def run_company_introduction(user_id: int, state: FSMContext):
    """Отправляет серию сообщений-шагов о компании."""
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=user_id).first()
        if not emp.onboarding_completed:
            emp.onboarding_completed = True
            db.commit()

        steps = db.query(OnboardingStep).filter_by(role=emp.role).order_by(OnboardingStep.order_index).all()

    await bot.send_message(user_id, get_text("company_introduction_start", "Отлично! Теперь немного о компании."))
    for step in steps:
        if step.message_text:
            await bot.send_message(user_id, step.message_text)

        if step.file_path and os.path.exists(step.file_path):
            try:
                file_to_send = FSInputFile(step.file_path)

                if step.file_type == 'video_note':
                    async with ChatActionSender(bot=bot, chat_id=user_id, action=ChatAction.RECORD_VIDEO_NOTE):
                        await bot.send_video_note(user_id, file_to_send)
                elif step.file_type == 'video':  # <-- ДОБАВЛЕН БЛОК ДЛЯ ОБЫЧНОГО ВИДЕО
                    async with ChatActionSender(bot=bot, chat_id=user_id, action=ChatAction.UPLOAD_VIDEO):
                        await bot.send_video(user_id, file_to_send)
                elif step.file_type == 'photo':
                    async with ChatActionSender(bot=bot, chat_id=user_id, action=ChatAction.UPLOAD_PHOTO):
                        await bot.send_photo(user_id, file_to_send)
                elif step.file_type == 'document':
                    async with ChatActionSender(bot=bot, chat_id=user_id, action=ChatAction.UPLOAD_DOCUMENT):
                        await bot.send_document(user_id, file_to_send)
            except Exception as e:
                logger.error(f"Failed to send file {step.file_path}: {e}")

        await asyncio.sleep(1.5)

    await state.clear()
    await bot.send_message(
        user_id,
        get_text("training_prompt_after_onboarding", "Знакомство завершено! Теперь нужно пройти финальный тренинг."),
        reply_markup=training_kb
    )


# --- Тренинг и квиз ---

@dp.message(F.text == "🏃‍♂️ Пройти тренинг")
async def start_training(msg: Message, state: FSMContext):
    await state.clear()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        if not emp or not emp.is_active: return
        onboarding = db.query(RoleOnboarding).filter_by(role=emp.role).first()

    if onboarding and onboarding.text:
        await msg.answer(onboarding.text, reply_markup=ReplyKeyboardRemove())
        if onboarding.file_path and os.path.exists(onboarding.file_path):
            try:
                file_to_send = FSInputFile(onboarding.file_path)
                if onboarding.file_type == 'video_note':
                    async with ChatActionSender(bot=bot, chat_id=msg.chat.id, action=ChatAction.RECORD_VIDEO_NOTE):
                        await bot.send_video_note(msg.chat.id, file_to_send)
            except Exception as e:
                logger.error(f"Failed to send training file {onboarding.file_path}: {e}")

    else:
        await msg.answer("📚 Материалы для вашего тренинга пока не добавлены.")
    await msg.answer("Нажмите «✅ Ознакомился», когда будете готовы начать квиз.", reply_markup=ack_kb)
    await state.set_state(Training.waiting_ack)


@dp.callback_query(F.data == "training_done")
async def training_done(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await cb.message.answer("✨ Отлично! Теперь давайте проверим знания в квизе.", reply_markup=quiz_start_kb)
    await cb.answer()
    await state.clear()


async def send_quiz_question(chat, question, idx):
    num = idx + 1
    if question.question_type == "choice":
        opts = question.options.split(";")
        buttons = [[InlineKeyboardButton(text=opt, callback_data=f"quiz_ans:{i}")] for i, opt in enumerate(opts)]
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await chat.answer(f"{num}. {question.question}", reply_markup=kb)
    else:
        await chat.answer(f"{num}. {question.question}")


@dp.callback_query(F.data == "quiz_start")
async def on_quiz_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=cb.from_user.id).first()
        qs = db.query(QuizQuestion).filter_by(role=emp.role).order_by(QuizQuestion.order_index).all()

        if not qs:
            emp.training_passed = True
            db.commit()
            kb = admin_kb if emp.role == "Admin" else employee_main_kb
            await cb.message.answer("🎉 Для вашей роли квиза нет — тренинг пройден.", reply_markup=kb)
            await cb.answer()
            return

    await cb.message.answer("📝 Начинаем квиз:")
    await send_quiz_question(cb.message, qs[0], 0)
    await state.update_data(quiz_questions=qs, quiz_index=0, correct=0)
    await state.set_state(Quiz.waiting_answer)
    await cb.answer()


async def finish_quiz(user_id: int, chat_id: int, state: FSMContext, correct: int, total: int):
    """Завершает квиз, проверяет членство в группе и отправляет результат."""
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=user_id).first()
        if not emp:
            # ... (обработка ошибки, если сотрудник не найден)
            return

        is_passed = correct >= total * 0.7
        emp.training_passed = is_passed
        db.commit() # Сохраняем результат квиза

    kb = admin_kb if emp.role == "Admin" else employee_main_kb
    if not is_passed:
        await bot.send_message(chat_id, f"😔 Вы не прошли квиз ({correct}/{total}). Попробуйте снова.",
                               reply_markup=training_kb)
        await state.clear()
        return

    # --- НОВЫЙ БЛОК ПРОВЕРКИ ЧЛЕНСТВА В ГРУППЕ ---
    # Сначала отправляем сообщение об успешном квизе
    quiz_success_text = get_text("quiz_success_message", "🎉 Поздравляем, {name}! Вы успешно прошли квиз ({correct}/{total})!").format(
        name=emp.name, correct=correct, total=total
    )
    await bot.send_message(chat_id, quiz_success_text)

    # Теперь проверяем группу
    chat_id_to_check = COMMON_CHAT_ID
    final_message = ""
    send_main_keyboard = False

    if not chat_id_to_check:
        logger.warning("COMMON_CHAT_ID не установлен. Проверка членства в группе пропущена.")
        final_message = get_text("group_join_success_message")
        send_main_keyboard = True
    else:
        try:
            member = await bot.get_chat_member(chat_id=chat_id_to_check, user_id=user_id)
            if member.status not in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}:
                # Пользователь в группе
                with get_session() as db:
                    emp = db.get(Employee, emp.id)
                    emp.joined_main_chat = True
                    db.commit()
                final_message = get_text("group_join_success_message")
                send_main_keyboard = True
            else:
                final_message = get_text("group_join_prompt_message")
        except Exception as e:
            logger.error(f"Не удалось проверить членство пользователя {user_id} в чате {chat_id_to_check}: {e}")
            # Если произошла ошибка (напр., бот не в чате), отправляем просьбу вступить
            final_message = get_text("group_join_prompt_message")

    # Отправляем финальное сообщение (либо с просьбой, либо с поздравлением)
    await bot.send_message(chat_id, final_message, reply_markup=kb if send_main_keyboard else None)
    await state.clear()

# --- БЛОК ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ ---

# Клавиатура для просмотра профиля
def get_profile_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="profile_edit")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="profile_back")]
    ])


@dp.message(F.text == "📊 Мой профиль")
async def show_profile(msg: Message, state: FSMContext):
    await state.clear()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()

    if not emp:
        await msg.answer("Не удалось найти ваш профиль.")
        return

    # Собираем данные для вывода
    profile_data = [
        f"<b>Имя:</b> {html.escape(emp.name or 'Не указано')}",
        f"<b>Роль:</b> {html.escape(emp.role or 'Не указана')}",
        f"<b>Email:</b> {html.escape(emp.email)}",
        f"<b>Контактная информация:</b> {html.escape(emp.contact_info or 'Не указана')}"
    ]
    caption = "\n".join(profile_data)

    if emp.photo_file_id:
        try:
            await msg.answer_photo(
                photo=emp.photo_file_id,
                caption=caption,
                reply_markup=get_profile_kb()
            )
        except Exception as e:
            logger.error(f"Failed to send photo by file_id for user {emp.id}: {e}")
            await msg.answer(caption, reply_markup=get_profile_kb())
    else:
        await msg.answer(f"📸 У вас пока нет аватара.\n\n{caption}", reply_markup=get_profile_kb())


@dp.callback_query(F.data == "profile_back")
async def process_profile_back(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.clear()
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=cb.from_user.id).first()
    kb = admin_kb if emp and emp.role == "Admin" else employee_main_kb
    await cb.message.answer("Вы в главном меню.", reply_markup=kb)
    await cb.answer()


# Клавиатура для выбора поля для редактирования
def get_edit_profile_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🖼️ Изменить аватар", callback_data="edit_field:photo")],
        [InlineKeyboardButton(text="👤 Изменить имя", callback_data="edit_field:name")],
        [InlineKeyboardButton(text="📞 Изменить контакты", callback_data="edit_field:contact_info")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="edit_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.callback_query(F.data == "profile_edit")
async def start_profile_edit(cb: CallbackQuery, state: FSMContext):
    new_text = "Выберите, что хотите изменить, или отправьте новое фото."
    new_kb = get_edit_profile_kb()

    # --- FIX STARTS HERE ---
    # Check if the message has a photo (and therefore a caption)
    if cb.message.photo:
        await cb.message.edit_caption(caption=new_text, reply_markup=new_kb)
    # Otherwise, it's a regular text message
    else:
        await cb.message.edit_text(new_text, reply_markup=new_kb)
    # --- FIX ENDS HERE ---

    await state.set_state(EditProfile.choosing_field)
    await cb.answer()

@dp.callback_query(F.data == "edit_cancel")
async def cancel_profile_edit(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()
    # Показываем профиль заново
    await show_profile(cb.message, state)
    await cb.answer("Редактирование отменено.")


@dp.callback_query(F.data.startswith("edit_field:"))
async def choose_field_to_edit(cb: CallbackQuery, state: FSMContext):
    field_to_edit = cb.data.split(":")[1]

    prompts = {
        "photo": "📸 Отправьте мне новое фото для аватара.",
        "name": "👤 Введите ваше новое имя.",
        "contact_info": "📞 Введите новую контактную информацию (например, номер телефона)."
    }

    await state.update_data(field_to_edit=field_to_edit)
    await state.set_state(EditProfile.waiting_for_new_value)

    await cb.message.answer(prompts.get(field_to_edit, "Введите новое значение:"))
    await cb.answer()


@dp.message(EditProfile.waiting_for_new_value, F.photo)
async def handle_new_photo(msg: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("field_to_edit") != "photo":
        await msg.answer("Сейчас я ожидаю текстовое значение. Чтобы сменить фото, нажмите кнопку 'Изменить аватар'.")
        return

    photo_file_id = msg.photo[-1].file_id
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        emp.photo_file_id = photo_file_id
        db.commit()

    await msg.answer("✅ Аватар успешно обновлен!")
    await state.clear()
    # Показываем обновленный профиль
    await show_profile(msg, state)


@dp.message(EditProfile.waiting_for_new_value, F.text)
async def handle_new_text_value(msg: Message, state: FSMContext):
    data = await state.get_data()
    field_to_edit = data.get("field_to_edit")

    if not field_to_edit or field_to_edit == "photo":
        await msg.answer("Неверное действие. Выберите поле для редактирования с помощью кнопок.")
        return

    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        setattr(emp, field_to_edit, msg.text)
        db.commit()

    await msg.answer(f"✅ Поле '{field_to_edit}' успешно обновлено!")
    await state.clear()
    # Показываем обновленный профиль
    await show_profile(msg, state)

@dp.message(Quiz.waiting_answer)
async def process_text_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    qs, idx, correct = data["quiz_questions"], data["quiz_index"], data["correct"]
    q = qs[idx]
    if q.question_type == "choice": return

    if msg.text.strip().lower() == q.answer.strip().lower():
        correct += 1

    idx += 1
    if idx < len(qs):
        await state.update_data(quiz_index=idx, correct=correct)
        await send_quiz_question(msg, qs[idx], idx)
    else:
        await finish_quiz(user_id=msg.from_user.id, chat_id=msg.chat.id, state=state, correct=correct, total=len(qs))


@dp.callback_query(Quiz.waiting_answer, F.data.startswith("quiz_ans:"))
async def process_choice_answer(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    data = await state.get_data()
    qs, idx, correct = data["quiz_questions"], data["quiz_index"], data["correct"]
    q = qs[idx]

    sel = int(cb.data.split(":", 1)[1])
    opts = q.options.split(";")
    user_ans = opts[sel]

    if user_ans.strip().lower() == q.answer.strip().lower():
        correct += 1

    idx += 1
    if idx < len(qs):
        await state.update_data(quiz_index=idx, correct=correct)
        await send_quiz_question(cb.message, qs[idx], idx)
    else:
        await finish_quiz(user_id=cb.from_user.id, chat_id=cb.message.chat.id, state=state, correct=correct, total=len(qs))
    await cb.answer()

@dp.message(TimeTracking.waiting_location, F.text == "🔙 Назад")
@access_check
async def cancel_time_tracking(msg: Message, state: FSMContext, **kwargs):
    # Сбрасываем состояние
    await state.clear()
    # Восстанавливаем главное меню
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
    kb = admin_kb if emp and emp.role == "Admin" else employee_main_kb
    await msg.answer("⏹️ Учет времени отменён.", reply_markup=kb)

@dp.message(F.text == "⏰ Учет времени")
@access_check
async def show_time_tracking_menu(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=time_tracking_kb)



@dp.message(F.text == "✅ Я на месте")
@access_check
async def ask_arrival(msg: Message, state: FSMContext, **kwargs):
    await state.update_data(tracking="arrival")
    await state.set_state(TimeTracking.waiting_location)
    await msg.answer(
        "Отлично! Теперь отправьте мне вашу геолокацию или нажмите «🔙 Назад»:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📍 Отправить локацию", request_location=True)],
                [KeyboardButton(text="🔙 Назад")]
            ],
            resize_keyboard=True
        )
    )


@dp.message(F.text == "👋 Я ухожу")
@access_check
async def ask_departure(msg: Message, state: FSMContext, **kwargs):
    await state.update_data(tracking="departure")
    await state.set_state(TimeTracking.waiting_location)
    await msg.answer(
        "Хорошо! Отправьте, пожалуйста, геолокацию или нажмите «🔙 Назад»:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📍 Отправить локацию", request_location=True)],
                [KeyboardButton(text="🔙 Назад")]
            ],
            resize_keyboard=True
        )
    )


@dp.message(F.content_type == ContentType.LOCATION)
@access_check
async def process_time_tracking(msg: Message, state: FSMContext, **kwargs):
    data = await state.get_data()
    kind = data.get("tracking")
    await state.clear()

    distance = haversine(
        msg.location.latitude, msg.location.longitude,
        OFFICE_LAT, OFFICE_LON
    )
    if distance > OFFICE_RADIUS_METERS:
        return await msg.answer(f"❌ Слишком далеко от офиса ({int(distance)} м).")

    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=msg.from_user.id).first()
        today = date.today()
        now = datetime.now().time()

        # берём запись за сегодня или создаём
        rec = db.query(Attendance).filter_by(employee_id=emp.id, date=today).first()
        if not rec:
            rec = Attendance(employee_id=emp.id, date=today)

            # на случай гонки: пытаемся вставить, если пара уже существует — перезагрузим
            db.add(rec)
            try:
                db.flush()  # без коммита
            except IntegrityError:
                db.rollback()
                rec = db.query(Attendance).filter_by(employee_id=emp.id, date=today).first()

        if kind == "arrival":
            if rec.arrival_time:
                resp = "🤔 Уже отмечали приход сегодня."
            else:
                rec.arrival_time = now
                db.commit()
                resp = f"✅ Приход зафиксирован в {now.strftime('%H:%M:%S')}."
        else:
            if not rec.arrival_time:
                resp = "🤔 Сначала отметьте приход."
            elif rec.departure_time:
                resp = "🤔 Уже отмечали уход сегодня."
            else:
                rec.departure_time = now
                db.commit()
                resp = f"👋 Уход зафиксирован в {now.strftime('%H:%M:%S')}."

        kb = admin_kb if emp.role == "Admin" else employee_main_kb
        await msg.answer(resp, reply_markup=kb)

@dp.message(F.text == "🎉 Посмотреть ивенты")
@access_check
async def view_events(msg: Message, state: FSMContext, **kwargs):
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


@dp.message(F.text == "💡 Поделиться идеей")
@access_check
async def share_idea_start(msg: Message, state: FSMContext, **kwargs):
    await msg.answer("Напишите вашу идею или предложение. Администрация обязательно рассмотрит его.",
                     reply_markup=ReplyKeyboardMarkup(keyboard=[[BACK_BTN]], resize_keyboard=True))
    await state.set_state(SubmitIdea.waiting_for_idea)


# bot.py - CORRECTED

@dp.message(SubmitIdea.waiting_for_idea)
async def process_idea(msg: Message, state: FSMContext, **kwargs):
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

        # This now correctly uses 'idea_text'
        new_idea = Idea(employee_id=emp.id, text=msg.text)
        db.add(new_idea)
        db.commit()

    kb = admin_kb if emp and emp.role == "Admin" else employee_main_kb
    await msg.answer("Спасибо! Ваша идея принята.", reply_markup=kb)
    await state.clear()

    # --- (отключено как дубль; используется новая версия ниже) ---




# --- Админские функции (не требуют декоратора, т.к. доступны только админам, которые уже прошли тренинг) ---
@dp.message(F.text == "Добавить ивент")
async def admin_add_event_start(msg: Message, state: FSMContext):
    # (Код без изменений)
    pass


# ... и так далее для всех админских функций

@dp.message(F.text == "Просмотр идей")
async def view_ideas(msg: Message):
    # (Код без изменений)
    pass


# --- Фоновые задачи ---

scheduler = AsyncIOScheduler(timezone="Asia/Almaty")

@scheduler.scheduled_job("cron", hour=7, minute=30)
async def send_daily_weather():
    if not WEATHER_API_KEY:
        logger.warning("WEATHER_API_KEY не задан. Рассылка погоды пропущена.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    weather_text = ""

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    temp = round(data['main']['temp'])
                    feels_like = round(data['main']['feels_like'])
                    description = data['weather'][0]['description'].capitalize()
                    wind_speed = round(data['wind']['speed'])

                    weather_text = (
                        f"☀️ <b>Доброе утро! Погода в г. {WEATHER_CITY} на сегодня:</b>\n\n"
                        f"🌡️ Температура: <b>{temp}°C</b> (ощущается как {feels_like}°C)\n"
                        f"📝 На небе: {description}\n"
                        f"💨 Ветер: {wind_speed} м/с\n\n"
                        f"Хорошего дня!"
                    )
                else:
                    logger.error(f"Ошибка получения погоды: {resp.status}")
                    return
    except Exception as e:
        logger.error(f"Исключение при запросе погоды: {e}")
        return

    with get_session() as db:
        users_to_notify = db.query(Employee.telegram_id).filter(
            Employee.is_active == True,
            Employee.telegram_id != None
        ).all()

    for (user_id,) in users_to_notify:
        try:
            await bot.send_message(user_id, weather_text)
        except Exception as e:
            logger.warning(f"Не удалось отправить погоду пользователю {user_id}: {e}")
        await asyncio.sleep(0.1)

@scheduler.scheduled_job("cron", hour=9, minute=00)
async def birthday_jobs():
    if COMMON_CHAT_ID is None:
        logger.warning("COMMON_CHAT_ID не задан. Рассылка поздравлений пропущена.")
        return

    from sqlalchemy.engine.url import make_url
    from sqlalchemy import text

    today_md = datetime.now().strftime("%m-%d")
    engine_url = make_url(os.getenv("DATABASE_URL", "sqlite:///bot.db"))

    with get_session() as db:
        if engine_url.get_backend_name().startswith("postgres"):
            emps = db.query(Employee).filter(
                text("to_char(birthday, 'MM-DD') = :md and is_active = true")
            ).params(md=today_md).all()
        else:
            from sqlalchemy import func
            emps = db.query(Employee).filter(
                func.strftime("%m-%d", Employee.birthday) == today_md,
                Employee.is_active == True
            ).all()


    greeting_template = get_text("birthday_greeting", "🎂 Сегодня у {name} ({role}) день рождения! Поздравляем! 🎉")
    for emp in emps:
        try:
            await bot.send_message(
                chat_id=COMMON_CHAT_ID,
                text=greeting_template.format(name=html.escape(emp.name or ""), role=html.escape(emp.role or "")),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Failed to send birthday greeting for {emp.name}: {e}")


# НОВЫЙ И УЛУЧШЕННЫЙ БЛОК "НАШИ СОТРУДНИКИ"
# Вставьте этот код в ваш файл, заменив старый блок

# --- Клавиатуры для нового функционала ---
def get_employees_menu_kb() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с выбором: поиск или просмотр по отделам."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗂 По отделам", callback_data="browse_by_role")],
        [InlineKeyboardButton(text="🔎 Поиск по имени", callback_data="search_by_name")],
    ])


# --- Главный обработчик команды "Наши сотрудники" ---
@dp.message(F.text == "👥 Наши сотрудники")
@access_check
async def show_employees_main_menu(msg: Message, state: FSMContext, **kwargs):
    """Отправляет стартовое меню для раздела сотрудников."""
    await state.clear()
    await msg.answer(
        "Как вы хотите найти сотрудника?",
        reply_markup=get_employees_menu_kb()
    )


# --- Ветвь 1: Поиск по имени ---
@dp.callback_query(F.data == "search_by_name")
async def start_employee_search(cb: CallbackQuery, state: FSMContext):
    """Запрашивает у пользователя имя для поиска."""
    await state.set_state(FindEmployee.waiting_for_name)
    await cb.message.edit_text(
        "Введите имя или фамилию сотрудника для поиска.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            # Кнопка для возврата в главное меню сотрудников
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_employees_menu")]
        ])
    )
    await cb.answer()


@dp.message(FindEmployee.waiting_for_name, F.text)
async def process_employee_search(msg: Message, state: FSMContext):
    """Обрабатывает введенное имя, ищет в БД и выводит результат."""
    await state.clear()
    query = msg.text.strip()
    with get_session() as db:
        # Ищем всех активных сотрудников, чье имя содержит введенный текст (без учета регистра)
        found_employees = db.query(Employee).filter(
            Employee.name.ilike(f'%{query}%'),
            Employee.is_active == True
        ).all()

    if not found_employees:
        await msg.answer(
            f"😔 Сотрудники с именем '{html.escape(query)}' не найдены.",
            reply_markup=get_employees_menu_kb()  # Даем возможность попробовать еще раз
        )
        return

    # Формируем клавиатуру с кнопками-результатами
    buttons = [
        [InlineKeyboardButton(text=emp.name, callback_data=f"view_employee:{emp.id}")]
        for emp in found_employees
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Назад к выбору", callback_data="back_to_employees_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await msg.answer(f"<b>🔎 Результаты поиска по запросу '{html.escape(query)}':</b>", reply_markup=kb)


# --- Ветвь 2: Просмотр по отделам ---
@dp.callback_query(F.data == "browse_by_role")
async def browse_by_role(cb: CallbackQuery):
    """Вызывает уже существующую функцию для показа списка отделов."""
    # `send_roles_page` из вашего кода отлично подходит для этого шага
    await send_roles_page(chat_id=cb.message.chat.id, message_id=cb.message.message_id)
    await cb.answer()


# Переименованная и улучшенная функция для показа сотрудников отдела в виде кнопок
async def send_employee_buttons_by_role(chat_id: int, message_id: int, role: str, page: int = 0):
    with get_session() as db:
        offset = page * PAGE_SIZE
        employees_on_page = db.query(Employee).filter(
            Employee.role == role, Employee.is_active == True
        ).offset(offset).limit(PAGE_SIZE).all()
        total_employees = db.query(func.count(Employee.id)).filter(
            Employee.role == role, Employee.is_active == True
        ).scalar()

    text = f"<b>Сотрудники отдела '{html.escape(role)}' (Стр. {page + 1}):</b>"

    # Кнопки с именами сотрудников
    buttons = [
        [InlineKeyboardButton(text=emp.name, callback_data=f"view_employee:{emp.id}")]
        for emp in employees_on_page
    ]

    # Кнопки пагинации
    pagination_row = []
    if page > 0:
        pagination_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"role_page:{role}:{page - 1}"))
    if (page + 1) * PAGE_SIZE < total_employees:
        pagination_row.append(InlineKeyboardButton(text="➡️", callback_data=f"role_page:{role}:{page + 1}"))

    if pagination_row:
        buttons.append(pagination_row)

    # Кнопка возврата к списку всех отделов
    buttons.append([InlineKeyboardButton(text="🔙 Назад к отделам", callback_data="back_to_roles")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=kb)

@dp.callback_query(F.data == "back_to_kb_main_menu")
async def back_to_kb_main_menu_handler(cb: CallbackQuery):
    """
    Возвращает пользователя в главное меню Базы Знаний (выбор между Статьями и Регламентами).
    """
    await cb.message.edit_text(
        "Выберите раздел Базы Знаний:",
        reply_markup=get_kb_menu_kb()
    )
    await cb.answer()

# Обработчик нажатия на отдел (запускает показ сотрудников этого отдела)
@dp.callback_query(F.data.startswith("role_select:"))
async def handle_role_select(cb: CallbackQuery):
    _, role, page_str = cb.data.split(":")
    await send_employee_buttons_by_role(cb.message.chat.id, cb.message.message_id, role, int(page_str))
    await cb.answer()


# Обработчик переключения страниц со списком сотрудников отдела
@dp.callback_query(F.data.startswith("role_page:"))
async def handle_employee_page_switch(cb: CallbackQuery):
    _, role, page_str = cb.data.split(":")
    await send_employee_buttons_by_role(cb.message.chat.id, cb.message.message_id, role, int(page_str))
    await cb.answer()


# --- Общая часть: Просмотр профиля сотрудника ---
@dp.callback_query(F.data.startswith("view_employee:"))
async def show_employee_profile(cb: CallbackQuery, state: FSMContext):
    """Показывает подробную карточку сотрудника с фото и контактами."""
    await state.clear()
    employee_id = int(cb.data.split(":")[1])

    with get_session() as db:
        emp = db.get(Employee, employee_id)

    if not emp:
        await cb.answer("Не удалось найти сотрудника.", show_alert=True)
        return

    # Собираем инфо для подписи
    profile_text = [
        f"<b>Имя:</b> {html.escape(emp.name or 'Не указано')}",
        f"<b>Роль:</b> {html.escape(emp.role or 'Не указана')}",
        f"<b>Email:</b> {html.escape(emp.email)}",
        f"<b>Контакт:</b> {html.escape(emp.contact_info or 'Не указан')}"
    ]
    caption = "\n".join(profile_text)

    # Собираем кнопки
    buttons = []
    if emp.telegram_id:  # Кнопка "Связаться" появится только если у юзера есть telegram_id
        buttons.append([InlineKeyboardButton(text="💬 Связаться в Telegram", url=f"tg://user?id={emp.telegram_id}")])

    # Кнопка назад, которая вернет в главное меню сотрудников
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_employees_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    # Удаляем предыдущее сообщение, чтобы чат был чище
    await cb.message.delete()

    if emp.photo_file_id:
        # Отправляем фото с подписью, если оно есть
        await cb.message.answer_photo(photo=emp.photo_file_id, caption=caption, reply_markup=kb)
    else:
        # Отправляем текст, если фото нет
        await cb.message.answer(f"📸 Аватар не установлен.\n\n{caption}", reply_markup=kb)

    await cb.answer()


# bot.py - ИСПРАВЛЕННАЯ ВЕРСИЯ

@dp.callback_query(F.data == "back_to_employees_menu")
async def back_to_employees_menu(cb: CallbackQuery, state: FSMContext):
    """Возвращает пользователя в главное меню раздела 'Наши сотрудники'."""
    await state.clear()

    # 1. Сначала удаляем предыдущее сообщение (с фото или без)
    await cb.message.delete()

    # 2. Затем отправляем новое чистое сообщение с меню
    await cb.message.answer(
        "Как вы хотите найти сотрудника?",
        reply_markup=get_employees_menu_kb()
    )

    # Не забываем ответить на callback, чтобы убрать "часики" с кнопки
    await cb.answer()


@dp.callback_query(F.data == "back_to_roles")
async def handle_back_to_roles(cb: CallbackQuery):
    """Возвращает к списку отделов."""
    await send_roles_page(chat_id=cb.message.chat.id, message_id=cb.message.message_id)
    await cb.answer()


# Эта функция остается из вашего кода, но теперь она часть нового флоу
# Убедитесь, что она есть и выглядит так:
async def send_roles_page(chat_id: int, message_id: int | None = None):
    with get_session() as db:
        roles = db.query(Employee.role).filter(Employee.is_active == True).distinct().all()
    text = "Выберите отдел для просмотра сотрудников:"
    buttons = [[InlineKeyboardButton(text=role[0], callback_data=f"role_select:{role[0]}:0")] for role in roles if
               role[0]]
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_employees_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message_id:
        await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=kb)
    else:
        await bot.send_message(chat_id, text, reply_markup=kb)


# НОВЫЙ БЛОК: БАЗА ЗНАНИЙ (KNOWLEDGE BASE)

async def send_kb_page(chat_id: int, message_id: int | None = None, page: int = 0):
    """
    Отправляет или редактирует сообщение со страницей топиков из Базы Знаний.
    """
    with get_session() as db:
        offset = page * PAGE_SIZE
        topics_on_page = db.query(Topic).order_by(Topic.title).offset(offset).limit(PAGE_SIZE).all()
        total_topics = db.query(func.count(Topic.id)).scalar()

    if not total_topics:
        text = "😔 В Базе Знаний пока нет ни одной статьи."
        kb = None
    else:
        text = f"<b>🧠 База знаний</b>\n\nВыберите интересующую вас тему (Страница {page + 1}):"

        # Кнопки с названиями статей
        buttons = [
            [InlineKeyboardButton(text=topic.title, callback_data=f"view_topic:{topic.id}:{page}")]
            for topic in topics_on_page
        ]

        # Кнопки для пагинации
        pagination_row = []
        if page > 0:
            pagination_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"kb_page:{page - 1}"))
        if (page + 1) * PAGE_SIZE < total_topics:
            pagination_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"kb_page:{page + 1}"))

        if pagination_row:
            buttons.append(pagination_row)

        buttons.append([InlineKeyboardButton(text="🔙 Назад к выбору раздела", callback_data="back_to_kb_main_menu")])

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    # Редактируем сообщение, если оно уже есть, или отправляем новое
    if message_id:
        await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=kb)
    else:
        await bot.send_message(chat_id, text, reply_markup=kb)


def get_kb_menu_kb() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с выбором разделов Базы Знаний."""
    buttons = [
        [InlineKeyboardButton(text="🧠 База знаний", callback_data="kb_show_topics")],
        [InlineKeyboardButton(text="📚 Регламенты и гайды", callback_data="kb_show_guides")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(F.text == "🧠 База знаний")
@access_check
async def show_kb_main_menu(message: Message, state: FSMContext, **kwargs):
    """
    Отправляет главное меню Базы Знаний с выбором разделов.
    """
    await state.clear()
    await message.answer("Выберите раздел Базы Знаний:", reply_markup=get_kb_menu_kb())

# Старый обработчик теперь будет на кнопке
@dp.callback_query(F.data == "kb_show_topics")
async def show_kb_topics_handler(cb: CallbackQuery):
    await send_kb_page(chat_id=cb.message.chat.id, message_id=cb.message.message_id)
    await cb.answer()


# --- 👇 НОВЫЙ ОБРАБОТЧИК ДЛЯ РЕГЛАМЕНТОВ 👇 ---
@dp.callback_query(F.data == "kb_show_guides")
async def show_role_guides(cb: CallbackQuery):
    await cb.answer()
    with get_session() as db:
        # Находим сотрудника и его роль
        emp = db.query(Employee).filter_by(telegram_id=cb.from_user.id).first()
        if not emp:
            await cb.message.edit_text("Не удалось найти ваш профиль.")
            return

        # Находим все гайды для его роли
        guides = db.query(RoleGuide).filter_by(role=emp.role).order_by(RoleGuide.order_index).all()

    if not guides:
        await cb.message.edit_text(f"Для вашей должности '{emp.role}' пока нет специальных регламентов.",
                                   reply_markup=get_kb_menu_kb()) # Даем вернуться назад
        return

    await cb.message.edit_text(f"<b>Регламенты для должности «{emp.role}»:</b>")

    # Отправляем каждый гайд отдельным сообщением
    for guide in guides:
        text = f"<b>{html.escape(guide.title)}</b>"
        if guide.content:
            text += f"\n\n{html.escape(guide.content)}"

        await cb.message.answer(text)

        if guide.file_path and os.path.exists(guide.file_path):
            try:
                file_to_send = FSInputFile(guide.file_path)
                await cb.message.answer_document(file_to_send)
            except Exception as e:
                logger.error(f"Не удалось отправить файл регламента {guide.file_path}: {e}")

        await asyncio.sleep(0.5) # Небольшая задержка для лучшего восприятия

@dp.callback_query(F.data.startswith("kb_page:"))
async def switch_kb_page(cb: CallbackQuery):
    """
    Обработчик для кнопок пагинации (вперед/назад) в списке статей.
    """
    page = int(cb.data.split(":")[1])
    await send_kb_page(chat_id=cb.message.chat.id, message_id=cb.message.message_id, page=page)
    await cb.answer()


@dp.callback_query(F.data.startswith("view_topic:"))
async def view_kb_topic(cb: CallbackQuery):
    """
    Показывает полную информацию о выбранной статье.
    """
    _, topic_id, page_to_return = cb.data.split(":")

    with get_session() as db:
        topic = db.get(Topic, int(topic_id))

    if not topic:
        await cb.answer("Статья не найдена!", show_alert=True)
        return

    # Формируем текст статьи
    text_content = f"<b>{html.escape(topic.title)}</b>\n\n{html.escape(topic.content)}"

    # Кнопка для возврата к списку
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к списку", callback_data=f"back_to_kb_list:{page_to_return}")]
    ])

    # Удаляем список статей, чтобы не засорять чат
    await cb.message.delete()

    # Отправляем статью с фото (если есть) или как обычный текст
    if topic.image_path and os.path.exists(topic.image_path):
        try:
            photo = FSInputFile(topic.image_path)
            await bot.send_photo(chat_id=cb.message.chat.id, photo=photo, caption=text_content, reply_markup=kb)
        except Exception as e:
            logger.error(f"Failed to send topic photo {topic.image_path}: {e}")
            await bot.send_message(cb.message.chat.id, text_content, reply_markup=kb, disable_web_page_preview=True)
    else:
        await bot.send_message(cb.message.chat.id, text_content, reply_markup=kb, disable_web_page_preview=True)

    await cb.answer()


@dp.callback_query(F.data.startswith("back_to_kb_list:"))
async def back_to_kb_list(cb: CallbackQuery):
    """
    Обработчик для кнопки 'Назад к списку', возвращает на нужную страницу.
    """
    page = int(cb.data.split(":")[1])
    # Удаляем сообщение со статьей
    await cb.message.delete()
    # Отправляем заново нужную страницу со списком
    await send_kb_page(chat_id=cb.message.chat.id, page=page)
    await cb.answer()

@dp.message(F.new_chat_members)
async def on_user_join_via_message(msg: Message):
    # работаем только в общем чате
    if COMMON_CHAT_ID is None or msg.chat.id != COMMON_CHAT_ID:
        return


    for user in msg.new_chat_members:
        # пропускаем ботов
        if user.is_bot:
            continue

        user_id = user.id
        user_name = user.full_name
        user_mention = f"@{user.username}" if user.username else user_name

        with get_session() as db:
            emp = db.query(Employee).filter_by(telegram_id=user_id).first()
            if not emp:
                continue

            # приветствуем только после тренинга и один раз
            if not emp.training_passed or emp.joined_main_chat:
                continue

            emp.joined_main_chat = True
            db.commit()

        welcome_text = get_text(
            "welcome_to_common_chat",
            "👋 Встречайте нового коллегу! {user_mention} ({user_name}) присоединился к нашему чату. Добро пожаловать! 🎉"
        ).format(user_mention=user_mention, user_name=html.escape(user_name))

        try:
            await bot.send_message(chat_id=COMMON_CHAT_ID, text=welcome_text)
        except Exception as e:
            logger.error(f"failed to send welcome: {e}")

# ⬇️ убираем фильтр на декораторе, решаем логику внутри
@dp.chat_member()
async def on_user_join_common_chat(event: ChatMemberUpdated):
    if COMMON_CHAT_ID is None or event.chat.id != COMMON_CHAT_ID:
        return


    # 2) лог — чтобы понять, что реально приходит
    logging.info(
        "chat_member update: chat=%s old=%s new=%s user=%s",
        event.chat.id,
        event.old_chat_member.status,
        event.new_chat_member.status,
        event.new_chat_member.user.id
    )

    # 3) интересует переход из «не в чате/ограничен» к «участник/админ/создатель»
    from aiogram.enums import ChatMemberStatus
    was = event.old_chat_member.status
    now = event.new_chat_member.status
    joined_from = {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED, ChatMemberStatus.RESTRICTED}
    joined_to   = {ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}

    if was not in joined_from or now not in joined_to:
        return

    user = event.new_chat_member.user
    user_id = user.id
    user_name = user.full_name
    user_mention = f"@{user.username}" if user.username else user_name  # красивое упоминание

    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=user_id).first()
        if not emp:
            logging.info("join ignored: employee not found for tg_id=%s", user_id)
            return

        # приветствуем только после тренинга и один раз
        if not emp.training_passed:
            logging.info("join ignored: training not passed for emp_id=%s", emp.id)
            return
        if emp.joined_main_chat:
            logging.info("join ignored: already marked joined for emp_id=%s", emp.id)
            return

        emp.joined_main_chat = True
        db.commit()

    welcome_text = get_text(
        "welcome_to_common_chat",
        "👋 Встречайте нового коллегу! {user_mention} ({user_name}) присоединился к нашему чату. Добро пожаловать! 🎉"
    ).format_map({
        "user_mention": user_mention,
        "user_name": html.escape(user_name),
        "name": html.escape(user_name),  # алиас для {name}
        "role": html.escape(emp.role or "—"),  # ← добавили подстановку {role}
    })

    try:
        await bot.send_message(chat_id=COMMON_CHAT_ID, text=welcome_text)
    except Exception as e:
        logging.error("failed to send welcome: %s", e)

# Обработчик для кнопки "Назад" из reply-меню (когда не активно никакое состояние)
@dp.message(F.text == "🔙 Назад", StateFilter(None))
async def back_to_main_menu_from_reply(message: Message, state: FSMContext):
    """
    Возвращает пользователя в главное меню из подменю.
    """
    with get_session() as db:
        emp = db.query(Employee).filter_by(telegram_id=message.from_user.id).first()

    # Определяем, какую главную клавиатуру показать — админа или сотрудника
    kb = admin_kb if emp and emp.role == "Admin" else employee_main_kb
    await message.answer("Вы в главном меню.", reply_markup=kb)

# — Запуск —
async def main():
    os.makedirs(UPLOAD_FOLDER_ONBOARDING, exist_ok=True)

    scheduler.start()
    logger.info("Bot starting polling...")
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())