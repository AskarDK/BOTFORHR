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



--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--



SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: _alembic_version; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._alembic_version (
    version_num character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._alembic_version OWNER TO hrbot_user;

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


ALTER TABLE public._archived_attendance OWNER TO hrbot_user;

--
-- Name: _archived_employees; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._archived_employees (
    id smallint,
    telegram_id character varying(11) DEFAULT NULL::character varying,
    email character varying(100) DEFAULT NULL::character varying,
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


ALTER TABLE public._archived_employees OWNER TO hrbot_user;

--
-- Name: _archived_ideas; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._archived_ideas (
    id smallint,
    employee_id smallint,
    idea_text character varying(3) DEFAULT NULL::character varying,
    submission_date character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._archived_ideas OWNER TO hrbot_user;

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


ALTER TABLE public._attendance OWNER TO hrbot_user;

--
-- Name: _bot_texts; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._bot_texts (
    id character varying(34) DEFAULT NULL::character varying,
    text character varying(294) DEFAULT NULL::character varying,
    description character varying(140) DEFAULT NULL::character varying
);


ALTER TABLE public._bot_texts OWNER TO hrbot_user;

--
-- Name: _employee_custom_data; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._employee_custom_data (
    id smallint,
    employee_id smallint,
    data_key character varying(12) DEFAULT NULL::character varying,
    data_value character varying(11) DEFAULT NULL::character varying
);


ALTER TABLE public._employee_custom_data OWNER TO hrbot_user;

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


ALTER TABLE public._employees OWNER TO hrbot_user;

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


ALTER TABLE public._events OWNER TO hrbot_user;

--
-- Name: _group_chats; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._group_chats (
    id smallint,
    name character varying(7) DEFAULT NULL::character varying,
    chat_id bigint
);


ALTER TABLE public._group_chats OWNER TO hrbot_user;

--
-- Name: _ideas; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._ideas (
    id smallint,
    employee_id smallint,
    text character varying(17) DEFAULT NULL::character varying,
    submission_date character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._ideas OWNER TO hrbot_user;

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


ALTER TABLE public._onboarding_questions OWNER TO hrbot_user;

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


ALTER TABLE public._onboarding_steps OWNER TO hrbot_user;

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


ALTER TABLE public._quiz_questions OWNER TO hrbot_user;

--
-- Name: _reg_codes; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._reg_codes (
    code integer,
    email character varying(44) DEFAULT NULL::character varying,
    used smallint
);


ALTER TABLE public._reg_codes OWNER TO hrbot_user;

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


ALTER TABLE public._role_guides OWNER TO hrbot_user;

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


ALTER TABLE public._role_onboarding OWNER TO hrbot_user;

--
-- Name: _roles; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._roles (
    id smallint,
    name character varying(7) DEFAULT NULL::character varying
);


ALTER TABLE public._roles OWNER TO hrbot_user;

--
-- Name: _sqlite_sequence; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._sqlite_sequence (
    name character varying(20) DEFAULT NULL::character varying,
    seq smallint
);


ALTER TABLE public._sqlite_sequence OWNER TO hrbot_user;

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


ALTER TABLE public._topics OWNER TO hrbot_user;

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


ALTER TABLE public._training_material OWNER TO hrbot_user;

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
54		Р°РјРёСЂС…Р°РЅРѕРІР°_РґРёР»СЊРЅР°Р·@example.com	Staff	РђРјРёСЂС…Р°РЅРѕРІР° Р”РёР»СЊРЅР°Р·		0	0	0								2025-08-11	
56		Р°РјРёСЂС…Р°РЅРѕРІ_РЅСѓСЂРјСѓС…Р°РјРјРµРґ@example.com	Staff	РђРјРёСЂС…Р°РЅРѕРІ РќСѓСЂРјСѓС…Р°РјРјРµРґ		0	0	0								2025-08-11	
58	-1076367879	dauletbekoffa@gmail.com	Hunter	РђСЃРєР°СЂ Р”Р°СѓР»РµС‚Р±РµРє		1	1	1								2025-08-05	
61	-1076367879	Dauletbekoff@gmail.com	Hunter	РђСЃРєР°СЂ		1	0	1								2025-08-05	
63		Dauletbekoffaa@gmail.com	Admin	Askar Dauletbek		0	0	0								2025-08-05	
64	-1076367879	Dauletbekoffa@gmail.com	РџСѓС€РµСЂ	Askar Dauletbek		1	0	1								2025-08-07	63
65	1267651407	ako@gmail.com	Hunter	РђРєРЅРёРµС‚		1	0	1								2025-08-07	60
66		Akoo@gmail.com	Trainer	Akmeyir		0	0	0								2025-08-07	59
67		Akhmad@gmail.com	Hunter	Akhmad		0	0	1								2025-08-07	62
68	-1076367879	akhmad@gmail.com	РџСѓС€РµСЂ	РђСЃРєР°СЂ		1	0	1								2025-08-07	58
69	-1076367879	Dauletbekoffa@gmail.com	РџСѓС€РµСЂ	РђСЃРєР°СЂ		1	0	0								2025-08-07	58
70	-1076367879	Dauletbekoffa@gmail.com	РџСѓС€РµСЂ	РђСЃРєР°СЂ		1	0	0								2025-08-07	58
71	-1076367879	usenov@example.com	РџСѓС€РµСЂ	РђРґРёР»СЊ		1	0	1								2025-08-11	3
72	964240622	admin@healthclub.local	Admin	РСЃРєР°РєРѕРІ РђСЃРєР°СЂ		1	0	1								2025-08-11	57
\.


--
-- Data for Name: _archived_ideas; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._archived_ideas (id, employee_id, idea_text, submission_date) FROM stdin;
1	58	Р•Р№	2025-08-07
2	58	Р™РѕСѓ	2025-08-07
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
account_deactivated	Р’Р°С€ Р°РєРєР°СѓРЅС‚ Р±С‹Р» РґРµР°РєС‚РёРІРёСЂРѕРІР°РЅ. РћР±СЂР°С‚РёС‚РµСЃСЊ Рє Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂСѓ.	РЎРѕРѕР±С‰РµРЅРёРµ РґР»СЏ СѓРІРѕР»РµРЅРЅРѕРіРѕ СЃРѕС‚СЂСѓРґРЅРёРєР°
welcome_back	РЎ РІРѕР·РІСЂР°С‰РµРЅРёРµРј, {name}!	РџСЂРёРІРµС‚СЃС‚РІРёРµ РґР»СЏ СЃРѕС‚СЂСѓРґРЅРёРєР°, РєРѕС‚РѕСЂС‹Р№ СѓР¶Рµ РїСЂРѕС€РµР» РѕРЅР±РѕСЂРґРёРЅРі
training_not_passed_prompt	РџСЂРёРІРµС‚! Р§С‚РѕР±С‹ РїРѕР»СѓС‡РёС‚СЊ РґРѕСЃС‚СѓРї РєРѕ РІСЃРµРј С„СѓРЅРєС†РёСЏРј Р±РѕС‚Р°, РѕСЃС‚Р°Р»РѕСЃСЊ РїСЂРѕР№С‚Рё С‚СЂРµРЅРёРЅРі.	РќР°РїРѕРјРёРЅР°РЅРёРµ Рѕ РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё РїСЂРѕР№С‚Рё С‚СЂРµРЅРёРЅРі
onboarding_not_finished	РџРѕС…РѕР¶Рµ, РІС‹ РЅРµ Р·Р°РєРѕРЅС‡РёР»Рё Р·РЅР°РєРѕРјСЃС‚РІРѕ. Р”Р°РІР°Р№С‚Рµ РїСЂРѕРґРѕР»Р¶РёРј!	Р•СЃР»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РїРµСЂРµР·Р°РїСѓСЃС‚РёР» Р±РѕС‚Р° РІРѕ РІСЂРµРјСЏ РѕРЅР±РѕСЂРґРёРЅРіР°
enter_reg_code	Р—РґСЂР°РІСЃС‚РІСѓР№С‚Рµ! РџРѕР¶Р°Р»СѓР№СЃС‚Р°, РІРІРµРґРёС‚Рµ РІР°С€ 8-Р·РЅР°С‡РЅС‹Р№ СЂРµРіРёСЃС‚СЂР°С†РёРѕРЅРЅС‹Р№ РєРѕРґ РєРѕС‚РѕСЂС‹Р№ РІР°Рј РІС‹РґР°Р» СЂРµРєСЂСѓС‚РµСЂ:	РџРµСЂРІРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ РЅРѕРІРѕРјСѓ РїРѕР»СЊР·РѕРІР°С‚РµР»СЋ
code_accepted	РљРѕРґ РїСЂРёРЅСЏС‚! Г°ВџВЋВ‰ Р”Р°РІР°Р№С‚Рµ РїРѕР·РЅР°РєРѕРјРёРј	РЎРѕРѕР±С‰РµРЅРёРµ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ РІРІРѕРґР° РєРѕРґР°
company_introduction_start	РћС‚Р»РёС‡РЅРѕ! РўРµРїРµСЂСЊ РЅРµРјРЅРѕРіРѕ Рѕ РєРѕРјРїР°РЅРёРё.	РќР°С‡Р°Р»Рѕ Р±Р»РѕРєР° 'Р—РЅР°РєРѕРјСЃС‚РІРѕ СЃ РєРѕРјРїР°РЅРёРµР№'
training_prompt_after_onboarding	Р—РЅР°РєРѕРјСЃС‚РІРѕ Р·Р°РІРµСЂС€РµРЅРѕ! РўРµРїРµСЂСЊ РЅСѓР¶РЅРѕ РїСЂРѕР№С‚Рё С„РёРЅР°Р»СЊРЅС‹Р№ С‚СЂРµРЅРёРЅРі.	РџСЂРµРґР»РѕР¶РµРЅРёРµ РїСЂРѕР№С‚Рё С‚СЂРµРЅРёРЅРі РїРѕСЃР»Рµ РѕРЅР±РѕСЂРґРёРЅРіР°
access_denied_training_required	РџРѕР¶Р°Р»СѓР№СЃС‚Р°, Р·Р°РІРµСЂС€РёС‚Рµ С‚СЂРµРЅРёРЅРі, С‡С‚РѕР±С‹ РїРѕР»СѓС‡РёС‚СЊ РґРѕСЃС‚СѓРї Рє СЌС‚РѕРјСѓ СЂР°Р·РґРµР»Сѓ.	РЎРѕРѕР±С‰РµРЅРёРµ РїСЂРё РїРѕРїС‹С‚РєРµ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ С„СѓРЅРєС†РёСЋ Р±РµР· РїСЂРѕР№РґРµРЅРЅРѕРіРѕ С‚СЂРµРЅРёРЅРіР°
birthday_greeting	Г°ВџВЋВ‚ РЎРµРіРѕРґРЅСЏ Сѓ {name} ({role}) РґРµРЅСЊ СЂРѕР¶РґРµРЅРёСЏ! РџРѕР·РґСЂР°РІР»СЏРµРј	РџРѕР·РґСЂР°РІР»РµРЅРёРµ СЃ Р”Р  РІ РѕР±С‰РµРј С‡Р°С‚Рµ
new_event_announcement	Г°ВџВЋВ‰ <b>РђРЅРѕРЅСЃ РЅРѕРІРѕРіРѕ РёРІРµРЅС‚Р°!</b> Г°ВџВЋВ‰\n\n<b>{title}</b>\n\n<i>{description}</i>\n\n<b>РљРѕРіРґР°:</b> {date}\n\nР–РґС‘Рј	РЈРІРµРґРѕРјР»РµРЅРёРµ Рѕ РЅРѕРІРѕРј РёРІРµРЅС‚Рµ РІ РѕР±С‰РµРј С‡Р°С‚Рµ
quiz_success_message	Г°ВџВЋВ‰ РџРѕР·РґСЂР°РІР»СЏРµРј, {name}! Р’С‹ СѓСЃРїРµС€РЅРѕ РїСЂРѕС€Р»Рё РєРІРёР· ({correct}/{total})! РўРµРїРµСЂСЊ РІР°Рј РґРѕСЃС‚СѓРїРµРЅ РІРµСЃСЊ С„СѓРЅРєС†РёРѕРЅ	РЎРѕРѕР±С‰РµРЅРёРµ РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РєРІРёР·Р°. Р”РѕСЃС‚СѓРїРЅС‹Рµ РїРµСЂРµРјРµРЅРЅС‹Рµ: {name}, {correct}, {total}.
group_join_success_message	РћС‚Р»РёС‡РЅРѕ, РјС‹ РІРёРґРёРј, С‡С‚Рѕ РІС‹ СѓР¶Рµ РІ РЅР°С€РµРј РѕР±С‰РµРј С‡Р°С‚Рµ! Р”РѕР±СЂРѕ РїРѕР¶Р°Р»РѕРІР°С‚СЊ РІ РєРѕРјР°РЅРґСѓ, С‚РµРїРµСЂСЊ РІР°Рј РґРѕСЃС‚СѓРїРµРЅ РІРµСЃСЊ С„СѓРЅРєС†РёРѕРЅР°Р». Г°	РЎРѕРѕР±С‰РµРЅРёРµ, РµСЃР»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РїСЂРѕС€РµР» РєРІРёР· Рё СѓР¶Рµ СЃРѕСЃС‚РѕРёС‚ РІ РѕР±С‰РµРј С‡Р°С‚Рµ.
group_join_prompt_message	РћСЃС‚Р°Р»СЃСЏ РїРѕСЃР»РµРґРЅРёР№ С€Р°Рі вЂ” РІСЃС‚СѓРїРёС‚Рµ РІ РЅР°С€ РѕСЃРЅРѕРІРЅРѕР№ СЂР°Р±РѕС‡РёР№ С‡Р°С‚, С‡С‚РѕР±С‹ Р±С‹С‚СЊ РІ РєСѓСЂСЃРµ РІСЃРµС… СЃРѕР±С‹С‚РёР№: https://t.me/+kvhVYarAmi1jNzNi	РЎРѕРѕР±С‰РµРЅРёРµ, РµСЃР»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РїСЂРѕС€РµР» РєРІРёР·, РЅРѕ РµС‰Рµ РЅРµ РІ РѕР±С‰РµРј С‡Р°С‚Рµ. Р’РђР–РќРћ: РІСЂСѓС‡РЅСѓСЋ Р·Р°РјРµРЅРёС‚Рµ {group_link} РЅР° СЂРµР°Р»СЊРЅСѓСЋ СЃСЃС‹Р»РєСѓ-РїСЂРёРіР»Р°С€РµРЅРёРµ РІ С‡Р°С‚.
welcome_to_common_chat	Г°ВџВ’ВЄ Р”РѕР±СЂРѕ РїРѕР¶Р°Р»РѕРІР°С‚СЊ РІ 35 Health Clubs!\r\nРЎРµРіРѕРґРЅСЏ РЅР°С€Р° РєРѕРјР°РЅРґР° СЃС‚Р°Р»Р° СЃРёР»СЊРЅРµРµ вЂ” Рє РЅР°Рј РїСЂРёСЃРѕРµРґРёРЅРёР»СЃСЏ(Р°СЃСЊ) <b>{name}</b> РЅР° РїРѕР·РёС†РёСЋ <b>{role}</b>.\r\nРњС‹ СѓРІРµСЂРµРЅС‹, С‡С‚Рѕ РІРїРµСЂРµРґРё РЅР°СЃ Р¶РґС‘С‚ РјРЅРѕРіРѕ РёРЅС‚РµСЂРµСЃРЅС‹С… РїСЂРѕРµРєС‚РѕРІ, СЌРЅРµСЂРіРёС‡РЅС‹С… С‚СЂРµРЅРёСЂРѕРІРѕРє Рё РїРѕР±РµРґ! Р–РµР»Р°РµРј Р»С‘РіРєРѕР№ Р°РґР°РїС‚Р°С†РёРё, РїРѕРґРґРµСЂР¶РєРё РєРѕР»Р»РµРі Рё РјРѕС‰РЅРѕРіРѕ СЃС‚Р°СЂС‚Р°	РЎРѕРѕР±С‰РµРЅРёРµ РІ РѕР±С‰РµРј С‡Р°С‚Рµ РїСЂРё РІСЃС‚СѓРїР»РµРЅРёРё РЅРѕРІРѕРіРѕ СЃРѕС‚СЂСѓРґРЅРёРєР°. Р”РѕСЃС‚СѓРїРЅС‹Рµ РїРµСЂРµРјРµРЅРЅС‹Рµ: {user_mention}, {user_name}.
employee_dismissed_announcement	Г°ВџВ’В™ РЎРїР°СЃРёР±Рѕ, С‡С‚Рѕ Р±С‹Р»Рё С‡Р°СЃС‚СЊСЋ РєРѕРјР°РЅРґС‹ 35 Health Clubs\r\nРЎРµРіРѕРґРЅСЏ РјС‹ РїСЂРѕС‰Р°РµРјСЃСЏ СЃ {name} ({role}) .\r\nРЎРїР°СЃРёР±Рѕ Р·Р° РІР°С€ РІРєР»Р°Рґ, РёРґРµРё Рё СЌРЅРµСЂРіРёСЋ, РєРѕС‚РѕСЂСѓСЋ РІС‹ РѕС‚РґР°РІР°Р»Рё РєРѕРјРїР°РЅРёРё Рё РЅР°С€РёРј РєР»РёРµРЅС‚Р°Рј. Р–РµР»Р°РµРј, С‡С‚РѕР±С‹ РІРїРµСЂРµРґРё Р±С‹Р»Рё С‚РѕР»СЊРєРѕ РЅРѕРІС‹Рµ РїРѕР±РµРґС‹, РёРЅС‚РµСЂРµСЃРЅС‹Рµ РїСЂРѕРµРєС‚С‹ Рё РІРґРѕС…РЅРѕРІР»СЏСЋС‰РёРµ Р»СЋРґРё	РЎРѕРѕР±С‰РµРЅРёРµ РїСЂРё СѓРІРѕР»СЊРЅРµРЅРёР№
employee_role_changed_announcement	Г°ВџВљВЂ РљР°СЂСЊРµСЂРЅС‹Р№ СЂРѕСЃС‚ РІ 35 Health Clubs\r\nРџРѕР·РґСЂР°РІР»СЏРµРј <b>{name}</b> СЃ РїРµСЂРµС…РѕРґРѕРј РЅР° РЅРѕРІСѓСЋ РїРѕР·РёС†РёСЋ вЂ” <b>{new}</b>!\r\nР­С‚Рѕ РЅРѕРІС‹Р№ СЌС‚Р°Рї, РЅРѕРІС‹Рµ Р·Р°РґР°С‡Рё Рё РЅРѕРІС‹Рµ РіРѕСЂРёР·РѕРЅС‚С‹. РњС‹ РІРµСЂРё	РЎРјРµРЅР° СЃРїРµС†РёР°Р»СЊРЅРѕСЃС‚Рё
\.


--
-- Data for Name: _employee_custom_data; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._employee_custom_data (id, employee_id, data_key, data_value) FROM stdin;
13	3	name	РђРґРёР»СЊ
14	3	contact_info	87078229829
17	58	name	РђСЃРєР°СЂ
18	58	contact_info	87472474546
21	44	name	РђСЃРєР°СЂ
22	44	contact_info	87472474546
\.


--
-- Data for Name: _employees; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._employees (id, telegram_id, email, role, name, birthday, registered, greeted, full_name, "position", contract_number, employment_date, contact_info, branch, cooperation_format, training_passed, last_seen, is_active, onboarding_completed, photo_file_id, joined_main_chat) FROM stdin;
1		Р±Р°С‚С‹СЂР±РµРєРѕРІ_Р°Р»РјР°СЃ@example.com	Staff	Р‘Р°С‚С‹СЂР±РµРєРѕРІ РђР»РјР°СЃ		0	0	Р‘Р°С‚С‹СЂР±РµРєРѕРІ РђР»РјР°СЃ	Р”РёСЂРµРєС‚РѕСЂ	unknown_value_please_contact_support		87762886229	unknown_value_please_contact_support	РџР°СЂС‚РЅРµСЂ	0		1	0		0
2		РёСЃРєР°РєРѕРІ_Р°СЃРєР°СЂ@example.com	Staff	РСЃРєР°РєРѕРІ РђСЃРєР°СЂ		0	0	РСЃРєР°РєРѕРІ РђСЃРєР°СЂ	Р”РёСЂРµРєС‚РѕСЂ	unknown_value_please_contact_support		87078223464	unknown_value_please_contact_support	РџР°СЂС‚РЅРµСЂ	0		1	0		0
4		yelena@example.com	Admin	Р‘РµР»РѕРєРѕРЅСЊ Р•Р»РµРЅР°		0	0	Р‘РµР»РѕРєРѕРЅСЊ Р•Р»РµРЅР°	РљРѕРјРјРµСЂС‡РµСЃРєРёР№ РґРёСЂРµРєС‚РѕСЂ	unknown_value_please_contact_support		87052506005	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
5		РёР±СЂР°РіРёРјРѕРІ_СЂР°РґР¶РёРІ_С…Р°С‡РёС…Р°РЅРѕРІРёС‡@example.com	Staff	РР±СЂР°РіРёРјРѕРІ Р Р°РґР¶РёРІ РҐР°С‡РёС…Р°РЅРѕРІРёС‡		0	0	РР±СЂР°РіРёРјРѕРІ Р Р°РґР¶РёРІ РҐР°С‡РёС…Р°РЅРѕРІРёС‡	Р“РµРЅРµСЂР°Р»СЊРЅС‹Р№ Р”РёСЂРµРєС‚РѕСЂ	unknown_value_please_contact_support		87011007557	unknown_value_please_contact_support	Р’РЅРµС€С‚Р°С‚РЅРѕРµ	0		1	0		0
6		РёСЃРєР°РєРѕРІ_РјРёСЂР°СЃ_РјРµР№СЂР°РјРѕРІРёС‡@example.com	Staff	РСЃРєР°РєРѕРІ РњРёСЂР°СЃ РњРµР№СЂР°РјРѕРІРёС‡		0	0	РСЃРєР°РєРѕРІ РњРёСЂР°СЃ РњРµР№СЂР°РјРѕРІРёС‡	РћРїРµСЂР°С†РёРѕРЅРЅС‹Р№ Р СѓРєРѕРІРѕРґРёС‚РµР»СЊ	unknown_value_please_contact_support		87079017029	unknown_value_please_contact_support	РЁС‚Р°С‚	0		1	0		0
7		Р¶РѕР»Р±Р°РµРІР°_Р°РєРјРµР№РёСЂ@example.com	Staff	Р–РѕР»Р±Р°РµРІР° РђРєРјРµР№РёСЂ		0	0	Р–РѕР»Р±Р°РµРІР° РђРєРјРµР№РёСЂ	РњРµРЅРµРґР¶РµСЂ РїРѕ СѓРїСЂР°РІР»РµРЅРёСЋ РїРµСЂСЃРѕРЅР°Р»Р°	unknown_value_please_contact_support		87006984741	unknown_value_please_contact_support	Р’РЅРµС€С‚Р°С‚РЅРѕРµ	0		1	0		0
8		Р±РёСЃРµРјР°Р»РёРµРІР°_Р°Р»РёРЅР°@example.com	Staff	Р‘РёСЃРµРјР°Р»РёРµРІР° РђР»РёРЅР°		0	0	Р‘РёСЃРµРјР°Р»РёРµРІР° РђР»РёРЅР°	РњРµРЅРµРґР¶РµСЂ РїРѕ РїРѕРґР±РѕСЂСѓ РїРµСЂСЃРѕРЅР°Р»Р°	unknown_value_please_contact_support		87006488667	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
9		РєР°РґС‹СЂРѕРІР°_РіСѓР·РµР»СЊ_С€Р°С‚Р»РёРєРѕРІРЅР°@example.com	Staff	РљР°РґС‹СЂРѕРІР° Р“СѓР·РµР»СЊ РЁР°С‚Р»РёРєРѕРІРЅР°		0	0	РљР°РґС‹СЂРѕРІР° Р“СѓР·РµР»СЊ РЁР°С‚Р»РёРєРѕРІРЅР°	РЎРњРњ-РјРµРЅРµРґР¶РµСЂ	unknown_value_please_contact_support		87770267798	unknown_value_please_contact_support	Р’РЅРµС€С‚Р°С‚РЅРѕРµ	0		1	0		0
10		Р¶Р°Р»РіР°СЃР±Р°Р№_Р°Р№РґР°РЅР°_РјСѓС…С‚Р°СЂРєС‹Р·С‹@example.com	Staff	Р–Р°Р»РіР°СЃР±Р°Р№ РђР№РґР°РЅР° РњСѓС…С‚Р°СЂРєС‹Р·С‹		0	0	Р–Р°Р»РіР°СЃР±Р°Р№ РђР№РґР°РЅР° РњСѓС…С‚Р°СЂРєС‹Р·С‹	РњРµРЅРµРґР¶РµСЂ РїРѕ СЂР°Р±РѕС‚Рµ СЃ Р±Р»РѕРіРµСЂР°РјРё	unknown_value_please_contact_support		87780420175	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
11		Р±Р°РіРґР°С‚РѕРІ_РґРёРґР°СЂ_Р°СЂРјР°РЅСѓР»С‹@example.com	Staff	Р‘Р°РіРґР°С‚РѕРІ Р”РёРґР°СЂ РђСЂРјР°РЅСѓР»С‹		0	0	Р‘Р°РіРґР°С‚РѕРІ Р”РёРґР°СЂ РђСЂРјР°РЅСѓР»С‹	РўР°СЂРіРµС‚РѕР»РѕРі	unknown_value_please_contact_support		87477750115	unknown_value_please_contact_support	Р’РЅРµС€С‚Р°С‚РЅРѕРµ	0		1	0		0
12		РїР°РєР°Р»РёРЅ_РґР°РЅРёРёР»_РІР»Р°РґРёРјРёСЂРѕРІРёС‡@example.com	Staff	РџР°РєР°Р»РёРЅ Р”Р°РЅРёРёР» Р’Р»Р°РґРёРјРёСЂРѕРІРёС‡		0	0	РџР°РєР°Р»РёРЅ Р”Р°РЅРёРёР» Р’Р»Р°РґРёРјРёСЂРѕРІРёС‡	Р’РёРґРµРѕРіСЂР°С„	unknown_value_please_contact_support		87066355661	unknown_value_please_contact_support	Р’РЅРµС€С‚Р°С‚РЅРѕРµ	0		1	0		0
13		РѕСЂР°Р·Р±Р°Р№_РіР°Р»С‹РјР¶Р°РЅ_Р±Р°СѓС‹СЂР¶Р°РЅСѓР»С‹@example.com	Staff	РћСЂР°Р·Р±Р°Р№ Р“Р°Р»С‹РјР¶Р°РЅ Р‘Р°СѓС‹СЂР¶Р°РЅСѓР»С‹		0	0	РћСЂР°Р·Р±Р°Р№ Р“Р°Р»С‹РјР¶Р°РЅ Р‘Р°СѓС‹СЂР¶Р°РЅСѓР»С‹	Р’РµР±-РґРёР·Р°Р№РЅРµСЂ	unknown_value_please_contact_support		87002789479	unknown_value_please_contact_support	Р’РЅРµС€С‚Р°С‚РЅРѕРµ	0		1	0		0
14		Р¶РµС‚РєРёР·РіРµРЅРѕРІР°_Р°РєР±РѕР±РµРє_С‚РёР»РµРєРєС‹Р·С‹@example.com	Staff	Р–РµС‚РєРёР·РіРµРЅРѕРІР° РђРєР±РѕР±РµРє РўРёР»РµРєРєС‹Р·С‹		0	0	Р–РµС‚РєРёР·РіРµРЅРѕРІР° РђРєР±РѕР±РµРє РўРёР»РµРєРєС‹Р·С‹	РњРµРЅРµРґР¶РµСЂ РєРѕРЅС‚СЂРѕР»СЏ Рё РєР°С‡РµСЃС‚РІР°	unknown_value_please_contact_support		87089798991	unknown_value_please_contact_support	Р’РЅРµС€С‚Р°С‚РЅРѕРµ	0		1	0		0
15		РµСЃС‚РµРЅРѕРІ_РµРґРёР»СЊ@example.com	Staff	Р•СЃС‚РµРЅРѕРІ Р•РґРёР»СЊ		0	0	Р•СЃС‚РµРЅРѕРІ Р•РґРёР»СЊ	РўРёРјР»РёРґРµСЂ РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87713168526	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
16		СЃР°Р»Р°РјР°С‚_Р°Р»РёРѕСЃРјР°РЅ_СЂСѓСЃС‚РµРјСѓР»С‹@example.com	Staff	РЎР°Р»Р°РјР°С‚ РђР»РёРѕСЃРјР°РЅ Р СѓСЃС‚РµРјСѓР»С‹		0	0	РЎР°Р»Р°РјР°С‚ РђР»РёРѕСЃРјР°РЅ Р СѓСЃС‚РµРјСѓР»С‹	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87022754563	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
17		РјСѓРєР°С€_Р°СЂСѓР¶Р°РЅ_РјСѓСЂР°С‚РєС‹Р·С‹@example.com	Staff	РњСѓРєР°С€ РђСЂСѓР¶Р°РЅ РњСѓСЂР°С‚РєС‹Р·С‹		0	0	РњСѓРєР°С€ РђСЂСѓР¶Р°РЅ РњСѓСЂР°С‚РєС‹Р·С‹	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87072772353	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°,261	РЁС‚Р°С‚	0		1	0		0
18		Р±Р°Т›РґР°СѓР»РµС‚Т›С‹Р·С‹_У™СЃРµР»@example.com	Staff	Р‘Р°Т›РґР°СѓР»РµС‚Т›С‹Р·С‹ УСЃРµР»		0	0	Р‘Р°Т›РґР°СѓР»РµС‚Т›С‹Р·С‹ УСЃРµР»	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87072251123	unknown_value_please_contact_support	unknown_value_please_contact_support	0		1	0		0
19		РІР°СЃРёР»СЊРµРІ_РёРІР°РЅ_СЃРµСЂРіРµРµРІРёС‡@example.com	Staff	Р’Р°СЃРёР»СЊРµРІ РРІР°РЅ РЎРµСЂРіРµРµРІРёС‡		0	0	Р’Р°СЃРёР»СЊРµРІ РРІР°РЅ РЎРµСЂРіРµРµРІРёС‡	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87051315304	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
20		Р¶СѓР±Р°РЅР°Р·Р°СЂРѕРІ_РЅСѓСЂР±РµРє_Р±Р°Р№Р±РѕР»СЃС‹РЅРѕРІРёС‡@example.com	Staff	Р–СѓР±Р°РЅР°Р·Р°СЂРѕРІ РќСѓСЂР±РµРє Р‘Р°Р№Р±РѕР»СЃС‹РЅРѕРІРёС‡		0	0	Р–СѓР±Р°РЅР°Р·Р°СЂРѕРІ РќСѓСЂР±РµРє Р‘Р°Р№Р±РѕР»СЃС‹РЅРѕРІРёС‡	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87780634928	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
21		СЂР°С€РёРґРёРЅРѕРІР°_С€Р°РёСЂР°_СЃР°РґРёСЂРґРёРЅРѕРІРЅР°@example.com	Staff	Р Р°С€РёРґРёРЅРѕРІР° РЁР°РёСЂР° РЎР°РґРёСЂРґРёРЅРѕРІРЅР°		0	0	Р Р°С€РёРґРёРЅРѕРІР° РЁР°РёСЂР° РЎР°РґРёСЂРґРёРЅРѕРІРЅР°	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87009919794	unknown_value_please_contact_support	Р’РЅРµС€С‚Р°С‚РЅРѕРµ	0		1	0		0
22		РіР»Р°РґС‡РµРЅРєРѕ_Р°РЅР°СЃС‚Р°СЃРёСЏ_РµРІРіРµРЅСЊРµРІРЅР°@example.com	Staff	Р“Р»Р°РґС‡РµРЅРєРѕ РђРЅР°СЃС‚Р°СЃРёСЏ Р•РІРіРµРЅСЊРµРІРЅР°		0	0	Р“Р»Р°РґС‡РµРЅРєРѕ РђРЅР°СЃС‚Р°СЃРёСЏ Р•РІРіРµРЅСЊРµРІРЅР°	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87006629814	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
23		РєР°Р»РѕРµРІ_Р°СЃР»Р°РЅР±РµРє_РєР°Р·Р±РµРєРѕРІРёС‡@example.com	Staff	РљР°Р»РѕРµРІ РђСЃР»Р°РЅР±РµРє РљР°Р·Р±РµРєРѕРІРёС‡		0	0	РљР°Р»РѕРµРІ РђСЃР»Р°РЅР±РµРє РљР°Р·Р±РµРєРѕРІРёС‡	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87770263453	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
24		РґР¶Р°РјР°Р»РѕРІ_Р¶Р°РЅР°РґРё_Р¶Р°РЅР°С‚РѕРІРёС‡@example.com	Staff	Р”Р¶Р°РјР°Р»РѕРІ Р–Р°РЅР°РґРё Р–Р°РЅР°С‚РѕРІРёС‡		0	0	Р”Р¶Р°РјР°Р»РѕРІ Р–Р°РЅР°РґРё Р–Р°РЅР°С‚РѕРІРёС‡	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87755523051	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
25		Р±Р°СЏРґРёР»РѕРІ_РјРµР№СЂР¶Р°РЅ@example.com	Staff	Р‘Р°СЏРґРёР»РѕРІ РњРµР№СЂР¶Р°РЅ		0	0	Р‘Р°СЏРґРёР»РѕРІ РњРµР№СЂР¶Р°РЅ	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87476896506	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
26		РµСЂРјСѓС…Р°РЅР±РµС‚_Р°Р№Р±Р°СЂ_Р±РµР№Р±С–С‚Т±Р»С‹@example.com	Staff	Р•СЂРјСѓС…Р°РЅР±РµС‚ РђР№Р±Р°СЂ Р‘РµР№Р±С–С‚Т±Р»С‹		0	0	Р•СЂРјСѓС…Р°РЅР±РµС‚ РђР№Р±Р°СЂ Р‘РµР№Р±С–С‚Т±Р»С‹	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87714387862	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
27		РґР¶СѓРјР°С…Р°РЅ_С‹СЂС‹СЃР¶Р°РЅ_Р±Р°Т›С‹С‚Р¶Р°РЅТ›С‹Р·С‹@example.com	Staff	Р”Р¶СѓРјР°С…Р°РЅ Р«СЂС‹СЃР¶Р°РЅ Р‘Р°Т›С‹С‚Р¶Р°РЅТ›С‹Р·С‹		0	0	Р”Р¶СѓРјР°С…Р°РЅ Р«СЂС‹СЃР¶Р°РЅ Р‘Р°Т›С‹С‚Р¶Р°РЅТ›С‹Р·С‹	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87473803311	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
28		Р±РѕР»Р°С‚РѕРІ_РјРёСЂР°СЃ_Т›Р°Р№СЂР°С‚Т±Р»С‹@example.com	Staff	Р‘РѕР»Р°С‚РѕРІ РњРёСЂР°СЃ ТљР°Р№СЂР°С‚Т±Р»С‹		0	0	Р‘РѕР»Р°С‚РѕРІ РњРёСЂР°СЃ ТљР°Р№СЂР°С‚Т±Р»С‹	РҐР°РЅС‚РµСЂ	unknown_value_please_contact_support		87711132069	РўСѓСЂРіСѓС‚ РћР·Р°Р»Р°, 261	РЁС‚Р°С‚	0		1	0		0
29		СЃС‹С‡С‘РІ_СЂРѕРґРёРѕРЅ_РІР°Р»РµСЂСЊРµРІРёС‡@example.com	Staff	РЎС‹С‡С‘РІ Р РѕРґРёРѕРЅ Р’Р°Р»РµСЂСЊРµРІРёС‡		0	0	РЎС‹С‡С‘РІ Р РѕРґРёРѕРЅ Р’Р°Р»РµСЂСЊРµРІРёС‡	РўРёРјР»РёРґРµСЂ РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87073606235	unknown_value_please_contact_support	РЁС‚Р°С‚	0		1	0		0
30		РґСЂРѕР·РґРѕРІ_СЂСѓСЃР»Р°РЅ_РІР°СЃРёР»СЊРµРІРёС‡@example.com	Staff	Р”СЂРѕР·РґРѕРІ Р СѓСЃР»Р°РЅ Р’Р°СЃРёР»СЊРµРІРёС‡		0	0	Р”СЂРѕР·РґРѕРІ Р СѓСЃР»Р°РЅ Р’Р°СЃРёР»СЊРµРІРёС‡	Р»РёРґРµСЂ Р»РѕРєР°С†РёРё РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87762082966	РЁР°С…СЂРёСЃС‚Р°РЅ	РЁС‚Р°С‚	0		1	0		0
31		Р±Р°С‚С‚Р°Р»РѕРІР°_Р°Р»СЊС„РёСЏ@example.com	Staff	Р‘Р°С‚С‚Р°Р»РѕРІР° РђР»СЊС„РёСЏ		0	0	Р‘Р°С‚С‚Р°Р»РѕРІР° РђР»СЊС„РёСЏ	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87015244302	РЁР°С…РёСЂРёСЃС‚Р°РЅ	РЁС‚Р°С‚	0		1	0		0
32		РјР°С…РјСѓС‚РѕРІ_РјР°РєСЃРёРј_РјР°СЂР°С‚РѕРІРёС‡@example.com	Staff	РњР°С…РјСѓС‚РѕРІ РњР°РєСЃРёРј РњР°СЂР°С‚РѕРІРёС‡		0	0	РњР°С…РјСѓС‚РѕРІ РњР°РєСЃРёРј РњР°СЂР°С‚РѕРІРёС‡	unknown_value_please_contact_support	unknown_value_please_contact_support		87082461277	РЁР°С…СЂРёСЃС‚Р°РЅ	РЁС‚Р°С‚	0		1	0		0
33		РєРѕРЅСЃС‚Р°РЅС‚РёРЅРѕРІ_РІРёРєС‚РѕСЂ_РµРІРіРµРЅСЊРµРІРёС‡@example.com	Staff	РљРѕРЅСЃС‚Р°РЅС‚РёРЅРѕРІ Р’РёРєС‚РѕСЂ Р•РІРіРµРЅСЊРµРІРёС‡		0	0	РљРѕРЅСЃС‚Р°РЅС‚РёРЅРѕРІ Р’РёРєС‚РѕСЂ Р•РІРіРµРЅСЊРµРІРёС‡	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87085508549	РЁР°С…СЂРёСЃС‚Р°РЅ	РЁС‚Р°С‚	0		1	0		0
34		СЃС‹РґС‹Рє_Р°Р№Р±Р°СЂ_Р±РµСЂРёРєСѓРµР»С‹@example.com	Staff	РЎС‹РґС‹Рє РђР№Р±Р°СЂ Р‘РµСЂРёРєСѓРµР»С‹		0	0	РЎС‹РґС‹Рє РђР№Р±Р°СЂ Р‘РµСЂРёРєСѓРµР»С‹	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87471303305	Р‘Р°СЂРёР±Р°РµРІР°	РЁС‚Р°С‚	0		1	0		0
35		РґСѓРґР°СЂРµРІ_РґР°РЅРёР»@example.com	Staff	Р”СѓРґР°СЂРµРІ Р”Р°РЅРёР»		0	0	Р”СѓРґР°СЂРµРІ Р”Р°РЅРёР»	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87785912498	Р‘Р°СЂРёР±Р°РµРІР°	РЁС‚Р°С‚	0		1	0		0
36		РіСѓСЃРµРІ_РґР°РЅРёР»_РІР»Р°РґРёСЃР»Р°РІРѕРІРёС‡@example.com	Staff	Р“СѓСЃРµРІ Р”Р°РЅРёР» Р’Р»Р°РґРёСЃР»Р°РІРѕРІРёС‡		0	0	Р“СѓСЃРµРІ Р”Р°РЅРёР» Р’Р»Р°РґРёСЃР»Р°РІРѕРІРёС‡	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87476241676	Р‘Р°СЂРёР±Р°РµРІР°	РЁС‚Р°С‚	0		1	0		0
37		СЃРµСЂРіРµРµРІ_СЃРµСЂРіРµР№_РІСЏС‡РµСЃР»Р°РІРѕРІРёС‡@example.com	Staff	РЎРµСЂРіРµРµРІ РЎРµСЂРіРµР№ Р’СЏС‡РµСЃР»Р°РІРѕРІРёС‡		0	0	РЎРµСЂРіРµРµРІ РЎРµСЂРіРµР№ Р’СЏС‡РµСЃР»Р°РІРѕРІРёС‡	Р»РёРґРµСЂ Р»РѕРєР°С†РёРё РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87055548252	Р¤СЂРёРґРѕРј	РЁС‚Р°С‚	0		1	0		0
38		РјСѓС…Р°РјРµС‚Р¶Р°РЅРѕРІР°_РіР°Р»РёРЅР°_Р°РЅРґСЂРµРµРІРЅР°@example.com	Staff	РњСѓС…Р°РјРµС‚Р¶Р°РЅРѕРІР° Р“Р°Р»РёРЅР° РђРЅРґСЂРµРµРІРЅР°		0	0	РњСѓС…Р°РјРµС‚Р¶Р°РЅРѕРІР° Р“Р°Р»РёРЅР° РђРЅРґСЂРµРµРІРЅР°	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87784490779	Р¤СЂРёРґРѕРј	РЁС‚Р°С‚	0		1	0		0
39		РѕР·Р±РµРє_РґР°РјРёСЂ_РјР°СЂР°С‚СѓР»С‹@example.com	Staff	РћР·Р±РµРє Р”Р°РјРёСЂ РњР°СЂР°С‚СѓР»С‹		0	0	РћР·Р±РµРє Р”Р°РјРёСЂ РњР°СЂР°С‚СѓР»С‹	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87473703932	Р¤СЂРёРґРѕРј	РЁС‚Р°С‚	0		1	0		0
40		РєСѓР·РЅРµС†РѕРІ_Р°РЅРґСЂРµР№_РѕР»РµРіРѕРІРёС‡@example.com	Staff	РљСѓР·РЅРµС†РѕРІ РђРЅРґСЂРµР№ РћР»РµРіРѕРІРёС‡		0	0	РљСѓР·РЅРµС†РѕРІ РђРЅРґСЂРµР№ РћР»РµРіРѕРІРёС‡	Р»РёРґРµСЂ Р»РѕРєР°С†РёРё РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87753790098 РІР°С‚СЃ Р°РїРї 87057413571 С‚РµР»РµРіСЂР°РјРј	РљРѕРєС‚РµРј	РЁС‚Р°С‚	0		1	0		0
41		Р¶РµС‚РїС–СЃ_РґРёСЏСЃ_РµСЂС‚Р°Р№Т±Р»С‹@example.com	Staff	Р–РµС‚РїС–СЃ Р”РёСЏСЃ Р•СЂС‚Р°Р№Т±Р»С‹		0	0	Р–РµС‚РїС–СЃ Р”РёСЏСЃ Р•СЂС‚Р°Р№Т±Р»С‹	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87712556618	РљРѕРєС‚РµРј	РЁС‚Р°С‚	0		1	0		0
42		Р°С…РјРµРґР¶Р°РЅРѕРІ_РјРµРґРµС‚_РјСѓСЂР°С‚РєР°РЅРѕРІРёС‡@example.com	Staff	РђС…РјРµРґР¶Р°РЅРѕРІ РњРµРґРµС‚ РњСѓСЂР°С‚РєР°РЅРѕРІРёС‡		0	0	РђС…РјРµРґР¶Р°РЅРѕРІ РњРµРґРµС‚ РњСѓСЂР°С‚РєР°РЅРѕРІРёС‡	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87014710296	РђР»РјР°СЃРёС‚Рё	РЁС‚Р°С‚	0		1	0		0
43		adema@example.com	РџСѓС€РµСЂ	РђСЃС‹Р»РєС‹Р·С‹ РђРґРµРјР°		0	0	РђСЃС‹Р»РєС‹Р·С‹ РђРґРµРјР°	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87082216212; 87470664231	РђР»РјР°СЃРёС‚Рё	РЁС‚Р°С‚	0		1	0		0
44	964240622	zhaniya@example.com	РџСѓС€РµСЂ	РђСЃРєР°СЂ		1	0	РђР·РёРјР±Р°РµРІР° Р–Р°РЅРёСЏ Р“Р°РЅРёРјСѓСЂР°С‚РѕРІРЅР°	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87472474546	РЎРёС‚Рё +	РЁС‚Р°С‚	1		1	1		1
45		РєР°Р№РЅР°СЂР±Р°РµРІР°_Р·Р°СЂРёРЅР°_РєР°СЃС‹РјРѕРІРЅР°@example.com	Staff	РљР°Р№РЅР°СЂР±Р°РµРІР° Р—Р°СЂРёРЅР° РљР°СЃС‹РјРѕРІРЅР°		0	0	РљР°Р№РЅР°СЂР±Р°РµРІР° Р—Р°СЂРёРЅР° РљР°СЃС‹РјРѕРІРЅР°	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87022643651	РЎРёС‚Рё +	РЁС‚Р°С‚	0		1	0		0
46		Р±РµР№Р±С–С‚С…Р°РЅТ›С‹Р·С‹_РЅТ±СЂРіТЇР»@example.com	Staff	Р‘РµР№Р±С–С‚С…Р°РЅТ›С‹Р·С‹ РќТ±СЂРіТЇР»		0	0	Р‘РµР№Р±С–С‚С…Р°РЅТ›С‹Р·С‹ РќТ±СЂРіТЇР»	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87066571306	РЎРёС‚Рё +	РЁС‚Р°С‚	0		1	0		0
47		РјР°СЂС‡РµРЅРєРѕ_Р°Р»РµСЃСЏ_Р°Р»РјР°Р·РѕРІРЅР°@example.com	Staff	РњР°СЂС‡РµРЅРєРѕ РђР»РµСЃСЏ РђР»РјР°Р·РѕРІРЅР°		0	0	РњР°СЂС‡РµРЅРєРѕ РђР»РµСЃСЏ РђР»РјР°Р·РѕРІРЅР°	Р»РёРґРµСЂ Р»РѕРєР°С†РёРё РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87015500995	Р”СѓР»Р°С‚Рё	РЁС‚Р°С‚	0		1	0		0
48		РІР°РЅРёРЅР°_РєСЂРёСЃС‚РёРЅР°_РјРёС…Р°Р№Р»РѕРІРЅР°@example.com	Staff	Р’Р°РЅРёРЅР° РљСЂРёСЃС‚РёРЅР° РњРёС…Р°Р№Р»РѕРІРЅР°		0	0	Р’Р°РЅРёРЅР° РљСЂРёСЃС‚РёРЅР° РњРёС…Р°Р№Р»РѕРІРЅР°	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87763272838	Р”СѓР»Р°С‚Рё	РЁС‚Р°С‚	0		1	0		0
49		СЃРµР№С„СѓР»Р»Р°РµРІ_РѕСЃРјР°РЅ@example.com	Staff	РЎРµР№С„СѓР»Р»Р°РµРІ РћСЃРјР°РЅ		0	0	РЎРµР№С„СѓР»Р»Р°РµРІ РћСЃРјР°РЅ	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87007620109	Р”СѓР»Р°С‚Рё, РўРµСЂРёСЃРєРµР№	РЁС‚Р°С‚	0		1	0		0
50		РєСѓСЃРёСЃ_Р°РЅР°СЃС‚Р°СЃРёСЏ_СЃРµСЂРіРµРµРІРЅР°@example.com	Staff	РљСѓСЃРёСЃ РђРЅР°СЃС‚Р°СЃРёСЏ РЎРµСЂРіРµРµРІРЅР°		0	0	РљСѓСЃРёСЃ РђРЅР°СЃС‚Р°СЃРёСЏ РЎРµСЂРіРµРµРІРЅР°	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87477394393	РўРµСЂРёСЃРєРµР№	РЁС‚Р°С‚	0		1	0		0
51		РЅР°СЃРёР±СѓР»Р»РёРЅР°_СЂРµРіРёРЅР°_СЂРёРјРѕРІРЅР°@example.com	Staff	РќР°СЃРёР±СѓР»Р»РёРЅР° Р РµРіРёРЅР° Р РёРјРѕРІРЅР°		0	0	РќР°СЃРёР±СѓР»Р»РёРЅР° Р РµРіРёРЅР° Р РёРјРѕРІРЅР°	РўСЂРµРЅРµСЂ	0		87077213568	РўРµСЂРёСЃРєРµР№	РЁС‚Р°С‚	0		1	0		0
52		Р±РѕР»РѕС‚РѕРІ_РјРёС…Р°РёР»_РёРіРѕСЂРµРІРёС‡@example.com	Staff	Р‘РѕР»РѕС‚РѕРІ РњРёС…Р°РёР» РРіРѕСЂРµРІРёС‡		0	0	Р‘РѕР»РѕС‚РѕРІ РњРёС…Р°РёР» РРіРѕСЂРµРІРёС‡	РўРёРјР›РёРґРµСЂ РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87781520526	unknown_value_please_contact_support	unknown_value_please_contact_support	0		1	0		0
53		С‚Р°Р№Р»Р°РЅРѕРІР°_Р°Р№РіРµСЂС–Рј_Р¶Р°РЅР±СѓР»Р°С‚Т›С‹Р·С‹@example.com	Staff	РўР°Р№Р»Р°РЅРѕРІР° РђР№РіРµСЂС–Рј Р–Р°РЅР±СѓР»Р°С‚Т›С‹Р·С‹		0	0	РўР°Р№Р»Р°РЅРѕРІР° РђР№РіРµСЂС–Рј Р–Р°РЅР±СѓР»Р°С‚Т›С‹Р·С‹	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87767972278	New expo life	РЁС‚Р°С‚	0		1	0		0
55		РµСЂС€РёРЅРѕРІ_СЂРёРЅР°С‚_РЅСѓРіРјР°РЅРѕРІРёС‡@example.com	Staff	Р•СЂС€РёРЅРѕРІ Р РёРЅР°С‚ РќСѓРіРјР°РЅРѕРІРёС‡		0	0	Р•СЂС€РёРЅРѕРІ Р РёРЅР°С‚ РќСѓРіРјР°РЅРѕРІРёС‡	РўСЂРµРЅРµСЂ	unknown_value_please_contact_support		87085435981	New expo life	РЁС‚Р°С‚	0		1	0		0
58	-1076367879	Dauletbekoffa@gmail.com	РџСѓС€РµСЂ	РђСЃРєР°СЂ		1	0	unknown_value_please_contact_support	unknown_value_please_contact_support	unknown_value_please_contact_support		87472474546	unknown_value_please_contact_support	unknown_value_please_contact_support	1		1	1		1
\.


--
-- Data for Name: _events; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._events (id, title, description, event_date, created_at) FROM stdin;
1	РўРёРјР±РёР»РґРёРЅРі	РЎРѕР±РёСЂР°РµРјСЃСЏ СЃ РєРѕР»Р»РµРіР°РјРё	2025-08-11	2025-08-01
2	РРІРµРЅС‚ С‚РµСЃС‚РѕРІС‹Р№	РџРѕСЃР»РµРґРЅРёР№ С‚РµСЃС‚	2025-08-11	2025-08-11
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
1	44	РЈ РјРµРЅСЏ С‚Р°РєР°СЏ РёРґРµСЏ	2025-08-11
2	44	Р™РѕСѓ	2025-08-11
\.


--
-- Data for Name: _onboarding_questions; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._onboarding_questions (id, role, order_index, question_text, data_key, is_required) FROM stdin;
1	РџСѓС€РµСЂ	0	РџСЂРёРІРµС‚. РњС‹ РЅР°С‡РёРЅР°РµРј СЂРµРіРёСЃС‚СЂР°С†РёСЋ. РџРµСЂРІС‹Р№ РІРѕРїСЂРѕСЃ, РєР°Рє С‚РµР±СЏ Р·РѕРІСѓС‚?	name	1
2	РџСѓС€РµСЂ	0	Р’РІРµРґРё СЃРІРѕР№ РЅРѕРјРµСЂ С‚РµР»РµС„РѕРЅР°	contact_info	1
3	РљР»РёРЅРёРЅРі	0	РљР°Рє С‚РІРѕРµ РёРјСЏ РўРµСЃС‚?	name	1
4	РљР»РёРЅРёРЅРі	0	РќРѕРјРµСЂ РєРѕРЅС‚Р°РєС‚Р°	contact_info	1
\.


--
-- Data for Name: _onboarding_steps; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._onboarding_steps (id, role, order_index, message_text, file_path, file_type) FROM stdin;
6	РџСѓС€РµСЂ	0	РўРµСЃС‚		
9	Admin	0		uploads/onboarding\\steps\\admin_step_IMG_3561.mp4	
10	Admin	0		uploads/onboarding\\steps\\admin_step_IMG_3561.mp4	video_note
15	Admin	0		uploads/onboarding\\steps\\admin_step_IMG_3561.mp4	video_note
16	РџСѓС€РµСЂ	0		uploads/onboarding\\steps\\step__512_x_512_..mp4	video_note
18	РљР»РёРЅРёРЅРі	0		uploads/onboarding\\steps\\step__512_x_512_..mp4	video_note
\.


--
-- Data for Name: _quiz_questions; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._quiz_questions (id, role, question, answer, order_index, question_type, options) FROM stdin;
1	Admin	РўРѕС‡РЅРѕ РёРґРµС‚Рµ?	Р”Р°	1	unknown_value_please_contact_support	
2	Hunter	РўРѕС‡РЅРѕ РёРґРµС‚Рµ?	Р”Р°	0	unknown_value_please_contact_support	
3	Admin	РљСЂСѓС‚СЊ	РќРµС‚	0	unknown_value_please_contact_support	
4	РџСѓС€РµСЂ	РўРѕС‡РЅРѕ РёРґРµС‚Рµ?	Р”Р°	0	unknown_value_please_contact_support	
5	РџСѓС€РµСЂ	РўРѕС‡РЅРѕ РёРґРµС‚Рµ?	Р”Р°	0	choice	Р”Р°;РќРµС‚;Р’РѕР·РјРѕР¶РЅРѕ
6	РљР»РёРЅРёРЅРі	РўРµСЃС‚РѕРІРѕРµ	Р”Р°	0	choice	Р”Р°;РќРµС‚;Р’РѕР·РјРѕР¶РЅРѕ
7	РљР»РёРЅРёРЅРі	РўРѕС‡РЅРѕ РёРґРµС‚Рµ?	Р”Р°	0	text	
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
2803737	Р°Р·РёРјР±Р°РµРІР°_Р¶Р°РЅРёСЏ_РіР°РЅРёРјСѓСЂР°С‚РѕРІРЅР°@example.com	1
20907978	Р°РјРёСЂС…Р°РЅРѕРІ_РЅСѓСЂРјСѓС…Р°РјРјРµРґ@example.com	0
71046651	Р°РјРёСЂС…Р°РЅРѕРІР°_РґРёР»СЊРЅР°Р·@example.com	0
28433495	Р°СЃС‹Р»РєС‹Р·С‹_Р°РґРµРјР°@example.com	0
52707522	Р°С…РјРµРґР¶Р°РЅРѕРІ_РјРµРґРµС‚_РјСѓСЂР°С‚РєР°РЅРѕРІРёС‡@example.com	0
24906139	Р±Р°РіРґР°С‚РѕРІ_РґРёРґР°СЂ_Р°СЂРјР°РЅСѓР»С‹@example.com	0
64096260	Р±Р°С‚С‚Р°Р»РѕРІР°_Р°Р»СЊС„РёСЏ@example.com	0
60330097	Р±Р°С‚С‹СЂР±РµРєРѕРІ_Р°Р»РјР°СЃ@example.com	0
71775759	Р±Р°СЏРґРёР»РѕРІ_РјРµР№СЂР¶Р°РЅ@example.com	0
58200227	Р±Р°Т›РґР°СѓР»РµС‚Т›С‹Р·С‹_У™СЃРµР»@example.com	0
20993431	Р±РµР№Р±С–С‚С…Р°РЅТ›С‹Р·С‹_РЅТ±СЂРіТЇР»@example.com	0
46725767	yelena@example.com	0
41580755	Р±РёСЃРµРјР°Р»РёРµРІР°_Р°Р»РёРЅР°@example.com	0
38088999	Р±РѕР»Р°С‚РѕРІ_РјРёСЂР°СЃ_Т›Р°Р№СЂР°С‚Т±Р»С‹@example.com	0
20903013	Р±РѕР»РѕС‚РѕРІ_РјРёС…Р°РёР»_РёРіРѕСЂРµРІРёС‡@example.com	0
13034684	РІР°РЅРёРЅР°_РєСЂРёСЃС‚РёРЅР°_РјРёС…Р°Р№Р»РѕРІРЅР°@example.com	0
16751254	РІР°СЃРёР»СЊРµРІ_РёРІР°РЅ_СЃРµСЂРіРµРµРІРёС‡@example.com	0
94062530	РіР»Р°РґС‡РµРЅРєРѕ_Р°РЅР°СЃС‚Р°СЃРёСЏ_РµРІРіРµРЅСЊРµРІРЅР°@example.com	0
81655705	РіСѓСЃРµРІ_РґР°РЅРёР»_РІР»Р°РґРёСЃР»Р°РІРѕРІРёС‡@example.com	0
93781002	РґР¶Р°РјР°Р»РѕРІ_Р¶Р°РЅР°РґРё_Р¶Р°РЅР°С‚РѕРІРёС‡@example.com	0
17271191	РґР¶СѓРјР°С…Р°РЅ_С‹СЂС‹СЃР¶Р°РЅ_Р±Р°Т›С‹С‚Р¶Р°РЅТ›С‹Р·С‹@example.com	0
21137783	РґСЂРѕР·РґРѕРІ_СЂСѓСЃР»Р°РЅ_РІР°СЃРёР»СЊРµРІРёС‡@example.com	0
31642034	РґСѓРґР°СЂРµРІ_РґР°РЅРёР»@example.com	0
60551688	РµСЂРјСѓС…Р°РЅР±РµС‚_Р°Р№Р±Р°СЂ_Р±РµР№Р±С–С‚Т±Р»С‹@example.com	0
68208761	РµСЂС€РёРЅРѕРІ_СЂРёРЅР°С‚_РЅСѓРіРјР°РЅРѕРІРёС‡@example.com	0
1600132	РµСЃС‚РµРЅРѕРІ_РµРґРёР»СЊ@example.com	0
51799010	Р¶Р°Р»РіР°СЃР±Р°Р№_Р°Р№РґР°РЅР°_РјСѓС…С‚Р°СЂРєС‹Р·С‹@example.com	0
40142482	Р¶РµС‚РєРёР·РіРµРЅРѕРІР°_Р°РєР±РѕР±РµРє_С‚РёР»РµРєРєС‹Р·С‹@example.com	0
3225053	Р¶РµС‚РїС–СЃ_РґРёСЏСЃ_РµСЂС‚Р°Р№Т±Р»С‹@example.com	0
6911053	Р¶РѕР»Р±Р°РµРІР°_Р°РєРјРµР№РёСЂ@example.com	0
77382132	Р¶СѓР±Р°РЅР°Р·Р°СЂРѕРІ_РЅСѓСЂР±РµРє_Р±Р°Р№Р±РѕР»СЃС‹РЅРѕРІРёС‡@example.com	0
21044982	РёР±СЂР°РіРёРјРѕРІ_СЂР°РґР¶РёРІ_С…Р°С‡РёС…Р°РЅРѕРІРёС‡@example.com	0
31716632	РёСЃРєР°РєРѕРІ_Р°СЃРєР°СЂ@example.com	0
47030323	РёСЃРєР°РєРѕРІ_РјРёСЂР°СЃ_РјРµР№СЂР°РјРѕРІРёС‡@example.com	0
12912721	РєР°РґС‹СЂРѕРІР°_РіСѓР·РµР»СЊ_С€Р°С‚Р»РёРєРѕРІРЅР°@example.com	0
3164802	РєР°Р№РЅР°СЂР±Р°РµРІР°_Р·Р°СЂРёРЅР°_РєР°СЃС‹РјРѕРІРЅР°@example.com	0
99722546	РєР°Р»РѕРµРІ_Р°СЃР»Р°РЅР±РµРє_РєР°Р·Р±РµРєРѕРІРёС‡@example.com	0
1163708	РєРѕРЅСЃС‚Р°РЅС‚РёРЅРѕРІ_РІРёРєС‚РѕСЂ_РµРІРіРµРЅСЊРµРІРёС‡@example.com	0
83806096	РєСѓР·РЅРµС†РѕРІ_Р°РЅРґСЂРµР№_РѕР»РµРіРѕРІРёС‡@example.com	0
7621752	РєСѓСЃРёСЃ_Р°РЅР°СЃС‚Р°СЃРёСЏ_СЃРµСЂРіРµРµРІРЅР°@example.com	0
6719999	РјР°СЂС‡РµРЅРєРѕ_Р°Р»РµСЃСЏ_Р°Р»РјР°Р·РѕРІРЅР°@example.com	0
70865554	РјР°С…РјСѓС‚РѕРІ_РјР°РєСЃРёРј_РјР°СЂР°С‚РѕРІРёС‡@example.com	0
962934	РјСѓРєР°С€_Р°СЂСѓР¶Р°РЅ_РјСѓСЂР°С‚РєС‹Р·С‹@example.com	0
1475076	РјСѓС…Р°РјРµС‚Р¶Р°РЅРѕРІР°_РіР°Р»РёРЅР°_Р°РЅРґСЂРµРµРІРЅР°@example.com	0
5097259	РЅР°СЃРёР±СѓР»Р»РёРЅР°_СЂРµРіРёРЅР°_СЂРёРјРѕРІРЅР°@example.com	0
44593062	РѕР·Р±РµРє_РґР°РјРёСЂ_РјР°СЂР°С‚СѓР»С‹@example.com	0
83861453	РѕСЂР°Р·Р±Р°Р№_РіР°Р»С‹РјР¶Р°РЅ_Р±Р°СѓС‹СЂР¶Р°РЅСѓР»С‹@example.com	0
61178373	РїР°РєР°Р»РёРЅ_РґР°РЅРёРёР»_РІР»Р°РґРёРјРёСЂРѕРІРёС‡@example.com	0
21922271	СЂР°С€РёРґРёРЅРѕРІР°_С€Р°РёСЂР°_СЃР°РґРёСЂРґРёРЅРѕРІРЅР°@example.com	0
55387044	СЃР°Р»Р°РјР°С‚_Р°Р»РёРѕСЃРјР°РЅ_СЂСѓСЃС‚РµРјСѓР»С‹@example.com	0
50442894	СЃРµР№С„СѓР»Р»Р°РµРІ_РѕСЃРјР°РЅ@example.com	0
21051563	СЃРµСЂРіРµРµРІ_СЃРµСЂРіРµР№_РІСЏС‡РµСЃР»Р°РІРѕРІРёС‡@example.com	0
42484003	СЃС‹РґС‹Рє_Р°Р№Р±Р°СЂ_Р±РµСЂРёРєСѓРµР»С‹@example.com	0
96145836	СЃС‹С‡С‘РІ_СЂРѕРґРёРѕРЅ_РІР°Р»РµСЂСЊРµРІРёС‡@example.com	0
3546708	С‚Р°Р№Р»Р°РЅРѕРІР°_Р°Р№РіРµСЂС–Рј_Р¶Р°РЅР±СѓР»Р°С‚Т›С‹Р·С‹@example.com	0
42802877	СѓСЃРµРЅРѕРІ_Р°РґРёР»СЊ_Р°СЃРєР°СЂРѕРІРёС‡@example.com	1
99816233	Р°Р·РёРјР±Р°РµРІР°_Р¶Р°РЅРёСЏ_РіР°РЅРёРјСѓСЂР°С‚РѕРІРЅР°@example.com	1
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
1	РџСѓС€РµСЂ	РўРµСЃС‚РѕРІРѕРµ	РўРµСЃС‚РѕРІРѕРµ		0
\.


--
-- Data for Name: _role_onboarding; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._role_onboarding (id, role, text, file_path, file_type) FROM stdin;
1	РџСѓС€РµСЂ	РџСЂРёРІРµС‚. РћР·РЅР°РєРѕРјСЊСЃСЏ СЃ РґР°РЅРЅС‹Рј РјР°С‚РµСЂРёР°Р»РѕРј	uploads/onboarding\\intro.mp4	video_note
2	Admin			document
3	РљР»РёРЅРёРЅРі	РўРµСЃС‚РѕРІРѕРµ РєР»РёРЅРёРЅРі, РєР°РєРѕР№ С‚Рѕ С‚РµРєСЃС‚	uploads/onboarding\\2025-07-24_092428.png	document
\.


--
-- Data for Name: _roles; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._roles (id, name) FROM stdin;
1	Admin
2	Hunter
5	РљР»РёРЅРёРЅРі
3	РџСѓС€РµСЂ
4	РўСЂРµРЅРµСЂ
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
1	Г°ВџВљВЂ Рћ РєРѕРјРїР°	<b>РќР°С€Р° РјРёСЃСЃРёСЏ:</b> .\n\n<b>РќР°С€Рё С†РµРЅРЅРѕСЃС‚Рё:</b>\n1. <i>РћС‚РєСЂС‹С‚РѕСЃС‚СЊ</i> - \n2. <i>Р Р°Р·РІРёС‚РёРµ</i> - \n3. <i>Р РµР·СѓР»СЊС‚Р°С‚</i> - \n\nРџРѕСЃРјРѕС‚СЂРµС‚СЊ РїРѕР»РЅСѓСЋ <b>РїСЂРµР·РµРЅС‚Р°С†РёСЋ Рѕ РєРѕРјРїР°РЅРёРё</b> РјРѕР¶РЅРѕ РїРѕ СЃСЃС‹Р»РєРµ:\n<a href=''>РџСЂРµР·РµРЅС‚Р°С†РёСЏ РєРѕРјРїР°РЅРёРё</a>	Р‘Р°Р·Р° Р·РЅР°РЅРёР№	unknown_value_please_contact_support
2	Г°ВџВ“В„ РћС„РёС†РёР°Р»СЊРЅРѕРµ РѕС„РѕСЂРјР»Рµ	Р”Р»СЏ РѕС„РёС†РёР°Р»СЊРЅРѕРіРѕ РѕС„РѕСЂРјР»РµРЅРёСЏ РїРѕ РўРљ Р Рљ РІСЃРµС… С€С‚Р°С‚РЅС‹С… СЃРѕС‚СЂСѓРґРЅРёРєРѕРІ, РїРѕР¶Р°Р»СѓР№СЃС‚Р°, РїРѕРґРіРѕС‚РѕРІСЊС‚Рµ СЃР»РµРґСѓСЋС‰РёРµ РґРѕРєСѓРјРµРЅС‚С‹:\nвЂў Р—Р°СЏРІР»РµРЅРёРµ РЅР° РїСЂРёС‘Рј (РѕС‚ СЂСѓРєРё)\nвЂў РЎРєР°РЅ СѓРґРѕСЃС‚РѕРІРµСЂРµРЅРёСЏ Р»РёС‡РЅРѕСЃС‚Рё\nвЂў РЎРїСЂР°РІРєР° РёР· РїСЃРёС…РґРёСЃРїР°РЅСЃРµСЂР°\nвЂў РЎРїСЂР°РІРєР° РёР· РЅР°СЂРєРѕР»РѕРіРёС‡РµСЃРєРѕРіРѕ РґРёСЃРїР°РЅСЃРµСЂР°\nвЂў РЎРїСЂР°РІРєР° РѕР± РѕС‚СЃСѓС‚СЃС‚РІРёРё СЃСѓРґРёРјРѕСЃС‚Рё\n\nвќ—пёЏР’СЃРµ СЃРїСЂР°РІРєРё РјРѕР¶РЅРѕ Р±С‹СЃС‚СЂРѕ РїРѕР»СѓС‡РёС‚СЊ С‡РµСЂРµР· Kaspi Рё Р•РіРѕРІ вЂ” СЌС‚Рѕ Р·Р°Р№РјС‘С‚ 10вЂ“15 РјРёРЅСѓС‚.\n\nРџРѕСЃР»Рµ РїРѕРґРіРѕС‚РѕРІРєРё РґРѕРєСѓРјРµРЅС‚РѕРІ, Р·Р°РїРѕР»РЅРёС‚Рµ Р°РЅРєРµС‚Сѓ РїРѕ СЃСЃС‹Р»РєРµ:\n<a href=''>Р¤РѕСЂРјР° РґР»СЏ РѕС„РѕСЂРјР»РµРЅРёСЏ</a>\n\nРћСЃС‚Р°Р»РёСЃСЊ РІРѕРїСЂРѕСЃС‹? РќР°РїРёС€РёС‚Рµ РЅР°С€РµРјСѓ HR-РјРµРЅРµРґР¶РµСЂСѓ!\n	Р‘Р°Р·Р° Р·РЅР°РЅРёР№	static/images/photo_2025-07-25_15-56-47.jpg
3	Г°ВџВЋВЃ Р‘РѕРЅСѓСЃС‹ Рё РїСЂРѕРіСЂР°	<b>Р РµС„РµСЂР°Р»СЊРЅР°СЏ РїСЂРѕРіСЂР°РјРјР°:</b>\nРџСЂРёРІРµРґРё РґСЂСѓРіР° РЅР° РѕС‚РєСЂС‹С‚СѓСЋ РІР°РєР°РЅСЃРёСЋ Рё РїРѕР»СѓС‡Рё Р±РѕРЅСѓСЃ! РџРѕРґСЂРѕР±РЅС‹Рµ СѓСЃР»РѕРІРёСЏ Рё СЃРїРёСЃРѕРє РІР°РєР°РЅСЃРёР№ РјРѕР¶РЅРѕ РЅР°Р№С‚Рё Р·РґРµСЃСЊ:\n<a href=''>РЈСЃР»РѕРІРёСЏ СЂРµС„РµСЂР°Р»СЊРЅРѕР№ РїСЂРѕРіСЂР°РјРјС‹</a>\n\n<b>РљРѕСЂРїРѕСЂР°С‚РёРІРЅС‹Рµ СЃРєРёРґРєРё:</b>\nРќР°С€Рё СЃРѕС‚СЂСѓРґРЅРёРєРё РїРѕР»СѓС‡Р°СЋС‚ СЃРєРёРґРєРё Сѓ РїР°СЂС‚РЅРµСЂРѕРІ. РЎРїРёСЃРѕРє Р°РєС‚СѓР°Р»СЊРЅС‹С… РїСЂРµРґР»РѕР¶РµРЅРёР№ (С„РёС‚РЅРµСЃ, РѕР±СѓС‡РµРЅРёРµ, РєР°С„Рµ) РЅР°С…РѕРґРёС‚СЃСЏ С‚СѓС‚:\n<a href=''>РЎРїРёСЃРѕРє РїР°СЂС‚РЅРµСЂСЃРєРёС… СЃРєРёРґРѕРє</a>	Р‘Р°Р·Р° Р·РЅР°РЅРёР№	unknown_value_please_contact_support
4	Г°ВџВ’В¬ РќР°С€Рё С‡Р°С‚С‹ Рё СЂРµСЃСѓ	<b>РќР°С€Рё РІРЅСѓС‚СЂРµРЅРЅРёРµ С‡Р°С‚С‹:</b>\nвЂў <a href=''>Backstage (Telegram)</a> - РЅР°С€ РіР»Р°РІРЅС‹Р№ С‡Р°С‚ РґР»СЏ РѕР±С‰РµРЅРёСЏ.\nвЂў <a href=''>WhatsApp-РіСЂСѓРїРїР°</a> - РґР»СЏ СЃСЂРѕС‡РЅС‹С… РѕРїРѕРІРµС‰РµРЅРёР№.\nвЂў <a href=''>Р¤Р»СѓРґРёР»РєР°</a> - РґР»СЏ РјРµРјРѕРІ Рё СЂР°Р·РіРѕРІРѕСЂРѕРІ РЅРµ РїРѕ СЂР°Р±РѕС‚Рµ.\n\n<b>РћР±С‰РёРµ СЂРµСЃСѓСЂСЃС‹:</b>\nР’СЃРµ СЂРµРіР»Р°РјРµРЅС‚С‹, С‚Р°Р±Р»РёС†С‹ Рё С‡РµРє-Р»РёСЃС‚С‹ С…СЂР°РЅСЏС‚СЃСЏ РЅР° РЅР°С€РµРј РѕР±С‰РµРј РґРёСЃРєРµ:\nвЂў <a href=''>РћР±С‰РёР№ РґРёСЃРє РєРѕРјРїР°РЅРёРё</a>\n\n<b>Р¤РѕС‚РѕР°Р»СЊР±РѕРј:</b>\nР’СЃРїРѕРјРёРЅР°РµРј Р»СѓС‡С€РёРµ РјРѕРјРµРЅС‚С‹ РІРјРµСЃС‚Рµ! РЎСЃС‹Р»РєР° РЅР° РЅР°С€ РѕР±С‰РёР№ С„РѕС‚РѕР°Р»СЊР±РѕРј:\nвЂў <a href=''>РљРѕСЂРїРѕСЂР°С‚РёРІРЅС‹Р№ С„РѕС‚РѕР°Р»СЊР±РѕРј</a>	Р‘Р°Р·Р° Р·РЅР°РЅРёР№	unknown_value_please_contact_support
5	Г°ВџВЋВ‰ РўСЂР°РґРёС†РёРё Рё РєСѓР»СЊС‚	<b>РќР°С€Рё С‚СЂР°РґРёС†РёРё:</b>\nвЂў <b>РџРѕ С‡РµС‚РІРµСЂРіР°Рј</b> РјС‹ .\nвЂў <b>РўСЂР°РґРёС†РёРё РїРѕ РіРѕСЂРѕРґР°Рј:</b> Р’ РђР»РјР°С‚С‹ РјС‹..., РІ РђСЃС‚Р°РЅРµ РјС‹...\nвЂў <b>РџРѕР·РґСЂР°РІР»РµРЅРёСЏ:</b> РњС‹ РїРѕР·РґСЂР°РІР»СЏРµРј РєРѕР»Р»РµРі СЃ РґРЅРµРј СЂРѕР¶РґРµРЅРёСЏ РІ РѕР±С‰РµРј С‡Р°С‚Рµ Рё РґР°СЂРёРј РїРѕРґР°СЂРєРё. РћС‚РґС‹С…Р°РµРј РЅР° РІСЃРµС… РѕС„РёС†РёР°Р»СЊРЅС‹С… РїСЂР°Р·РґРЅРёРєР°С…!\n\n<b>РћС‚Р·С‹РІС‹ Рё Р°РєС‚РёРІРЅРѕСЃС‚Рё:</b>\nРџРѕС‡РёС‚Р°С‚СЊ РѕС‚Р·С‹РІС‹ Рѕ РЅР°С€РёС… С‚РёРјР±РёР»РґРёРЅРіР°С… Рё РїРѕСЃРјРѕС‚СЂРµС‚СЊ С„РѕС‚Рѕ РјРѕР¶РЅРѕ РІ СЃРїРµС†РёР°Р»СЊРЅРѕРј СЂР°Р·РґРµР»Рµ:\n<a href=''>РћС‚Р·С‹РІС‹ Рѕ РІРЅСѓС‚СЂРµРЅРЅРёС… Р°РєС‚РёРІРЅРѕСЃС‚СЏС…</a>	Р‘Р°Р·Р° Р·РЅР°РЅРёР№	unknown_value_please_contact_support
7	Г°ВџВ§В  РљРѕСЂРїРѕСЂР°С‚РёРІРЅС‹Р№ СЃР»РѕРІ	РќР°С€ РІРЅСѓС‚СЂРµРЅРЅРёР№ СЏР·С‹Рє, РєРѕС‚РѕСЂС‹Р№ РїРѕРјРѕРіР°РµС‚ Р±С‹С‚СЊ РЅР° РѕРґРЅРѕР№ РІРѕР»РЅРµ:\n\nГ°ВџВ“В <b>В«BackstageВ»</b> вЂ” <i>РЅР°С€ РіР»Р°РІРЅС‹Р№ РєРѕРјР°РЅРґРЅС‹Р№ С‡Р°С‚ РІ Telegram.</i>\n\nГ°ВџВ¤Вќ <b>В«Р’Р°Р№Р±-РґСЌР№В»</b> вЂ” <i>РµР¶РµРЅРµРґРµР»СЊРЅР°СЏ РЅРµС„РѕСЂРјР°Р»СЊРЅР°СЏ РІСЃС‚СЂРµС‡Р° РєРѕРјР°РЅРґС‹ РїРѕ РїСЏС‚РЅРёС†Р°Рј РґР»СЏ РѕР±РјРµРЅР° РЅРѕРІРѕСЃС‚СЏРјРё.</i>\n\nГ°ВџВ“ВЉ <b>В«Р¦РљРџВ»</b> вЂ” <i>Р¦РµР»Рё Рё РљР»СЋС‡РµРІС‹Рµ РџРѕРєР°Р·Р°С‚РµР»Рё, РЅР°С€Рё РѕСЂРёРµРЅС‚РёСЂС‹ РІ СЂР°Р±РѕС‚Рµ.</i>\n\nГ°ВџВЊВЂ <b>В«РЎРїРёРєРёРЅРіВ»</b> вЂ” <i>Speaking Club, РµР¶РµРЅРµРґРµР»СЊРЅР°СЏ РїСЂР°РєС‚РёРєР° Р°РЅРіР»РёР№СЃРєРѕРіРѕ СЏР·С‹РєР°.</i>\n\nГ°ВџВ’ВЎ <i>Р­С‚РѕС‚ СЃР»РѕРІР°СЂСЊ РјРѕР¶РЅРѕ Рё РЅСѓР¶РЅРѕ РґРѕРїРѕР»РЅСЏС‚СЊ! РџСЂРµРґР»Р°РіР°Р№С‚Рµ СЃРІРѕРё С‚РµСЂРјРёРЅС‹ РІ 	Р‘Р°Р·Р° Р·РЅР°РЅРёР№	unknown_value_please_contact_support
8	РўРµСЃС‚РѕРІРѕРµ	РўРµСЃС‚РѕРІРѕРµ РґР»СЏ Р°РєРѕ	Р‘Р°Р·Р° Р·РЅР°РЅРёР№	uploads/topics\\2025-07-24_092428.png
\.


--
-- Data for Name: _training_material; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._training_material (id, role, title, content, file_path) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

