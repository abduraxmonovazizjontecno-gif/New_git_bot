import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN = "8636125421:AAGJ40ZQf-DMmHeA3aaYG_3FJ-nNsBPSK1s"

dp = Dispatcher()



@dp.message(F.text == "/start")
async def start(message:Message):
    await message.answer(text="Select one :")
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="Cinema"),
        KeyboardButton(text="TV Show"),
        KeyboardButton(text="Cartoon"),
    )
    rkb.adjust(1,1,1)
    await message.answer("Menu ",reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(F.text == "Cinema")
async def cinema(message:Message):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="Interstellar"),
        KeyboardButton(text="Inception"),
        KeyboardButton(text="The Dark knight"),
        KeyboardButton(text="Shutter Island"),
        KeyboardButton(text="Titanic"),
        KeyboardButton(text="Fight Club"),
        KeyboardButton(text="Forest Gump"),
        KeyboardButton(text="Avatar"),
        KeyboardButton(text="Oppenheimer"),
        KeyboardButton(text="The Wolf of Wall Street"),

    )
    rkb.adjust(2,2,2,2,2)
    await message.answer("Menu ",reply_markup=rkb.as_markup(resize_keyboard=True))



@dp.message(F.text == "TV Show")
async def cinema(message:Message):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="Breaking Bad"),
        KeyboardButton(text="Game of Thrones"),
        KeyboardButton(text="Better Call Saul"),
        KeyboardButton(text="Walking Dead"),
        KeyboardButton(text="Dexter"),
        KeyboardButton(text="True Detective"),
        KeyboardButton(text="Dark"),
        KeyboardButton(text="Sherlock"),
        KeyboardButton(text="Prison Break"),
        KeyboardButton(text="Sopranos"),

    )
    rkb.adjust(2,2,2,2,2)
    await message.answer("Menu ",reply_markup=rkb.as_markup(resize_keyboard=True))



@dp.message(F.text == "Cartoon")
async def cinema(message:Message):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="Up"),
        KeyboardButton(text="Toy story"),
        KeyboardButton(text="Soul"),
        KeyboardButton(text="Ratatouille"),
        KeyboardButton(text="Lion King"),
        KeyboardButton(text="Kung Fu Panda"),
        KeyboardButton(text="Cars"),
        KeyboardButton(text="Puss in Boots"),
        KeyboardButton(text="Shrek"),
        KeyboardButton(text="WALL-E"),

    )
    rkb.adjust(2,2,2,2,2)
    await message.answer("Menu ",reply_markup=rkb.as_markup(resize_keyboard=True))


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