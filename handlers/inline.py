from aiogram import types
from loader import dp
from uuid import uuid4
from data.api_source import UniversalAPI

api = UniversalAPI()

@dp.inline_handler()
async def send_data(query: types.InlineQuery):
    try:
        data = await api.inline_pic(query.query)
        results = []

        for info in data:
            if not info['alt']:
                info['alt'] = query.query.title()

            photo_url = info['src']['original']
            photo_thumb = info['src']['small']
            photo_caption = f"{info['alt']}\nPhotographer: {info['photographer']}"

            result = types.InlineQueryResultPhoto(
                id=str(uuid4()),
                photo_url=photo_url,
                thumb_url=photo_thumb,
                caption=photo_caption,
                parse_mode='Markdown'
            )
            results.append(result)

        await query.answer(results=results, cache_time=120, is_personal=True)
    except:
        pass
