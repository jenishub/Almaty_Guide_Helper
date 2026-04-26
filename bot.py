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

roles = {}

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="I am Tourist")],
        [KeyboardButton(text="I am Guide")]
    ],
    resize_keyboard=True
)

tourist_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Itinerary"), KeyboardButton(text="AI Voice Tours")],
        [KeyboardButton(text="Guide Contacts"), KeyboardButton(text="FAQ")],
        [KeyboardButton(text="Emergency / Support")]
    ],
    resize_keyboard=True
)

guide_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Driver Details"), KeyboardButton(text="Ticketing Database")],
        [KeyboardButton(text="Tour & Historical Points")],
        [KeyboardButton(text="First Aid Information")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Welcome to Almaty Guide & Helper.\nPlease choose your role:",
        reply_markup=start_keyboard
    )

@dp.message(F.text == "I am Tourist")
async def tourist_role(message: Message):
    roles[message.from_user.id] = "tourist"
    await message.answer("Tourist menu:", reply_markup=tourist_keyboard)

@dp.message(F.text == "I am Guide")
async def guide_role(message: Message):
    roles[message.from_user.id] = "guide"
    await message.answer("Guide menu:", reply_markup=guide_keyboard)

@dp.message(F.text == "Itinerary")
async def itinerary(message: Message):
    await message.answer(
        "Day 1: Arrival + transfer to hotel\n"
        "Day 2: Kok Tobe + Green Bazaar\n"
        "Day 3: City Tour\n"
        "Day 4: Shymbulak\n"
        "Day 5: Airport transfer"
    )

@dp.message(F.text == "AI Voice Tours")
async def voice_tours(message: Message):
    await message.answer("Please select a tour point. Voice messages will be added here.")

@dp.message(F.text == "Guide Contacts")
async def guide_contacts(message: Message):
    await message.answer("Guide: Ayan\nPhone: +7 XXX XXX XXXX")

@dp.message(F.text == "FAQ")
async def faq(message: Message):
    await message.answer(
        "FAQ:\n"
        "1. What time is pickup? Please check itinerary.\n"
        "2. What to wear? Comfortable shoes and warm clothes for mountains.\n"
        "3. Who to contact? Your guide or support."
    )

@dp.message(F.text == "Driver Details")
async def driver_details(message: Message):
    await message.answer("Driver: Daniyar\nCar: Mercedes Sprinter\nPlate: 777 ABC 02")

@dp.message(F.text == "Ticketing Database")
async def tickets(message: Message):
    await message.answer("Tickets database will show attraction tickets, QR codes, and status.")

@dp.message(F.text == "Tour & Historical Points")
async def history(message: Message):
    await message.answer(
        "Zenkov Cathedral: Wooden Orthodox cathedral in Panfilov Park.\n"
        "Kok Tobe: Viewpoint above Almaty.\n"
        "Shymbulak: Mountain resort near Medeu."
    )

@dp.message(F.text == "First Aid Information")
async def first_aid(message: Message):
    await message.answer(
        "First Aid:\n"
        "- For emergency: call 112\n"
        "- Keep group calm\n"
        "- Inform the office immediately\n"
        "- Do not give medicine unless guest confirms it is safe for them"
    )

async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
