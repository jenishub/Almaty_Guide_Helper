# bot.py
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()

# --- User state storage ---
user_lang = {}
user_role = {}

# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
TEXTS = {
    "en": {
        # Language selection
        "choose_lang": "Welcome to JABE Tour Assistant!\nPlease choose your language:",

        # Role selection
        "choose_role": "Please choose your role:",
        "btn_tourist": "🧳 I am Tourist",
        "btn_guide":   "🗺 I am Guide",

        # Tourist menu buttons
        "btn_itinerary":  "📅 Itinerary",
        "btn_voice":      "🎙 AI Voice Tours",
        "btn_contacts":   "📞 Guide Contacts",
        "btn_faq":        "❓ FAQ",
        "btn_emergency":  "🚨 Emergency / Support",

        # Guide menu buttons
        "btn_driver":     "🚗 Driver Details",
        "btn_tickets":    "🎟 Ticketing Database",
        "btn_history":    "🏛 Tour & Historical Points",
        "btn_firstaid":   "🩺 First Aid Information",

        # Back button
        "btn_back":       "⬅ Back to Menu",

        # Menu labels
        "tourist_menu":   "Tourist menu:",
        "guide_menu":     "Guide menu:",

        # Content
        "itinerary": (
            "📅 *Itinerary*\n\n"
            "Day 1: Arrival + transfer to hotel\n"
            "Day 2: Kok Tobe + Green Bazaar\n"
            "Day 3: City Tour\n"
            "Day 4: Shymbulak\n"
            "Day 5: Airport transfer"
        ),
        "voice": "🎙 Please select a tour point. Voice messages will be added here.",
        "contacts": "📞 *Guide Contacts*\n\nGuide: Ayan\nPhone: +7 XXX XXX XXXX",
        "faq": (
            "❓ *FAQ*\n\n"
            "1. What time is pickup? Please check itinerary.\n"
            "2. What to wear? Comfortable shoes and warm clothes for mountains.\n"
            "3. Who to contact? Your guide or support."
        ),
        "emergency": (
            "🚨 *Emergency / Support*\n\n"
            "Emergency number: 112\n"
            "JABE Support: +7 XXX XXX XXXX\n"
            "Please stay calm and contact your guide immediately."
        ),
        "driver": (
            "🚗 *Driver Details*\n\n"
            "Driver: Daniyar\n"
            "Car: Mercedes Sprinter\n"
            "Plate: 777 ABC 02"
        ),
        "tickets": "🎟 Tickets database will show attraction tickets, QR codes, and status.",
        "history": (
            "🏛 *Tour & Historical Points*\n\n"
            "Zenkov Cathedral: Wooden Orthodox cathedral in Panfilov Park.\n"
            "Kok Tobe: Viewpoint above Almaty.\n"
            "Shymbulak: Mountain resort near Medeu."
        ),
        "firstaid": (
            "🩺 *First Aid Information*\n\n"
            "- For emergency: call 112\n"
            "- Keep group calm\n"
            "- Inform JABE office immediately\n"
            "- Do not give medicine unless guest confirms it is safe for them"
        ),
    },

    "ru": {
        "choose_lang": "Добро пожаловать в JABE Tour Assistant!\nПожалуйста, выберите язык:",

        "choose_role": "Пожалуйста, выберите вашу роль:",
        "btn_tourist": "🧳 Я Турист",
        "btn_guide":   "🗺 Я Гид",

        "btn_itinerary":  "📅 Маршрут",
        "btn_voice":      "🎙 AI Аудиогиды",
        "btn_contacts":   "📞 Контакты гида",
        "btn_faq":        "❓ Часто задаваемые вопросы",
        "btn_emergency":  "🚨 Экстренная помощь",

        "btn_driver":     "🚗 Данные водителя",
        "btn_tickets":    "🎟 База билетов",
        "btn_history":    "🏛 Тур и исторические места",
        "btn_firstaid":   "🩺 Первая помощь",

        "btn_back":       "⬅ Назад в меню",

        "tourist_menu":   "Меню туриста:",
        "guide_menu":     "Меню гида:",

        "itinerary": (
            "📅 *Маршрут*\n\n"
            "День 1: Прибытие + трансфер в отель\n"
            "День 2: Кок-Тобе + Зелёный базар\n"
            "День 3: Обзорная экскурсия по городу\n"
            "День 4: Шымбулак\n"
            "День 5: Трансфер в аэропорт"
        ),
        "voice": "🎙 Выберите точку тура. Голосовые сообщения будут добавлены здесь.",
        "contacts": "📞 *Контакты гида*\n\nГид: Аян\nТелефон: +7 XXX XXX XXXX",
        "faq": (
            "❓ *Часто задаваемые вопросы*\n\n"
            "1. Во сколько забирают? Смотрите маршрут.\n"
            "2. Что надеть? Удобная обувь и тёплая одежда для гор.\n"
            "3. С кем связаться? С вашим гидом или службой поддержки."
        ),
        "emergency": (
            "🚨 *Экстренная помощь*\n\n"
            "Номер экстренной службы: 112\n"
            "Поддержка JABE: +7 XXX XXX XXXX\n"
            "Сохраняйте спокойствие и немедленно свяжитесь с гидом."
        ),
        "driver": (
            "🚗 *Данные водителя*\n\n"
            "Водитель: Данияр\n"
            "Автомобиль: Mercedes Sprinter\n"
            "Номер: 777 ABC 02"
        ),
        "tickets": "🎟 База билетов покажет билеты на аттракционы, QR-коды и статус.",
        "history": (
            "🏛 *Тур и исторические места*\n\n"
            "Собор Зенкова: Деревянный православный собор в парке Панфилова.\n"
            "Кок-Тобе: Смотровая площадка над Алматы.\n"
            "Шымбулак: Горный курорт вблизи Медеу."
        ),
        "firstaid": (
            "🩺 *Первая помощь*\n\n"
            "- В случае ЧП: звоните 112\n"
            "- Сохраняйте спокойствие в группе\n"
            "- Немедленно сообщите в офис JABE\n"
            "- Не давайте лекарства, пока гость не подтвердит безопасность"
        ),
    },

    "kk": {
        "choose_lang": "JABE Tour Assistant-қа қош келдіңіз!\nТілді таңдаңыз:",

        "choose_role": "Рөліңізді таңдаңыз:",
        "btn_tourist": "🧳 Мен Турист",
        "btn_guide":   "🗺 Мен Гид",

        "btn_itinerary":  "📅 Маршрут",
        "btn_voice":      "🎙 AI Дыбыстық тур",
        "btn_contacts":   "📞 Гид байланыстары",
        "btn_faq":        "❓ Жиі қойылатын сұрақтар",
        "btn_emergency":  "🚨 Жедел жәрдем",

        "btn_driver":     "🚗 Жүргізуші деректері",
        "btn_tickets":    "🎟 Билет базасы",
        "btn_history":    "🏛 Тур және тарихи орындар",
        "btn_firstaid":   "🩺 Алғашқы жәрдем",

        "btn_back":       "⬅ Мәзірге оралу",

        "tourist_menu":   "Турист мәзірі:",
        "guide_menu":     "Гид мәзірі:",

        "itinerary": (
            "📅 *Маршрут*\n\n"
            "1-күн: Жету + қонақүйге трансфер\n"
            "2-күн: Кок-Тобе + Жасыл базар\n"
            "3-күн: Қала бойынша экскурсия\n"
            "4-күн: Шымбұлақ\n"
            "5-күн: Әуежайға трансфер"
        ),
        "voice": "🎙 Тур нүктесін таңдаңыз. Дыбыстық хабарлар осында қосылады.",
        "contacts": "📞 *Гид байланыстары*\n\nГид: Аян\nТелефон: +7 XXX XXX XXXX",
        "faq": (
            "❓ *Жиі қойылатын сұрақтар*\n\n"
            "1. Қай уақытта алып кетеді? Маршрутты қараңыз.\n"
            "2. Не киюге болады? Ыңғайлы аяқкиім және таулы жылы киім.\n"
            "3. Кіммен байланысуға болады? Гидіңізбен немесе қолдау қызметімен."
        ),
        "emergency": (
            "🚨 *Жедел жәрдем*\n\n"
            "Жедел қызмет нөмірі: 112\n"
            "JABE қолдауы: +7 XXX XXX XXXX\n"
            "Сабырлы болыңыз және гидіңізбен дереу байланысыңыз."
        ),
        "driver": (
            "🚗 *Жүргізуші деректері*\n\n"
            "Жүргізуші: Данияр\n"
            "Көлік: Mercedes Sprinter\n"
            "Нөмірі: 777 ABC 02"
        ),
        "tickets": "🎟 Билет базасы тарту билеттерін, QR-кодтар мен мәртебені көрсетеді.",
        "history": (
            "🏛 *Тур және тарихи орындар*\n\n"
            "Зенков соборы: Панфилов саябағындағы ағаш православ шіркеуі.\n"
            "Кок-Тобе: Алматы үстіндегі көру алаңы.\n"
            "Шымбұлақ: Медеу маңындағы тау курорты."
        ),
        "firstaid": (
            "🩺 *Алғашқы жәрдем*\n\n"
            "- Төтенше жағдайда: 112-ге қоңырау шалыңыз\n"
            "- Топты сабырлы ұстаңыз\n"
            "- JABE кеңсесіне дереу хабарлаңыз\n"
            "- Қонақ растамаса дәрі бермеңіз"
        ),
    },
}

# ─────────────────────────────────────────────
# KEYBOARDS
# ─────────────────────────────────────────────
lang_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇬🇧 English")],
        [KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇰🇿 Қазақша")],
    ],
    resize_keyboard=True
)

def role_keyboard(lang: str) -> ReplyKeyboardMarkup:
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["btn_tourist"])],
            [KeyboardButton(text=t["btn_guide"])],
        ],
        resize_keyboard=True
    )

def tourist_keyboard(lang: str) -> ReplyKeyboardMarkup:
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["btn_itinerary"]),  KeyboardButton(text=t["btn_voice"])],
            [KeyboardButton(text=t["btn_contacts"]),   KeyboardButton(text=t["btn_faq"])],
            [KeyboardButton(text=t["btn_emergency"])],
            [KeyboardButton(text=t["btn_back"])],
        ],
        resize_keyboard=True
    )

def guide_keyboard(lang: str) -> ReplyKeyboardMarkup:
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["btn_driver"]),    KeyboardButton(text=t["btn_tickets"])],
            [KeyboardButton(text=t["btn_history"])],
            [KeyboardButton(text=t["btn_firstaid"])],
            [KeyboardButton(text=t["btn_back"])],
        ],
        resize_keyboard=True
    )

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_lang(user_id: int) -> str:
    return user_lang.get(user_id, "en")

def get_text(user_id: int, key: str) -> str:
    return TEXTS[get_lang(user_id)][key]

# ─────────────────────────────────────────────
# HANDLERS — Language & Start
# ─────────────────────────────────────────────
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Welcome to JABE Tour Assistant!\n"
        "Добро пожаловать! / Қош келдіңіз!\n\n"
        "Please choose your language / Выберите язык / Тілді таңдаңыз:",
        reply_markup=lang_keyboard
    )

@dp.message(F.text == "🇬🇧 English")
async def set_lang_en(message: Message):
    user_lang[message.from_user.id] = "en"
    await message.answer(TEXTS["en"]["choose_role"], reply_markup=role_keyboard("en"))

@dp.message(F.text == "🇷🇺 Русский")
async def set_lang_ru(message: Message):
    user_lang[message.from_user.id] = "ru"
    await message.answer(TEXTS["ru"]["choose_role"], reply_markup=role_keyboard("ru"))

@dp.message(F.text == "🇰🇿 Қазақша")
async def set_lang_kk(message: Message):
    user_lang[message.from_user.id] = "kk"
    await message.answer(TEXTS["kk"]["choose_role"], reply_markup=role_keyboard("kk"))

# ─────────────────────────────────────────────
# HANDLERS — Role Selection
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"🧳 I am Tourist", "🧳 Мен Турист", "🧳 Я Турист"}))
async def tourist_role(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    user_role[uid] = "tourist"
    await message.answer(TEXTS[lang]["tourist_menu"], reply_markup=tourist_keyboard(lang))

@dp.message(F.text.in_({"🗺 I am Guide", "🗺 Мен Гид", "🗺 Я Гид"}))
async def guide_role(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    user_role[uid] = "guide"
    await message.answer(TEXTS[lang]["guide_menu"], reply_markup=guide_keyboard(lang))

# ─────────────────────────────────────────────
# HANDLERS — Back to Menu
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"⬅ Back to Menu", "⬅ Назад в меню", "⬅ Мәзірге оралу"}))
async def back_to_menu(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    role = user_role.get(uid)
    if role == "tourist":
        await message.answer(TEXTS[lang]["tourist_menu"], reply_markup=tourist_keyboard(lang))
    elif role == "guide":
        await message.answer(TEXTS[lang]["guide_menu"], reply_markup=guide_keyboard(lang))
    else:
        await message.answer(TEXTS[lang]["choose_role"], reply_markup=role_keyboard(lang))

# ─────────────────────────────────────────────
# HANDLERS — Tourist Menu Items
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"📅 Itinerary", "📅 Маршрут"}))
async def itinerary(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "itinerary"), parse_mode="Markdown")

@dp.message(F.text.in_({"🎙 AI Voice Tours", "🎙 AI Аудиогиды", "🎙 AI Дыбыстық тур"}))
async def voice_tours(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "voice"))

@dp.message(F.text.in_({"📞 Guide Contacts", "📞 Контакты гида", "📞 Гид байланыстары"}))
async def guide_contacts(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "contacts"), parse_mode="Markdown")

@dp.message(F.text.in_({"❓ FAQ", "❓ Часто задаваемые вопросы", "❓ Жиі қойылатын сұрақтар"}))
async def faq(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "faq"), parse_mode="Markdown")

@dp.message(F.text.in_({"🚨 Emergency / Support", "🚨 Экстренная помощь", "🚨 Жедел жәрдем"}))
async def emergency(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "emergency"), parse_mode="Markdown")

# ─────────────────────────────────────────────
# HANDLERS — Guide Menu Items
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"🚗 Driver Details", "🚗 Данные водителя", "🚗 Жүргізуші деректері"}))
async def driver_details(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "driver"), parse_mode="Markdown")

@dp.message(F.text.in_({"🎟 Ticketing Database", "🎟 База билетов", "🎟 Билет базасы"}))
async def tickets(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "tickets"))

@dp.message(F.text.in_({"🏛 Tour & Historical Points", "🏛 Тур и исторические места", "🏛 Тур және тарихи орындар"}))
async def history(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "history"), parse_mode="Markdown")

@dp.message(F.text.in_({"🩺 First Aid Information", "🩺 Первая помощь", "🩺 Алғашқы жәрдем"}))
async def first_aid(message: Message):
    uid = message.from_user.id
    await message.answer(get_text(uid, "firstaid"), parse_mode="Markdown")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
