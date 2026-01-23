# Telegram-бот "Заработались"
# Библиотека: pyTelegramBotAPI (telebot)
# Установка: pip3 install pyTelegramBotAPI

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '8453804590:AAGekhTUAaY8MwXVn3HKKfWRdv58bmMI_4Q' # ← ТОКЕН ОТ @BotFather
OWNER_CHAT_ID = -1003589420810      # ← Telegram ID (число)

bot = telebot.TeleBot(BOT_TOKEN)
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from datetime import datetime

# Состояния
STATE_NONE            = 0
STATE_NAME            = 1
STATE_EXPERIENCE      = 2
STATE_EDUCATION       = 3
STATE_REQUEST         = 4
STATE_RESUME_LINK     = 5
STATE_RESUME_CONFIRM  = 6
STATE_COMMUNITY_ASK   = 7

user_states = {}
user_data   = {}


WELCOME_TEXT = (
    "Что умеет этот бот?\n"
    "Привет!\n"
    "Это бот проекта «Заработались».\n"
    "Мы помогаем расти в карьере и зарабатывать больше.\n\n"
    "• Узнать подробнее про проект\n"
    "• Вступить в комьюнити\n"
    "• Записаться на консультацию\n"
    "• Послушать подкаст\n\n"
    "Чтобы начать пользоваться — напиши или нажми /start"
)


def get_main_menu_inline():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Про проект Заработались", callback_data="menu_project"),
        InlineKeyboardButton("Комьюнити", callback_data="menu_community")
    )
    markup.add(
        InlineKeyboardButton("Консультации", callback_data="menu_consult"),
        InlineKeyboardButton("Подкаст", callback_data="menu_podcast")
    )
    return markup


def send_main_menu_message(uid):
    bot.send_message(
        uid,
        "Ты в главном меню, выбери ниже, что тебе было бы ещё интересно узнать о проекте",
        reply_markup=get_main_menu_inline()
    )


@bot.message_handler(commands=['start'])
def cmd_start(message):
    uid = message.chat.id

    consent_text = (
        "Прежде, чем узнать об исследовании больше, просим вас подтвердить согласие с политикой обработки персональных данных:\n\n"
        "https://docs.google.com/document/d/1b9SE68JUncTm57EWK3xF0zVF2f0udLZKpSxRTgFuVDk/edit?usp=sharing\n\n"
        "Нажмите кнопку ниже:"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Даю согласие", callback_data="consent_pd_yes"),
        InlineKeyboardButton("Не даю согласие", callback_data="consent_pd_no")
    )

    bot.send_message(uid, consent_text, reply_markup=markup)


@bot.message_handler(commands=['menu'])
def cmd_menu(message):
    send_main_menu_message(message.chat.id)


@bot.message_handler(commands=['getid'])
def cmd_getid(message):
    bot.reply_to(message, f"Chat ID этого чата: `{message.chat.id}`", parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.message.chat.id
    data = call.data

    bot.answer_callback_query(call.id)

    # Согласие на обработку ПДн
    if data in ["consent_pd_yes", "consent_pd_no"]:
        if data == "consent_pd_yes":
            bot.edit_message_text(
                chat_id=uid,
                message_id=call.message.message_id,
                text="Спасибо за согласие на обработку персональных данных! 🧡"
            )

            # Второй этап — согласие на рассылку
            mailing_text = (
                "Также просим подтвердить согласие на получение рекламной рассылки от проекта:\n\n"
                "https://docs.google.com/document/d/1kLMLZ2gjpyzvri--zqRw6Usr1t5wPrJ-6CCcDMy7JFA/edit?usp=sharing\n\n"
                "Нажмите кнопку ниже:"
            )

            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("Даю согласие", callback_data="consent_mailing_yes"),
                InlineKeyboardButton("Не даю согласие", callback_data="consent_mailing_no")
            )

            bot.send_message(uid, mailing_text, reply_markup=markup)
        else:
            bot.edit_message_text(
                chat_id=uid,
                message_id=call.message.message_id,
                text="Хорошо, мы уважаем ваш выбор.\nЕсли передумаете — напишите /start заново."
            )
            bot.send_message(uid, " ", reply_markup=ReplyKeyboardRemove())
        return

    # Согласие на рассылку
    if data in ["consent_mailing_yes", "consent_mailing_no"]:
        if data == "consent_mailing_yes":
            bot.edit_message_text(
                chat_id=uid,
                message_id=call.message.message_id,
                text="Спасибо за согласие на рассылку! Теперь вы будете получать полезные обновления и предложения от проекта."
            )
        else:
            bot.edit_message_text(
                chat_id=uid,
                message_id=call.message.message_id,
                text="Хорошо, мы не будем присылать вам рассылку."
            )

        # В любом случае — переходим в главное меню
        user_states[uid] = STATE_NONE
        send_main_menu_message(uid)
        return

    # Главное меню — Inline-кнопки
    if data.startswith("menu_"):
        bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)

        if data == "menu_project":
            bot.send_message(uid, "Здесь подробное описание проекта Заработались.\n(вставьте ваш текст)")
            send_main_menu_message(uid)

        elif data == "menu_community":
            community_text = (
                "Наше комьюнити — это закрытое сообщество участников проекта «Заработались».\n\n"
                "Здесь ты сможешь:\n"
                "• Общаться с единомышленниками\n"
                "• Получать эксклюзивные материалы и обновления\n"
                "• Задавать вопросы экспертам\n"
                "• Делиться результатами и опытом\n\n"
                "(дополните текст)"
            )

            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("Да, вступить", callback_data="join_community"),
                InlineKeyboardButton("Назад в меню", callback_data="back_to_main")
            )

            bot.send_message(uid, community_text)
            bot.send_message(uid, "Хочешь вступить в комьюнити?", reply_markup=markup)
            return

        elif data == "menu_consult":
            consult_text = (
                "Мы проводим индивидуальные консультации по темам проекта.\n\n"
                "Хочешь записаться? Выбери тип ниже ↓"
            )

            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("Карьерная консультация", callback_data="consult_type_career"),
                InlineKeyboardButton("Разбор резюме", callback_data="consult_type_resume")
            )
            markup.add(
                InlineKeyboardButton("Карьерная стратегия", callback_data="consult_type_strategy"),
                InlineKeyboardButton("Свой вариант", callback_data="consult_type_custom")
            )
            markup.add(
                InlineKeyboardButton("Назад к меню", callback_data="back_to_main")
            )

            bot.send_message(uid, consult_text, reply_markup=markup)
            return

        elif data == "menu_podcast":
            pod_text = (
                "Слушай наш подкаст на удобных платформах:\n\n"
                "• Spotify → https://...\n"
                "• Apple Podcasts → https://...\n"
                "• Яндекс.Музыка → https://...\n"
                "• Telegram-канал → @ваш_канал"
            )
            bot.send_message(uid, pod_text)
            send_main_menu_message(uid)

    # Вступление в комьюнити
    if data == "join_community":
        bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)

        now = datetime.now().strftime("%d.%m.%Y %H:%M")

        bot.send_message(
            uid,
            "Отлично! Вот ссылка для вступления:\n"
            "https://t.me/+clgaWMRXw0lkNTYy\n\n"
            "Ждём тебя внутри! 🧡"
        )

        send_community_join_notification(uid, now)

        send_main_menu_message(uid)
        return

    # Назад в главное меню
    if data == "back_to_main":
        bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)
        send_main_menu_message(uid)
        return

    # Выбор типа консультации
    if data.startswith("consult_type_"):
        consult_type = ""
        if data == "consult_type_career":
            consult_type = "Карьерная консультация"
        elif data == "consult_type_resume":
            consult_type = "Разбор резюме"
        elif data == "consult_type_strategy":
            consult_type = "Карьерная стратегия"
        elif data == "consult_type_custom":
            consult_type = "Свой вариант"

        user_data[uid] = user_data.get(uid, {})
        user_data[uid]['consult_type'] = consult_type

        bot.answer_callback_query(call.id, f"Выбрано: {consult_type}")
        bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)

        bot.send_message(uid, "Опиши кратко свой опыт работы:")
        user_states[uid] = STATE_EXPERIENCE
        return

    # Подтверждение доступа к резюме
    if data == "resume_checked":
        bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)

        markup = InlineKeyboardMarkup(row_width=3)
        markup.add(
            InlineKeyboardButton("Аня", callback_data="consultant_anya"),
            InlineKeyboardButton("Лера", callback_data="consultant_lera"),
            InlineKeyboardButton("Любой", callback_data="consultant_any")
        )

        bot.send_message(uid, "Если вы хотите конкретно к Ане или Лере — выберите ниже, иначе нажмите «Любой»", reply_markup=markup)
        return

    # Выбор консультанта
    if data in ["consultant_anya", "consultant_lera", "consultant_any"]:
        consultant = ""
        if data == "consultant_anya":
            consultant = "Аня"
        elif data == "consultant_lera":
            consultant = "Лера"
        else:
            consultant = "Любой"

        user_data[uid]['consultant'] = consultant

        bot.answer_callback_query(call.id, f"Выбрано: {consultant}")
        bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)

        send_application(uid)
        bot.send_message(
            uid,
            "Заявка отправлена! Спасибо.\nМы свяжемся с вами в течение недели."
        )
        del user_states[uid]
        user_data.pop(uid, None)
        send_main_menu_message(uid)
        return


@bot.message_handler(func=lambda m: True)
def handle_text(message):
    uid = message.chat.id
    text = message.text.strip()

    # Первый контакт — WELCOME
    if uid not in user_states:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("/start"))
        bot.send_message(uid, WELCOME_TEXT, reply_markup=markup)
        return

    # Обработка состояний (заявка)
    if uid in user_states and user_states[uid] != STATE_NONE:
        state = user_states[uid]

        if state == STATE_NAME:
            user_data[uid]['name'] = text
            bot.send_message(uid, "Опиши кратко свой опыт работы:")
            user_states[uid] = STATE_EXPERIENCE

        elif state == STATE_EXPERIENCE:
            user_data[uid]['experience'] = text
            bot.send_message(uid, "Укажите ваше образование:")
            user_states[uid] = STATE_EDUCATION

        elif state == STATE_EDUCATION:
            user_data[uid]['education'] = text
            bot.send_message(uid, "Напишите ваш запрос на консультацию, чем подробнее тем лучше!")
            user_states[uid] = STATE_REQUEST

        elif state == STATE_REQUEST:
            user_data[uid]['request'] = text
            bot.send_message(uid, "Прикрепи ссылку на своё резюме, это поможет нам лучше понять твой кейс.")
            user_states[uid] = STATE_RESUME_LINK
            return

        elif state == STATE_RESUME_LINK:
            user_data[uid]['resume_link'] = text
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("Да, проверил(а)", callback_data="resume_checked")
            )
            bot.send_message(
                uid,
                "Проверь, точно ли открыт доступ на просмотр файла\n"
                "Подтверди, что доступ открыт:",
                reply_markup=markup
            )
            user_states[uid] = STATE_RESUME_CONFIRM
            return

        return

    # Если текст не распознан — возвращаем в главное меню
    send_main_menu_message(uid)


def send_application(uid):
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    if uid not in user_data:
        return

    d = user_data[uid]
    chat = bot.get_chat(uid)
    username_str = f"@{chat.username}" if chat.username else f"ID {uid}"
    first_name = chat.first_name or ""

    resume_link = d.get('resume_link', '— не прикреплена')

    text = (
        f"❗️ НОВАЯ ЗАЯВКА НА КОНСУЛЬТАЦИЮ\n"
        f"━━━━━━━━━━\n"
        f"Дата и время: {now}\n"
        f"От: {username_str} ({first_name})\n"
        f"━━━━━━━━━━\n"
        f"Тип консультации: {d.get('consult_type', '—')}\n"
        f"Имя: {d.get('name', '—')}\n"
        f"Опыт работы: {d.get('experience', '—')}\n"
        f"Образование: {d.get('education', '—')}\n"
        f"Запрос: {d.get('request', '—')}\n"
        f"Ссылка на резюме: {resume_link}\n"
        f"Желаемый консультант: {d.get('consultant', '—')}\n"
        f"━━━━━━━━━━\n"
    )

    try:
        bot.send_message(OWNER_CHAT_ID, text)
    except Exception as e:
        print(f"Ошибка отправки заявки: {e}")


def send_community_join_notification(uid, now):
    chat = bot.get_chat(uid)
    username_str = f"@{chat.username}" if chat.username else f"ID {uid}"
    first_name = chat.first_name or ""

    text = (
        f"💟 Запрос на вступление в комьюнити\n"
        f"━━━━━━━━━\n"
        f"Дата и время: {now}\n"
        f"От: {username_str} ({first_name})\n"
    )

    try:
        bot.send_message(OWNER_CHAT_ID, text)
    except Exception as e:
        print(f"Ошибка отправки уведомления о комьюнити: {e}")


if __name__ == '__main__':
    print("Бот 'Заработались' запущен...")
    print("Заявки и запросы на комьюнити отправляются в группу")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
