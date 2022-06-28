import os

from environs import Env

dot_env_path = os.path.abspath(os.path.join(__file__, os.pardir, '.env'))
if not os.path.exists(dot_env_path):
    raise FileNotFoundError(f'Не найден файл {dot_env_path} В нем хранятся адреса, пароли, явки...')

env = Env()
env.read_env()  # read .env file

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
PROXIES = env.dict('PROXIES', subcast_values=str)
