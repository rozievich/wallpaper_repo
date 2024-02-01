import httpx
from utils.misc.translations import translate_txt
from aiogram.types import InputMediaPhoto


class UniversalAPI:
    HOST = 'https://api.pexels.com/v1/search'
    AUTH = 'TDQtaySGS2nzPtvHWo0BtLHxXzbHS81R2pIi6PNSky8A1ymYjXsbbu8p'
    TOP = 'https://api.pexels.com/v1/curated'

    async def search_pic(self, msg: str):
        index = await translate_txt(msg)
        async with httpx.AsyncClient() as client:
            try:
                result = await client.get(self.HOST, headers={'Authorization': self.AUTH}, params={'query': index, 'per_page': 10})
                if result.status_code == 200:
                    data = result.json()
                    image_medias = [InputMediaPhoto(media=i['src']['original'], caption="@pictarchbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥" if v == 0 else None) for v, i in enumerate(data['photos'])]
                    return image_medias
                else:
                    return []
            except:
                return []

    async def inline_pic(self, msg: str):
        index = await translate_txt(msg)
        async with httpx.AsyncClient() as client:
            try:
                result = httpx.get(self.HOST, headers={'Authorization': self.AUTH}, params={'query': index,'per_page': 50})
                if result.status_code == 200:
                    data = result.json()
                    return data['photos']
                else:
                    return []
            except:
                return []

    async def trend_pic(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.TOP, headers={'Authorization': self.AUTH}, params={'per_page': 50})
                if response.status_code == 200:
                    data = response.json()['photos']
                    media_data = []
                    if len(data) > 10:
                        for i in range(0, len(data), 10):
                            small_media = [InputMediaPhoto(media=v['src']['original']) for v in data[i:i + 10]]
                            media_data.append(small_media)
                    else:
                        media_data = [InputMediaPhoto(media=i['src']['original'], caption="@pictarchbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥" if v == 0 else None) for v, i in enumerate(data)]

                    return media_data
                else:
                    return []
            except:
                return []
