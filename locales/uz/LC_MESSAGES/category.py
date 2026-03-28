import asyncio
import logging
import sys
from dataclasses import dataclass

import psycopg2
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TOKEN = "8636125421:AAFxlnqDFhs1bwoOJShlV84fSDYeMV_PdP0"

dp = Dispatcher()


import psycopg2


class DB:
    dbname = "postgres"
    port = 5432
    host = "localhost"
    user = "postgres"
    password = '1'
    connect = psycopg2.connect(dbname=dbname,port=port,host=host,user=user,password=password)
    cursor = connect.cursor()


class CRUD:
    def delete(self):
        table_name = self.__class__.__name__.lower() + "s"
        query = f"""
                    delete from {table_name} where id = %s
                    """
        DB.cursor.execute(query, (self.id,))
        DB.connect.commit()

    def update(self , **kwargs):
        table_name = self.__class__.__name__.lower() + "s"
        set_format = "= %s ,".join(kwargs.keys()) + "= %s "
        query = f"""
            update {table_name} set {set_format} where id = %s
            """
        vals = list(kwargs.values()) + [self.id]
        DB.cursor.execute(query , tuple(vals))
        DB.connect.commit()

    def get_data(self)-> list:

        table_name = self.__class__.__name__.lower() + "s"


        fields = {}
        for field, value in self.__dict__.items():
            if value != None:
                fields[field] = value
        condition_format = "where " + "= %s and ".join(fields.keys()) + "= %s" if fields else ""
        query = f"""
                            select * from {table_name} {condition_format}
                            """
        objects = []

        DB.cursor.execute(query, tuple(fields.values()))
        for data in DB.cursor.fetchall():
            obj = self.__class__(*data)
            objects.append(obj)
        return objects

    def save(self):
        table_name = self.__class__.__name__.lower() + "s"
        fields = {}
        for field , value in self.__dict__.items():
            if value != None:
                fields[field] = value
        field_format = ",".join(fields.keys())
        values_format = ",".join(["%s"]*len(fields.keys()))
        query = f"""
            insert into {table_name} ({field_format}) values ({values_format})
            """
        DB.cursor.execute(query , tuple(fields.values()))
        DB.connect.commit()


@dataclass
class Category(CRUD):
    table_name = "categories"
    id: int = None
    title: str = None
@dataclass
class Product(CRUD):
    table_name = "products"
    id: int = None
    title: str = None
    category_id: int = None



@dp.message(F.text == "/start")
async def start(message: Message):
     await message.answer("Select Genre: " ,reply_markup=categories_button())

@dp.callback_query(F.data.startswith("cat_"))
async def category_handler(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    products = Product(category_id = category_id).get_data()
    markup = products_show(products)
    await callback.message.edit_text("Select Movies: " ,reply_markup=markup)
def categories_button():
    ikb = InlineKeyboardBuilder()
    categories:list['Category'] = Category().get_data()
    ikb.add(*[InlineKeyboardButton(text=category.title , callback_data=f"cat_{category.id}" )for category in categories])
    ikb.adjust(2 , repeat=True)
    return ikb.as_markup()


def products_show(products):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text=product.title, callback_data=f"pro_{product.id}") for product in products])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()



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