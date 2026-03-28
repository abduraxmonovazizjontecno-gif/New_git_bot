import asyncio
import logging
import sys
import psycopg2

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN = "8636125421:AAGJ40ZQf-DMmHeA3aaYG_3FJ-nNsBPSK1s"

dp = Dispatcher()

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    price VARCHAR(50),
    photo TEXT,
    stock VARCHAR(50)
)
""")
conn.commit()



class NewState(StatesGroup):
    title = State()
    price = State()
    photo = State()
    stock = State()



@dp.message(F.text == "/start")
async def start_command(message: Message):
    markup = start_menu()
    await message.answer("Quyidagilarni to'ldiring", reply_markup=markup)



def start_menu():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text="Add New Product"))
    rkb.adjust(1)
    return rkb.as_markup(resize_keyboard=True)


@dp.message(F.text == "Add New Product")
async def get_title(message: Message, state: FSMContext):
    await state.set_state(NewState.title)
    await message.answer("Mahsulot nomini kiriting:")


@dp.message(NewState.title)
async def get_price(message: Message, state: FSMContext):
    await state.update_data(title=message.text)

    await state.set_state(NewState.price)
    await message.answer("Mahsulot narxini kiriting:")

@dp.message(NewState.price)
async def get_price_value(message: Message, state: FSMContext):
    await state.update_data(price=message.text)

    await state.set_state(NewState.photo)
    await message.answer("Mahsulot rasmini yuboring:")


@dp.message(NewState.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    await state.update_data(photo=photo_id)

    await state.set_state(NewState.stock)
    await message.answer("Mahsulot sonini kiriting:")


@dp.message(NewState.photo)
async def wrong_photo(message: Message):
    await message.answer("Iltimos mahsulot rasmini yuboring 📷")

@dp.message(NewState.stock)
async def get_stock(message: Message, state: FSMContext):
    await state.update_data(stock=message.text)

    data = await state.get_data()


    cursor.execute(
        """
        INSERT INTO products (title, price, photo, stock)
        VALUES (%s, %s, %s, %s)
        """,
        (data["title"], data["price"], data["photo"], data["stock"])
    )
    conn.commit()

    await message.answer(
        f"✅ Mahsulot qo'shildi\n\n"
        f"Nomi: {data['title']}\n"
        f"Narxi: {data['price']}\n"
        f"Soni: {data['stock']}"
    )

    await message.answer_photo(data["photo"])

    await state.clear()



async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())