import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from dotenv import load_dotenv
import os


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if BOT_TOKEN is None:
    print("ОШИБКА: BOT_TOKEN не найден в .env!")
    exit(1)

print("Текущий BOT_TOKEN:", BOT_TOKEN[:15] + "...")  # покажет первые 15 символов
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_CHAT_ID=os.getenv('GROUP_CHAT_ID')
THREAD_COMMUNITY_JOIN=os.getenv('THREAD_COMMUNITY_JOIN')
THREAD_CONSULT_APP=os.getenv('THREAD_CONSULT_APP')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Состояния
STATE_NONE = 0
STATE_NAME = 1
STATE_EXPERIENCE = 2
STATE_EDUCATION = 3
STATE_REQUEST = 4
STATE_RESUME_LINK = 5
STATE_RESUME_ACCESS_CHECK = 6
STATE_CONSULTANT_CHOICE = 7
STATE_CONFIRM_APPLICATION = 8

user_states = {}
user_data = {}

WELCOME_TEXT = (
    "Привет!\n"
    "Очень рада видеть тебя в <b>«Заработались»</b> 💛\n\n"
    "Это тёплое место, где мы говорим о карьере без выгорания.\n"
    "Обсуждаем , как расти профессионально, но при этом не выгорать, не ломать себя "
    "и слышать свои настоящие «хочу» и «могу».\n\n"
    "Здесь у нас:\n\n"
    "🎙️ <b>подкаст</b> — честные, без розовых очков разговоры о работе, важных поворотах, "
    "деньгах, ценностях и о том, как найти свой путь среди всей этой неопределённости\n\n"
    "🫂 <b>уютное сообщество</b> — где собираются классные люди из самых разных сфер и этапов. "
    "Поддерживаем друг друга, делимся опытом, ищем вместе устойчивый и честный путь "
    "в этом быстро крутящемся мире\n\n"
    "🎯 <b>индивидуальное карьерное консультирование</b> — когда хочется сесть, спокойно "
    "разобрать свою ситуацию, понять, куда дальше и сделать шаги, которые правда твои\n\n"
    "Заходи, устраивайся поудобнее ☕\n"
    "Тут тебе всегда рады ✨"
)

def get_main_menu_inline():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🫂 Сообщество", callback_data="menu_community"),
        InlineKeyboardButton("🎯 Консультации", callback_data="menu_consult")
    )
    markup.add(
        InlineKeyboardButton("🎙️ Подкаст", callback_data="menu_podcast"),
        InlineKeyboardButton("🤝 Сотрудничество", callback_data="menu_collaboration")
    )
    return markup


def send_main_menu(uid):
    bot.send_message(
        uid,
        "Выбери, что тебя интересует:",
        reply_markup=get_main_menu_inline()
    )


def get_consult_format_inline():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Разбор резюме", callback_data="consult_format_resume"),
        InlineKeyboardButton("Тестовое HR-собеседование", callback_data="consult_format_interview"),
        InlineKeyboardButton("Карьерная консультация", callback_data="consult_format_consultation"),
        InlineKeyboardButton("Выход на рынок труда", callback_data="consult_format_market"),
    )
    return markup


@bot.message_handler(commands=['start'])
def cmd_start(message):
    uid = message.chat.id
    welcome_photo = "https://drive.google.com/uc?export=view&id=1s9R41fJOX93lSG8OgTZljDopGezlkEs9"
    try:
        bot.send_photo(
            chat_id=uid,
            photo=welcome_photo,                     # ← картинка
            caption=WELCOME_TEXT,                    # ← текст под картинкой
            parse_mode="HTML",                       # чтобы работали <b>, <i> и т.д.
            disable_notification=False               # можно True, если хотите без звука
        )
    except Exception as e:
        print(f"Не удалось отправить фото: {e}")
        # Если фото не отправилось — отправляем просто текст
        bot.send_message(
            uid,
            WELCOME_TEXT,
            parse_mode="HTML"
        )

    # После приветствия сразу показываем главное меню
    send_main_menu(uid)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data

    try:
        bot.answer_callback_query(call.id)
    except:
        pass

    # Главное меню
    if data.startswith("menu_"):
        try:
            bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)
        except:
            pass

        if data == "menu_community":
            photo_url = "https://drive.google.com/uc?export=view&id=1PvfsaqigBcVVEM4WmtYvfs0wNjY1wPU_"
            short_caption = "<b>«Заработались» — тёплое сообщество карьерной поддержки 🧡 </b>"
            community_text = (
                "Здесь собрались специалисты из разных сфер и этапов — от джунов до опытных профи.\n\n "
                "Вместе мы:\n"
                "- обсуждаем стратегии роста, смену ролей и выход на рынок без хаоса\n"
                "- прокачиваем резюме, портфолио и самопрезентацию\n"
                "- говорим про деньги, грейды и переговоры\n"
                "- смотрим на реальный рынок и требования\n"
                "- используем ИИ в карьерных задачах\n"
                "- разбираем твои конкретные ситуации\n"
                "- даём честную обратную связь с разных сторон\n\n"
                "<b>Мы проводим офлайн-встречи и мастермаинды в разных городах и укрепляем нетворкинг☕ </b>\n\n"
                "Наша миссия — объединять людей и помогать раскрывать их карьерный потенциал. "
                "Если откликается — нам точно по пути 💛\n\n"
                "<b> ⚡ Только до 1 мая — полностью бесплатный доступ ко всем функциям сообщества!</b>🔥\n"
            )
            try:
                bot.send_photo(uid, photo=photo_url, caption=short_caption, parse_mode="HTML")
            except Exception as e:
                print(f"Ошибка отправки фото сообщества: {e}")
                bot.send_message(uid, short_caption, parse_mode="HTML")

            bot.send_message(uid, community_text, parse_mode="HTML")
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("Да, хочу вступить", callback_data="community_join_yes"),
                InlineKeyboardButton("Пока нет", callback_data="community_join_no")
            )
            bot.send_message(uid, "Хочешь вступить в сообщество прямо сейчас?", reply_markup=markup)
            return

        elif data == "menu_podcast":
            photo_url = "https://drive.google.com/uc?export=view&id=12VcTWSaCh0SZonPbEYp6VDyLUUDSfE5u"
            short_caption = "<b>«Заработались»</b> — подкаст, где мы говорим о работе без прикрас,обсуждаем достижения, провалы и, конечно, как не потерять себя в ежедневной гонке.\n\n"
            podcast_text = (
                "В каждом выпуске болтаем с крутыми экспертами и практиками (IT, digital, менеджмент, психология, нейробиология, карьерные коучи) про самое живое:\n"
                "🌱 как строить карьеру, которая питает, а не истощает\n"
                "🗣️ эффективную коммуникацию и отношения в команде\n"
                "🚀 ведение проектов — корпоративных и своих личных\n"
                "🤝 баланс между бизнесом и человеческим фактором\n\n"
                "Учимся вписывать амбиции в реальность рынка, расти без выгорания и делать себя главным проектом своей жизни.\n\n"
                "<b>Включай, если чувствуешь: «Я окончательно заработался на своей любимой работе...»</b> 😅\n\n"
            )
            try:
                bot.send_photo(uid, photo=photo_url, caption=short_caption, parse_mode="HTML")
            except Exception as e:
                print(f"Ошибка отправки фото подкаста: {e}")
                bot.send_message(uid, short_caption, parse_mode="HTML")

            bot.send_message(uid, podcast_text, parse_mode="HTML")

            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("Слушать на Яндекс Музыке", url="https://music.yandex.com/album/33028086?dir=desc&activeTab=about"),
                InlineKeyboardButton("Слушать на Apple Podcasts", url="https://podcasts.apple.com/ru/podcast/%D0%BA%D0%B5%D0%BC-%D1%8F-%D0%BC%D0%B5%D1%87%D1%82%D0%B0%D1%8E-%D1%81%D1%82%D0%B0%D1%82%D1%8C/id1764912319"),
                InlineKeyboardButton("Смотреть на YouTube", url="https://www.youtube.com/@over_worked"),
                InlineKeyboardButton("Смотреть на RuTube", url="https://rutube.ru/channel/47932583/"),
                InlineKeyboardButton("Подписаться на Telegram-канал", url="https://t.me/overworked_community"),
                InlineKeyboardButton("← Обратно в меню", callback_data="back_to_menu")
            )
            bot.send_message(uid, "Где удобно слушать/смотреть? 👇\n\nИли вернись в главное меню:", reply_markup=markup)
            return

        elif data == "menu_consult":
            photo_url = "https://drive.google.com/uc?export=view&id=1NRlRUoVCIChBYhBHtWw0QFppdCynbp2B"
            short_caption = "Для начала — расскажем подробнее про форматы консультаций, чтобы ты выбрал(а) то, что даст максимальный результат:"
            consult_text =(
                "✨ <b> Вариант 1 — Разбор резюме (документ с комментариями) — 2000 ₽</b>\n"
                "Хочешь быстро усилить резюме и сделать его “продающим” под вакансии.\n"
                "Что входит:\n"
                "• детальный разбор резюме со всеми правками и комментариями прямо в документе\n"
                "• рекомендации, что исправить/добавить, чтобы чаще приглашали на собеседования\n"
                "• общение в чате в Telegram + ответы на твои вопросы\n\n"
                "⚡️️ <b> Вариант 2 — Тестовое HR-собеседование (40 минут, онлайн-звонок) — 3000 ₽</b>\n"
                "Что будет:\n"
                "• живое тестовое интервью как на реальном HR-скрининге\n"
                "• самые популярные вопросы + индивидуальные вопросы под твою сферу и опыт\n"
                "• разбор твоих ответов: как отвечать сильнее и увереннее\n"
                "• понимание, что именно ждёт HR и как успешно пройти скрининг\n\n"
                "🚀 <b> Вариант 3 — Карьерная консультация (40 минут, онлайн-звонок) — 3500 ₽</b>\n"
                "Если нужен план действий и стратегия поиска работы, а не просто “поправить резюме”.\n"
                "Что входит:\n"
                "• разбор резюме и внесение актуальных правок\n"
                "• разбор стратегии поиска работы (куда и как откликаться, как выделиться среди кандидатов)\n"
                "• ответы на любые вопросы в течение 24 часов после консультации\n\n"
                "🔥 <b> Вариант 4 — “Выход на рынок труда” (60 минут, онлайн-звонок) — 5000 ₽</b>\n"
                "Максимальный пакет “под ключ”, чтобы уверенно выйти на рынок и начать получать офферы.\n"
                "Что входит:\n"
                "• разбор резюме со всеми комментариями и правками\n"
                "• разбор сопроводительного письма (чтобы оно реально работало)\n"
                "• тестовое HR-собеседование\n"
                "• разбор стратегии поиска работы\n"
                "• ответы на любые вопросы в течение 48 часов\n\n"
            )
            try:
                bot.send_photo(uid, photo=photo_url, caption=short_caption, parse_mode="HTML")
            except Exception as e:
                print(f"Ошибка отправки фото: {e}")
                bot.send_message(uid, short_caption, parse_mode="HTML")
            bot.send_message(uid, consult_text, parse_mode="HTML")
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("Да, хочу", callback_data="want_consult_yes"),
                InlineKeyboardButton("Не сейчас", callback_data="want_consult_no")
            )
            bot.send_message(uid, "Хочешь оставить заявку на консультацию?", reply_markup=markup)
            return

        elif data == "menu_collaboration":
            photo_url = "https://drive.google.com/uc?export=view&id=1ncDx8bJRckx1IcFL6ewrcAA6L0x2eW5N"  # ← ВСТАВЬ СВОЮ ССЫЛКУ НА ФОТО

            caption = "<b>Форматы сотрудничества с проектом «Заработались»</b>\n\n"  # ← можно поменять

            try:
                bot.send_photo(uid, photo=photo_url, caption=caption, parse_mode="HTML")
            except Exception as e:
                print(f"Ошибка отправки фото сотрудничества: {e}")
                bot.send_message(uid, caption, parse_mode="HTML")

            collaboration_text = (
                "Мы открыты к партнёрствам и коллаборациям с экспертами, компаниями и медиа, которым близки темы карьеры, рынка труда и профессионального развития.\n\n"
                "Делимся доступными форматами коллабораций:\n\n"
                "<b>🎙 Запись эпизода подкаста «Заработались»</b>\n"
                "Совместные выпуски с экспертами, представителями компаний и проектами. Обсуждаем карьерные треки, рынок труда, развитие специалистов и команд, а также смотрим на работу и карьерные решения через призму нейробиологии и психологии: мотивацию, выгорание, адаптацию, принятие решений и устойчивость в профессиональной среде.\n\n"
                "<b>🎤 Участие в вашем проекте</b>\n"
                "Будем рады присоединиться к вашему проекту в роли спикеров — в рамках подкаста, эфира, митапа, конференции или образовательной программы.\n\n"
                "Поделимся практическим и аналитическим взглядом на карьерные стратегии, рост внутри компаний, смену ролей и переход в новую сферу, рынок труда и осознанное развитие карьеры. Работаем с реальными кейсами и адаптируем формат под аудиторию и цели проекта.\n\n"
                "<b>📢 Ваша реклама в эпизоде подкаста или в сообществе карьерной поддержки</b> \n"
                "Мы открыты к аккуратным и нативным интеграциям, которые будут полезны и релевантны нашей аудитории.\n\n"
                "<b>По вопросам рекламы и сотрудничества:</b>\n"
                "Аня @poliikarpova\n"
                "Лера @valeria_brzn\n"
                "Почта overworked.agency@gmail.com\n"
            )

            bot.send_message(uid, collaboration_text, parse_mode="HTML")

            # Кнопка назад
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("← Назад в меню", callback_data="back_to_menu")
            )
            bot.send_message(uid, "Вернуться в главное меню?", reply_markup=markup)
            return

    # Сообщество: да / нет
    if data in ["community_join_yes", "community_join_no"]:
        try:
            bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)
        except:
            pass

        if data == "community_join_no":
            bot.send_message(uid, "Хорошо, возвращаемся в меню.")
            send_main_menu(uid)
            return

        username = call.from_user.username
        username_str = f"@{username}" if username else f"ID {uid}"
        join_text = (
            "Отлично! Вот ссылка на наше сообщество:\n"
            "https://t.me/+тут_твоя_ссылка_на_чат\n\n"
            "Приятного общения! ✨"
        )
        bot.send_message(uid, join_text)

        notify_text = (
            f"💟 Новый участник cообщества!\n"
            f"Пользователь: {username_str}\n"
            f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        try:
            bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=notify_text,
                message_thread_id=THREAD_COMMUNITY_JOIN
            )
        except Exception as e:
            print(f"Ошибка отправки уведомления о сообществе: {e}")

        send_main_menu(uid)
        return

    # Заявка на консультацию — да / нет
    if data in ["want_consult_yes", "want_consult_no"]:
        if data == "want_consult_no":
            send_main_menu(uid)
            return

        try:
            bot.delete_message(uid, call.message.message_id)
        except:
            pass

        bot.send_message(
            uid,
            "Выбери формат, который на данный момент тебя интересует:",
            reply_markup=get_consult_format_inline()
        )
        return

    # Выбор формата консультации
    if data in ["consult_format_resume", "consult_format_interview", "consult_format_consultation", "consult_format_market"]:
        format_map = {
            "consult_format_resume": "Разбор резюме",
            "consult_format_interview": "Тестовое HR-собеседование",
            "consult_format_consultation": "Карьерная консультация",
            "consult_format_market": "Выход на рынок труда",
        }
        user_data.setdefault(uid, {})
        user_data[uid]["consult_format"] = format_map[data]

        try:
            bot.edit_message_reply_markup(chat_id=uid, message_id=call.message.message_id, reply_markup=None)
        except:
            pass

        bot.send_message(uid, "Подскажи, как к тебе можно обращаться?")
        user_states[uid] = STATE_NAME
        return

    # Проверка доступа к резюме
    if data in ["resume_access_yes", "resume_access_no"]:

        try:
            bot.edit_message_text(
                "Отлично, спасибо что проверил(а) доступ!" if data == "resume_access_yes" else "Хорошо, тогда пропустим резюме.",
                uid,
                call.message.message_id
            )
        except:
            bot.send_message(uid,
                             "Отлично, спасибо что проверил(а) доступ!" if data == "resume_access_yes" else "Хорошо, тогда пропустим резюме.")

        if data == "resume_access_no":
            user_data[uid]['resume_link'] = "не прикреплялось"
        photo_consultants = "https://drive.google.com/uc?export=view&id=17qqmUeF2z7Qksca9kcK3EJnjX54Q8-Sz"  # ← вставь свою ссылку сюда!
        caption_photo = "На данный момент консультации проводят Аня и Лера. Давай познакомим тебя с ними поближе:"

        try:
            bot.send_photo(
                uid,
                photo=photo_consultants,
                caption=caption_photo,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Ошибка отправки фото консультантов: {e}")
            # Если фото не загрузилось — просто продолжаем без него
            pass

        consultants_text = (
            "<b>Аня</b> — руководитель проектов и HR в КванторФорм.\n"
            "Пишет курсы для менеджеров в Яндекс Практикуме, а также является ментором в программе «Women in Tech»\n"
            "Аня ведёт канал про менеджмент и поиск работы: @itspolikarpova — там рассказывает обо всём подробнее.\n"
            "Отзывы о консультациях Ани: @review_poliikarpova\n\n"
            "<i>Она считает, что можно всего добиться, когда у тебя есть план и календарь! Её хобби — путешествия и обучение</i>\n\n"
            "<b>Лера</b> — карьерный консультант, HR-эксперт и менеджер в Яндекс Практикуме.\n"
            "@career_tet_a_tet — тут размышляет о работе и жизни в эпоху перемен.\n"
            "<i>Адепт карьерного развития через ценности, нетворкинг и бережную реализацию амбиций. В свободное от консультаций время ходит на пилатес и растит кота Ластика🤍</i>\n\n"
            "Выбери, пожалуйста, хочешь ли на консультацию к конкретному специалисту или подойдёт любой из них."
        )
        markup = InlineKeyboardMarkup(row_width=3)
        markup.add(
            InlineKeyboardButton("Аня", callback_data="consultant_anya"),
            InlineKeyboardButton("Лера", callback_data="consultant_lera"),
            InlineKeyboardButton("Любой", callback_data="consultant_any")
        )
        bot.send_message(uid, consultants_text, reply_markup=markup)
        user_states[uid] = STATE_CONSULTANT_CHOICE
        return

    # Выбор консультанта
    if data in ["consultant_anya", "consultant_lera", "consultant_any"]:
        consultant = {"consultant_anya": "Аня", "consultant_lera": "Лера", "consultant_any": "Любой"}[data]
        user_data.setdefault(uid, {})
        user_data[uid]['consultant'] = consultant

        try:
            bot.delete_message(uid, call.message.message_id)
        except:
            pass

        preview_text = (
            "Отлично, проверь свою заявку:\n\n"
            f"Формат: {user_data[uid].get('consult_format', '—')}\n"
            f"Имя: {user_data[uid].get('name', '—')}\n"
            f"Опыт: {user_data[uid].get('experience', '—')}\n"
            f"Образование: {user_data[uid].get('education', '—')}\n"
            f"Запрос: {user_data[uid].get('request', '—')}\n"
            f"Резюме: {user_data[uid].get('resume_link', 'не указано')}\n"
            f"Желаемый консультант: {consultant}\n"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Отправить заявку", callback_data="confirm_send_app"),
            InlineKeyboardButton("Вернуться в меню", callback_data="back_to_menu")
        )
        bot.send_message(uid, preview_text, reply_markup=markup)
        user_states[uid] = STATE_CONFIRM_APPLICATION
        return

    # Отправка заявки
    if data == "confirm_send_app":
        try:
            bot.delete_message(uid, call.message.message_id)
        except:
            pass

        username = call.from_user.username
        username_str = f"@{username}" if username else f"ID {uid}"

        app_text = (
            f"❗️ НОВАЯ ЗАЯВКА НА КОНСУЛЬТАЦИЮ\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Формат: {user_data[uid].get('consult_format', '—')}\n"
            f"Имя: {user_data[uid].get('name', '—')}\n"
            f"Опыт: {user_data[uid].get('experience', '—')}\n"
            f"Образование: {user_data[uid].get('education', '—')}\n"
            f"Запрос: {user_data[uid].get('request', '—')}\n"
            f"Резюме: {user_data[uid].get('resume_link', 'не указано')}\n"
            f"Желаемый консультант: {user_data[uid].get('consultant', '—')}\n"
            f"Пользователь: {username_str}\n"
            f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

        try:
            bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=app_text,
                message_thread_id=THREAD_CONSULT_APP
            )
            bot.send_message(uid, "Заявка отправлена! Скоро мы с тобой свяжемся 💛")
        except Exception as e:
            print(f"Ошибка отправки заявки: {e}")
            bot.send_message(uid, "Не удалось отправить заявку 😔\nНапиши /start и попробуй ещё раз.")

        user_data.pop(uid, None)
        user_states[uid] = STATE_NONE
        send_main_menu(uid)
        return

    if data == "back_to_menu":
        try:
            bot.delete_message(uid, call.message.message_id)
        except:
            pass
        bot.send_message(uid, "Хорошо, возвращаемся в главное меню.")
        user_data.pop(uid, None)
        user_states[uid] = STATE_NONE
        send_main_menu(uid)
        return


@bot.message_handler(func=lambda m: True)
def handle_text(message):
    uid = message.chat.id
    text = message.text.strip()

    if uid not in user_states or user_states[uid] == STATE_NONE:
        send_main_menu(uid)
        return

    state = user_states.get(uid)

    if state == STATE_NAME:
        user_data.setdefault(uid, {})
        user_data[uid]['name'] = text
        bot.send_message(uid, "Кратко опиши свой опыт работы:")
        user_states[uid] = STATE_EXPERIENCE

    elif state == STATE_EXPERIENCE:
        user_data[uid]['experience'] = text
        bot.send_message(uid, "Какое у тебя образование?")
        user_states[uid] = STATE_EDUCATION

    elif state == STATE_EDUCATION:
        user_data[uid]['education'] = text
        bot.send_message(uid, "Есть ли у тебя определенный запрос на консультацию? (Если да, напиши нам его тут)")
        user_states[uid] = STATE_REQUEST

    elif state == STATE_REQUEST:
        user_data[uid]['request'] = text
        bot.send_message(uid, "Ссылка на резюме (если есть, можно написать «нет» или поставить прочерк):")
        user_states[uid] = STATE_RESUME_LINK

    elif state == STATE_RESUME_LINK:
        user_data[uid]['resume_link'] = text if text.strip() and text.lower() != "нет" else "не указано"
        access_text = (
            "Если ты прикрепил ссылку, проверь, пожалуйста, открыт ли у тебя доступ для просмотра.\n\n"
            "Если доступа нет — консультант не сможет посмотреть резюме."
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Да, всё открыто", callback_data="resume_access_yes"),
            InlineKeyboardButton("Не прикреплял", callback_data="resume_access_no")
        )
        bot.send_message(uid, access_text, reply_markup=markup)
        user_states[uid] = STATE_RESUME_ACCESS_CHECK


if __name__ == '__main__':
    print("Бот «Заработались» запущен...")
    bot.infinity_polling(
        timeout=35,
        long_polling_timeout=60,
        allowed_updates=["message", "callback_query"],
        skip_pending=True
    )
