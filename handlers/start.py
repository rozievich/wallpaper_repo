from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from keyboards.btns import main_btn
from utils.db_api.orm import User

user = User()

@dp.message_handler(CommandStart())
async def welcome_page(msg: types.Message):
    check = user.get_user(str(msg.from_user.id))
    if not check:
        user.create_user(str(msg.from_user.id), msg.from_user.username, msg.from_user.first_name)
    await msg.answer(text=f"Assalom alaykum {msg.from_user.first_name}\nBotga xush kelibsiz 🤖\nBot orqali rasm qidirishingiz va yuklab olishingiz mumkin 📲", reply_markup=main_btn())
