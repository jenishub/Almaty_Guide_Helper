import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

# Store user language and role
user_data = {}  # {user_id: {"lang": "en", "role": "tourist"} }

# ==================== LANGUAGES & TEXTS ====================
LANGUAGES = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "kz": "🇰🇿 Қазақша"
}

TEXTS = {
    "en": {
        "welcome": "Welcome to JABE Tour Assistant!\nPlease choose your language:",
        "choose_role": "Please choose your role:",
        "tourist": "👤 I am Tourist",
        "guide": "🧭 I am Guide",
        "tourist_menu": "🧳 Tourist Menu:",
        "guide_menu": "🗺️ Guide Menu:",
        "change_lang": "🌐 Change Language",
        "itinerary": "Itinerary",
        "ai_voice": "AI Voice Tours",
        "guide_contacts": "Guide Contacts",
        "faq": "FAQ",
        "emergency": "Emergency / Support",
        "driver_details": "Driver Details",
        "ticketing": "Ticketing Database",
        "history_points": "Tour & Historical Points",
        "first_aid": "First Aid Information",

        "itinerary_content": "Day 1: Arrival + transfer to hotel\nDay 2: Kok Tobe + Green Bazaar\nDay 3: City Tour\nDay 4: Shymbulak\nDay 5: Airport transfer",
        "voice_tours_content": "Please select a tour point. Voice messages will be added here soon.",
        "guide_contacts_content": "Guide: Ayan\nPhone: +7 XXX XXX XXXX",
        "faq_content": "FAQ:\n1. What time is pickup? → Check the itinerary.\n2. What to wear? → Comfortable shoes and warm clothes for mountains.\n3. Who to contact? → Your guide or support.",
        "driver_content": "Driver: Daniyar\nCar: Mercedes Sprinter\nPlate: 777 ABC 02",
        "tickets_content": "Tickets database will show attraction tickets, QR codes, and status.",
        "history_content": "• Zenkov Cathedral: Wooden Orthodox cathedral in Panfilov Park.\n• Kok Tobe: Viewpoint above Almaty.\n• Shymbulak: Mountain resort near Medeu.",
        "first_aid_content": "First Aid:\n- Emergency: call 112\n- Keep the group calm\n- Inform JABE office immediately\n- Do not give medicine unless the guest confirms it is safe"
    },
    "ru": {
        "welcome": "Добро пожаловать в JABE Tour Assistant!\nПожалуйста, выберите язык:",
        "choose_role": "Пожалуйста, выберите вашу роль:",
        "tourist": "👤 Я Турист",
        "guide": "🧭 Я Гид",
        "tourist_menu": "🧳 Меню туриста:",
        "guide_menu": "🗺️ Меню гида:",
        "change_lang": "🌐 Сменить язык",
        "itinerary": "Маршрут",
        "ai_voice": "AI Аудио Экскурсии",
        "guide_contacts": "Контакты гида",
        "faq": "ЧАВО",
        "emergency": "Экстренная помощь",
        "driver_details": "Данные водителя",
        "ticketing": "База билетов",
        "history_points": "Туры и исторические места",
        "first_aid": "Первая помощь",

        "itinerary_content": "День 1: Прибытие + трансфер в отель\nДень 2: Кок-Тобе + Зеленый базар\nДень 3: Городская экскурсия\nДень 4: Шымбулак\nДень 5: Трансфер в аэропорт",
        "voice_tours_content": "Пожалуйста, выберите точку экскурсии. Голосовые сообщения будут добавлены позже.",
        "guide_contacts_content": "Гид: Аян\nТелефон: +7 XXX XXX XXXX",
        "faq_content": "ЧАВО:\n1. Во сколько сбор? → Смотрите маршрут.\n2. Что надеть? → Удобную обувь и теплую одежду для гор.\n3. Кому обращаться? → К гиду или в поддержку.",
        "driver_content": "Водитель: Данияр\nАвто: Mercedes Sprinter\nНомер: 777 ABC 02",
        "tickets_content": "База билетов покажет билеты, QR-к
