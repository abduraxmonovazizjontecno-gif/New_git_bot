import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client import bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from sqlalchemy.testing.suite.test_reflection import users

TOKEN = "8636125421:AAGJ40ZQf-DMmHeA3aaYG_3FJ-nNsBPSK1s"

dp = Dispatcher()


@dp.message(F.text == "/start")
async def start_command(message: Message):
    users.append(message.from_user.id)
    await message.answer(text="Salomu alaykum")


# @dp.message(F.from_user.id ==6341903269 )
# async def salom_user_command(message: Message):
#     print(message.text)
#     await message.bot.send_message(,message.text)
#
# @dp.message(F.text.startswith("reklama"))
# async def send_ads(message: Message):
#     ads_message = message.text.split(":")[-1]
#     for user_id in users:
#         await bot.send_message(user_id, ads_message)
# #
# @dp.message(F.text.lower() == "menu")
# async def menu(message: Message):
#     rkb = ReplyKeyboardBuilder()
#     rkb.add(*[
#         KeyboardButton(text="button"),
#         KeyboardButton(text="🐶"),
#         KeyboardButton(text="🚩"),
#         KeyboardButton(text="😊"),
#         KeyboardButton(text="Currency"),
#         KeyboardButton(text="Menu"),
#         KeyboardButton(text="1"),
#         KeyboardButton(text="phone",request_contact=True),
#         KeyboardButton(text="kun uz",web_app=WebAppInfo(url="https://kun.uz")),
#         KeyboardButton(text="location",request_location=True),
#     ])
#
#     rkb.adjust(4,2,3,1)
#     markup = rkb.as_markup(resize_keyboard=True)
#
#     await message.answer("Menu:", reply_markup=markup)
#
# @dp.message(F.text.lower() == "menu")
# async def menu(message: Message):
#     ikb = InlineKeyboardBuilder()
#     ikb.add(*[
#         InlineKeyboardButton(text="uylar",callback_data="houses"),
#         InlineKeyboardButton(text="oziq - ovqat",callback_data="foods"),
#         InlineKeyboardButton(text="kiyim kechak",callback_data="clothes"),
#     ])
#     ikb.adjust(2,1)
#     markup = ikb.as_markup()
#     await message.answer("Menu:", reply_markup=markup)
def menu_button():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="uylar", callback_data="houses"),
        InlineKeyboardButton(text="oziq - ovqat", callback_data="foods"),
        InlineKeyboardButton(text="kiyim kechak", callback_data="clothes"),
    ])
    ikb.adjust(2, 1)
    markup = ikb.as_markup()
    return markup

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
