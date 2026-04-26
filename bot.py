import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

# User data storage
user_data = {}  # {user_id: {"role": "tourist/guide", "lang": "en/ru/kz"}}

# ==================== LANGUAGES ====================
LANGUAGES = {
    "en": {"flag": "🇬🇧", "name": "English"},
    "ru": {"flag": "🇷🇺", "name": "Русский"},
    "kz": {"flag": "🇰🇿", "name": "Қазақша"}
}

# ==================== TEXTS (multilingual) ====================
TEXTS = {
    "en": {
        "welcome": "Welcome to JABE Tour Assistant!\nPlease choose your language:",
        "choose_role": "Please choose your role:",
        "tourist": "I am Tourist 👤",
        "guide": "I am Guide 🧭",
        "tourist_menu": "Tourist menu:",
        "guide_menu": "Guide menu:",
        "itinerary": "Itinerary",
        "ai_voice": "AI Voice Tours",
        "guide_contacts": "Guide Contacts",
        "faq": "FAQ",
        "emergency": "Emergency / Support",
        "driver_details": "Driver Details",
        "ticketing": "Ticketing Database",
        "history_points": "Tour & Historical Points",
        "first_aid": "First Aid Information",

        # Content
        "itinerary_content": "Day 1: Arrival + transfer to hotel\nDay 2: Kok Tobe + Green Bazaar\nDay 3: City Tour\nDay 4: Shymbulak\nDay 5: Airport transfer",
        "voice_tours_content": "Please select a tour point. Voice messages will be added here.",
        "guide_contacts_content": "Guide: Ayan\nPhone: +7 XXX XXX XXXX",
        "faq_content": "FAQ:\n1. What time is pickup? Please check itinerary.\n2. What to wear? Comfortable shoes and warm clothes for mountains.\n3. Who to contact? Your guide or support.",
        "driver_content": "Driver: Daniyar\nCar: Mercedes Sprinter\nPlate: 777 ABC 02",
        "tickets_content": "Tickets database will show attraction tickets, QR codes, and status.",
        "history_content": "Zenkov Cathedral: Wooden Orthodox cathedral in Panfilov Park.\nKok Tobe: Viewpoint above Almaty.\nShymbulak: Mountain resort near Medeu.",
        "first_aid_content": "First Aid:\n- For emergency: call 112\n- Keep group calm\n- Inform JABE office immediately\n- Do not give medicine unless guest confirms it is safe for them"
    },
    "ru": {
        "welcome": "Добро пожаловать в JABE Tour Assistant!\nПожалуйста, выберите язык:",
        "choose_role": "Пожалуйста, выберите вашу роль:",
        "tourist": "Я Турист 👤",
        "guide": "Я Гид 🧭",
        "tourist_menu": "Меню туриста:",
        "guide_menu": "Меню гида:",
        "itinerary": "Маршрут",
        "ai_voice": "AI Аудио Экскурсии",
        "guide_contacts": "Контакты гида",
        "faq": "ЧАВО",
        "emergency": "Экстренная помощь / Поддержка",
        "driver_details": "Данные водителя",
        "ticketing": "База билетов",
        "history_points": "Туры и исторические места",
        "first_aid": "Информация первой помощи",

        "itinerary_content": "День 1: Прибытие + трансфер в отель\nДень 2: Кок-Тобе + Зеленый базар\nДень 3: Городская экскурсия\nДень 4: Шымбулак\nДень 5: Трансфер в аэропорт",
        "voice_tours_content": "Пожалуйста, выберите точку экскурсии. Голосовые сообщения будут добавлены здесь.",
        "guide_contacts_content": "Гид: Аян\nТелефон: +7 XXX XXX XXXX",
        "faq_content": "ЧАВО:\n1. Во сколько pickup? Смотрите маршрут.\n2. Что надеть? Удобную обувь и теплую одежду для гор.\n3. Кому звонить? Вашему гиду или поддержке.",
        "driver_content": "Водитель: Данияр\nАвто: Mercedes Sprinter\nНомер: 777 ABC 02",
        "tickets_content": "База билетов покажет билеты на достопримечательности, QR-коды и статус.",
        "history_content": "Кафедральный собор Зенкова: Деревянный православный собор в парке Панфилова.\nКок-Тобе: Смотровая площадка над Алматы.\nШымбулак: Горнолыжный курорт рядом с Медеу.",
        "first_aid_content": "Первая помощь:\n- При ЧП звоните 112\n- Сохраняйте спокойствие в группе\n- Немедленно сообщите в офис JABE\n- Не давайте лекарства, если гость не подтвердил безопасность"
    },
    "kz": {
        "welcome": "JABE Tour Assistant-қа қош келдіңіз!\nТілді таңдаңыз:",
        "choose_role": "Рөліңізді таңдаңыз:",
        "tourist": "Мен туристпін 👤",
        "guide": "Мен гидпін 🧭",
        "tourist_menu": "Турист мәзірі:",
        "guide_menu": "Гид мәзірі:",
        "itinerary": "Маршрут",
        "ai_voice": "AI Дауыстық турлар",
        "guide_contacts": "Гидтің байланыстары",
        "faq": "Жиі қойылатын сұрақтар",
        "emergency": "Төтенше жағдай / Қолдау",
        "driver_details": "Жүргізуші мәліметтері",
        "ticketing": "Билеттер базасы",
        "history_points": "Турлар мен тарихи нысандар",
        "first_aid": "Алғашқы көмек ақпараты",

        "itinerary_content": "1-күн: Келу + қонақүйге трансфер\n2-күн: Көк-Төбе + Жасыл базар\n3-күн: Қала туры\n4-күн: Шымбұлақ\n5-күн: Әуежайға трансфер",
        "voice_tours_content": "Тур нүктесін таңдаңыз. Дауыстық хабарламалар осында қосылады.",
        "guide_contacts_content": "Гид: Аян\nТелефон: +7 XXX XXX XXXX",
        "faq_content": "Жиі қойылатын сұрақтар:\n1. Қашан алады? Маршрутты қараңыз.\n2. Не кию керек? Жайлы аяқ киім және тауға жылы киім.\n3. Кімге хабарласу керек? Сіздің гидке немесе қолдау қызметіне.",
        "driver_content": "Жүргізуші: Данияр\nАвто: Mercedes Sprinter\nНөмірі: 777 ABC 02",
        "tickets_content": "Билеттер базасында аттракцион билеттері, QR-кодтар және статус көрсетіледі.",
        "history_content": "Зенков соборы: Панфилов саябағындағы ағаш православие соборы.\nКөк-Төбе: Алматы үстіндегі бақылау алаңы.\nШымбұлақ: Медеу маңындағы тау курорты.",
        "first_aid_content": "Алғашқы көмек:\n- Төтенше жағдайда 112-ге қоңырау шалыңыз\n- Топты тыныштандырыңыз\n- JABE офисіне дереу хабарлаңыз\n- Қонақ растағанша дәрі бермеңіз"
    }
}

# ==================== KEYBOARDS ====================
def get_language_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"{LANGUAGES['en']['flag']} English")],
            [KeyboardButton(text=f"{LANGUAGES['ru']['flag']} Русский")],
            [KeyboardButton(text=f"{LANGUAGES['kz']['flag']} Қазақша")]
        ],
        resize_keyboard=True
    )

def get_role_keyboard(lang: str):
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["tourist"])],
            [KeyboardButton(text=t["guide"])]
        ],
        resize_keyboard=True
    )

def get_tourist_keyboard(lang: str):
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["itinerary"]), KeyboardButton(text=t["ai_voice"])],
            [KeyboardButton(text=t["guide_contacts"]), KeyboardButton(text=t["faq"])],
            [KeyboardButton(text=t["emergency"])]
        ],
        resize_keyboard=True
    )

def get_guide_keyboard(lang: str):
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["driver_details"]), KeyboardButton(text=t["ticketing"])],
            [KeyboardButton(text=t["history_points"])],
            [KeyboardButton(text=t["first_aid"])]
        ],
        resize_keyboard=True
    )

# ==================== HANDLERS ====================
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        TEXTS["en"]["welcome"],   # default welcome in English
        reply_markup=get_language_keyboard()
    )

@dp.message(F.text.contains("English") | F.text.contains("Русский") | F.text.contains("Қазақша"))
async def choose_language(message: Message):
    text = message.text
    if "English" in text:
        lang = "en"
    elif "Русский" in text:
        lang = "ru"
    else:
        lang = "kz"

    user_data[message.from_user.id] = {"lang": lang}

    t = TEXTS[lang]
    await message.answer(
        t["choose_role"],
        reply_markup=get_role_keyboard(lang)
    )

@dp.message(F.text.contains
