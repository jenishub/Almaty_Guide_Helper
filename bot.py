import asyncio
import os
import io
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import openai

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API client
openai.api_key = OPENAI_API_KEY

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- User state storage ---
user_lang = {}
user_role = {}

# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
TEXTS = {
    "en": {
        "choose_lang": "Welcome to Almaty Guide & Helper!\nPlease choose your language:",
        "choose_role": "Please choose your role:",
        "btn_tourist": "🧳 I am Tourist",
        "btn_guide":   "🗺 I am Guide",
        "btn_itinerary":  "📅 Itinerary",
        "btn_voice":      "🎙 AI Voice Tours",
        "btn_contacts":   "📞 Guide Contacts",
        "btn_faq":        "❓ FAQ",
        "btn_emergency":  "🚨 Emergency / Support",
        "btn_back":       "⬅ Back to Menu",
        "tourist_menu":   "Tourist menu:",
        "voice": "🎙 Please select a tour point. Voice messages will be added here.",
        "voice_panfilov":   "🌳 *Panfilov Park*\n\nVoice tour for Panfilov Park will be available here soon.",
        "voice_greenbazaar":"🛒 *Green Bazaar*\n\nVoice tour for Green Bazaar will be available here soon.",
        "voice_koktobe":    "🏔 *Kok Tobe*\n\nVoice tour for Kok Tobe will be available here soon.",
        "voice_shymbulak":  "⛷ *Shymbulak Ski Resort*\n\nVoice tour for Shymbulak will be available here soon.",
        "voice_charyn":     "🏜 *Charyn Canyon*\n\nVoice tour for Charyn Canyon will be available here soon.",
        "voice_kolsai":     "💧 *Kolsai Lakes*\n\nVoice tour for Kolsai Lakes will be available here soon.",
        "voice_issyk":      "🌊 *Issyk Lake*\n\nVoice tour for Issyk Lake will be available here soon.",
    },
    "ru": {
        "choose_lang": "Добро пожаловать в Almaty Guide & Helper!\nПожалуйста, выберите язык:",
        "choose_role": "Пожалуйста, выберите вашу роль:",
        "btn_tourist": "🧳 Я Турист",
        "btn_guide":   "🗺 Я Гид",
        "btn_itinerary":  "📅 Маршрут",
        "btn_voice":      "🎙 AI Аудиогиды",
        "btn_contacts":   "📞 Контакты гида",
        "btn_faq":        "❓ Часто задаваемые вопросы",
        "btn_emergency":  "🚨 Экстренная помощь",
        "btn_back":       "⬅ Назад в меню",
        "tourist_menu":   "Меню туриста:",
        "voice": "🎙 Выберите точку тура. Голосовые сообщения будут добавлены здесь.",
        "voice_panfilov":   "🌳 *Парк Панфилова*\n\nАудиотур по Парку Панфилова скоро будет доступен здесь.",
        "voice_greenbazaar":"🛒 *Зелёный базар*\n\nАудиотур по Зелёному базару скоро будет доступен здесь.",
        "voice_koktobe":    "🏔 *Кок-Тобе*\n\nАудиотур по Кок-Тобе скоро будет доступен здесь.",
        "voice_shymbulak":  "⛷ *Шымбулак*\n\nАудиотур по Шымбулаку скоро будет доступен здесь.",
        "voice_charyn":     "🏜 *Чарын каньоны*\n\nАудиотур по Шарын каньоны скоро будет доступен здесь.",
        "voice_kolsai":     "💧 *Көлсай көлдері*\n\nАудиотур по Көлсай көлдері скоро будет доступен здесь.",
        "voice_issyk":      "🌊 *Ыссық көл*\n\nАудиотур по Ыссық көл скоро будет доступен здесь.",
    },
    "kk": {
        "choose_lang": "Almaty Guide & Helper чат-ботқа қош келдіңіз!\nТілді таңдаңыз:",
        "choose_role": "Рөліңізді таңдаңыз:",
        "btn_tourist": "🧳 Мен Турист",
        "btn_guide":   "🗺 Мен Гид",
        "btn_itinerary":  "📅 Маршрут",
        "btn_voice":      "🎙 AI Дыбыстық тур",
        "btn_contacts":   "📞 Гид байланыстары",
        "btn_faq":        "❓ Жиі қойылатын сұрақтар",
        "btn_emergency":  "🚨 Жедел жәрдем",
        "btn_back":       "⬅ Мәзірге оралу",
        "tourist_menu":   "Турист мәзірі:",
        "voice": "🎙 Тур нүктесін таңдаңыз. Дыбыстық хабарлар осында қосылады.",
        "voice_panfilov":   "🌳 *Панфилов саябағы*\n\nПанфилов саябағына арналған аудиотур жақында осында қолжетімді болады.",
        "voice_greenbazaar":"🛒 *Жасыл базар*\n\nЖасыл базарға арналған аудиотур жақында осында қолжетімді болады.",
        "voice_koktobe":    "🏔 *Кок-Тобе*\n\nКок-Тобеге арналған аудиотур жақында осында қолжетімді болады.",
        "voice_shymbulak":  "⛷ *Шымбулак*\n\nШымбулакқа арналған аудиотур жақында осында қолжетімді болады.",
        "voice_charyn":     "🏜 *Шарын каньоны*\n\nШарын каньонына арналған аудиотур жақында осында қолжетімді болады.",
        "voice_kolsai":     "💧 *Көлсай көлдері*\n\nКөлсай көлдеріне арналған аудиотур жақында осында қолжетімді болады.",
        "voice_issyk":      "🌊 *Ыссық көл*\n\nЫссық көлге арналған аудиотур жақында осында қолжетімді болады.",
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
            [KeyboardButton(text=t["btn_itinerary"]), KeyboardButton(text=t["btn_voice"])],
            [KeyboardButton(text=t["btn_contacts"]), KeyboardButton(text=t["btn_faq"])],
            [KeyboardButton(text=t["btn_emergency"])],
            [KeyboardButton(text=t["btn_back"])],
        ],
        resize_keyboard=True
    )

def voice_keyboard(lang: str) -> ReplyKeyboardMarkup:
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["btn_panfilov"]), KeyboardButton(text=t["btn_greenbazaar"])],
            [KeyboardButton(text=t["btn_koktobe"]), KeyboardButton(text=t["btn_shymbulak"])],
            [KeyboardButton(text=t["btn_charyn"]), KeyboardButton(text=t["btn_kolsai"])],
            [KeyboardButton(text=t["btn_issyk"])],
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

async def generate_voice(text: str) -> io.BytesIO:
    """Generate voice audio from text using OpenAI TTS"""
    logging.info("Generating voice for text: %s", text)
    try:
        response = openai.Audio.create(
            model="text-to-speech-1",  # Check if this model is available
            voice="en_us_male",        # Adjust as needed
            input=text,
            response_format="ogg_opus"  # Ensure this is compatible with Telegram
        )
        audio_buffer = io.BytesIO(response.content)
        audio_buffer.name = "voice.ogg"
        logging.info("Voice generated successfully.")
        return audio_buffer
    except Exception as e:
        logging.error("Error generating voice: %s", e)
        raise

# ─────────────────────────────────────────────
# HANDLERS — Language & Start
# ─────────────────────────────────────────────
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        TEXTS["en"]["choose_lang"],
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
    await message.answer(TEXTS[lang]["tourist_menu"], reply_markup=tourist_keyboard(lang))

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
    lang = get_lang(uid)
    await message.answer(
        TEXTS[lang]["voice"],
        reply_markup=voice_keyboard(lang)
    )

# ─────────────────────────────────────────────
# HANDLERS — Voice Tour Locations
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"🌳 Panfilov Park", "🌳 Парк Панфилова", "🌳 Панфилов саябағы"}))
async def voice_panfilov(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    tour_text = get_text(uid, "voice_panfilov")
    audio = await generate_voice(tour_text)
    await message.answer_voice(
        voice=FSInputFile(audio, filename="voice.ogg"),
        caption=tour_text,
        parse_mode="Markdown"
    )

@dp.message(F.text.in_({"🛒 Green Bazaar", "🛒 Зелёный базар", "🛒 Жасыл базар"}))
async def voice_greenbazaar(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    tour_text = get_text(uid, "voice_greenbazaar")
    audio = await generate_voice(tour_text)
    await message.answer_voice(
        voice=FSInputFile(audio, filename="voice.ogg"),
        caption=tour_text,
        parse_mode="Markdown"
    )

@dp.message(F.text.in_({"🏔 Kok Tobe", "🏔 Кок-Тобе"}))
async def voice_koktobe(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    tour_text = get_text(uid, "voice_koktobe")
    audio = await generate_voice(tour_text)
    await message.answer_voice(
        voice=FSInputFile(audio, filename="voice.ogg"),
        caption=tour_text,
        parse_mode="Markdown"
    )

@dp.message(F.text.in_({"⛷ Shymbulak Ski Resort", "⛷ Шымбулак", "⛷ Шымбұлақ"}))
async def voice_shymbulak(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    tour_text = get_text(uid, "voice_shymbulak")
    audio = await generate_voice(tour_text)
    await message.answer_voice(
        voice=FSInputFile(audio, filename="voice.ogg"),
        caption=tour_text,
        parse_mode="Markdown"
    )

@dp.message(F.text.in_({"🏜 Charyn Canyon", "🏜 Каньон Чарын", "🏜 Шарын каньоны"}))
async def voice_charyn(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    tour_text = get_text(uid, "voice_charyn")
    audio = await generate_voice(tour_text)
    await message.answer_voice(
        voice=FSInputFile(audio, filename="voice.ogg"),
        caption=tour_text,
        parse_mode="Markdown"
    )

@dp.message(F.text.in_({"💧 Kolsai Lakes", "💧 Озёра Кольсай", "💧 Көлсай көлдері"}))
async def voice_kolsai(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    tour_text = get_text(uid, "voice_kolsai")
    audio = await generate_voice(tour_text)
    await message.answer_voice(
        voice=FSInputFile(audio, filename="voice.ogg"),
        caption=tour_text,
        parse_mode="Markdown"
    )

@dp.message(F.text.in_({"🌊 Issyk Lake", "🌊 Озеро Иссык", "🌊 Ыссық көл"}))
async def voice_issyk(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    tour_text = get_text(uid, "voice_issyk")
    audio = await generate_voice(tour_text)
    await message.answer_voice(
        voice=FSInputFile(audio, filename="voice.ogg"),
        caption=tour_text,
        parse_mode="Markdown"
    )

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
