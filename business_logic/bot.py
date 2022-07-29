import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from business_logic.usd import Usd
from business_logic.prepared_bot_replies import bot_start_reply, bot_details_reply, bot_use_buttons_reply
from utils.cfg_logging import log
from settings import TELEGRAM_BOT_TOKEN
from database import db

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


def db_update_last_activity(msg):
    # добавляем пользователя, если существует - обновляем дату и время последней активности
    db.User.replace(telegram_id=msg.from_user.id,
                    first_name=msg.from_user.first_name,
                    last_name=msg.from_user.last_name,
                    last_activity=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ).execute()


def get_user_data(msg):
    first_name = msg.from_user.first_name if msg.from_user.first_name is not None else ''
    last_name = msg.from_user.last_name if msg.from_user.last_name is not None else ''
    full_name = f'{first_name} {last_name}'
    return f'user_id: {msg.from_user.id:11} name: {full_name:25s}'


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    db_update_last_activity(msg)
    log.info(f'{get_user_data(msg)} вызвал команду "/start"')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['показать курс', 'подробности']
    keyboard.add(*buttons)
    await msg.answer(bot_start_reply, reply_markup=keyboard, parse_mode=types.ParseMode.HTML,
                     disable_web_page_preview=True)


@dp.message_handler(lambda message: message.text == "показать курс")
async def process_exchange_rate_button(msg: types.Message):
    db_update_last_activity(msg)
    log.info(f'{get_user_data(msg)} нажал кнопку "показать курс"')
    usd = Usd()
    usd.get_bot_prices_info_reply()
    await msg.answer(usd.bot_prices_info_reply, parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda message: message.text == 'подробности')
async def process_details_button(msg: types.Message):
    db_update_last_activity(msg)
    log.info(f'{get_user_data(msg)} нажал кнопку "подробности"')

    await msg.answer(bot_details_reply, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)


@dp.message_handler()
async def process_any_message(msg: types.Message):
    db_update_last_activity(msg)
    log.info(f'{get_user_data(msg)} отправил сообщение "{msg.text}"')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['показать курс', 'подробности']
    keyboard.add(*buttons)
    await bot.send_message(msg.from_user.id, bot_use_buttons_reply, reply_markup=keyboard)


if __name__ == '__main__':
    log.info('USD_info_bot запущен')
    executor.start_polling(dp)
