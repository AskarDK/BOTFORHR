--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: _alembic_version; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._alembic_version (
    version_num character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._alembic_version OWNER TO rebasedata;

--
-- Name: _archived_attendance; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._archived_attendance (
    id character varying(1) DEFAULT NULL::character varying,
    employee_id character varying(1) DEFAULT NULL::character varying,
    date character varying(1) DEFAULT NULL::character varying,
    arrival_time character varying(1) DEFAULT NULL::character varying,
    departure_time character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._archived_attendance OWNER TO rebasedata;

--
-- Name: _archived_employees; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._archived_employees (
    id smallint,
    telegram_id character varying(11) DEFAULT NULL::character varying,
    email character varying(33) DEFAULT NULL::character varying,
    role character varying(7) DEFAULT NULL::character varying,
    name character varying(21) DEFAULT NULL::character varying,
    birthday character varying(1) DEFAULT NULL::character varying,
    registered smallint,
    greeted smallint,
    training_passed smallint,
    full_name character varying(1) DEFAULT NULL::character varying,
    "position" character varying(1) DEFAULT NULL::character varying,
    contract_number character varying(1) DEFAULT NULL::character varying,
    employment_date character varying(1) DEFAULT NULL::character varying,
    contact_info character varying(1) DEFAULT NULL::character varying,
    branch character varying(1) DEFAULT NULL::character varying,
    cooperation_format character varying(1) DEFAULT NULL::character varying,
    dismissal_date character varying(10) DEFAULT NULL::character varying,
    original_employee_id character varying(2) DEFAULT NULL::character varying
);


ALTER TABLE public._archived_employees OWNER TO rebasedata;

--
-- Name: _archived_ideas; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._archived_ideas (
    id smallint,
    employee_id smallint,
    idea_text character varying(3) DEFAULT NULL::character varying,
    submission_date character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._archived_ideas OWNER TO rebasedata;

--
-- Name: _attendance; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._attendance (
    id smallint,
    employee_id smallint,
    date character varying(1) DEFAULT NULL::character varying,
    arrival_time character varying(15) DEFAULT NULL::character varying,
    departure_time character varying(15) DEFAULT NULL::character varying
);


ALTER TABLE public._attendance OWNER TO rebasedata;

--
-- Name: _bot_texts; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._bot_texts (
    id character varying(34) DEFAULT NULL::character varying,
    text character varying(294) DEFAULT NULL::character varying,
    description character varying(140) DEFAULT NULL::character varying
);


ALTER TABLE public._bot_texts OWNER TO rebasedata;

--
-- Name: _employee_custom_data; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._employee_custom_data (
    id smallint,
    employee_id smallint,
    data_key character varying(12) DEFAULT NULL::character varying,
    data_value character varying(11) DEFAULT NULL::character varying
);


ALTER TABLE public._employee_custom_data OWNER TO rebasedata;

--
-- Name: _employees; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._employees (
    id smallint,
    telegram_id character varying(11) DEFAULT NULL::character varying,
    email character varying(44) DEFAULT NULL::character varying,
    role character varying(5) DEFAULT NULL::character varying,
    name character varying(32) DEFAULT NULL::character varying,
    birthday character varying(1) DEFAULT NULL::character varying,
    registered smallint,
    greeted smallint,
    full_name character varying(36) DEFAULT NULL::character varying,
    "position" character varying(36) DEFAULT NULL::character varying,
    contract_number character varying(36) DEFAULT NULL::character varying,
    employment_date character varying(1) DEFAULT NULL::character varying,
    contact_info character varying(42) DEFAULT NULL::character varying,
    branch character varying(36) DEFAULT NULL::character varying,
    cooperation_format character varying(36) DEFAULT NULL::character varying,
    training_passed smallint,
    last_seen character varying(1) DEFAULT NULL::character varying,
    is_active smallint,
    onboarding_completed smallint,
    photo_file_id character varying(1) DEFAULT NULL::character varying,
    joined_main_chat smallint
);


ALTER TABLE public._employees OWNER TO rebasedata;

--
-- Name: _events; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._events (
    id smallint,
    title character varying(14) DEFAULT NULL::character varying,
    description character varying(22) DEFAULT NULL::character varying,
    event_date character varying(10) DEFAULT NULL::character varying,
    created_at character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._events OWNER TO rebasedata;

--
-- Name: _group_chats; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._group_chats (
    id smallint,
    name character varying(7) DEFAULT NULL::character varying,
    chat_id bigint
);


ALTER TABLE public._group_chats OWNER TO rebasedata;

--
-- Name: _ideas; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._ideas (
    id smallint,
    employee_id smallint,
    text character varying(17) DEFAULT NULL::character varying,
    submission_date character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._ideas OWNER TO rebasedata;

--
-- Name: _onboarding_questions; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._onboarding_questions (
    id smallint,
    role character varying(7) DEFAULT NULL::character varying,
    order_index smallint,
    question_text character varying(63) DEFAULT NULL::character varying,
    data_key character varying(12) DEFAULT NULL::character varying,
    is_required smallint
);


ALTER TABLE public._onboarding_questions OWNER TO rebasedata;

--
-- Name: _onboarding_steps; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._onboarding_steps (
    id smallint,
    role character varying(7) DEFAULT NULL::character varying,
    order_index smallint,
    message_text character varying(4) DEFAULT NULL::character varying,
    file_path character varying(48) DEFAULT NULL::character varying,
    file_type character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._onboarding_steps OWNER TO rebasedata;

--
-- Name: _quiz_questions; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._quiz_questions (
    id smallint,
    role character varying(7) DEFAULT NULL::character varying,
    question character varying(12) DEFAULT NULL::character varying,
    answer character varying(3) DEFAULT NULL::character varying,
    order_index smallint,
    question_type character varying(36) DEFAULT NULL::character varying,
    options character varying(15) DEFAULT NULL::character varying
);


ALTER TABLE public._quiz_questions OWNER TO rebasedata;

--
-- Name: _reg_codes; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._reg_codes (
    code integer,
    email character varying(44) DEFAULT NULL::character varying,
    used smallint
);


ALTER TABLE public._reg_codes OWNER TO rebasedata;

--
-- Name: _role_guides; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._role_guides (
    id smallint,
    role character varying(5) DEFAULT NULL::character varying,
    title character varying(8) DEFAULT NULL::character varying,
    content character varying(8) DEFAULT NULL::character varying,
    file_path character varying(1) DEFAULT NULL::character varying,
    order_index smallint
);


ALTER TABLE public._role_guides OWNER TO rebasedata;

--
-- Name: _role_onboarding; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._role_onboarding (
    id smallint,
    role character varying(7) DEFAULT NULL::character varying,
    text character varying(38) DEFAULT NULL::character varying,
    file_path character varying(40) DEFAULT NULL::character varying,
    file_type character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._role_onboarding OWNER TO rebasedata;

--
-- Name: _roles; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._roles (
    id smallint,
    name character varying(7) DEFAULT NULL::character varying
);


ALTER TABLE public._roles OWNER TO rebasedata;

--
-- Name: _sqlite_sequence; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._sqlite_sequence (
    name character varying(20) DEFAULT NULL::character varying,
    seq smallint
);


ALTER TABLE public._sqlite_sequence OWNER TO rebasedata;

--
-- Name: _topics; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._topics (
    id smallint,
    title character varying(24) DEFAULT NULL::character varying,
    content character varying(497) DEFAULT NULL::character varying,
    category character varying(11) DEFAULT NULL::character varying,
    image_path character varying(43) DEFAULT NULL::character varying
);


ALTER TABLE public._topics OWNER TO rebasedata;

--
-- Name: _training_material; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._training_material (
    id character varying(1) DEFAULT NULL::character varying,
    role character varying(1) DEFAULT NULL::character varying,
    title character varying(1) DEFAULT NULL::character varying,
    content character varying(1) DEFAULT NULL::character varying,
    file_path character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._training_material OWNER TO rebasedata;

--
-- Data for Name: _alembic_version; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: _archived_attendance; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._archived_attendance (id, employee_id, date, arrival_time, departure_time) FROM stdin;
\.


--
-- Data for Name: _archived_employees; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._archived_employees (id, telegram_id, email, role, name, birthday, registered, greeted, training_passed, full_name, "position", contract_number, employment_date, contact_info, branch, cooperation_format, dismissal_date, original_employee_id) FROM stdin;
54		амирханова_дильназ@example.com	Staff	Амирханова Дильназ		0	0	0								2025-08-11	
56		амирханов_нурмухаммед@example.com	Staff	Амирханов Нурмухаммед		0	0	0								2025-08-11	
58	-1076367879	dauletbekoffa@gmail.com	Hunter	Аскар Даулетбек		1	1	1								2025-08-05	
61	-1076367879	Dauletbekoff@gmail.com	Hunter	Аскар		1	0	1								2025-08-05	
63		Dauletbekoffaa@gmail.com	Admin	Askar Dauletbek		0	0	0								2025-08-05	
64	-1076367879	Dauletbekoffa@gmail.com	Пушер	Askar Dauletbek		1	0	1								2025-08-07	63
65	1267651407	ako@gmail.com	Hunter	Акниет		1	0	1								2025-08-07	60
66		Akoo@gmail.com	Trainer	Akmeyir		0	0	0								2025-08-07	59
67		Akhmad@gmail.com	Hunter	Akhmad		0	0	1								2025-08-07	62
68	-1076367879	akhmad@gmail.com	Пушер	Аскар		1	0	1								2025-08-07	58
69	-1076367879	Dauletbekoffa@gmail.com	Пушер	Аскар		1	0	0								2025-08-07	58
70	-1076367879	Dauletbekoffa@gmail.com	Пушер	Аскар		1	0	0								2025-08-07	58
71	-1076367879	usenov@example.com	Пушер	Адиль		1	0	1								2025-08-11	3
72	964240622	admin@healthclub.local	Admin	Искаков Аскар		1	0	1								2025-08-11	57
\.


--
-- Data for Name: _archived_ideas; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._archived_ideas (id, employee_id, idea_text, submission_date) FROM stdin;
1	58	Ей	2025-08-07
2	58	Йоу	2025-08-07
\.


--
-- Data for Name: _attendance; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._attendance (id, employee_id, date, arrival_time, departure_time) FROM stdin;
1	58		00:12:53.728248	00:25:57.929747
\.


--
-- Data for Name: _bot_texts; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._bot_texts (id, text, description) FROM stdin;
account_deactivated	Ваш аккаунт был деактивирован. Обратитесь к администратору.	Сообщение для уволенного сотрудника
welcome_back	С возвращением, {name}!	Приветствие для сотрудника, который уже прошел онбординг
training_not_passed_prompt	Привет! Чтобы получить доступ ко всем функциям бота, осталось пройти тренинг.	Напоминание о необходимости пройти тренинг
onboarding_not_finished	Похоже, вы не закончили знакомство. Давайте продолжим!	Если пользователь перезапустил бота во время онбординга
enter_reg_code	Здравствуйте! Пожалуйста, введите ваш 8-значный регистрационный код который вам выдал рекрутер:	Первое сообщение новому пользователю
code_accepted	Код принят! ð Давайте познакомим	Сообщение после успешного ввода кода
company_introduction_start	Отлично! Теперь немного о компании.	Начало блока 'Знакомство с компанией'
training_prompt_after_onboarding	Знакомство завершено! Теперь нужно пройти финальный тренинг.	Предложение пройти тренинг после онбординга
access_denied_training_required	Пожалуйста, завершите тренинг, чтобы получить доступ к этому разделу.	Сообщение при попытке использовать функцию без пройденного тренинга
birthday_greeting	ð Сегодня у {name} ({role}) день рождения! Поздравляем	Поздравление с ДР в общем чате
new_event_announcement	ð <b>Анонс нового ивента!</b> ð\n\n<b>{title}</b>\n\n<i>{description}</i>\n\n<b>Когда:</b> {date}\n\nЖдём	Уведомление о новом ивенте в общем чате
quiz_success_message	ð Поздравляем, {name}! Вы успешно прошли квиз ({correct}/{total})! Теперь вам доступен весь функцион	Сообщение после успешного прохождения квиза. Доступные переменные: {name}, {correct}, {total}.
group_join_success_message	Отлично, мы видим, что вы уже в нашем общем чате! Добро пожаловать в команду, теперь вам доступен весь функционал. ð	Сообщение, если пользователь прошел квиз и уже состоит в общем чате.
group_join_prompt_message	Остался последний шаг — вступите в наш основной рабочий чат, чтобы быть в курсе всех событий: https://t.me/+kvhVYarAmi1jNzNi	Сообщение, если пользователь прошел квиз, но еще не в общем чате. ВАЖНО: вручную замените {group_link} на реальную ссылку-приглашение в чат.
welcome_to_common_chat	ðª Добро пожаловать в 35 Health Clubs!\r\nСегодня наша команда стала сильнее — к нам присоединился(ась) <b>{name}</b> на позицию <b>{role}</b>.\r\nМы уверены, что впереди нас ждёт много интересных проектов, энергичных тренировок и побед! Желаем лёгкой адаптации, поддержки коллег и мощного старта	Сообщение в общем чате при вступлении нового сотрудника. Доступные переменные: {user_mention}, {user_name}.
employee_dismissed_announcement	ð Спасибо, что были частью команды 35 Health Clubs\r\nСегодня мы прощаемся с {name} ({role}) .\r\nСпасибо за ваш вклад, идеи и энергию, которую вы отдавали компании и нашим клиентам. Желаем, чтобы впереди были только новые победы, интересные проекты и вдохновляющие люди	Сообщение при увольнений
employee_role_changed_announcement	ð Карьерный рост в 35 Health Clubs\r\nПоздравляем <b>{name}</b> с переходом на новую позицию — <b>{new}</b>!\r\nЭто новый этап, новые задачи и новые горизонты. Мы вери	Смена специальности
\.


--
-- Data for Name: _employee_custom_data; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._employee_custom_data (id, employee_id, data_key, data_value) FROM stdin;
13	3	name	Адиль
14	3	contact_info	87078229829
17	58	name	Аскар
18	58	contact_info	87472474546
21	44	name	Аскар
22	44	contact_info	87472474546
\.


--
-- Data for Name: _employees; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._employees (id, telegram_id, email, role, name, birthday, registered, greeted, full_name, "position", contract_number, employment_date, contact_info, branch, cooperation_format, training_passed, last_seen, is_active, onboarding_completed, photo_file_id, joined_main_chat) FROM stdin;
1		батырбеков_алмас@example.com	Staff	Батырбеков Алмас		0	0	Батырбеков Алмас	Директор	unknown_value_please_contact_support		87762886229	unknown_value_please_contact_support	Партнер	0		1	0		0
2		искаков_аскар@example.com	Staff	Искаков Аскар		0	0	Искаков Аскар	Директор	unknown_value_please_contact_support		87078223464	unknown_value_please_contact_support	Партнер	0		1	0		0
4		yelena@example.com	Admin	Белоконь Елена		0	0	Белоконь Елена	Коммерческий директор	unknown_value_please_contact_support		87052506005	Тургут Озала, 261	Штат	0		1	0		0
5		ибрагимов_раджив_хачиханович@example.com	Staff	Ибрагимов Раджив Хачиханович		0	0	Ибрагимов Раджив Хачиханович	Генеральный Директор	unknown_value_please_contact_support		87011007557	unknown_value_please_contact_support	Внештатное	0		1	0		0
6		искаков_мирас_мейрамович@example.com	Staff	Искаков Мирас Мейрамович		0	0	Искаков Мирас Мейрамович	Операционный Руководитель	unknown_value_please_contact_support		87079017029	unknown_value_please_contact_support	Штат	0		1	0		0
7		жолбаева_акмейир@example.com	Staff	Жолбаева Акмейир		0	0	Жолбаева Акмейир	Менеджер по управлению персонала	unknown_value_please_contact_support		87006984741	unknown_value_please_contact_support	Внештатное	0		1	0		0
8		бисемалиева_алина@example.com	Staff	Бисемалиева Алина		0	0	Бисемалиева Алина	Менеджер по подбору персонала	unknown_value_please_contact_support		87006488667	Тургут Озала, 261	Штат	0		1	0		0
9		кадырова_гузель_шатликовна@example.com	Staff	Кадырова Гузель Шатликовна		0	0	Кадырова Гузель Шатликовна	СММ-менеджер	unknown_value_please_contact_support		87770267798	unknown_value_please_contact_support	Внештатное	0		1	0		0
10		жалгасбай_айдана_мухтаркызы@example.com	Staff	Жалгасбай Айдана Мухтаркызы		0	0	Жалгасбай Айдана Мухтаркызы	Менеджер по работе с блогерами	unknown_value_please_contact_support		87780420175	Тургут Озала, 261	Штат	0		1	0		0
11		багдатов_дидар_арманулы@example.com	Staff	Багдатов Дидар Арманулы		0	0	Багдатов Дидар Арманулы	Таргетолог	unknown_value_please_contact_support		87477750115	unknown_value_please_contact_support	Внештатное	0		1	0		0
12		пакалин_даниил_владимирович@example.com	Staff	Пакалин Даниил Владимирович		0	0	Пакалин Даниил Владимирович	Видеограф	unknown_value_please_contact_support		87066355661	unknown_value_please_contact_support	Внештатное	0		1	0		0
13		оразбай_галымжан_бауыржанулы@example.com	Staff	Оразбай Галымжан Бауыржанулы		0	0	Оразбай Галымжан Бауыржанулы	Веб-дизайнер	unknown_value_please_contact_support		87002789479	unknown_value_please_contact_support	Внештатное	0		1	0		0
14		жеткизгенова_акбобек_тилеккызы@example.com	Staff	Жеткизгенова Акбобек Тилеккызы		0	0	Жеткизгенова Акбобек Тилеккызы	Менеджер контроля и качества	unknown_value_please_contact_support		87089798991	unknown_value_please_contact_support	Внештатное	0		1	0		0
15		естенов_едиль@example.com	Staff	Естенов Едиль		0	0	Естенов Едиль	Тимлидер Хантер	unknown_value_please_contact_support		87713168526	Тургут Озала, 261	Штат	0		1	0		0
16		саламат_алиосман_рустемулы@example.com	Staff	Саламат Алиосман Рустемулы		0	0	Саламат Алиосман Рустемулы	Хантер	unknown_value_please_contact_support		87022754563	Тургут Озала, 261	Штат	0		1	0		0
17		мукаш_аружан_мураткызы@example.com	Staff	Мукаш Аружан Мураткызы		0	0	Мукаш Аружан Мураткызы	Хантер	unknown_value_please_contact_support		87072772353	Тургут Озала,261	Штат	0		1	0		0
18		бақдаулетқызы_әсел@example.com	Staff	Бақдаулетқызы Әсел		0	0	Бақдаулетқызы Әсел	Хантер	unknown_value_please_contact_support		87072251123	unknown_value_please_contact_support	unknown_value_please_contact_support	0		1	0		0
19		васильев_иван_сергеевич@example.com	Staff	Васильев Иван Сергеевич		0	0	Васильев Иван Сергеевич	Хантер	unknown_value_please_contact_support		87051315304	Тургут Озала, 261	Штат	0		1	0		0
20		жубаназаров_нурбек_байболсынович@example.com	Staff	Жубаназаров Нурбек Байболсынович		0	0	Жубаназаров Нурбек Байболсынович	Хантер	unknown_value_please_contact_support		87780634928	Тургут Озала, 261	Штат	0		1	0		0
21		рашидинова_шаира_садирдиновна@example.com	Staff	Рашидинова Шаира Садирдиновна		0	0	Рашидинова Шаира Садирдиновна	Хантер	unknown_value_please_contact_support		87009919794	unknown_value_please_contact_support	Внештатное	0		1	0		0
22		гладченко_анастасия_евгеньевна@example.com	Staff	Гладченко Анастасия Евгеньевна		0	0	Гладченко Анастасия Евгеньевна	Хантер	unknown_value_please_contact_support		87006629814	Тургут Озала, 261	Штат	0		1	0		0
23		калоев_асланбек_казбекович@example.com	Staff	Калоев Асланбек Казбекович		0	0	Калоев Асланбек Казбекович	Хантер	unknown_value_please_contact_support		87770263453	Тургут Озала, 261	Штат	0		1	0		0
24		джамалов_жанади_жанатович@example.com	Staff	Джамалов Жанади Жанатович		0	0	Джамалов Жанади Жанатович	Хантер	unknown_value_please_contact_support		87755523051	Тургут Озала, 261	Штат	0		1	0		0
25		баядилов_мейржан@example.com	Staff	Баядилов Мейржан		0	0	Баядилов Мейржан	Хантер	unknown_value_please_contact_support		87476896506	Тургут Озала, 261	Штат	0		1	0		0
26		ермуханбет_айбар_бейбітұлы@example.com	Staff	Ермуханбет Айбар Бейбітұлы		0	0	Ермуханбет Айбар Бейбітұлы	Хантер	unknown_value_please_contact_support		87714387862	Тургут Озала, 261	Штат	0		1	0		0
27		джумахан_ырысжан_бақытжанқызы@example.com	Staff	Джумахан Ырысжан Бақытжанқызы		0	0	Джумахан Ырысжан Бақытжанқызы	Хантер	unknown_value_please_contact_support		87473803311	Тургут Озала, 261	Штат	0		1	0		0
28		болатов_мирас_қайратұлы@example.com	Staff	Болатов Мирас Қайратұлы		0	0	Болатов Мирас Қайратұлы	Хантер	unknown_value_please_contact_support		87711132069	Тургут Озала, 261	Штат	0		1	0		0
29		сычёв_родион_валерьевич@example.com	Staff	Сычёв Родион Валерьевич		0	0	Сычёв Родион Валерьевич	Тимлидер Тренер	unknown_value_please_contact_support		87073606235	unknown_value_please_contact_support	Штат	0		1	0		0
30		дроздов_руслан_васильевич@example.com	Staff	Дроздов Руслан Васильевич		0	0	Дроздов Руслан Васильевич	лидер локации Тренер	unknown_value_please_contact_support		87762082966	Шахристан	Штат	0		1	0		0
31		батталова_альфия@example.com	Staff	Батталова Альфия		0	0	Батталова Альфия	Тренер	unknown_value_please_contact_support		87015244302	Шахиристан	Штат	0		1	0		0
32		махмутов_максим_маратович@example.com	Staff	Махмутов Максим Маратович		0	0	Махмутов Максим Маратович	unknown_value_please_contact_support	unknown_value_please_contact_support		87082461277	Шахристан	Штат	0		1	0		0
33		константинов_виктор_евгеньевич@example.com	Staff	Константинов Виктор Евгеньевич		0	0	Константинов Виктор Евгеньевич	Тренер	unknown_value_please_contact_support		87085508549	Шахристан	Штат	0		1	0		0
34		сыдык_айбар_берикуелы@example.com	Staff	Сыдык Айбар Берикуелы		0	0	Сыдык Айбар Берикуелы	Тренер	unknown_value_please_contact_support		87471303305	Барибаева	Штат	0		1	0		0
35		дударев_данил@example.com	Staff	Дударев Данил		0	0	Дударев Данил	Тренер	unknown_value_please_contact_support		87785912498	Барибаева	Штат	0		1	0		0
36		гусев_данил_владиславович@example.com	Staff	Гусев Данил Владиславович		0	0	Гусев Данил Владиславович	Тренер	unknown_value_please_contact_support		87476241676	Барибаева	Штат	0		1	0		0
37		сергеев_сергей_вячеславович@example.com	Staff	Сергеев Сергей Вячеславович		0	0	Сергеев Сергей Вячеславович	лидер локации Тренер	unknown_value_please_contact_support		87055548252	Фридом	Штат	0		1	0		0
38		мухаметжанова_галина_андреевна@example.com	Staff	Мухаметжанова Галина Андреевна		0	0	Мухаметжанова Галина Андреевна	Тренер	unknown_value_please_contact_support		87784490779	Фридом	Штат	0		1	0		0
39		озбек_дамир_маратулы@example.com	Staff	Озбек Дамир Маратулы		0	0	Озбек Дамир Маратулы	Тренер	unknown_value_please_contact_support		87473703932	Фридом	Штат	0		1	0		0
40		кузнецов_андрей_олегович@example.com	Staff	Кузнецов Андрей Олегович		0	0	Кузнецов Андрей Олегович	лидер локации Тренер	unknown_value_please_contact_support		87753790098 ватс апп 87057413571 телеграмм	Коктем	Штат	0		1	0		0
41		жетпіс_дияс_ертайұлы@example.com	Staff	Жетпіс Дияс Ертайұлы		0	0	Жетпіс Дияс Ертайұлы	Тренер	unknown_value_please_contact_support		87712556618	Коктем	Штат	0		1	0		0
42		ахмеджанов_медет_муратканович@example.com	Staff	Ахмеджанов Медет Муратканович		0	0	Ахмеджанов Медет Муратканович	Тренер	unknown_value_please_contact_support		87014710296	Алмасити	Штат	0		1	0		0
43		adema@example.com	Пушер	Асылкызы Адема		0	0	Асылкызы Адема	Тренер	unknown_value_please_contact_support		87082216212; 87470664231	Алмасити	Штат	0		1	0		0
44	964240622	zhaniya@example.com	Пушер	Аскар		1	0	Азимбаева Жания Ганимуратовна	Тренер	unknown_value_please_contact_support		87472474546	Сити +	Штат	1		1	1		1
45		кайнарбаева_зарина_касымовна@example.com	Staff	Кайнарбаева Зарина Касымовна		0	0	Кайнарбаева Зарина Касымовна	Тренер	unknown_value_please_contact_support		87022643651	Сити +	Штат	0		1	0		0
46		бейбітханқызы_нұргүл@example.com	Staff	Бейбітханқызы Нұргүл		0	0	Бейбітханқызы Нұргүл	Тренер	unknown_value_please_contact_support		87066571306	Сити +	Штат	0		1	0		0
47		марченко_алеся_алмазовна@example.com	Staff	Марченко Алеся Алмазовна		0	0	Марченко Алеся Алмазовна	лидер локации Тренер	unknown_value_please_contact_support		87015500995	Дулати	Штат	0		1	0		0
48		ванина_кристина_михайловна@example.com	Staff	Ванина Кристина Михайловна		0	0	Ванина Кристина Михайловна	Тренер	unknown_value_please_contact_support		87763272838	Дулати	Штат	0		1	0		0
49		сейфуллаев_осман@example.com	Staff	Сейфуллаев Осман		0	0	Сейфуллаев Осман	Тренер	unknown_value_please_contact_support		87007620109	Дулати, Терискей	Штат	0		1	0		0
50		кусис_анастасия_сергеевна@example.com	Staff	Кусис Анастасия Сергеевна		0	0	Кусис Анастасия Сергеевна	Тренер	unknown_value_please_contact_support		87477394393	Терискей	Штат	0		1	0		0
51		насибуллина_регина_римовна@example.com	Staff	Насибуллина Регина Римовна		0	0	Насибуллина Регина Римовна	Тренер	0		87077213568	Терискей	Штат	0		1	0		0
52		болотов_михаил_игоревич@example.com	Staff	Болотов Михаил Игоревич		0	0	Болотов Михаил Игоревич	ТимЛидер Тренер	unknown_value_please_contact_support		87781520526	unknown_value_please_contact_support	unknown_value_please_contact_support	0		1	0		0
53		тайланова_айгерім_жанбулатқызы@example.com	Staff	Тайланова Айгерім Жанбулатқызы		0	0	Тайланова Айгерім Жанбулатқызы	Тренер	unknown_value_please_contact_support		87767972278	New expo life	Штат	0		1	0		0
55		ершинов_ринат_нугманович@example.com	Staff	Ершинов Ринат Нугманович		0	0	Ершинов Ринат Нугманович	Тренер	unknown_value_please_contact_support		87085435981	New expo life	Штат	0		1	0		0
58	-1076367879	Dauletbekoffa@gmail.com	Пушер	Аскар		1	0	unknown_value_please_contact_support	unknown_value_please_contact_support	unknown_value_please_contact_support		87472474546	unknown_value_please_contact_support	unknown_value_please_contact_support	1		1	1		1
\.


--
-- Data for Name: _events; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._events (id, title, description, event_date, created_at) FROM stdin;
1	Тимбилдинг	Собираемся с коллегами	2025-08-11	2025-08-01
2	Ивент тестовый	Последний тест	2025-08-11	2025-08-11
\.


--
-- Data for Name: _group_chats; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._group_chats (id, name, chat_id) FROM stdin;
1	35 test	-2034343133
\.


--
-- Data for Name: _ideas; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._ideas (id, employee_id, text, submission_date) FROM stdin;
1	44	У меня такая идея	2025-08-11
2	44	Йоу	2025-08-11
\.


--
-- Data for Name: _onboarding_questions; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._onboarding_questions (id, role, order_index, question_text, data_key, is_required) FROM stdin;
1	Пушер	0	Привет. Мы начинаем регистрацию. Первый вопрос, как тебя зовут?	name	1
2	Пушер	0	Введи свой номер телефона	contact_info	1
3	Клининг	0	Как твое имя Тест?	name	1
4	Клининг	0	Номер контакта	contact_info	1
\.


--
-- Data for Name: _onboarding_steps; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._onboarding_steps (id, role, order_index, message_text, file_path, file_type) FROM stdin;
6	Пушер	0	Тест		
9	Admin	0		uploads/onboarding\\steps\\admin_step_IMG_3561.mp4	
10	Admin	0		uploads/onboarding\\steps\\admin_step_IMG_3561.mp4	video_note
15	Admin	0		uploads/onboarding\\steps\\admin_step_IMG_3561.mp4	video_note
16	Пушер	0		uploads/onboarding\\steps\\step__512_x_512_..mp4	video_note
18	Клининг	0		uploads/onboarding\\steps\\step__512_x_512_..mp4	video_note
\.


--
-- Data for Name: _quiz_questions; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._quiz_questions (id, role, question, answer, order_index, question_type, options) FROM stdin;
1	Admin	Точно идете?	Да	1	unknown_value_please_contact_support	
2	Hunter	Точно идете?	Да	0	unknown_value_please_contact_support	
3	Admin	Круть	Нет	0	unknown_value_please_contact_support	
4	Пушер	Точно идете?	Да	0	unknown_value_please_contact_support	
5	Пушер	Точно идете?	Да	0	choice	Да;Нет;Возможно
6	Клининг	Тестовое	Да	0	choice	Да;Нет;Возможно
7	Клининг	Точно идете?	Да	0	text	
\.


--
-- Data for Name: _reg_codes; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._reg_codes (code, email, used) FROM stdin;
1	admin@healthclub.local	1
20040058	dauletbekoffa@gmail.com	1
20020059	Akoo@gmail.com	0
25359563	ako@gmail.com	1
60004769	Dauletbekoff@gmail.com	1
36355127	Akhmad@gmail.com	1
24006170	Dauletbekoffaa@gmail.com	0
69736665	Akhmad@gmail.com	0
89055448	Dauletbekoffa@gmail.com	0
22484242	Dauletbekoffa@gmail.com	1
84697377	akhmad@gmail.com	0
65517483	akhmad@gmail.com	0
22287843	akhmad@gmail.com	1
33452416	Dauletbekoffa@gmail.com	1
3352148	Dauletbekoffa@gmail.com	1
4992009	Dauletbekoffa@gmail.com	1
24063061	Dauletbekoffa@gmail.com	1
16803686	Dauletbekoffa@gmail.com	0
87238382	Dauletbekoffa@gmail.com	1
29468128	Dauletbekoffa@gmail.com	1
88212879	Dauletbekoffa@gmail.com	1
96156876	Dauletbekoffa@gmail.com	1
87761363	Dauletbekoffa@gmail.com	1
2803737	азимбаева_жания_ганимуратовна@example.com	1
20907978	амирханов_нурмухаммед@example.com	0
71046651	амирханова_дильназ@example.com	0
28433495	асылкызы_адема@example.com	0
52707522	ахмеджанов_медет_муратканович@example.com	0
24906139	багдатов_дидар_арманулы@example.com	0
64096260	батталова_альфия@example.com	0
60330097	батырбеков_алмас@example.com	0
71775759	баядилов_мейржан@example.com	0
58200227	бақдаулетқызы_әсел@example.com	0
20993431	бейбітханқызы_нұргүл@example.com	0
46725767	yelena@example.com	0
41580755	бисемалиева_алина@example.com	0
38088999	болатов_мирас_қайратұлы@example.com	0
20903013	болотов_михаил_игоревич@example.com	0
13034684	ванина_кристина_михайловна@example.com	0
16751254	васильев_иван_сергеевич@example.com	0
94062530	гладченко_анастасия_евгеньевна@example.com	0
81655705	гусев_данил_владиславович@example.com	0
93781002	джамалов_жанади_жанатович@example.com	0
17271191	джумахан_ырысжан_бақытжанқызы@example.com	0
21137783	дроздов_руслан_васильевич@example.com	0
31642034	дударев_данил@example.com	0
60551688	ермуханбет_айбар_бейбітұлы@example.com	0
68208761	ершинов_ринат_нугманович@example.com	0
1600132	естенов_едиль@example.com	0
51799010	жалгасбай_айдана_мухтаркызы@example.com	0
40142482	жеткизгенова_акбобек_тилеккызы@example.com	0
3225053	жетпіс_дияс_ертайұлы@example.com	0
6911053	жолбаева_акмейир@example.com	0
77382132	жубаназаров_нурбек_байболсынович@example.com	0
21044982	ибрагимов_раджив_хачиханович@example.com	0
31716632	искаков_аскар@example.com	0
47030323	искаков_мирас_мейрамович@example.com	0
12912721	кадырова_гузель_шатликовна@example.com	0
3164802	кайнарбаева_зарина_касымовна@example.com	0
99722546	калоев_асланбек_казбекович@example.com	0
1163708	константинов_виктор_евгеньевич@example.com	0
83806096	кузнецов_андрей_олегович@example.com	0
7621752	кусис_анастасия_сергеевна@example.com	0
6719999	марченко_алеся_алмазовна@example.com	0
70865554	махмутов_максим_маратович@example.com	0
962934	мукаш_аружан_мураткызы@example.com	0
1475076	мухаметжанова_галина_андреевна@example.com	0
5097259	насибуллина_регина_римовна@example.com	0
44593062	озбек_дамир_маратулы@example.com	0
83861453	оразбай_галымжан_бауыржанулы@example.com	0
61178373	пакалин_даниил_владимирович@example.com	0
21922271	рашидинова_шаира_садирдиновна@example.com	0
55387044	саламат_алиосман_рустемулы@example.com	0
50442894	сейфуллаев_осман@example.com	0
21051563	сергеев_сергей_вячеславович@example.com	0
42484003	сыдык_айбар_берикуелы@example.com	0
96145836	сычёв_родион_валерьевич@example.com	0
3546708	тайланова_айгерім_жанбулатқызы@example.com	0
42802877	усенов_адиль_аскарович@example.com	1
99816233	азимбаева_жания_ганимуратовна@example.com	1
61232785	usenov@example.com	1
26624039	zhaniya@example.com	1
1190725	Dauletbekoffa@gmail.com	1
617249	zhaniya@example.com	1
51440529	zhaniya@example.com	1
65433146	adema@example.com	0
\.


--
-- Data for Name: _role_guides; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._role_guides (id, role, title, content, file_path, order_index) FROM stdin;
1	Пушер	Тестовое	Тестовое		0
\.


--
-- Data for Name: _role_onboarding; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._role_onboarding (id, role, text, file_path, file_type) FROM stdin;
1	Пушер	Привет. Ознакомься с данным материалом	uploads/onboarding\\intro.mp4	video_note
2	Admin			document
3	Клининг	Тестовое клининг, какой то текст	uploads/onboarding\\2025-07-24_092428.png	document
\.


--
-- Data for Name: _roles; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._roles (id, name) FROM stdin;
1	Admin
2	Hunter
5	Клининг
3	Пушер
4	Тренер
\.


--
-- Data for Name: _sqlite_sequence; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._sqlite_sequence (name, seq) FROM stdin;
onboarding_questions	4
onboarding_steps	18
employee_custom_data	22
\.


--
-- Data for Name: _topics; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._topics (id, title, content, category, image_path) FROM stdin;
1	ð О компа	<b>Наша миссия:</b> .\n\n<b>Наши ценности:</b>\n1. <i>Открытость</i> - \n2. <i>Развитие</i> - \n3. <i>Результат</i> - \n\nПосмотреть полную <b>презентацию о компании</b> можно по ссылке:\n<a href=''>Презентация компании</a>	База знаний	unknown_value_please_contact_support
2	ð Официальное оформле	Для официального оформления по ТК РК всех штатных сотрудников, пожалуйста, подготовьте следующие документы:\n• Заявление на приём (от руки)\n• Скан удостоверения личности\n• Справка из психдиспансера\n• Справка из наркологического диспансера\n• Справка об отсутствии судимости\n\n❗️Все справки можно быстро получить через Kaspi и Егов — это займёт 10–15 минут.\n\nПосле подготовки документов, заполните анкету по ссылке:\n<a href=''>Форма для оформления</a>\n\nОстались вопросы? Напишите нашему HR-менеджеру!\n	База знаний	static/images/photo_2025-07-25_15-56-47.jpg
3	ð Бонусы и програ	<b>Реферальная программа:</b>\nПриведи друга на открытую вакансию и получи бонус! Подробные условия и список вакансий можно найти здесь:\n<a href=''>Условия реферальной программы</a>\n\n<b>Корпоративные скидки:</b>\nНаши сотрудники получают скидки у партнеров. Список актуальных предложений (фитнес, обучение, кафе) находится тут:\n<a href=''>Список партнерских скидок</a>	База знаний	unknown_value_please_contact_support
4	ð¬ Наши чаты и ресу	<b>Наши внутренние чаты:</b>\n• <a href=''>Backstage (Telegram)</a> - наш главный чат для общения.\n• <a href=''>WhatsApp-группа</a> - для срочных оповещений.\n• <a href=''>Флудилка</a> - для мемов и разговоров не по работе.\n\n<b>Общие ресурсы:</b>\nВсе регламенты, таблицы и чек-листы хранятся на нашем общем диске:\n• <a href=''>Общий диск компании</a>\n\n<b>Фотоальбом:</b>\nВспоминаем лучшие моменты вместе! Ссылка на наш общий фотоальбом:\n• <a href=''>Корпоративный фотоальбом</a>	База знаний	unknown_value_please_contact_support
5	ð Традиции и культ	<b>Наши традиции:</b>\n• <b>По четвергам</b> мы .\n• <b>Традиции по городам:</b> В Алматы мы..., в Астане мы...\n• <b>Поздравления:</b> Мы поздравляем коллег с днем рождения в общем чате и дарим подарки. Отдыхаем на всех официальных праздниках!\n\n<b>Отзывы и активности:</b>\nПочитать отзывы о наших тимбилдингах и посмотреть фото можно в специальном разделе:\n<a href=''>Отзывы о внутренних активностях</a>	База знаний	unknown_value_please_contact_support
7	ð§  Корпоративный слов	Наш внутренний язык, который помогает быть на одной волне:\n\nð <b>«Backstage»</b> — <i>наш главный командный чат в Telegram.</i>\n\nð¤ <b>«Вайб-дэй»</b> — <i>еженедельная неформальная встреча команды по пятницам для обмена новостями.</i>\n\nð <b>«ЦКП»</b> — <i>Цели и Ключевые Показатели, наши ориентиры в работе.</i>\n\nð <b>«Спикинг»</b> — <i>Speaking Club, еженедельная практика английского языка.</i>\n\nð¡ <i>Этот словарь можно и нужно дополнять! Предлагайте свои термины в 	База знаний	unknown_value_please_contact_support
8	Тестовое	Тестовое для ако	База знаний	uploads/topics\\2025-07-24_092428.png
\.


--
-- Data for Name: _training_material; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._training_material (id, role, title, content, file_path) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

