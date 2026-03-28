import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import I18n, gettext as _
from aiogram.utils.i18n.middleware import FSMI18nMiddleware
from aiogram.fsm.context import FSMContext

TOKEN = "8636125421:AAFX7oCplHQSf0FgfSEym3pSeclkFYQLaP0"

dp = Dispatcher()


def language():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="English"),
        KeyboardButton(text="Uzbek"),
        KeyboardButton(text="Russian")
    )
    rkb.adjust(3)
    return rkb.as_markup(resize_keyboard=True)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(_("Hello"), reply_markup=language())


@dp.message(F.text == "English")
async def set_english(message: Message, state: FSMContext):
    await state.update_data(locale="en")
    await message.answer(_("Hello"), reply_markup=language())


@dp.message(F.text == "Uzbek")
async def set_uzbek(message: Message, state: FSMContext):
    await state.update_data(locale="uz")
    await message.answer(_("Hello"), reply_markup=language())


@dp.message(F.text == "Russian")
async def set_russian(message: Message, state: FSMContext):
    await state.update_data(locale="ru")
    await message.answer(_("Hello"), reply_markup=language())


@dp.message()
async def echo_handler(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main():
    i18n = I18n(path="locales", default_locale="en", domain="messages")

    middleware = FSMI18nMiddleware(i18n, key="locale")
    dp.message.outer_middleware(middleware)

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())