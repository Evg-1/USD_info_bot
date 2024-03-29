import logging
import os

log = logging.getLogger('log')
log.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_path = os.path.abspath(os.path.join(__file__, os.pardir, 'bot.log'))
file_handler = logging.FileHandler(filename=log_path, mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(style='{', fmt='{asctime} - {levelname} - {message}', datefmt='%Y-%m-%d %H:%M:%S')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

log.addHandler(console_handler)
log.addHandler(file_handler)


