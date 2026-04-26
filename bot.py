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
        "btn_driver":       "Driver Details",
        "btn_hist_details": "Tour Historical Details",
        "btn_first_aid":    "First Aid Info",
        "btn_tickets":      "Ticket Database",
        "btn_panfilov":     "Panfilov Park",
        "btn_greenbazaar":  "Green Bazaar",
        "btn_koktobe":      "Kok Tobe",
        "btn_shymbulak":    "Shymbulak",
        "btn_charyn":       "Charyn Canyon",
        "btn_kolsai":       "Kolsai Lakes",
        "btn_issyk":        "Issyk Lake",
        "voice_menu":       "Select a location for your audio tour:",
        "hist_menu":        "Select a location for historical details:",
        "contacts":         "Guide Contacts:\n\nAikhansha: +7 747 709 8035",
        "faq":              "FAQ:\n\nQ: How do I book a tour?\nA: Contact our guides directly.\n\nQ: Is the app free?\nA: Yes, completely free!",
        "emergency":        "Emergency / Support:\n\nPolice: 102\nAmbulance: 103\nFire: 101",

        # ── TOURIST ITINERARY ──────────────────────────────────────────────
        "itinerary": (
            "Almaty Tour Itinerary\n\n"
            "1. Panfilov Park\n"
            "A beloved city park named after the heroic Panfilov soldiers of WWII. Home to the stunning Zenkov Cathedral, one of the few wooden cathedrals in the world built without a single nail. Perfect for a peaceful morning stroll.\n\n"
            "2. Kok Tobe\n"
            "A hilltop park at 1,100 m above sea level offering breathtaking panoramic views of Almaty. Reachable by a scenic cable car. Features the famous Beatles monument, cafes, and amusement rides.\n\n"
            "3. Shymbulak Ski Resort\n"
            "Central Asia's premier ski resort located 25 km from the city at 2,200 m elevation. Offers world-class ski slopes for all levels, a modern gondola lift, and spectacular Tian Shan mountain scenery.\n\n"
            "4. Charyn Canyon\n"
            "Often called Kazakhstan's Grand Canyon, stretching 80 km along the Charyn River. The Valley of Castles features dramatic red and orange rock formations carved over millions of years. A must-see natural wonder.\n\n"
            "5. Kolsai Lakes\n"
            "A series of three stunning emerald-green alpine lakes nestled in the Northern Tian Shan mountains. Surrounded by dense spruce forests and snow-capped peaks. A paradise for hiking and nature lovers.\n\n"
            "6. Issyk Lake\n"
            "A serene mountain lake 75 km east of Almaty at 1,756 m elevation. Famous for its turquoise waters and nearby Issyk Museum housing golden artifacts of the ancient Saka warrior civilization.\n\n"
            "7. Green Bazaar\n"
            "Almaty's most vibrant traditional market. Packed with fresh fruits, vegetables, spices, meats, and authentic Kazakh foods under one roof. The best place to taste local flavors and experience real city life."
        ),

        # ── GUIDE: DRIVER DETAILS ──────────────────────────────────────────
        "driver_details": (
            "Driver Details\n\n"
            "Company: Royal Transfer\n"
            "Phone: +7 705 770 0075\n\n"
            "Please coordinate all pickups, drop-offs, and schedule changes directly with the driver. "
            "Ensure the driver is informed at least 30 minutes before each departure."
        ),

        # ── GUIDE: HISTORICAL DETAILS ──────────────────────────────────────
        "hist_panfilov": (
            "Panfilov Park - Historical Details\n\n"
            "Panfilov Park was established in the late 19th century during the Russian Imperial period, originally called Pushkin Park. "
            "It was renamed in honor of General Ivan Panfilov and his 28 guardsmen, who heroically defended Moscow against Nazi forces in November 1941 during the Battle of Volokolamsk Highway. "
            "All 28 soldiers were posthumously awarded the title Hero of the Soviet Union.\n\n"
            "The centerpiece of the park is the Zenkov Cathedral (Ascension Cathedral), constructed between 1904 and 1907 by architect Andrei Zenkov. "
            "Standing 54 meters tall, it is one of the tallest wooden buildings in the world and was built entirely without nails using traditional Russian carpentry techniques. "
            "Remarkably, the cathedral survived the devastating 1911 Kebin earthquake, which measured 7.7 on the Richter scale and destroyed much of the city.\n\n"
            "The park also contains a WWII memorial with an eternal flame dedicated to fallen Kazakh soldiers. "
            "It was declared a protected historical monument and fully restored in the 1970s and again in the 2000s."
        ),
        "hist_koktobe": (
            "Kok Tobe - Historical Details\n\n"
            "Kok Tobe, meaning Blue Hill in the Kazakh language, has been a significant landmark above Almaty for centuries. "
            "Historically, the hill served as a natural watchtower and strategic observation point over the Ili River valley and the surrounding steppes.\n\n"
            "In the Soviet era, Kok Tobe became home to the Almaty TV Tower, constructed in 1975. "
            "Standing 372 meters above the hill's base, the tower was once the tallest structure in Central Asia and remains an iconic part of the city skyline. "
            "The tower was built using advanced engineering to withstand seismic activity, as Almaty sits in one of the most earthquake-prone zones in Kazakhstan.\n\n"
            "The cable car connecting the city center to Kok Tobe was inaugurated in 1967 and has become one of the most beloved attractions in Almaty. "
            "The famous bronze Beatles monument, gifted by a Kazakh businessman and Beatles fan in 2007, has become a cultural symbol and popular photo spot. "
            "The park was extensively renovated in the 2000s and 2010s, adding entertainment facilities and dining venues while preserving its natural landscape."
        ),
        "hist_shymbulak": (
            "Shymbulak Ski Resort - Historical Details\n\n"
            "Shymbulak, whose name derives from the Kazakh words meaning a place where horses graze, has a rich sporting history dating back to the 1930s. "
            "The area was first developed as a ski destination during the Soviet period, when Almaty, then known as Alma-Ata, was a major Soviet city.\n\n"
            "In 1972, the resort gained international recognition when it hosted the World Alpine Skiing Championships, putting Central Asian skiing on the global map. "
            "Soviet athletes trained extensively at Shymbulak, and it became a prestigious destination for elite Soviet sports programs.\n\n"
            "The resort sits at the foot of the Zailiysky Alatau range, part of the Northern Tian Shan mountains, which have been inhabited and traversed by nomadic Kazakh tribes for thousands of years. "
            "The ancient Silk Road trade routes passed through the mountain passes near this region, connecting China, Central Asia, and Europe.\n\n"
            "After Kazakhstan's independence in 1991, Shymbulak underwent major modernization investments, including the installation of a high-speed gondola lift in 2011, "
            "transforming it into a world-class resort. The nearby Medeu ice skating rink, built in 1972 at 1,691 meters elevation, holds the record for the highest altitude speed skating rink in the world."
        ),
        "hist_charyn": (
            "Charyn Canyon - Historical Details\n\n"
            "Charyn Canyon is one of the most remarkable geological formations in Central Asia, formed over 12 million years through erosion by the Charyn River and wind forces. "
            "The canyon stretches approximately 80 kilometers in length, reaching depths of up to 300 meters in some sections.\n\n"
            "The most famous section, the Valley of Castles, earned its name from the towering rock formations that resemble medieval fortresses and castle spires. "
            "The reddish and orange hues of the rocks come from iron oxide deposits within the ancient sedimentary layers.\n\n"
            "Archaeological evidence suggests that the canyon and its surrounding areas were inhabited by ancient nomadic peoples dating back to the Bronze Age, approximately 3,000 to 4,000 years ago. "
            "Stone tools, burial mounds called kurgans, and petroglyphs have been discovered in the region.\n\n"
            "The Ash Grove within the canyon is of significant scientific importance. It contains a relic grove of Sogdian ash trees, a species that survived the last Ice Age in this sheltered microclimate. "
            "These trees are considered living fossils and are protected as a UNESCO-recognized natural heritage site. "
            "The canyon was declared a national nature reserve in 2004."
        ),
        "hist_kolsai": (
            "Kolsai Lakes - Historical Details\n\n"
            "The Kolsai Lakes, known in Kazakh as Kolsay Kolderi meaning lakes of the valley, are a system of three glacial lakes located in the Kungey Alatau mountain range of the Northern Tian Shan. "
            "They sit at elevations of 1,818 meters, 2,252 meters, and 2,850 meters respectively.\n\n"
            "The lakes are fed by glacial meltwater and mountain springs, giving them their characteristic deep emerald-green color. "
            "The surrounding forests of Tian Shan spruce, which can grow to heights of 60 meters, represent one of the last significant spruce forest ecosystems in Central Asia.\n\n"
            "Historically, the mountain valleys around Kolsai were seasonal grazing grounds for Kazakh nomadic tribes, particularly the Great Zhuz clan confederation. "
            "The Tian Shan mountain range formed a natural barrier between the Kazakh steppes and Chinese territory, and the passes near Kolsai were used by Silk Road traders and nomadic migrations.\n\n"
            "The Kolsai Lakes were declared a State National Nature Park in 2007, protecting over 160,000 hectares of mountain ecosystem. "
            "The area is home to endangered species including the Snow Leopard, Marco Polo sheep, and the Tian Shan brown bear."
        ),
        "hist_issyk": (
            "Issyk Lake - Historical Details\n\n"
            "Issyk Lake holds extraordinary historical significance as the site of one of the most remarkable archaeological discoveries in Central Asian history. "
            "In 1969, Soviet archaeologists excavating a burial mound near the lake uncovered the tomb of a Saka warrior prince, dating back to the 5th to 4th century BC.\n\n"
            "The burial contained over 4,000 golden artifacts, including an ornate golden suit of armor adorned with intricate animal motifs, a golden headdress standing 70 cm tall, golden weapons, and golden vessels. "
            "This discovery became known as the Golden Man or Altyn Adam in Kazakh, and the image of the Golden Man has become the national symbol of Kazakhstan, "
            "appearing on the state emblem and the country's currency.\n\n"
            "The Saka people were a branch of the ancient Scythian civilization, skilled horsemen and warriors who dominated the Eurasian steppe from approximately the 8th to the 3rd century BC. "
            "Their sophisticated goldsmithing techniques and the wealth of the burial indicate Issyk was a site of great political and ceremonial importance.\n\n"
            "The lake itself was formed by a massive landslide in 1963 caused by a catastrophic mudflow that destroyed the original smaller lake. "
            "The Issyk State Historical and Cultural Museum, located near the lake, houses replicas of the Golden Man artifacts, with the originals displayed in the National Museum of Kazakhstan in Nur-Sultan."
        ),
        "hist_greenbazaar": (
            "Green Bazaar - Historical Details\n\n"
            "The Green Bazaar, officially known as Zelyony Bazar in Russian, has been the commercial heart of Almaty for over 150 years. "
            "Its origins trace back to the mid-19th century when the Russian Imperial military garrison of Verny, the original name of Almaty, established a trading post in the area.\n\n"
            "As the city of Verny grew through the late 1800s, the bazaar expanded into a major trading hub connecting Russian settlers, Kazakh nomads, Chinese merchants from Xinjiang, and traders from across Central Asia. "
            "Silk, spices, livestock, dried fruits, and handcrafted goods were the primary commodities exchanged.\n\n"
            "The current permanent market structure was built during the Soviet era in the mid-20th century, replacing the open-air market stalls with a covered facility. "
            "The Soviet authorities used the bazaar as a model of collective agricultural trade, where state farm cooperatives sold produce directly to urban consumers.\n\n"
            "After Kazakhstan's independence in 1991, the bazaar transitioned to a free market economy and became a symbol of the entrepreneurial spirit of Almaty. "
            "Today it spans over 10,000 square meters and hosts hundreds of vendors selling everything from fresh produce and meats to spices, nuts, dairy, and traditional Kazakh handicrafts. "
            "It remains one of the most authentic cultural experiences in the city."
        ),

        # ── GUIDE: FIRST AID ───────────────────────────────────────────────
        "first_aid": (
            "First Aid Information for Tour Guides\n\n"
            "EMERGENCY NUMBERS:\n"
            "Police: 102 | Ambulance: 103 | Fire: 101 | Mountain Rescue: 112\n\n"
            "--- GENERAL PRINCIPLES ---\n"
            "1. Ensure the scene is safe before approaching.\n"
            "2. Call 103 (ambulance) immediately for serious injuries.\n"
            "3. Stay calm and reassure the patient.\n"
            "4. Do not move a person with a suspected spinal injury.\n\n"
            "--- CPR (CARDIOPULMONARY RESUSCITATION) ---\n"
            "1. Check for responsiveness - tap shoulders and shout.\n"
            "2. Call 103 immediately.\n"
            "3. Place heel of hand on center of chest.\n"
            "4. Press down 5-6 cm, 30 compressions at 100-120 per minute.\n"
            "5. Give 2 rescue breaths if trained, then repeat cycle.\n"
            "6. Continue until ambulance arrives.\n\n"
            "--- CHOKING ---\n"
            "1. Encourage strong coughing if person can cough.\n"
            "2. Give up to 5 firm back blows between shoulder blades.\n"
            "3. If ineffective, give up to 5 abdominal thrusts (Heimlich).\n"
            "4. Alternate back blows and abdominal thrusts until clear.\n"
            "5. Call 103 if person becomes unconscious.\n\n"
            "--- BLEEDING ---\n"
            "1. Apply firm direct pressure with clean cloth or bandage.\n"
            "2. Do not remove the cloth - add more on top if soaking.\n"
            "3. Elevate the injured limb above heart level if possible.\n"
            "4. Keep pressure for at least 10 minutes continuously.\n"
            "5. Seek medical help for deep or non-stopping wounds.\n\n"
            "--- ALTITUDE SICKNESS (Relevant for Shymbulak & Kolsai) ---\n"
            "Symptoms: Headache, nausea, dizziness, fatigue, shortness of breath.\n"
            "1. Stop ascending immediately.\n"
            "2. Rest and hydrate with water.\n"
            "3. If symptoms worsen, descend to lower altitude immediately.\n"
            "4. Administer ibuprofen or aspirin for headache if available.\n"
            "5. Call 112 for mountain rescue if person cannot walk.\n\n"
            "--- HYPOTHERMIA (Cold Exposure) ---\n"
            "Symptoms: Shivering, confusion, slurred speech, pale cold skin.\n"
            "1. Move person to a warm sheltered area immediately.\n"
            "2. Remove wet clothing and replace with dry warm layers.\n"
            "3. Cover with blankets including head and neck.\n"
            "4. Give warm (not hot) drinks if person is conscious.\n"
            "5. Do not rub limbs - it can cause heart complications.\n"
            "6. Call 103 for severe cases.\n\n"
            "--- FRACTURES & SPRAINS ---\n"
            "1. Do not attempt to straighten the injured limb.\n"
            "2. Immobilize using a splint or improvised support.\n"
            "3. Apply ice pack wrapped in cloth to reduce swelling.\n"
            "4. Elevate the injured limb.\n"
            "5. Transport to hospital or call 103 for serious fractures.\n\n"
            "--- HEAT EXHAUSTION ---\n"
            "Symptoms: Heavy sweating, weakness, cold pale clammy skin, faint pulse.\n"
            "1. Move to a cool shaded area immediately.\n"
            "2. Loosen tight clothing.\n"
            "3. Apply cool wet cloths to skin.\n"
            "4. Give cool water to drink in small sips.\n"
            "5. If vomiting or unconscious, call 103 immediately.\n\n"
            "NOTE: Always carry a basic first aid kit on all tours. "
            "Recommended kit: bandages, gauze, antiseptic wipes, medical gloves, "
            "scissors, tweezers, ibuprofen, rehydration salts, emergency blanket, whistle."
        ),

        # ── GUIDE: TICKET DATABASE ─────────────────────────────────────────
        "tickets": (
            "Ticket Database\n\n"
            "Shymbulak Ski Resort\n"
            "Official Website: https://shymbulak.com\n"
            "Purchase ski passes, gondola tickets, and check current prices and operating hours directly on the website.\n\n"
            "Kok Tobe\n"
            "Official Website: https://koktobe.com\n"
            "Purchase cable car tickets, check park entry fees, and view current event schedules on the website.\n\n"
            "Note: Always check the official websites for the most up-to-date pricing, seasonal availability, and group booking options before your tour."
        ),

        # ── VOICE TOUR CONTENT ─────────────────────────────────────────────
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
        "btn_driver":       "Данные водителя",
        "btn_hist_details": "Исторические данные",
        "btn_first_aid":    "Первая помощь",
        "btn_tickets":      "База билетов",
        "btn_panfilov":     "Парк Панфилова",
        "btn_greenbazaar":  "Зелёный базар",
        "btn_koktobe":      "Кок-Тобе",
        "btn_shymbulak":    "Шымбулак",
        "btn_charyn":       "Чарынский каньон",
        "btn_kolsai":       "Озёра Кольсай",
        "btn_issyk":        "Озеро Иссык",
        "voice_menu":       "Выберите место для аудиотура:",
        "hist_menu":        "Выберите место для исторических данных:",
        "contacts":         "Контакты гида:\n\nАйханша: +7 747 709 8035",
        "faq":              "Частые вопросы:\n\nВ: Как забронировать тур?\nО: Свяжитесь с гидами напрямую.\n\nВ: Приложение бесплатное?\nО: Да, полностью бесплатно!",
        "emergency":        "Экстренная помощь:\n\nПолиция: 102\nСкорая: 103\nПожарная: 101",

        "itinerary": (
            "Маршрут по Алматы\n\n"
            "1. Парк Панфилова\n"
            "Любимый городской парк, названный в честь героев-панфиловцев ВОВ. Здесь находится Вознесенский собор — один из немногих деревянных соборов мира, построенный без единого гвоздя. Идеален для утренней прогулки.\n\n"
            "2. Кок-Тобе\n"
            "Парк на вершине холма высотой 1100 м над уровнем моря с панорамным видом на Алматы. Добраться можно на канатной дороге. Здесь расположены памятник Битлз, кафе и аттракционы.\n\n"
            "3. Горнолыжный курорт Шымбулак\n"
            "Лучший горнолыжный курорт Центральной Азии в 25 км от города на высоте 2200 м. Трассы для всех уровней подготовки, гондольный подъёмник и виды на Тянь-Шань.\n\n"
            "4. Чарынский каньон\n"
            "Казахстанский аналог Гранд-Каньона протяжённостью 80 км вдоль реки Чарын. Долина Замков с красно-оранжевыми скалами — обязательное место для посещения.\n\n"
            "5. Озёра Кольсай\n"
            "Три изумрудных горных озера в Северном Тянь-Шане. Окружены еловыми лесами и снежными вершинами. Рай для любителей пешего туризма и природы.\n\n"
            "6. Озеро Иссык\n"
            "Горное озеро в 75 км к востоку от Алматы. Знаменито бирюзовой водой и музеем с золотыми артефактами сакской цивилизации.\n\n"
            "7. Зелёный базар\n"
            "Самый яркий рынок Алматы. Фрукты, овощи, специи, мясо и казахские деликатесы под одной крышей. Лучшее место для дегустации местных вкусов."
        ),

        "driver_details": (
            "Данные водителя\n\n"
            "Компания: Royal Transfer\n"
            "Телефон: +7 705 770 0075\n\n"
            "Пожалуйста, координируйте все посадки, высадки и изменения расписания напрямую с водителем. "
            "Убедитесь, что водитель предупреждён не менее чем за 30 минут до каждого отправления."
        ),

        "hist_panfilov": (
            "Парк Панфилова - Исторические данные\n\n"
            "Парк был основан в конце XIX века в период Российской Империи, первоначально назывался Парком Пушкина. "
            "Переименован в честь генерала Ивана Панфилова и его 28 гвардейцев, героически оборонявших Москву от нацистских войск в ноябре 1941 года. "
            "Все 28 солдат посмертно удостоены звания Героя Советского Союза.\n\n"
            "Главная достопримечательность — Вознесенский собор (1904-1907), построенный архитектором Андреем Зенковым. "
            "Высотой 54 метра, это одно из самых высоких деревянных зданий в мире, возведённое без единого гвоздя. "
            "Собор пережил разрушительное землетрясение 1911 года магнитудой 7,7 балла.\n\n"
            "В парке также находится мемориал ВОВ с вечным огнём. Объект охраняется как исторический памятник."
        ),
        "hist_koktobe": (
            "Кок-Тобе - Исторические данные\n\n"
            "Кок-Тобе, что означает Синий холм, на протяжении веков служил стратегическим наблюдательным пунктом над долиной реки Или.\n\n"
            "В советскую эпоху здесь была построена Алматинская телебашня (1975 г.) высотой 372 метра над основанием холма — некогда самое высокое сооружение в Центральной Азии. "
            "Башня спроектирована с учётом сейсмической активности региона.\n\n"
            "Канатная дорога открыта в 1967 году. Памятник Битлз, подаренный в 2007 году казахским меломаном, стал культурным символом. "
            "В 2000-х и 2010-х годах парк был масштабно реконструирован."
        ),
        "hist_shymbulak": (
            "Шымбулак - Исторические данные\n\n"
            "Название Шымбулак в переводе означает место, где пасутся лошади. История курорта как горнолыжного направления начинается в 1930-х годах.\n\n"
            "В 1972 году здесь прошёл Чемпионат мира по горнолыжному спорту. Советские спортсмены активно тренировались на Шымбулаке.\n\n"
            "Горный хребет Заилийский Алатай тысячелетиями был летним пастбищем для казахских кочевников, а через перевалы пролегали маршруты Великого Шёлкового пути.\n\n"
            "После независимости в 1991 году проведена масштабная модернизация: в 2011 году установлен скоростной гондольный подъёмник. "
            "Каток Медеу (1972 г.) на высоте 1691 м — самый высокогорный каток в мире."
        ),
        "hist_charyn": (
            "Чарынский каньон - Исторические данные\n\n"
            "Каньон формировался более 12 миллионов лет под воздействием реки Чарын и ветровой эрозии. "
            "Протяжённость около 80 км, глубина до 300 метров.\n\n"
            "Долина Замков получила название благодаря скальным образованиям, похожим на средневековые крепости. "
            "Красно-оранжевый цвет пород объясняется содержанием оксида железа.\n\n"
            "Археологические находки свидетельствуют о заселении района людьми Бронзового века (3000-4000 лет назад): орудия труда, курганы, петроглифы.\n\n"
            "Реликтовая роща ясеня Согдийского — живые ископаемые, пережившие Ледниковый период. "
            "Каньон объявлен государственным природным заповедником в 2004 году."
        ),
        "hist_kolsai": (
            "Озёра Кольсай - Исторические данные\n\n"
            "Три ледниковых озера на высотах 1818, 2252 и 2850 метров в хребте Кунгей Алатау. "
            "Питаются талыми ледниковыми и родниковыми водами, отсюда их характерный изумрудный цвет.\n\n"
            "Исторически горные долины служили летними пастбищами казахских кочевников Старшего жуза. "
            "Горные перевалы использовались торговцами Шёлкового пути.\n\n"
            "В 2007 году территория объявлена Государственным национальным природным парком (более 160 000 га). "
            "Здесь обитают снежный барс, архар Марко Поло и тяньшанский бурый медведь."
        ),
        "hist_issyk": (
            "Озеро Иссык - Исторические данные\n\n"
            "В 1969 году советские археологи обнаружили у озера захоронение сакского воина-принца V-IV вв. до н.э. "
            "В кургане находилось более 4000 золотых артефактов: золотой костюм с зооморфными мотивами, "
            "головной убор высотой 70 см, оружие и сосуды.\n\n"
            "Это открытие стало известно как Золотой человек (Алтын Адам). "
            "Образ Золотого человека стал национальным символом Казахстана, изображён на гербе и валюте страны.\n\n"
            "Саки — ветвь скифской цивилизации, искусные воины-конники VIII-III вв. до н.э.\n\n"
            "Само озеро образовалось в результате катастрофического оползня в 1963 году. "
            "Копии артефактов хранятся в местном музее, оригиналы — в Национальном музее в Нур-Султане."
        ),
        "hist_greenbazaar": (
            "Зелёный базар - Исторические данные\n\n"
            "История базара насчитывает более 150 лет. Он возник в середине XIX века как торговая точка при российском военном гарнизоне Верный (первоначальное название Алматы).\n\n"
            "Базар стал крупным торговым узлом, соединявшим русских переселенцев, казахских кочевников, китайских купцов и торговцев всей Центральной Азии. "
            "Основные товары: шёлк, специи, скот, сухофрукты, ремесленные изделия.\n\n"
            "В советский период построено крытое здание рынка. После независимости в 1991 году базар перешёл на свободную торговлю. "
            "Сегодня он занимает более 10 000 кв. м и остаётся символом предпринимательского духа Алматы."
        ),

        "first_aid": (
            "Информация о первой помощи\n\n"
            "ЭКСТРЕННЫЕ НОМЕРА:\n"
            "Полиция: 102 | Скорая: 103 | Пожарная: 101 | Горноспасательная: 112\n\n"
            "--- ОБЩИЕ ПРИНЦИПЫ ---\n"
            "1. Убедитесь в безопасности места происшествия.\n"
            "2. Немедленно вызовите 103 при серьёзных травмах.\n"
            "3. Сохраняйте спокойствие и успокойте пострадавшего.\n"
            "4. Не перемещайте человека при подозрении на травму позвоночника.\n\n"
            "--- СЛР (СЕРДЕЧНО-ЛЁГОЧНАЯ РЕАНИМАЦИЯ) ---\n"
            "1. Проверьте реакцию — похлопайте по плечам и громко окликните.\n"
            "2. Немедленно вызовите 103.\n"
            "3. Положите основание ладони на центр грудной клетки.\n"
            "4. Надавливайте на 5-6 см, 30 нажатий со скоростью 100-120 в минуту.\n"
            "5. При наличии навыков — 2 вдоха, затем повторяйте цикл.\n"
            "6. Продолжайте до приезда скорой.\n\n"
            "--- УДУШЬЕ ---\n"
            "1. Поощряйте сильный кашель, если пострадавший может кашлять.\n"
            "2. Нанесите до 5 ударов по спине между лопатками.\n"
            "3. При неэффективности — до 5 абдоминальных толчков (приём Геймлиха).\n"
            "4. Чередуйте удары по спине и толчки до освобождения.\n"
            "5. При потере сознания вызовите 103.\n\n"
            "--- КРОВОТЕЧЕНИЕ ---\n"
            "1. Плотно прижмите чистую ткань или бинт к ране.\n"
            "2. Не снимайте ткань — накладывайте новый слой поверх пропитанного.\n"
            "3. По возможности приподнимите повреждённую конечность выше уровня сердца.\n"
            "4. Держите давление не менее 10 минут непрерывно.\n"
            "5. При глубоких ранах обратитесь за медицинской помощью.\n\n"
            "--- ГОРНАЯ БОЛЕЗНЬ (актуально для Шымбулака и Кольсай) ---\n"
            "Симптомы: головная боль, тошнота, головокружение, одышка.\n"
            "1. Немедленно прекратите подъём.\n"
            "2. Отдохните и пейте воду.\n"
            "3. При ухудшении — немедленно спуститесь на меньшую высоту.\n"
            "4. При наличии — дайте ибупрофен или аспирин от головной боли.\n"
            "5. При невозможности ходить вызовите горных спасателей: 112.\n\n"
            "--- ПЕРЕОХЛАЖДЕНИЕ ---\n"
            "Симптомы: дрожь, спутанность сознания, бледная холодная кожа.\n"
            "1. Переместите пострадавшего в тёплое укрытие.\n"
            "2. Снимите мокрую одежду, оденьте в сухую и тёплую.\n"
            "3. Укутайте одеялами, включая голову и шею.\n"
            "4. Дайте тёплое (не горячее) питьё при сознании.\n"
            "5. Не растирайте конечности — риск осложнений.\n"
            "6. При тяжёлых случаях вызовите 103.\n\n"
            "ПРИМЕЧАНИЕ: Всегда берите с собой аптечку первой помощи. "
            "Рекомендуемый состав: бинты, марля, антисептические салфетки, перчатки, "
            "ножницы, пинцет, ибупрофен, соли для регидратации, термоодеяло, свисток."
        ),

        "tickets": (
            "База билетов\n\n"
            "Горнолыжный курорт Шымбулак\n"
            "Официальный сайт: https://shymbulak.com\n"
            "Покупка ски-пассов, билетов на гондолу, актуальные цены и часы работы.\n\n"
            "Кок-Тобе\n"
            "Официальный сайт: https://koktobe.com\n"
            "Покупка билетов на канатную дорогу, вход в парк, расписание мероприятий.\n\n"
            "Примечание: Всегда проверяйте актуальные цены и сезонную доступность на официальных сайтах перед туром."
        ),

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
        "btn_driver":       "Жүргізуші деректері",
        "btn_hist_details": "Тарихи деректер",
        "btn_first_aid":    "Алғашқы жәрдем",
        "btn_tickets":      "Билет базасы",
        "btn_panfilov":     "Панфилов саябағы",
        "btn_greenbazaar":  "Жасыл базар",
        "btn_koktobe":      "Кок-Тобе",
        "btn_shymbulak":    "Шымбулак",
        "btn_charyn":       "Шарын каньоны",
        "btn_kolsai":       "Көлсай көлдері",
        "btn_issyk":        "Ыссық көл",
        "voice_menu":       "Аудиотур үшін орын таңдаңыз:",
        "hist_menu":        "Тарихи деректер үшін орын таңдаңыз:",
        "contacts":         "Гид байланыстары:\n\nАйханша: +7 747 709 8035",
        "faq":              "Жиі сұрақтар:\n\nС: Турды қалай брондауға болады?\nЖ: Гидтермен тікелей хабарласыңыз.\n\nС: Қолданба тегін бе?\nЖ: Иә, толықтай тегін!",
        "emergency":        "Жедел жәрдем:\n\nПолиция: 102\nЖедел жәрдем: 103\nӨрт сөндіру: 101",

        "itinerary": (
            "Алматы бойынша маршрут\n\n"
            "1. Панфилов саябағы\n"
            "Екінші дүниежүзілік соғыс батырлары — Панфилов жауынгерлері атындағы саябақ. "
            "Бірде-бір шегесіз салынған Вознесенский соборы орналасқан. Таңғы серуен үшін тамаша орын.\n\n"
            "2. Кок-Тобе\n"
            "Теңіз деңгейінен 1100 м биіктіктегі төбе паркі. Алматының керемет панорамасы ашылады. "
            "Канат жолымен жетуге болады. Битлз ескерткіші, кафелер мен аттракциондар бар.\n\n"
            "3. Шымбулак тау-шаңғы курорты\n"
            "Алматыдан 25 км жерде, 2200 м биіктіктегі Орталық Азияның үздік тау-шаңғы курорты. "
            "Барлық деңгейдегі трассалар, гондольды көтергіш және Тянь-Шань тауларының керемет көрінісі.\n\n"
            "4. Шарын каньоны\n"
            "Қазақстанның Гранд Каньоны деп аталатын, Шарын өзені бойындағы 80 км созылатын каньон. "
            "Қамалдар алқабының қызыл-қызғылт сары жартастары — міндетті баратын орын.\n\n"
            "5. Көлсай көлдері\n"
            "Солтүстік Тянь-Шаньдағы үш зумрут таулы көл. Шырша ормандары мен қар шыңдармен қоршалған. "
            "Жаяу саяхатшылар мен табиғат сүйгіштеріне арналған жұмақ.\n\n"
            "6. Ыссық көл\n"
            "Алматыдан 75 км шығысқа қарай, 1756 м биіктіктегі таулы көл. "
            "Бирюза суымен және сақ өркениетінің алтын жәдігерлерімен атақты.\n\n"
            "7. Жасыл базар\n"
            "Алматының ең жарқын базары. Бір шаңырақ астында жаңа жемістер, дәмдеуіштер, ет және қазақ тағамдары. "
            "Жергілікті дәмдерді татып көрудің ең жақсы орны."
        ),

        "driver_details": (
            "Жүргізуші деректері\n\n"
            "Компания: Royal Transfer\n"
            "Телефон: +7 705 770 0075\n\n"
            "Барлық тасымалдар, тастап кету және кесте өзгерістерін тікелей жүргізушімен үйлестіріңіз. "
            "Жүргізушіні әр жолаушылықтан кемінде 30 минут бұрын ескертіңіз."
        ),

        "hist_panfilov": (
            "Панфилов саябағы - Тарихи деректер\n\n"
            "Саябақ XIX ғасырдың аяғында Ресей Империясы кезінде негізделді, бастапқыда Пушкин паркі деп аталды. "
            "1941 жылы Мәскеу шайқасында нацист күштеріне қарсы батылдықпен соғысқан генерал Иван Панфилов мен оның 28 гвардиашысы құрметіне қайта аталды. "
            "28 жауынгердің барлығы Кеңес Одағының Батыры атағын алды.\n\n"
            "Саябақтың бас ескерткіші — 1904-1907 жылдары архитектор Андрей Зенков салған Вознесенский соборы. "
            "Биіктігі 54 метр, бірде-бір шегесіз салынған дүниедегі ең биік ағаш ғимараттардың бірі. "
            "Собор 1911 жылғы 7,7 балдық жер сілкінісінен аман қалды.\n\n"
            "Саябақта мәңгілік от жанатын ҰОС мемориалы бар. Тарихи ескерткіш ретінде қорғалады."
        ),
        "hist_koktobe": (
            "Кок-Тобе - Тарихи деректер\n\n"
            "Қазақ тілінде Көк төбе деген мағынаны білдіретін Кок-Тобе ғасырлар бойы Іле өзені алқабын бақылайтын стратегиялық орын болды.\n\n"
            "Кеңес дәуірінде мұнда 1975 жылы Алматы телемұнарасы салынды. "
            "Биіктігі — төбенің негізінен 372 метр, бұрын Орталық Азиядағы ең биік құрылыс болды.\n\n"
            "Канат жолы 1967 жылы ашылды. 2007 жылы сыйға тартылған Битлз ескерткіші мәдени символға айналды. "
            "2000-2010 жылдары парк кеңінен жаңғыртылды."
        ),
        "hist_shymbulak": (
            "Шымбулак - Тарихи деректер\n\n"
            "Шымбулақ атауы жылқы жайылатын жер деген мағынаны білдіреді. Тау-шаңғы курорты ретінде тарихы 1930 жылдардан басталады.\n\n"
            "1972 жылы Әлемдік тау шаңғы чемпионаты өтті. Кеңес спортшылары Шымбулақта белсенді дайындықтан өтті.\n\n"
            "Іле Алатауы таулары мыңдаған жылдар бойы қазақ көшпенділерінің жайлауы болды, тауасулары Жібек жолы саудагерлері пайдаланды.\n\n"
            "1991 жылғы тәуелсіздіктен кейін күрделі жаңғырту жүргізілді: 2011 жылы жоғары жылдамдықты гондольды көтергіш орнатылды. "
            "Медеу мұз айдыны (1972 ж.) теңіз деңгейінен 1691 м биіктікте — дүниедегі ең биік шаңғы стадионы."
        ),
        "hist_charyn": (
            "Шарын каньоны - Тарихи деректер\n\n"
            "Каньон Шарын өзені мен жел эрозиясы арқылы 12 миллион жыл бойы қалыптасты. "
            "Ұзындығы шамамен 80 км, тереңдігі кейбір жерлерде 300 метрге дейін жетеді.\n\n"
            "Қамалдар алқабы ортағасырлық бекіністерге ұқсайтын жартас пішіндерінен атауын алды. "
            "Жартастардың қызыл-қызғылт сары түсі темір оксидінен туындайды.\n\n"
            "Қола ғасырынан (3000-4000 жыл бұрын) мекенделгенін дәлелдейтін тас құралдар, қорғандар, петроглифтер табылды.\n\n"
            "Соғды үйеңкісінің реликті ормандығы — мұздық дәуірінен аман қалған тірі қазба. "
            "Каньон 2004 жылы мемлекеттік табиғат қорығы деп жарияланды."
        ),
        "hist_kolsai": (
            "Көлсай көлдері - Тарихи деректер\n\n"
            "Күнгей Алатаудағы 1818, 2252 және 2850 метр биіктіктердегі үш мұздық көл. "
            "Мұздық сулары мен бұлақтармен қоректенеді, осыдан зумрут-жасыл түсі.\n\n"
            "Тарихи тұрғыдан таулы алқаптар Ұлы жүздің қазақ көшпенділерінің жайлауы болды. "
            "Таулы асулар Жібек жолы саудагерлері пайдаланды.\n\n"
            "2007 жылы Мемлекеттік ұлттық табиғи парк деп жарияланды (160 000 га-дан астам). "
            "Мұнда ілбіс, Марко Поло тауешкісі және Тянь-Шань қоңыр аюы мекен етеді."
        ),
        "hist_issyk": (
            "Ыссық көл - Тарихи деректер\n\n"
            "1969 жылы кеңес археологтары көл жанындағы қорғаннан б.з.б. V-IV ғасырлардағы сақ жауынгер-ханзада жерленген жерді тапты. "
            "4000-нан астам алтын жәдігер: зооморфты өрнекті алтын сауыт, биіктігі 70 см алтын бас киім, алтын қару-жарақ.\n\n"
            "Бұл жаңалық Алтын Адам деп аталды. Алтын Адам бейнесі Қазақстанның ұлттық символына айналды, "
            "мемлекеттік елтаңбада және валютада бейнеленген.\n\n"
            "Сақтар — б.з.б. VIII-III ғасырларда евразиялық далада үстемдік еткен скиф өркениетінің бір тармағы.\n\n"
            "Көл 1963 жылғы апатты сел нәтижесінде пайда болды. "
            "Жәдігерлердің көшірмелері жергілікті мұражайда, түпнұсқалары Нұр-Сұлтан қаласындағы Ұлттық мұражайда сақтаулы."
        ),
        "hist_greenbazaar": (
            "Жасыл базар - Тарихи деректер\n\n"
            "Жасыл базар, ресми атауы Зелёный базар, Алматының коммерциялық жүрегі болып табылады. "
            "Оның түпкі негізі 19-шы ғасырдың ортасына дейін созылады, Ресей Империясы уақытында Верный әскери гарнизонының сауда орыны ретінде құрылды.\n\n"
            "Верный қаласы 1800-ші жылдардың соңында өскен сайын базар да кеңейіп, орыс қоныс аударушылары, қазақ кочевниктері, Шыңжаңнан келген қытай саудагерлері және бүкіл Орталық Азиядан келген саудагерлер арасындағы сауда орталығына айналды. "
            "Негізгі тауарлар: жібек, дәмдеуіштер, мал, кептірілген жемістер және қолөнер бұйымдары.\n\n"
            "Ағымдағы базар құрылымы 20-шы ғасырдың ортасында Кеңес дәуірінде салынды, ашық базарларды жабық нысанға ауыстырды. "
            "Кеңес билігі базарды ауыл шаруашылығы өнімдерін тікелей қала тұрғындарына сатуға арналған мемлекеттік кооперативтер модельі ретінде пайдаланды.\n\n"
            "1991 жылы Қазақстанның тәуелсіздігіне қол жеткізгеннен кейін, базар еркін нарық экономикасына өтті және Алматының кәсіпкерлік рухының символына айналды. "
            "Бүгінде базар 10,000 шаршы метрден асады және жаңа өнімдер, ет, дәмдеуіштер, жаңғақтар, сүт өнімдері және дәстүрлі қазақ қолөнер бұйымдары сататын жүздеген сатушыларды қабылдайды. "
            "Ол қаланың ең шынайы мәдени тәжірибелерінің бірі болып қала береді."
        ),

        # ── VOICE TOUR CONTENT ─────────────────────────────────────────────
        "tour_panfilov":    "Панфилов саябағы — Алматының ең сүйікті жасыл аймақтарының бірі. Екінші дүниежүзілік соғыс батырлары Панфилов жауынгерлері құрметіне аталған, Вознесенский соборы — бірде-бір шегесіз салынған әлемдегі ең биік ағаш ғимарат. Саябақтың тыныш аллеялары мен жаяу жүргіншілер жолдары сізді Алматының жүрегінде серуендеуге шақырады.",
        "tour_greenbazaar": "Жасыл базар, немесе Зелёный базар, Алматының сауда мәдениетінің жанданған орталығы. Мұнда жаңа жемістер, көкөністер, дәмдеуіштер, ет және дәстүрлі қазақ тағамдары бір шаңырақ астында. Жергілікті дәмдерді татып көру, достық сатушылармен қарым-қатынас жасау және шынайы қалалық өмірді сезіну үшін ең жақсы орын.",
        "tour_koktobe":     "Кок-Тобе, қазақ тілінде Көк төбе, теңіз деңгейінен 1100 метр биіктікте орналасқан, Алматының тамаша панорамасын ұсынады. Канат жолымен жетуге болады, төбедегі аттракциондар, кафелер және Битлз ескерткіші сізді күтуде. Күн батқанда Тянь-Шань тауларының үстінде тамаша көрініс.",
        "tour_shymbulak":   "Шымбулак тау-шаңғы курорты Алматыдан 25 шақырым жерде, 2200 метр биіктікте орналасқан. Бұл Орталық Азияның жетекші тау-шаңғы курорты, барлық деңгейдегі шаңғышыларға арналған керемет трассалар, заманауи гондольды көтергіш және Тянь-Шань тауларындағы көркем көріністер.",
        "tour_charyn":      "Чарын каньоны, Қазақстанның Гранд Каньоны деп аталады, 80 шақырым бойы Шарын өзенімен созылып жатыр. Қызыл және қызғылт сары жартас пішіндері, миллиондаған жылдар бойы қалыптасқан, әлемдегі ең ерекше табиғи көріністердің бірі.",
        "tour_kolsai":      "Көлсай көлдері — үш тамаша таулы көл жүйесі, Солтүстік Тянь-Шань тауларында орналасқан. Тығыз шырша ормандары мен қар басқан шыңдармен қоршалған, бұл жасыл көлдер жаяу жүру және табиғат сүйетіндер үшін нағыз жұмақ.",
        "tour_issyk":       "Ыссық көл — Алматыдан 75 шақырым шығысқа қарай, 1756 метр биіктікте орналасқан тыныш таулы көл. Айналадағы таулар мен жасыл ормандармен қоршалған, бұл қаладан тыныштық іздейтіндер үшін керемет орын. Көлдің көгілдір суы мен Иссық мұражайындағы көне сақ артефактілері әйгілі."
    }
}

# ─────────────────────────────────────────────
# KEYBOARD SETUP
# ─────────────────────────────────────────────
lang_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="English")],
        [KeyboardButton(text="Русский")],
        [KeyboardButton(text="Қазақша")],
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
            [KeyboardButton(text=t["btn_driver"]), KeyboardButton(text=t["btn_hist_details"])],
            [KeyboardButton(text=t["btn_first_aid"]), KeyboardButton(text=t["btn_tickets"])],
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
    logging.info("Generating voice for lang=%s, text preview: %s", lang, text[:60])
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

@dp.message(F.text == "Қазақша")
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

@dp.message(F.text.in_({"Driver Details", "Данные водителя"}))
async def driver_details(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["driver_details"])

@dp.message(F.text.in_({"Tour Historical Details", "Исторические данные"}))
async def historical_details_menu(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["hist_menu"], reply_markup=guide_keyboard(lang))

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
# HANDLERS — Historical Details
# ─────────────────────────────────────────────
@dp.message(F.text.in_({"Driver Details", "Данные водителя"}))
async def driver_details(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["driver_details"])

@dp.message(F.text.in_({"Tour Historical Details", "Исторические данные"}))
async def historical_details_menu(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["hist_menu"], reply_markup=guide_keyboard(lang))

@dp.message(F.text.in_({"First Aid Info", "Первая помощь"}))
async def first_aid_info(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["first_aid"])

@dp.message(F.text.in_({"Ticket Database", "База билетов"}))
async def ticket_database(message: Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    await message.answer(TEXTS[lang]["tickets"])

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
async def main():
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

