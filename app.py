import os
import random
from datetime import datetime
from sqlalchemy import func
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv, set_key
import subprocess                # ← добавили
import asyncio # <-- ДОБАВИТЬ
from aiogram import Bot # <-- ДОБАВИТЬ

from models import (
    Base, engine, get_session, Employee, Event, Idea, QuizQuestion,
    RoleOnboarding, Topic, RegCode, ArchivedEmployee, Attendance,
    ArchivedAttendance, ArchivedIdea, Role,
    BotText, OnboardingQuestion, OnboardingStep, EmployeeCustomData
)

# --- НАСТРОЙКА ПРИЛОЖЕНИЯ ---
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "a_very_secret_key_for_flask")

UPLOAD_FOLDER_ONBOARDING = 'uploads/onboarding'
UPLOAD_FOLDER_TOPICS = 'uploads/topics'
app.config['UPLOAD_FOLDER_ONBOARDING'] = UPLOAD_FOLDER_ONBOARDING
app.config['UPLOAD_FOLDER_TOPICS'] = UPLOAD_FOLDER_TOPICS

os.makedirs(UPLOAD_FOLDER_ONBOARDING, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_TOPICS, exist_ok=True)
Base.metadata.create_all(engine)

ONBOARDING_DATA_KEYS = {
    'name': 'Имя (обновляет основной профиль)',
    'birthday': 'Дата рождения (обновляет профиль, формат ДД.ММ.ГГГГ)',
    'contact_info': 'Контактная информация (обновляет профиль)',
    'hobby': 'Хобби (дополнительное поле)',
    'favorite_quote': 'Любимая цитата (дополнительное поле)',
    'tshirt_size': 'Размер футболки (дополнительное поле)'
}

def get_text(key: str, default: str = "Текст не найден") -> str:
    """Получает текст для бота из БД по ключу."""
    with get_session() as db:
        text_obj = db.get(BotText, key)
        return text_obj.text if text_obj else default


# --- ОСНОВНОЙ МАРШРУТ (ГЛАВНАЯ СТРАНИЦА) ---
@app.route('/')
def index():
    with get_session() as db:
        employees = db.query(Employee).filter_by(is_active=True).order_by(Employee.name).all()
        archived_employees = db.query(ArchivedEmployee).order_by(ArchivedEmployee.dismissal_date.desc()).all()
        events = db.query(Event).order_by(Event.event_date.desc()).all()

        # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
        # Теперь мы загружаем идею и имя автора одним запросом
        ideas = db.query(Idea, Employee.name).join(Employee, Idea.employee_id == Employee.id).order_by(
            Idea.submission_date.desc()).all()

        topics = db.query(Topic).order_by(Topic.title).all()
        roles = db.query(Role).order_by(Role.name).all()
        bot_texts = db.query(BotText).order_by(BotText.id).all()

        onboarding_constructor_data = {}
        for role in roles:
            questions = db.query(OnboardingQuestion).filter_by(role=role.name).order_by(
                OnboardingQuestion.order_index).all()
            steps = db.query(OnboardingStep).filter_by(role=role.name).order_by(OnboardingStep.order_index).all()
            onboarding_constructor_data[role.name] = {
                "questions": questions,
                "steps": steps
            }


        onboarding_data = {}
        for role in roles:
            onboarding_info = db.query(RoleOnboarding).filter_by(role=role.name).first()
            quiz_questions = db.query(QuizQuestion).filter_by(role=role.name).order_by(QuizQuestion.order_index).all()
            onboarding_data[role.name] = {
                "info": onboarding_info,
                "quizzes": quiz_questions
            }

        config = {
            "BOT_TOKEN": os.getenv("BOT_TOKEN"),
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "COMMON_CHAT_ID": os.getenv("COMMON_CHAT_ID"),
            "OFFICE_LAT": os.getenv("OFFICE_LAT"),
            "OFFICE_LON": os.getenv("OFFICE_LON"),
            "OFFICE_RADIUS_METERS": os.getenv("OFFICE_RADIUS_METERS")
        }

    return render_template('index.html', employees=employees, archived_employees=archived_employees,
                           events=events, ideas=ideas, topics=topics,
                           onboarding_data=onboarding_data, roles=roles, config=config, bot_texts=bot_texts,
                           onboarding_constructor_data=onboarding_constructor_data, onboarding_data_keys=ONBOARDING_DATA_KEYS)


# --- НОВЫЕ РОУТЫ ДЛЯ УПРАВЛЕНИЯ ТЕКСТАМИ ---
@app.route('/texts/update/<string:text_id>', methods=['POST'])
def update_text(text_id):
    with get_session() as db:
        text_obj = db.get(BotText, text_id)
        if text_obj:
            text_obj.text = request.form.get('text', '')
            db.commit()
            flash(f"Текст '{text_id}' успешно обновлен.", "success")
        else:
            flash(f"Текст с ключом '{text_id}' не найден.", "danger")
    return redirect(url_for('index')) # В идеале - редирект на нужную вкладку


# --- НОВЫЕ РОУТЫ ДЛЯ УПРАВЛЕНИЯ ВОПРОСАМИ ОНБОРДИНГА ---
@app.route('/onboarding/question/add/<role>', methods=['POST'])
def add_onboarding_question(role):
    with get_session() as db:
        max_idx = db.query(func.max(OnboardingQuestion.order_index)).filter_by(role=role).scalar() or -1
        new_q = OnboardingQuestion(
            role=role,
            question_text=request.form['question_text'],
            data_key=request.form['data_key'],
            order_index=max_idx + 1,
            is_required='is_required' in request.form
        )
        db.add(new_q)
        db.commit()
        flash("Новый вопрос для онбординга добавлен.", "success")
    return redirect(url_for('index'))

@app.route('/onboarding/question/delete/<int:q_id>', methods=['POST'])
def delete_onboarding_question(q_id):
    with get_session() as db:
        q = db.get(OnboardingQuestion, q_id)
        if q:
            db.delete(q)
            db.commit()
            flash("Вопрос онбординга удален.", "warning")
    return redirect(url_for('index'))

@app.route('/onboarding/question/reorder', methods=['POST'])
def reorder_onboarding_question():
    ordered_ids = request.get_json(silent=True).get('ordered_ids', [])
    with get_session() as session:
        for index, qid in enumerate(ordered_ids):
            q = session.get(OnboardingQuestion, int(qid))
            if q:
                q.order_index = index
        session.commit()
    return jsonify(success=True)

@app.route('/onboarding/step/add/<role>', methods=['POST'])
def add_onboarding_step(role):
    with get_session() as db:
        max_idx = db.query(func.max(OnboardingStep.order_index)).filter_by(role=role).scalar() or -1
        new_step = OnboardingStep(
            role=role,
            message_text=request.form.get('message_text'),
            order_index=max_idx + 1
        )

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(f"{role.lower()}_step_{file.filename}")
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER_ONBOARDING'], 'steps')
            os.makedirs(upload_folder, exist_ok=True)
            orig_path = os.path.join(upload_folder, filename)
            file.save(orig_path)

            file_type = request.form.get('file_type', 'document')
            if file_type == 'video_note':
                # Конвертация в квадратный видео-кружок для Telegram
                base, _ = os.path.splitext(orig_path)
                conv_path = f"{base}_tn.mp4"
                # ffmpeg: масштабируем, добавляем паддинг, удаляем аудио
                cmd = [
                    'ffmpeg', '-y', '-i', orig_path,
                    '-vf', 'scale=\'min(iw,ih)\':\'min(iw,ih)\',pad=\'min(iw,ih)\':\'min(iw,ih)\':(ow-iw)/2:(oh-ih)/2,format=yuv420p\'',
                    '-c:v', 'libx264', '-preset', 'veryfast',
                    '-an',
                    conv_path
                ]
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    new_step.file_path = conv_path
                    new_step.file_type = 'video_note'
                    # Опционально: можно удалить оригинал, чтобы не дублировать
                    os.remove(orig_path)
                except Exception as e:
                    # Если конвертация не удалась — оставляем оригинал на всякий случай
                    new_step.file_path = orig_path
                    new_step.file_type = file_type
                    flash(f"Видео-кружок сохранён, но конвертация не удалась: {e}", "warning")
            else:
                # Для всех остальных типов просто сохраняем как есть
                new_step.file_path = orig_path
                new_step.file_type = file_type

        db.add(new_step)
        db.commit()
        flash("Новый шаг знакомства добавлен.", "success")
    return redirect(url_for('index'))

@app.route('/onboarding/step/delete/<int:step_id>', methods=['POST'])
def delete_onboarding_step(step_id):
    with get_session() as db:
        step = db.get(OnboardingStep, step_id)
        if step:
            # Опционально: удалить связанный файл с диска
            if step.file_path and os.path.exists(step.file_path):
                os.remove(step.file_path)
            db.delete(step)
            db.commit()
            flash("Шаг знакомства удален.", "warning")
    return redirect(url_for('index'))

@app.route('/onboarding/step/reorder', methods=['POST'])
def reorder_onboarding_step():
    ordered_ids = request.get_json(silent=True).get('ordered_ids', [])
    with get_session() as session:
        for index, sid in enumerate(ordered_ids):
            step = session.get(OnboardingStep, int(sid))
            if step:
                step.order_index = index
        session.commit()
    return jsonify(success=True)


# --- УПРАВЛЕНИЕ РОЛЯМИ (СПЕЦИАЛЬНОСТЯМИ) ---
@app.route('/role/add', methods=['POST'])
def add_role():
    with get_session() as db:
        role_name = request.form.get('role_name')
        if role_name and not db.query(Role).filter_by(name=role_name).first():
            db.add(Role(name=role_name))
            db.commit()
            flash(f"Роль '{role_name}' успешно добавлена.", "success")
        else:
            flash(f"Роль '{role_name}' уже существует или имя не указано.", "danger")
    return redirect(url_for('index'))


@app.route('/role/delete/<int:role_id>', methods=['POST'])
def delete_role(role_id):
    with get_session() as db:
        role = db.get(Role, role_id)
        if role:
            db.delete(role)
            db.commit()
            flash(f"Роль '{role.name}' удалена.", "warning")
    return redirect(url_for('index'))


# --- УПРАВЛЕНИЕ СОТРУДНИКАМИ ---
@app.route('/employee/add', methods=['POST'])
def add_employee():
    with get_session() as db:
        email = request.form['email']
        role = request.form['role'] # Добавили получение роли
        if db.query(Employee).filter_by(email=email).first():
            flash(f"Сотрудник с email {email} уже существует!", "danger")
            return redirect(url_for('index'))

        # Создаем сотрудника только с email и ролью. Имя = email как заглушка.
        new_emp = Employee(
            email=email,
            name=email, # Используем email как временное имя
            role=role,
            is_active=True
        )
        db.add(new_emp)
        db.flush()

        while True:
            code = "".join(str(random.randint(0, 9)) for _ in range(8))
            if not db.query(RegCode).filter_by(code=code).first(): break

        db.add(RegCode(code=code, email=new_emp.email, used=False))
        db.commit()
        flash(f"Сотрудник с email {email} добавлен. Код для регистрации: {code}", "success")
    return redirect(url_for('index'))

@app.route('/employee/reset_progress/<int:emp_id>', methods=['POST'])
def reset_progress(emp_id):
    with get_session() as db:
        emp = db.get(Employee, emp_id)
        if not emp:
            flash("Сотрудник не найден!", "danger")
            return redirect(url_for('index'))

        # Сбрасываем прогресс
        emp.onboarding_completed = False
        emp.training_passed = False

        # Удаляем его кастомные ответы на вопросы онбординга
        db.query(EmployeeCustomData).filter_by(employee_id=emp_id).delete(synchronize_session=False)

        db.commit()

        # Асинхронно отправляем уведомление в Telegram, если есть привязка
        if emp.telegram_id:
            async def send_notification():
                token = os.getenv("BOT_TOKEN")
                # Убедитесь, что в вашей таблице bot_texts есть ключ 'progress_reset_notification'
                message_text = get_text('progress_reset_notification',
                                        'Администратор сбросил ваш прогресс. Вам потребуется заново пройти онбординг и тренинг при следующем входе в бота.')
                if not token:
                    flash("Токен бота не найден в .env, уведомление не отправлено.", "warning")
                    return

                tg_bot = Bot(token=token)
                try:
                    await tg_bot.send_message(emp.telegram_id, message_text)
                except Exception as e:
                    flash(f"Не удалось отправить уведомление: {e}", "danger")
                    print(f"Could not send reset notification to {emp.id}: {e}")
                finally:
                    await tg_bot.session.close()

            try:
                asyncio.run(send_notification())
            except RuntimeError: # Если уже есть запущенный event loop
                 # Это может произойти в некоторых средах. Более сложная обработка может потребоваться.
                 # Для простоты пока просто логируем.
                 print("Could not run asyncio.run(), possibly due to existing loop.")


        flash(f"Прогресс для сотрудника {emp.name or emp.email} полностью сброшен.", "warning")
    return redirect(url_for('index'))


@app.route('/broadcast/send', methods=['POST'])
def send_broadcast():
    message_text = request.form.get('message_text')
    target_role = request.form.get('target_role')

    if not message_text:
        flash("Текст сообщения не может быть пустым.", "danger")
        return redirect(url_for('index'))

    with get_session() as db:
        query = db.query(Employee.telegram_id).filter(Employee.is_active == True, Employee.telegram_id != None)
        if target_role != 'all':
            query = query.filter(Employee.role == target_role)

        target_users_ids = [row[0] for row in query.all()]

    if not target_users_ids:
        flash("Не найдено сотрудников для рассылки в выбранном сегменте.", "warning")
        return redirect(url_for('index'))

    token = os.getenv("BOT_TOKEN")
    if not token:
        flash("Токен бота не найден в .env, рассылка невозможна.", "danger")
        return redirect(url_for('index'))

    # Статистика отправки
    success_count = 0
    error_count = 0

    async def _send_to_all():
        nonlocal success_count, error_count
        tg_bot = Bot(token=token)
        try:
            for user_id in target_users_ids:
                try:
                    await tg_bot.send_message(chat_id=user_id, text=message_text)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Failed to send message to {user_id}: {e}")
                await asyncio.sleep(0.1)  # Пауза во избежание лимитов Telegram
        finally:
            await tg_bot.session.close()

    try:
        asyncio.run(_send_to_all())
    except RuntimeError:
        flash("Ошибка выполнения асинхронной задачи рассылки.", "danger")
        return redirect(url_for('index'))

    flash(f"Рассылка завершена. Успешно отправлено: {success_count}. Ошибок: {error_count}.", "success")
    return redirect(url_for('index'))

@app.route('/employee/edit/<int:emp_id>', methods=['POST'])
def edit_employee(emp_id):
    with get_session() as db:
        emp = db.get(Employee, emp_id)
        if not emp:
            flash("Сотрудник не найден!", "danger")
            return redirect(url_for('index'))

        new_email = request.form['email']
        if emp.email != new_email and db.query(Employee).filter_by(email=new_email).first():
            flash(f"Email {new_email} уже занят другим сотрудником!", "danger")
            return redirect(url_for('index'))

        emp.name = request.form['name']
        emp.email = new_email
        emp.role = request.form['role']
        emp.birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d').date() if request.form[
            'birthday'] else None
        db.commit()
        flash(f"Данные сотрудника {emp.name} обновлены.", "success")
    return redirect(url_for('index'))


@app.route('/employee/dismiss/<int:emp_id>', methods=['POST'])
def dismiss_employee(emp_id):
    with get_session() as db:
        emp = db.get(Employee, emp_id)
        if not emp:
            flash("Сотрудник не найден!", "danger")
            return redirect(url_for('index'))

        # Собираем данные для архивации, исключая старый ID
        emp_data = {
            "telegram_id": emp.telegram_id,
            "email": emp.email,
            "role": emp.role,
            "name": emp.name,
            "birthday": emp.birthday,
            "registered": emp.registered,
            "training_passed": emp.training_passed,
        }

        # Создаем архивную запись, добавляя original_employee_id
        archived_emp = ArchivedEmployee(
            original_employee_id=emp.id,
            **emp_data
        )
        db.add(archived_emp)

        # Логика архивации посещений и идей остается без изменений
        for att in db.query(Attendance).filter_by(employee_id=emp_id).all():
            db.add(ArchivedAttendance(
                employee_id=att.employee_id,
                date=att.date,
                arrival_time=att.arrival_time,
                departure_time=att.departure_time
            ))
            db.delete(att)

        for idea in db.query(Idea).filter_by(employee_id=emp_id).all():
            db.add(ArchivedIdea(
                employee_id=idea.employee_id,
                text=idea.text,
                submission_date=idea.submission_date
            ))
            db.delete(idea)

        # Удаляем сотрудника из основной таблицы
        db.delete(emp)
        db.commit()

        flash(f"Сотрудник {emp.name} уволен и перенесен в архив.", "warning")
    return redirect(url_for('index'))

@app.route('/employee/reset_telegram/<int:emp_id>', methods=['POST'])
def reset_telegram(emp_id):
    with get_session() as db:
        emp = db.get(Employee, emp_id)
        if not emp:
            flash("Сотрудник не найден!", "danger")
            return redirect(url_for('index'))
        emp.telegram_id = None
        emp.registered = False
        db.commit()
        flash(f"Привязка Telegram для сотрудника {emp.name} сброшена. Ему потребуется новый код для входа.", "warning")
    return redirect(url_for('index'))


@app.route('/employee/generate_code/<int:emp_id>', methods=['POST'])
def generate_new_code(emp_id):
    with get_session() as db:
        emp = db.get(Employee, emp_id)
        if not emp:
            flash("Сотрудник не найден!", "danger")
            return redirect(url_for('index'))
        while True:
            code = "".join(str(random.randint(0, 9)) for _ in range(8))
            if not db.query(RegCode).filter_by(code=code).first(): break
        db.add(RegCode(code=code, email=emp.email, used=False))
        db.commit()
        flash(f"Сгенерирован новый код для {emp.name}: {code}", "success")
    return redirect(url_for('index'))


# --- УПРАВЛЕНИЕ ОНБОРДИНГОМ И КВИЗАМИ ---
@app.route('/onboarding/update/<role>', methods=['POST'])
def update_onboarding(role):
    with get_session() as db:
        onboarding = db.query(RoleOnboarding).filter_by(role=role).first()
        if not onboarding:
            onboarding = RoleOnboarding(role=role)
            db.add(onboarding)

        onboarding.text = request.form['text']
        onboarding.file_type = request.form['file_type']

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(f"{role.lower()}_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER_ONBOARDING'], filename)
            file.save(file_path)
            onboarding.file_path = file_path

        db.commit()
        flash(f"Онбординг для роли '{role}' обновлен.", "success")
    return redirect(url_for('index'))


@app.route('/quiz/add/<role>', methods=['POST'])
def add_quiz(role):
    with get_session() as db:
        qtype    = request.form['question_type']
        question = request.form['question']

        if qtype == 'choice':
            options = request.form.get('options')        # "Вариант1;Вариант2;…"
            answer  = request.form.get('answer')         # из скрытого поля
        else:
            options = None
            answer  = request.form.get('text_answer')    # из текстового поля

        # вычисляем следующий индекс
        max_idx = db.query(func.max(QuizQuestion.order_index)).filter_by(role=role).scalar() or -1

        new_q = QuizQuestion(
            role=role,
            question=question,
            answer=answer,
            question_type=qtype,
            options=options,
            order_index=max_idx + 1
        )
        db.add(new_q)
        db.commit()
        flash("Новый вопрос добавлен.", "success")
    return redirect(url_for('index'))

@app.route('/quiz/edit/<int:quiz_id>', methods=['POST'])
def edit_quiz(quiz_id):
    with get_session() as db:
        quiz = db.get(QuizQuestion, quiz_id)
        qtype = request.form['question_type']

        quiz.question = request.form['question']
        if qtype == 'choice':
            quiz.options = request.form.get('options')
            quiz.answer  = request.form.get('answer')
        else:
            quiz.options = None
            quiz.answer  = request.form.get('text_answer')

        quiz.question_type = qtype
        db.commit()
        flash("Вопрос обновлён.", "success")
    return redirect(url_for('index'))

@app.route('/quiz/delete/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    with get_session() as db:
        quiz = db.get(QuizQuestion, quiz_id)
        if quiz:
            db.delete(quiz)
            db.commit()
            flash("Вопрос квиза удален.", "warning")
    return redirect(url_for('index'))


@app.route('/quiz/reorder', methods=['POST'])
def reorder_quiz():
    data = request.get_json(silent=True) or {}
    ordered_ids = data.get('ordered_ids', [])
    # используем session вместо db, чтобы не получить NameError
    with get_session() as session:
        for index, qid in enumerate(ordered_ids):
            quiz = session.get(QuizQuestion, int(qid))
            if quiz:
                quiz.order_index = index
        session.commit()
    return jsonify(success=True, message="Порядок вопросов обновлен")

# --- УПРАВЛЕНИЕ ИВЕНТАМИ ---
@app.route('/event/add', methods=['POST'])
def add_event():
    with get_session() as db:
        db.add(Event(
            title=request.form['title'], description=request.form['description'],
            event_date=datetime.strptime(request.form['event_date'], '%Y-%m-%dT%H:%M')
        ))
        db.commit()
        flash("Новый ивент успешно добавлен.", "success")
    return redirect(url_for('index'))


@app.route('/event/edit/<int:event_id>', methods=['POST'])
def edit_event(event_id):
    with get_session() as db:
        event = db.get(Event, event_id)
        if event:
            event.title = request.form['title']
            event.description = request.form['description']
            event.event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%dT%H:%M')
            db.commit()
            flash("Ивент обновлен.", "success")
    return redirect(url_for('index'))


@app.route('/event/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    with get_session() as db:
        event = db.get(Event, event_id)
        if event:
            db.delete(event)
            db.commit()
            flash("Ивент удален.", "warning")
    return redirect(url_for('index'))


# --- УПРАВЛЕНИЕ ИДЕЯМИ ---
@app.route('/idea/delete/<int:idea_id>', methods=['POST'])
def delete_idea(idea_id):
    with get_session() as db:
        idea = db.get(Idea, idea_id)
        if idea:
            db.delete(idea)
            db.commit()
            flash("Идея удалена.", "warning")
    return redirect(url_for('index'))


# --- УПРАВЛЕНИЕ БАЗОЙ ЗНАНИЙ (ТОПИКАМИ) ---
@app.route('/topic/add', methods=['POST'])
def add_topic():
    with get_session() as db:
        new_topic = Topic(title=request.form['title'], content=request.form['content'])
        if 'image' in request.files and request.files['image'].filename != '':
            file = request.files['image']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_TOPICS'], filename)
            file.save(file_path)
            new_topic.image_path = file_path
        db.add(new_topic)
        db.commit()
        flash("Новая тема в Базе Знаний создана.", "success")
    return redirect(url_for('index'))


@app.route('/topic/edit/<int:topic_id>', methods=['POST'])
def edit_topic(topic_id):
    with get_session() as db:
        topic = db.get(Topic, topic_id)
        if topic:
            topic.title = request.form['title']
            topic.content = request.form['content']
            if 'image' in request.files and request.files['image'].filename != '':
                file = request.files['image']
                if topic.image_path and os.path.exists(topic.image_path):
                    os.remove(topic.image_path)
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER_TOPICS'], filename)
                file.save(file_path)
                topic.image_path = file_path
            db.commit()
            flash("Тема в Базе Знаний обновлена.", "success")
    return redirect(url_for('index'))


@app.route('/topic/delete/<int:topic_id>', methods=['POST'])
def delete_topic(topic_id):
    with get_session() as db:
        topic = db.get(Topic, topic_id)
        if topic:
            if topic.image_path and os.path.exists(topic.image_path):
                os.remove(topic.image_path)
            db.delete(topic)
            db.commit()
            flash("Тема из Базы Знаний удалена.", "warning")
    return redirect(url_for('index'))


# --- УПРАВЛЕНИЕ НАСТРОЙКАМИ (.ENV) ---
@app.route('/config/update', methods=['POST'])
def update_config():
    env_file = '.env'
    set_key(env_file, "COMMON_CHAT_ID", request.form.get("COMMON_CHAT_ID", ""))
    set_key(env_file, "OFFICE_LAT", request.form.get("OFFICE_LAT", ""))
    set_key(env_file, "OFFICE_LON", request.form.get("OFFICE_LON", ""))
    set_key(env_file, "OFFICE_RADIUS_METERS", request.form.get("OFFICE_RADIUS_METERS", ""))
    if request.form.get("BOT_TOKEN"):
        set_key(env_file, "BOT_TOKEN", request.form.get("BOT_TOKEN"))
    flash("Настройки сохранены. Перезапустите бота, чтобы они применились.", "info")
    return redirect(url_for('index'))


# --- ЗАПУСК ПРИЛОЖЕНИЯ ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
