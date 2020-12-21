import logging
from config import *

from random import choice

from aiogram import Bot, Dispatcher, types, executor

import sqlite3

conn = sqlite3.connect('chat.db')
c = conn.cursor()
API_TOKEN = '1420201172:AAFJv4SyCNvsO-4l7o7lrQ85uRcqoET4KBE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await types.ChatActions.typing()
    c.execute('INSERT INTO chats VALUES(%s);' % message.chat.id)
    conn.commit()
    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    text_and_data = (
        ('Платная продленка(инд.занятия)', 'zan'),
        ('Олимпиадная математика', 'olimp'),
        ('Чат поддержки для мам', 'mumchat')
    )
    # in real life for the callback_data the callback data factory should be used
    # here the raw string is used for the simplicity
    0 in (keyboard_markup.row(types.InlineKeyboardButton(text, callback_data=data)) for text, data in text_and_data)

    keyboard_markup.add(
        # url buttons have no callback data
        types.InlineKeyboardButton('WhatsApp чат тех.поддержки',
                                   url='https://chat.whatsapp.com/EeMz7l5JYXY8RgPjbsjELF'),
    )
    await message.answer(
        'Здравствуйте! Меня зовут Матяма. Я помогу вам выбрать нужную программу для вашего ребенка.\nЧто вас интересует?',
        reply_markup=keyboard_markup)


@dp.callback_query_handler(text='olimp')
async def olimp(query: types.CallbackQuery):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    text_and_data = (
        ('Станислав Викторович\n\t(член жюри ВсОШ)', 'stas'),
        ('Екатерина Сергеевна', 'katya'),
        ('Анастасия Андреевна', 'nastya')
    )
    # in real life for the callback_data the callback data factory should be used
    # here the raw string is used for the simplicity
    0 in (keyboard_markup.row(types.InlineKeyboardButton(text, callback_data=data)) for text, data in text_and_data)
    await bot.send_message(query.from_user.id, OLIMP, reply_markup=keyboard_markup)


@dp.callback_query_handler(text='stas')
@dp.callback_query_handler(text='katya')
@dp.callback_query_handler(text='nastya')
async def teacherinfo(query: types.CallbackQuery):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    ans = query.data
    text = eval(ans.upper())
    link = eval(ans.upper() + 'LINK')
    keyboard_markup.add(types.InlineKeyboardButton('Записываюсь!', url=link))
    await bot.send_message(query.from_user.id, text, reply_markup=keyboard_markup)


@dp.callback_query_handler(text='zan')
async def zan(query: types.CallbackQuery):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    text_and_data = (
        ('Екатерина Сергеевна', 'katya'),
        ('Анастасия Андреевна', 'nastya')
    )
    # in real life for the callback_data the callback data factory should be used
    # here the raw string is used for the simplicity
    0 in (keyboard_markup.row(types.InlineKeyboardButton(text, callback_data=data)) for text, data in text_and_data)
    await bot.send_message(query.from_user.id, ZAN, reply_markup=keyboard_markup)


@dp.callback_query_handler(text='mumchat')
async def mumchat(query: types.CallbackQuery):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    text_and_data = (
        ('Екатерина Сергеевна', 'katya'),
        ('Анастасия Андреевна', 'nastya')
    )
    # in real life for the callback_data the callback data factory should be used
    # here the raw string is used for the simplicity
    0 in (keyboard_markup.row(types.InlineKeyboardButton(text, callback_data=data)) for text, data in text_and_data)
    await bot.send_message(query.from_user.id, MUMCHAT, reply_markup=keyboard_markup)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer('Если вы хотите связаться с реальным человеком, свяжитесь с 79273364899(Станислав Викторович).\nА если  с ботом, используйте /start .')


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)
