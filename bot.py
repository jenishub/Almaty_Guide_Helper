import asyncio
import os
import io
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BufferedInputFile
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from openai import OpenAI

# ─────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_lang = {}
user_role = {}

# ─────────────────────────────────────────────
# TEXTS
# ─────────────────────────────────────────────
TEXTS = {
    "en": {
        "choose_lang":      "Welcome to Almaty Guide & Helper! Please choose your language:",
        "choose_role":      "Please choose your role:",
        "tourist_menu":     "Welcome, Tourist! Choose an option:",
        "guide_menu":       "Welcome, Guide! Choose an option:",
        "btn_tourist":      "I am Tourist",
        "btn_guide":        "I am Guide",
        "btn_itinerary":    "Itinerary",
        "btn_voice":        "AI Voice Tours",
        "btn_contacts":     "Guide Contacts",
        "btn_faq":          "FAQ",
        "btn_emergency":    "Emergency / Support",
        "btn_back":         "Back to Menu",
        "btn_my_tours":     "My Tours",
        "btn_earnings":     "My Earnings",
        "btn_schedule":     "My Schedule",
        "btn_panfilov":     "Panfilov Park",
        "btn_greenbazaar":  "Green Bazaar",
        "btn_koktobe":      "Kok Tobe",
        "btn_shymbulak":    "Shymbulak",
        "btn_charyn":       "Charyn Canyon",
        "btn_kolsai":       "Kolsai Lakes",
        "btn_issyk":        "Issyk Lake",
        "voice_menu":       "Select a location for your audio tour:",
        "contacts":         "Guide Contacts:\n\nAikhansha: +7 747 709 8035",
        "faq":              "FAQ:\n\nQ: How do I book a tour?\nA: Contact our guides directly.\n\nQ: Is the app free?\nA: Yes, completely free!",
        "emergency":        "Emergency / Support:\n\nPolice: 102\nAmbulance: 103\nFire: 101",
        "itinerary":        "Recommended Almaty Itinerary:\n\nDay 1: Panfilov Park, Green Bazaar\nDay 2: Kok Tobe, Medeu\nDay 3: Shymbulak Ski Resort\nDay 4: Charyn Canyon\nDay 5: Kolsai Lakes & Issyk Lake",
        "my_tours":         "Your upcoming tours will appear here.",
        "earnings":         "Your earnings summary will appear here.",
        "schedule":         "Your schedule will appear here.",
        "tour_panfilov":    "Panfilov Park is one of the most beloved green spaces in Almaty. Named after the heroic Panfilov soldiers of World War Two, it features the stunning Zenkov Cathedral, one of the few wooden cathedrals in the world, built without a single nail. Stroll through its tree-lined paths and enjoy the peaceful atmosphere in the heart of the city.",
        "tour_greenbazaar": "Green Bazaar, or Zelyony Bazar, is the vibrant heart of Almaty's trading culture. Here you will find fresh fruits, vegetables, spices, meats, and traditional Kazakh foods all under one roof. It is the best place to taste local flavors, interact with friendly vendors, and experience the authentic daily life of Almaty residents.",
        "tour_koktobe":     "Kok Tobe, meaning Blue Hill in Kazakh, rises 1100 meters above sea level and offers a breathtaking panoramic view of Almaty city. Accessible by a scenic cable car ride, the hilltop features amusement rides, cafes, and the famous Beatles monument. It is the perfect spot to watch the sunset over the Tian Shan mountains.",
        "tour_shymbulak":   "Shymbulak Ski Resort sits at an elevation of 2200 meters in the Zailiysky Alatau mountains, just 25 kilometers from Almaty city center. It is Central Asia's premier skiing destination, offering world-class slopes for all levels, a gondola lift with spectacular mountain views, and a lively apres-ski atmosphere.",
        "tour_charyn":      "Charyn Canyon, often called Kazakhstan's answer to the Grand Canyon, stretches 80 kilometers along the Charyn River. Its dramatic red and orange rock formations, carved over millions of years, create an otherworldly landscape. The Valley of Castles section is the most famous, where towering rock pillars rise dramatically from the canyon floor.",
        "tour_kolsai":      "The Kolsai Lakes are a series of three stunning alpine lakes nestled in the Northern Tian Shan mountains. Surrounded by dense spruce forests and snow-capped peaks, these emerald-green lakes are a paradise for hikers and nature lovers. The lakes sit at progressively higher elevations, each one more beautiful and remote than the last.",
        "tour_issyk":       "Issyk Lake is a serene mountain lake located 75 kilometers east of Almaty at an elevation of 1756 meters. Surrounded by majestic mountains and lush forests, it offers a peaceful escape from the city. The lake is famous for its turquoise waters and the nearby Issyk Museum, which houses golden artifacts from the ancient Saka warrior civilization.",
    },
    "ru": {
        "choose_lang":      "Добро пожаловать! Выберите язык:",
        "choose_role":      "Выберите вашу роль:",
        "tourist_menu":     "Добро пожаловать, Турист! Выберите опцию:",
        "guide_menu":       "Добро пожаловать, Гид! Выберите опцию:",
        "btn_tourist":      "Я Турист",
        "btn_guide":        "Я Гид",
        "btn_itinerary":    "Маршрут",
        "btn_voice":        "AI Аудиогиды",
        "btn_contacts":     "Контакты гида",
        "btn_faq":          "Частые вопросы",
        "btn_emergency":    "Экстренная помощь",
        "btn_back":         "Назад в меню",
        "btn_my_tours":     "Мои туры",
        "btn_earnings":     "Мой доход",
        "btn_schedule":     "Моё расписание",
        "btn_panfilov":     "Парк Панфилова",
        "btn_greenbazaar":  "Зелёный базар",
        "btn_koktobe":      "Кок-Тобе",
        "btn_shymbulak":    "Шымбулак",
        "btn_charyn":       "Чарынский каньон",
        "btn_kolsai":       "Озёра Кольсай",
        "btn_issyk":        "Озеро Иссык",
        "voice_menu":       "Выберите место для аудиотура:",
        "contacts":         "Контакты гида:\n\nАйханша: +7 747 709 8035",
        "faq":              "Частые вопросы:\n\nВ: Как забронировать тур?\nО: Свяжитесь с гидами напрямую.\n\nВ: Приложение бесплатное?\nО: Да, полностью бесплатно!",
        "emergency":        "Экстренная помощь:\n\nПолиция: 102\nСкорая: 103\nПожарная: 101",
        "itinerary":        "Рекомендуемый маршрут по Алматы:\n\nДень 1: Парк Панфилова, Зелёный базар\nДень 2: Кок-Тобе, Медеу\nДень 3: Шымбулак\nДень 4: Чарынский каньон\nДень 5: Озёра Кольсай и Иссык",
        "my_tours":         "Ваши предстоящие туры появятся здесь.",
        "earnings":         "Сводка доходов появится здесь.",
        "schedule":         "Ваше расписание появится здесь.",
        "tour_panfilov":    "Парк Панфилова — одно из любимых мест отдыха алматинцев. Назван в честь героев-панфиловцев Второй мировой войны. Здесь находится величественный Вознесенский собор — один из немногих деревянных соборов мира, построенный без единого гвоздя. Прогуляйтесь по тенистым аллеям и насладитесь тишиной в самом сердце города.",
        "tour_greenbazaar": "Зелёный базар — это яркое сердце торговой культуры Алматы. Здесь вы найдёте свежие фрукты, овощи, специи, мясо и традиционные казахские продукты под одной крышей. Лучшее место, чтобы попробовать местные вкусы и почувствовать настоящую жизнь города.",
        "tour_koktobe":     "Кок-Тобе, что в переводе с казахского означает Синий холм, возвышается на 1100 метров над уровнем моря и предлагает захватывающую панораму Алматы. Добраться можно на живописной канатной дороге. На вершине вас ждут аттракционы, кафе и знаменитый памятник группе Битлз.",
        "tour_shymbulak":   "Горнолыжный курорт Шымбулак расположен на высоте 2200 метров в горах Заилийского Алатау, всего в 25 километрах от центра Алматы. Это лучший горнолыжный курорт Центральной Азии с трассами для любого уровня подготовки и великолепными видами на горы.",
        "tour_charyn":      "Чарынский каньон часто называют казахстанским Гранд-Каньоном. Он протянулся на 80 километров вдоль реки Чарын. Долина Замков — самая известная часть каньона, где высокие скальные образования из красного и оранжевого камня создают неземной пейзаж.",
        "tour_kolsai":      "Озёра Кольсай — это три великолепных горных озера в горах Северного Тянь-Шаня. Окружённые густыми еловыми лесами и заснеженными вершинами, эти изумрудно-зелёные озёра — настоящий рай для туристов и любителей природы.",
        "tour_issyk":       "Озеро Иссык — спокойное горное озеро в 75 километрах к востоку от Алматы на высоте 1756 метров. Знаменито бирюзовой водой и расположенным рядом музеем, где хранятся золотые артефакты древней сакской цивилизации.",
    },
    "kk": {
        "choose_lang":      "Қош келдіңіз! Тілді таңдаңыз:",
        "choose_role":      "Рөліңізді таңдаңыз:",
        "tourist_menu":     "Қош келдіңіз, Турист! Опция таңдаңыз:",
        "guide_menu":       "Қош келдіңіз, Гид! Опция таңдаңыз:",
        "btn_tourist":      "Мен Турист",
        "btn_guide":        "Мен Гид",
        "btn_itinerary":    "Маршрут",
        "btn_voice":        "AI Дыбыстық тур",
        "btn_contacts":     "Гид байланыстары",
        "btn_faq":          "Жиі сұрақтар",
        "btn_emergency":    "Жедел жәрдем",
        "btn_back":         "Мәзірге оралу",
        "btn_my_tours":     "Менің турларым",
        "btn_earnings":     "Менің табысым",
        "btn_schedule":     "Менің кестем",
        "btn_panfilov":     "Панфилов саябағы",
        "btn_greenbazaar":  "Жасыл базар",
        "btn_koktobe":      "Кок-Тобе",
        "btn_shymbulak":    "Шымбулак",
        "btn_charyn":       "Шарын каньоны",
        "btn_kolsai":       "Көлсай көлдері",
        "btn_issyk":        "Ыссық көл",
        "voice_menu":       "Аудиотур үшін орын таңдаңыз:",
        "contacts":         "Гид байланыстары:\n\nАйханша: +7 747 709 8035",
        "faq":              "Жиі сұрақтар:\n\nС: Турды қалай брондауға болады?\nЖ: Гидтермен тікелей хабарласыңыз.\n\nС: Қолданба тегін бе?\nЖ: Иә, толықтай тегін!",
        "emergency":        "Жедел жәрдем:\n\nПолиция: 102\nЖедел жәрдем: 103\nӨрт сөндіру: 101",
        "itinerary":        "Алматы бойынша ұсынылатын маршрут:\n\n1-күн: Панфилов саябағы, Жасыл базар\n2-күн: Кок-Тобе, Медеу\n3-күн: Шымбулак\n4-күн: Шарын каньоны\n5-күн: Көлсай көлдері және Ыссық көл",
        "my_tours":         "Алдағы турларыңыз осында көрсетіледі.",
        "earnings":         "Табыс қорытындысы осында көрсетіледі.",
        "schedule":         "Кестеңіз осында көрсетіледі.",
        "tour_panfilov":    "Панфилов саябағы — Алматының ең сүйікті жасыл аймақтарының бірі. Екінші дүниежүзілік соғыстың батыр панфиловшылары құрметіне аталған бұл саябақта бірде-бір шегесіз салынған әлемдегі ең сирек ағаш соборлардың бірі — Вознесенский собор орналасқан.",
        "tour_greenbazaar": "Жасыл базар — Алматының сауда мәдениетінің жарқын жүрегі. Мұнда бір шаңырақ астында жаңа жемістер, көкөністер, дәмдеуіштер, ет және дәстүрлі қазақ тағамдарын таба аласыз. Жергілікті дәмдерді татып көру және қаланың шынайы өмірін сезіну үшін ең жақсы орын.",
        "tour_koktobe":     "Қазақша Көк төбе деп аталатын Кок-Тобе теңіз деңгейінен 1100 метр биіктікте орналасып, Алматының тамаша панорамасын ұсынады. Живописті канат жолымен жетуге болады. Төбеде аттракциондар, кафелер және атақты Битлз ескерткіші бар.",
        "tour_shymbulak":   "Шымбулак тау-шаңғы курорты Алматы орталығынан 25 шақырым жерде, Іле Алатауы тауларында теңіз деңгейінен 2200 метр биіктікте орналасқан. Бұл Орталық Азияның үздік тау-шаңғы курорты.",
        "tour_charyn":      "Шарын каньоны жиі Қазақстанның Гранд-Каньоны деп аталады. Ол Шарын өзені бойында 80 шақырымға созылады. Қамалдар алқабы — қызыл және қызғылт сары жартастардан тұратын ең атақты бөлігі.",
        "tour_kolsai":      "Көлсай көлдері — Солтүстік Тянь-Шань тауларындағы үш тамаша таулы көл. Қалың шырша ормандары мен қар басқан шыңдармен қоршалған бұл зумрут жасыл көлдер туристер мен табиғат сүйгіштер үшін шын мәнінде жұмақ.",
        "tour_issyk":       "Ыссық көл — Алматыдан 75 шақырым шығысқа қарай, теңіз деңгейінен 1756 метр биіктікте орналасқан тыныш таулы көл. Бирюза суымен және көне сақ өркениетінің алтын жәдігерлері сақталған жанындағы мұражаймен атақты.",
    },
}

# ─────────────────────────────────────────────
# KEYBOARDS
# ─────────────────────────────────────────────
lang_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="English")],
        [KeyboardButton(text="Русский")],
        [KeyboardButton(text="Казакша")],
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

def guide_keyboard(lang: str) -> ReplyKeyboardMarkup:
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["btn_my_tours"]), KeyboardButton(text=t["btn_schedule"])],
            [KeyboardButton(text=t["btn_earnings"])],
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

async def generate_voice(text: str, lang: str) -> bytes:
    """Generate voice audio from text using OpenAI TTS"""
    logging.info("Generating voice, lang=%s, text preview: %s", lang, text[:60])
    voice_map = {"en": "nova", "ru": "nova", "kk": "nova"}
    selected_voice = voice_map.get(lang, "nova")
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=selected_voice,
            input=text,
            response_format="opus"
        )
        audio_bytes = response.read()
        logging.info("Voice generated successfully, size=%d bytes", len(audio_bytes))
        return audio_bytes
    except Exception as e:
        logging.error("Voice generation failed: %s", e)
        raise

async def send_voice_tour(message: Message, tour_key: str):
    """Helper to generate and send a voice tour message"""
    uid = message.from_user.id
    lang = get_lang(uid)
    tour_text = TEXTS[lang][tour_key]
    caption = tour_text[:1024]
    try:
        await message.answer("Generating your audio tour, please wait...")
        audio_bytes = await generate_voice(tour_text, lang)
        audio_file = BufferedInputFile(audio_bytes, filename="tour.ogg")
        await message.answer_voice(voice=audio_file, caption=caption)
    except Exception as e:
        logging.error("Failed to send voice tour: %s", e)
        await message.answer("Sorry, voice generation failed. Please try again later.")

# ─────────────────────────────────────────────
# HANDLERS — Start & Language
# ─────────────────────────────────────────────
@dp.message(CommandStart())
async def start(message: Message):
    logging.info("User %s started the bot", message.from_user.id)
    await message.answer(TEXTS["en"]["choose_lang"], reply_markup=lang_keyboard)

@dp.message(F.text == "English")
async def set_lang_en(message: Message):
    user_lang[message.from_user.id] = "en"
    await message.answer(TEXTS["en"]["choose_role"], reply_markup=role_keyboard("en"))

@dp.message(F.text == "Русский")
async def set_lang_ru(message: Message):
    user_lang[message.from_user.id] = "ru"
    await message.answer(TEXTS["ru"]["choose_role"], reply_markup=role_keyboard("ru"))

@dp.message(F.text == "Казакша")
async def set_lang_kk(message: Message):
    user_lang[message.from_user.id] = "kk"
    await message.answer(TEXTS["kk"]["choose_role"], reply_markup=role_keyboard("kk"))

# ─────────────────────────────────────────────
# HANDLERS — Role Selection
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"I am Tourist", "Мен Турист", "Я Турист"}))
async def tourist_role(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    user_role[uid] = "tourist"
    logging.info("User %s selected Tourist role", uid)
    await message.answer(TEXTS[lang]["tourist_menu"], reply_markup=tourist_keyboard(lang))

@dp.message(F.text.in_({"I am Guide", "Мен Гид", "Я Гид"}))
async def guide_role(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    user_role[uid] = "guide"
    logging.info("User %s selected Guide role", uid)
    await message.answer(TEXTS[lang]["guide_menu"], reply_markup=guide_keyboard(lang))

# ─────────────────────────────────────────────
# HANDLERS — Back to Menu
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"Back to Menu", "Назад в меню", "Мәзірге оралу"}))
async def back_to_menu(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    role = user_role.get(uid, "tourist")
    if role == "guide":
        await message.answer(TEXTS[lang]["guide_menu"], reply_markup=guide_keyboard(lang))
    else:
        await message.answer(TEXTS[lang]["tourist_menu"], reply_markup=tourist_keyboard(lang))

# ─────────────────────────────────────────────
# HANDLERS — Tourist Menu Items
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"Itinerary", "Маршрут"}))
async def itinerary(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["itinerary"])

@dp.message(F.text.in_({"AI Voice Tours", "AI Аудиогиды", "AI Дыбыстық тур"}))
async def voice_tours_menu(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["voice_menu"], reply_markup=voice_keyboard(lang))

@dp.message(F.text.in_({"Guide Contacts", "Контакты гида", "Гид байланыстары"}))
async def guide_contacts(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["contacts"])

@dp.message(F.text.in_({"FAQ", "Частые вопросы", "Жиі сұрақтар"}))
async def faq(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["faq"])

@dp.message(F.text.in_({"Emergency / Support", "Экстренная помощь", "Жедел жәрдем"}))
async def emergency(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["emergency"])

# ─────────────────────────────────────────────
# HANDLERS — Guide Menu Items
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"My Tours", "Мои туры", "Менің турларым"}))
async def my_tours(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["my_tours"])

@dp.message(F.text.in_({"My Earnings", "Мой доход", "Менің табысым"}))
async def my_earnings(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["earnings"])

@dp.message(F.text.in_({"My Schedule", "Моё расписание", "Менің кестем"}))
async def my_schedule(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["schedule"])

# ─────────────────────────────────────────────
# HANDLERS — Voice Tour Locations
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"Panfilov Park", "Парк Панфилова", "Панфилов саябағы"}))
async def voice_panfilov(message: Message):
    await send_voice_tour(message, "tour_panfilov")

@dp.message(F.text.in_({"Green Bazaar", "Зелёный базар", "Жасыл базар"}))
async def voice_greenbazaar(message: Message):
    await send_voice_tour(message, "tour_greenbazaar")

@dp.message(F.text.in_({"Kok Tobe", "Кок-Тобе"}))
async def voice_koktobe(message: Message):
    await send_voice_tour(message, "tour_koktobe")

@dp.message(F.text.in_({"Shymbulak", "Шымбулак"}))
async def voice_shymbulak(message: Message):
    await send_voice_tour(message, "tour_shymbulak")

@dp.message(F.text.in_({"Charyn Canyon", "Чарынский каньон", "Шарын каньоны"}))
async def voice_charyn(message: Message):
    await send_voice_tour(message, "tour_charyn")

@dp.message(F.text.in_({"Kolsai Lakes", "Озёра Кольсай", "Көлсай көлдері"}))
async def voice_kolsai(message: Message):
    await send_voice_tour(message, "tour_kolsai")

@dp.message(F.text.in_({"Issyk Lake", "Озеро Иссык", "Ыссық көл"}))
async def voice_issyk(message: Message):
    await send_voice_tour(message, "tour_issyk")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
async def main():
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
