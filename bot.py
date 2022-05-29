# id 238440394

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import datetime
from business_logic import Usd
from prepared_messages import *
from settings import TELEGRAM_BOT_TOKEN, PROXIES

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
    await msg.answer(start_msg, reply_markup=keyboard, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)


@dp.message_handler(lambda message: message.text == "показать курс")
async def process_exchange_rate_button(msg: types.Message):
    print(f'{get_log_head(msg)} нажал кнопку "показать курс"')

    usd = Usd()

    try:
        usd.get_prices_and_spread_from_binance_p2p(proxies=None)
    except Exception as exc:
        print(f'{get_log_head(msg)} [ERROR] Something went wrong in get_prices_and_spread_from_binance_p2p() \n{exc}')
        binance_p2p_response = 'не удалось получить данные 😭'
    else:
        binance_p2p_response = f'{usd.price_buy_binance:.2f}/{usd.price_sell_binance:.2f} Δ{usd.spread_binance:.2f}'

    try:
        usd.get_prices_and_spread_from_alfabank(proxies=PROXIES)
    except Exception as exc:
        print(f'{get_log_head(msg)} [ERROR] Something went wrong in get_prices_and_spread_from_alfabank() \n{exc}')
        alfabank_response = 'не удалось получить данные 😭'
    else:
        alfabank_response = f'{usd.price_buy_alfa:.2f}/{usd.price_sell_alfa:.2f} Δ{usd.spread_alfa:.2f}'

    try:
        usd.get_prices_and_spread_from_tinkoffbank(proxies=None)
    except Exception as exc:
        print(f'{get_log_head(msg)} [ERROR] Something went wrong in get_prices_and_spread_from_tinkoffbank() \n{exc}')
        tinkoffbank_response = 'не удалось получить данные 😭'
    else:
        tinkoffbank_response = f'{usd.price_buy_tinkoff:.2f}/{usd.price_sell_tinkoff:.2f} Δ{usd.spread_tinkoff:.2f}'

    await msg.answer(f'Binance p2p через Tinkoff:\n'
                     f'<code>{binance_p2p_response}</code>\n'
                     f'Alfa-bank:\n'
                     f'<code>{alfabank_response}</code>\n'
                     f'Tinkoff-bank\n'
                     f'<code>{tinkoffbank_response}</code>'
                     , parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda message: message.text == 'подробности')
async def process_details_button(msg: types.Message):
    print(f'{get_log_head(msg)} нажал кнопку "подробности"')

    await msg.answer(details_msg, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)


@dp.message_handler()
async def process_any_message(msg: types.Message):
    print(f'{get_log_head(msg)} отправил сообщение "{msg.text}"')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['показать курс', 'подробности']
    keyboard.add(*buttons)
    await bot.send_message(msg.from_user.id, 'Сложна... сложна... непанятна...\nПожалуйста, используй кнопки',
                           reply_markup=keyboard)


if __name__ == '__main__':
    print(f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}] USD_info_bot запущен')
    executor.start_polling(dp)
