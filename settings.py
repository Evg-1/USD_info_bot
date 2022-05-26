# import os
# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env
# API = os.getenv('API')


import os
from dotenv import dotenv_values


if not os.path.exists('.env'):
    raise FileNotFoundError(f'В каталоге {os.getcwd()} Не найден файл ".env" В нем хранятся адреса, пароли, явки...')

settings_dict = dotenv_values('.env')
TELEGRAM_BOT_TOKEN = settings_dict['TELEGRAM_BOT_TOKEN'] # 12345
PROXY_AUTH = settings_dict['PROXY_AUTH'] # http://login:password@ip:port

