from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from keyboards.btns import main_btn


@dp.message_handler(CommandStart())
async def welcome_page(msg: types.Message):
    await msg.answer(text=f"Assalom alaykum {msg.from_user.first_name}\nBotga xush kelibsiz 🤖\nBot orqali rasm qidirishingiz va yuklab olishingiz mumkin 📲", reply_markup=main_btn())
