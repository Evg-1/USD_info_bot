# id 238440394

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from scrap_binance_p2p import get_prices_and_spread_from_binance_p2p
from scrap_alfa_bank import get_prices_and_spread_from_alfabank
from scrap_tinkoff_bank import get_prices_and_spread_from_tinkoffbank
import datetime
from settings import TELEGRAM_BOT_TOKEN


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

def get_log_head(msg):
    first_name = msg.from_user.first_name if msg.from_user.first_name is not None else ''
    last_name = msg.from_user.last_name if msg.from_user.last_name is not None else ''
    log_head = f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}] ' \
               f'user_id: {msg.from_user.id:11} ' \
               f'name: {first_name + " " + last_name:25s}'
    return log_head

@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['показать курс', 'подробности']
    keyboard.add(*buttons)
    await msg.answer('Привет!\n'
                     'Я покажу актуальный\n'
                     '- курс покупки $ (USD)\n'
                     '- цену_покупки/цену_продажи\n'
                     '- и \u0394 разницу между ними\n'
                     'на <a href="https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=RUB">binance p2p</a> через Tinkoff\n'
                     'в <a href="https://alfabank.ru/currency/">Alfa банке</a>\n'
                     'в <a href="https://www.tinkoff.ru/about/exchange/">Tinkoff банке</a>\n'
                     'и расскажу как вывести $ из РФ в любой банк мира 🌍\n'
                     'Нажми на кнопку, получишь результат...'
                     , reply_markup=keyboard, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)


@dp.message_handler(lambda message: message.text == "показать курс")
async def process_exchange_rate_button(msg: types.Message):
    print(f'{get_log_head(msg)} нажал кнопку "показать курс"')

    try:
        price_buy_binance, price_sell_binance, spread_binance = get_prices_and_spread_from_binance_p2p()
    except Exception as err:
        print(f'{get_log_head(msg)} [ERROR] Something went wrong in get_prices_and_spread_from_binance_p2p() \n{err}')
        binance_p2p_response = 'не удалось получить данные 😭'
    else:
        binance_p2p_response = f'{price_buy_binance:.2f}/{price_sell_binance:.2f} \u0394{spread_binance:.2f}'

    try:
        price_buy_alfa, price_sell_alfa, spread_alfa = get_prices_and_spread_from_alfabank()
    except Exception as err:
        print(f'{get_log_head(msg)} [ERROR] Something went wrong in get_prices_and_spread_from_alfabank() \n{err}')
        alfabank_response = 'не удалось получить данные 😭'
    else:
        alfabank_response = f'{price_buy_alfa:.2f}/{price_sell_alfa:.2f} \u0394{spread_alfa:.2f}'

    try:
        price_buy_tinkoff, price_sell_tinkoff, spread_tinkoff = get_prices_and_spread_from_tinkoffbank()
    except Exception as err:
        print(f'{get_log_head(msg)} [ERROR] Something went wrong in get_prices_and_spread_from_tinkoffbank() \n{err}')
        tinkoffbank_response = 'не удалось получить данные 😭'
    else:
        tinkoffbank_response = f'{price_buy_tinkoff:.2f}/{price_sell_tinkoff:.2f} \u0394{spread_tinkoff:.2f}'

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

    await msg.answer('Я показываю актуальный\n'
                     'курс покупки $ (USD):\n'
                     '- цену_покупки/цену_продажи\n'
                     '- и \u0394 разницу между ними\n'
                     'на <a href="https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=RUB">binance p2p</a> через Tinkoff\n'
                     'в <a href="https://alfabank.ru/currency/">Alfa банке</a>\n'
                     'в <a href="https://www.tinkoff.ru/about/exchange/">Tinkoff банке</a>\n'
                     '\n'
                     '<a href="https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=RUB">binance p2p</a> позволяет\n'
                     'сконвертировать ₽ в $ по выгодному курсу и вывести их в любой банк мира 🌍\n'
                     'без глупых условностей типа:\n'
                     '- остановки торгов на ночь, выходные дни, праздники или вообще по решению 1 человека!\n'
                     '- выдуманных комиссий в 12%\n'
                     '- запрета перевода $ в иностранные банки\n'
                     'подробная инструкция <a href="https://vc.ru/finance/379297-poshagovaya-instrukciya-kak-pokupat-i-perevodit-deshevle-kursa-bez-komissiy-i-ogranicheniy">➡тут⬅</a>\n'
                     '\n'
                     'проще всего использовать не санкционные банки:\n'
                     '«Тинькофф», «Росбанк», «Райфайзен», «Почта Банк», «Хоум Кредит», «МТС-банк», «Уралсиб», «БКС банк»\n'
                     'сейчас Сбербанк отсутствует в списке доступных банков, но если очень хочется то <a href="https://www.youtube.com/watch?v=DVq_RxIOq68&t=200s">можно</a>'
                     , parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)


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
