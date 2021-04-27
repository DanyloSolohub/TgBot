from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

if __name__ == '__main__':
    from handlers import *

    executor.start_polling(dispatcher=dp, on_startup=send_to_admin_start, on_shutdown=send_to_admin_shut,
                           skip_updates=True)
