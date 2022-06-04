import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from business_logic import Usd
from prepared_bot_replies import *
from settings import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


def get_log_head(msg):
    first_name = msg.from_user.first_name if msg.from_user.first_name is not None else ''
    last_name = msg.from_user.last_name if msg.from_user.last_name is not None else ''
    full_name = f'{first_name} {last_name}'
    log_head = f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}] ' \
               f'user_id: {msg.from_user.id:11} ' \
               f'name: {full_name:25s}'
    return log_head


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['показать курс', 'подробности']
    keyboard.add(*buttons)
    await msg.answer(bot_start_reply, reply_markup=keyboard, parse_mode=types.ParseMode.HTML,
                     disable_web_page_preview=True)


@dp.message_handler(lambda message: message.text == "показать курс")
async def process_exchange_rate_button(msg: types.Message):
    print(f'{get_log_head(msg)} нажал кнопку "показать курс"')

    usd = Usd()
    usd.get_bot_prices_info_reply()
    await msg.answer(usd.bot_prices_info_reply, parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda message: message.text == 'подробности')
async def process_details_button(msg: types.Message):
    print(f'{get_log_head(msg)} нажал кнопку "подробности"')

    await msg.answer(bot_details_reply, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)


@dp.message_handler()
async def process_any_message(msg: types.Message):
    print(f'{get_log_head(msg)} отправил сообщение "{msg.text}"')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['показать курс', 'подробности']
    keyboard.add(*buttons)
    await bot.send_message(msg.from_user.id, bot_use_buttons_reply, reply_markup=keyboard)


if __name__ == '__main__':
    print(f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}] USD_info_bot запущен')
    executor.start_polling(dp)
