from aiogram import executor

from loader import dp
import handlers, utils, keyboards, states, data
from utils.db_api.connect import create_db
from utils.notify_send_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    create_db()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)