from loader import bot, dp
from aiogram import  types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from states.admin_state import AdminState, RekState
from utils.misc.translations import translate_txt
from utils.misc.send_ads import send_adversment
from utils.db_api.orm import User
from data.api_source import UniversalAPI
from data.config import ADMINS
from keyboards.btns import exit_btn, main_btn, admin_btn

user = User()
api = UniversalAPI()

@dp.message_handler(Text("Top 🔝"))
async def top_picture(msg: types.Message):
    msg_stiker = await msg.answer("⏳")
    data = await api.trend_pic()
    if data:
        await msg.answer(text="Top Suratlar")
        await msg_stiker.delete()
        for i in data:
            try:
                await msg.answer_photo(photo=i['url'], caption=i['caption'])
            except:
                pass
    else:
        await msg.answer(text="Hozircha rasmlar mavjud emas!")


@dp.message_handler(Text("Dasturchiga xabar 💬"))
async def admin_send(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=f'{msg.from_user.first_name} admin sahifaga xush kelibsiz!',
                         reply_markup=admin_btn())
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
    if msg.from_user.id in ADMINS:
        await msg.answer(text='Bosh menu 🛎', reply_markup=main_btn())
    else:
        await msg.answer("Siz admin emassiz ❌")


@dp.message_handler(Text("📊 Statistika"))
async def statistika(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=f'Foydalanuvchilar Soni: {len(user.all_users())}')
    else:
        await msg.answer("Siz admin emassiz ❌")


@dp.message_handler(Text("🗣 Reklama"))
async def reklama_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await RekState.reklama.set()
        await msg.answer(text="Reklama Bo'limi: ", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌")


@dp.message_handler(state=RekState.reklama, content_types=types.ContentType.ANY)
async def rek_state_handler(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish bekor qilindi 🤖❌", reply_markup=admin_btn())
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish boshlandi 🤖✅", reply_markup=admin_btn())
        summa = 0
        users = user.all_users()
        for i in users:
            if int(i[1]) not in ADMINS:
                summa += await send_adversment(msg, i[1])
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(ADMINS[0], text=f"Botni bloklagan userlar soni: {summa}")

@dp.message_handler()
async def search_picture(msg: types.Message):
    msg_stiker = await msg.answer("⏳")
    if 'sex' in await translate_txt(msg.text.lower()):
        await msg.answer(text="Siz taqiqlangan kontent qidiryabsiz 🆘")
    else:
        data = await api.search_pic(msg.text)
        if data:
            await msg_stiker.delete()
            try:
                await bot.send_media_group(chat_id=msg.chat.id, photo=data)
            except:
                pass
        else:
            await msg.answer(text="Siz qidirgan mavzu bo'yicha hech qanday rasm topilmadi 😔", reply_markup=main_btn())
