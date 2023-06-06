import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand
from dotenv import load_dotenv

from api_source import search_pic, trend_pic, translate_txt, read, get_users
from btns import main_btn, exit_btn, admin_btn
from states import Search, AdminState, RekState

load_dotenv('.env')

PROXY_URL = 'http://proxy.server:3128'
logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def welcome_page(msg: types.Message):
    read(msg.from_user.id)
    await bot.set_my_commands([BotCommand('start', 'Botni qayta ishga tushirish 🔄')])
    await msg.answer(
        text=f"Assalom alaykum {msg.from_user.first_name}\nBotga xush kelibsiz 🤖\nBot orqali rasm qidirishingiz va yuklab olishingiz mumkin 📲",
        reply_markup=main_btn())


@dp.message_handler(Text("Search 🔍"))
async def search_picture(msg: types.Message):
    await Search.search.set()
    await msg.answer(text=f"Qanday rasm qidiryabsiz: ", reply_markup=exit_btn())


@dp.message_handler(state=Search.search)
async def search_page(msg: types.Message, state: FSMContext):
    if msg.text == '❌':
        await state.finish()
        await msg.answer(text="Qidiruv bekor qilindi ❌", reply_markup=main_btn())
    elif 'sex' in translate_txt(msg.text).lower():
        await msg.answer(text="Siz taqiqlangan kontent qidiryabsiz 🆘")
    else:
        data = search_pic(msg.text)
        if data:
            await msg.answer(text="Sizning qidiruv natijalaringiz ✅")
            for i in data:
                try:
                    await msg.answer_photo(photo=i)
                except:  # noqa
                    pass
            else:
                await msg.answer(text="Bizda hozircha shular 🖇", reply_markup=main_btn())
                await state.finish()
        else:
            await state.finish()
            await msg.answer(text="Siz qidirgan mavzu bo'yicha hech qanday rasm topilmadi 😔", reply_markup=main_btn())


@dp.message_handler(Text("Top 🔝"))
async def top_picture(msg: types.Message):
    data = trend_pic()
    if data:
        await msg.answer(text="Top Suratlar")
        for i in data:
            try:
                await msg.answer_photo(photo=i['url'], caption=i['caption'])
            except:
                pass
    else:
        await msg.answer(text="Hozircha rasmlar mavjud emas!")


@dp.message_handler(Text("Dasturchiga xabar 💬"))
async def admin_send(msg: types.Message):
    if msg.from_user.id == 6066967779:
        await msg.answer(text=f'{msg.from_user.first_name} admin sahifaga xush kelibsiz!',
                         reply_markup=admin_btn())  # noqa
    else:
        await AdminState.comment.set()
        await msg.answer(text="Talab va takliflaringizni yozib qoldiring ✍️", reply_markup=exit_btn())


@dp.message_handler(state=AdminState.comment)
async def admin_message(msg: types.Message, state: FSMContext):
    if len(msg.text) <= 1000 and msg.text != '❌':
        await bot.send_message(6066967779,
                               f"ID: {msg.from_user.id}\nIsm: {msg.from_user.first_name}\nUsername: @{msg.from_user.username}\nFikrlar: {msg.text}")
        await msg.answer(text="✅ Talab va takliflar adminga yuborildi!", reply_markup=main_btn())
        await state.finish()
    elif msg.text == '❌':
        await state.finish()
        await msg.answer(text="Xabar yuborish bekor qilindi 🌐", reply_markup=main_btn())
    else:
        await msg.answer(text="Matningiz juda uzun iltimos qisaqroq matn yuboring 🖋")


@dp.message_handler(Text("Back ⬅️"))
async def back_menu(msg: types.Message):
    await msg.answer(text='Bosh menu 🛎', reply_markup=main_btn())


@dp.message_handler(Text("📊 Statistika"))
async def statistika(msg: types.Message):
    users = get_users()
    await msg.answer(text=f'Foydalanuvchilar Soni: {len(users)}')


@dp.message_handler(Text("🗣 Reklama"))
async def reklama_handler(msg: types.Message):
    await RekState.reklama.set()
    await msg.answer(text="Reklama Bo'limi!")


@dp.message_handler(state=RekState.reklama, content_types=types.ContentType.ANY)
async def rek_state(msg: types.Message, state: FSMContext):
    await msg.answer(text="Reklama jo'natish boshlandi!")
    users = get_users()
    summa = 0
    for i in users:
        try:
            await msg.copy_to(i, caption=msg.caption, caption_entities=msg.caption_entities,
                              reply_markup=msg.reply_markup)
        except:  # noqa
            summa += 1
    else:
        await msg.answer(text=f"Bloklagan userlar soni: {summa}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
