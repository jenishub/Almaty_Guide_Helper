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
        "choose_lang": "Welcome to Almaty Guide & Helper!\nPlease choose your language:",

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

         # Audio tour menu
        "btn_voice_menu_title": "🎙 Select a location for your audio tour:",
        "btn_panfilov":   "🌳 Panfilov Park",
        "btn_greenbazaar":"🛒 Green Bazaar",
        "btn_koktobe":    "🏔 Kok Tobe",
        "btn_shymbulak":  "⛷ Shymbulak Ski Resort",
        "btn_charyn":     "🏜 Charyn Canyon",
        "btn_kolsai":     "💧 Kolsai Lakes",
        "btn_issyk":      "🌊 Issyk Lake",
        "btn_back_voice": "⬅ Back",

        

        # Content
        "itinerary": (
    "📅 *Itinerary*\n\n"
    "1. **City Tour of Almaty**: Explore the vibrant city's key sights, including the Medeu Ice Skating Rink, the world’s highest ice rink located in a scenic valley, and the Palace of the Republic, a striking concert hall. Visit the historic Zenkov Cathedral, a stunning wooden structure in Panfilov Park, and finish the tour at the bustling Green Bazaar, filled with local food and crafts.\n\n"
    "2. **Kok Tobe**: A picturesque hill that provides panoramic views of Almaty and the surrounding mountains. Enjoy a cable car ride to reach the top, where you can explore various attractions, including the famous Kok Tobe TV Tower and enjoy a leisurely walk through the park.\n\n"
    "3. **Shymbulak Ski Resort**: A premier ski destination located just 25 kilometers from Almaty, known for its modern facilities and diverse slopes catering to all skill levels. Visitors can enjoy skiing, snowboarding, and breathtaking views of the surrounding peaks.\n\n"
    "4. **Charyn Canyon**: Often referred to as Kazakhstan's Grand Canyon, Charyn Canyon is a stunning natural wonder with towering rock formations and vibrant colors. Take a hike through its etched landscapes and enjoy nature’s artistry, especially at sunrise or sunset when the colors are most vivid.\n\n"
    "5. **Kolsai Lakes**: A series of stunning alpine lakes nestled between mountains, Kolsai Lakes offer breathtaking scenery and excellent hiking opportunities. The first lake is an easy hike from the parking area, while the second lake requires a bit more effort but rewards visitors with tranquility and stunning views.\n\n"
    "6. **Issyk Lake**: A beautiful glacial lake located in the Trans-Ili Alatau Mountains, known for its stunning turquoise color. The lake is surrounded by majestic peaks and is a great spot for picnicking and hiking. The area also has a rich history, with ancient burial mounds dating back to the Saka period."
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
            "Support: +7 XXX XXX XXXX\n"
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
            "- Inform the office immediately\n"
            "- Do not give medicine unless guest confirms it is safe for them"
        ),
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

        "btn_driver":     "🚗 Данные водителя",
        "btn_tickets":    "🎟 База билетов",
        "btn_history":    "🏛 Тур и исторические места",
        "btn_firstaid":   "🩺 Первая помощь",

        "btn_back":       "⬅ Назад в меню",

        "tourist_menu":   "Меню туриста:",
        "guide_menu":     "Меню гида:",
        "btn_voice_menu_title": "🎙 Выберите локацию для аудиотура:",
        "btn_panfilov":   "🌳 Парк Панфилова",
        "btn_greenbazaar": "🛒 Зелёный базар",
        "btn_koktobe":    "🏔 Кок-Тобе",
        "btn_shymbulak":  "⛷ Шымбулак",
        "btn_charyn":     "🏜 Каньон Чарын",
        "btn_kolsai":     "💧 Озёра Кольсай",
        "btn_issyk":      "🌊 Озеро Иссык",
        "btn_back_voice": "⬅ Назад",

        

        "itinerary": (
    "📅 *Маршрут*\n\n"
    "1. **Обзорная экскурсия по Алматы**: Исследуйте основные достопримечательности яркого города, включая каток Медеу, расположенный в живописной долине и являющийся самым высоким в мире, и Дворец Республики, впечатляющий концертный зал. Посетите исторический храм Зенкова — красивое деревянное строение в панфиловском парке, и завершите экскурсию на оживлённом Зеленом Базаре, полном местной еды и ремесел.\n\n"
    "2. **Кок-Тобе**: Красивый холм, который предлагает панорамные виды на Алматы и окружающие горы. Наслаждайтесь поездкой на канатной дороге, чтобы добраться до вершины, где вы можете исследовать различные достопримечательности, включая знаменитую телебашню Кок-Тобе, и прогуляться по парку.\n\n"
    "3. **Горнолыжный курорт Шымбулак**: Премиум-курорт для лыжников, расположенный всего в 25 километрах от Алматы, известен своими современными удобствами и разнообразными склонами для лыжников любого уровня подготовки. Посетители могут наслаждаться лыжным спортом, сноубордингом и захватывающими видами на окружающие вершины.\n\n"
    "4. **Каньон Чарын**: Часто называют 'Казахским Гранд Каньоном', каньон Чарын — это потрясающее природное чудо с высокими скальными образованиями и яркими цветами. Пройдите по его вырезанным пейзажам и наслаждайтесь искусством природы, особенно на рассвете или закате, когда цвета наиболее яркие.\n\n"
    "5. **Озера Кольсай**: Серия потрясающих альпийских озер, расположенных между горами. Озера Кольсай предлагают захватывающие пейзажи и отличные возможности для хайкинга. Первое озеро легко достигнуть от парковки, а для второго потребуется немного больше усилий, но вы будете вознаграждены спокойствием и потрясающими видами.\n\n"
    "6. **Озеро Иссык**: Красивое ледниковое озеро, расположенное в горном массиве Заилийский Алатау, известное своим удивительным бирюзовым цветом. Озеро окружено величественными вершинами и отлично подходит для пикников и хайкинга. Этот район также богат историей, с древними курганами, относящимися к сакскому периоду."
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
            "Поддержка: +7 XXX XXX XXXX\n"
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
            "- Немедленно сообщите в офис \n"
            "- Не давайте лекарства, пока гость не подтвердит безопасность"
        ),
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

        "btn_driver":     "🚗 Жүргізуші деректері",
        "btn_tickets":    "🎟 Билет базасы",
        "btn_history":    "🏛 Тур және тарихи орындар",
        "btn_firstaid":   "🩺 Алғашқы жәрдем",

        "btn_back":       "⬅ Мәзірге оралу",

        "tourist_menu":   "Турист мәзірі:",
        "guide_menu":     "Гид мәзірі:",
        "btn_voice_menu_title": "🎙 Аудиотур үшін орынды таңдаңыз:",
        "btn_panfilov":   "🌳 Панфилов саябағы",
        "btn_greenbazaar": "🛒 Жасыл базар",
        "btn_koktobe":    "🏔 Кок-Тобе",
        "btn_shymbulak":  "⛷ Шымбұлақ",
        "btn_charyn":     "🏜 Шарын каньоны",
        "btn_kolsai":     "💧 Көлсай көлдері",
        "btn_issyk":      "🌊 Ыссық көл",
        "btn_back_voice": "⬅ Артқа",
        

        "itinerary": (
    "📅 *Маршрут*\n\n"
    "1. **Алматы қаласына экскурсия**: Жанды қаланың басты көрнекті орындарын зерттеңіз, соның ішінде Медеу мұз айдынын, керемет көркем алқапта орналасқан әлемнің ең жоғары мұз айдынын, және Республика сарайын, тамаша концерт залы. Панфилов паркіндегі Зенков соборына барып, жергілікті тамақтар мен қолөнер бұйымдарымен толтырылған Жасыл базарда экскурсияны аяқтаңыз.\n\n"
    "2. **Кок-Тобе**: Алматы мен айналасындағы таулардың панорамалық көріністерін ұсынатын көркем төбе. Төбеге жету үшін канат жолымен көтеріліп, әйгілі Кок-Тобе телеқабылдағышы мен парктің бойымен серуендеуді тамашалаңыз.\n\n"
    "3. **Шымбулак тау-шаңғы курорты**: Алматыдан небәрі 25 шақырым жерде орналасқан үздік шаңғы орны, заманауи құрал-жабдықтарымен және түрлі деңгейдегі шаңғы жолдарымен танымал. Қонақтар шаңғы тебу, сноубордпен сырғанау мен таулардың керемет көріністерін тамашалай алады.\n\n"
    "4. **Шарын каньоны**: Қазақстанның Гранд Каньоны деп аталатын Шарын каньоны — бұл таудағы таңғажайып табиғи көрініс, жоғары тастар мен жарқын түстермен. Ол арқылы серуендеп, кешкісін немесе таңыда түстердің ең айқын сәттерін тамашалаңыз.\n\n"
    "5. **Көлсай көлдері**: Тау арасында орналасқан керемет альпілік көлдердің сериясы, Көлсай көлдері керемет көріністер мен тамаша серуендеу мүмкіндіктерін ұсынады. Бірінші көлге автотұрақтан оңай жетуге болады, екінші көлге жету үшін біраз күш жұмсау керек, бірақ тыныштық пен керемет көрініс ұсынады.\n\n"
    "6. **Ыссық көл**: Заилий Алатау тауларындағы әдемі мұздық көл, таңғажайып көгілдір түсімен танымал. Көл аспаннан көркем шыңдармен қоршалған, пикник жасау мен серуендеу үшін тамаша орын. Бұл аймақта сол саналы заманауи кезеңіне тиесілі көне қорымдар бар."
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
            "Қолдау: +7 XXX XXX XXXX\n"
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
            "- Кеңсесіне дереу хабарлаңыз\n"
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
        "Welcome to Almaty Guide & Helper!\n"
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
