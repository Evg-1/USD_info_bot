import os

from environs import Env

if not os.path.exists('.env'):
    raise FileNotFoundError(f'В каталоге {os.getcwd()} Не найден файл ".env" В нем хранятся адреса, пароли, явки...')

env = Env()
env.read_env()  # read .env file

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
PROXIES = env.dict('PROXIES', subcast_values=str)
