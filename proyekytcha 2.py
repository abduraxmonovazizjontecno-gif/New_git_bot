import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN ="8636125421:AAFX7oCplHQSf0FgfSEym3pSeclkFYQLaP0"

dp = Dispatcher()


users = {}

@dp.message(F.text == "/start")
async def start_command(message: Message):
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {"gender": None, "chat_with": None}

    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="users"),
        KeyboardButton(text="settings"),
    )
    rkb.adjust(2)

    await message.answer("Menu:", reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(F.text == "settings")
async def settings_command(message: Message):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="gender"),
    )

    await message.answer("Tanlang:", reply_markup=rkb.as_markup(resize_keyboard=True))

@dp.message(F.text == "gender")
async def gender_menu(message: Message):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="Ayol"),
        KeyboardButton(text="Erkak"),
    )
    rkb.adjust(2)

    await message.answer("Jinsingizni tanlang:", reply_markup=rkb.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(["Ayol", "Erkak"]))
async def set_gender(message: Message):
    user_id = message.from_user.id
    users[user_id]["gender"] = message.text

    await message.answer(f"Saqlandi: {message.text}")

@dp.message(F.text == "users")
async def users_list(message: Message):
    text = "Users:\n\n"

    for uid, data in users.items():
        gender = data["gender"] if data["gender"] else "None"
        text += f"{uid} : {gender}\n"

    await message.answer(text)

@dp.message()
async def chat(message: Message):
    sender_id = message.from_user.id


    for uid in users:
        if uid != sender_id:
            receiver_id = uid
            break
    else:
        await message.answer("Boshqa user yo‘q")
        return


    await message.answer(f"sender_id: {message.text}")
    await message.bot.send_message(receiver_id, f"receiver_id: {message.text}")


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