from business_logic.bot import *

if __name__ == '__main__':
    log.info('USD_info_bot запущен')
    executor.start_polling(dp)