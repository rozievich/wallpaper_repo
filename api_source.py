import httpx
import translate
import json


def search_pic(msg: str):
    index = translate_txt(msg)
    headers = {
        'Authorization': 'TDQtaySGS2nzPtvHWo0BtLHxXzbHS81R2pIi6PNSky8A1ymYjXsbbu8p'
    }
    params = {
        'query': index,
        'per_page': 10
    }
    url = 'https://api.pexels.com/v1/search'
    result = httpx.get(url, headers=headers, params=params)  # noqa
    if result.status_code == 200:
        data = result.json()
        return [data['photos'][i]['src']['original'] for i in range(0, len(data['photos']))]
    else:
        return []


def trend_pic():
    headers = {
        'Authorization': 'TDQtaySGS2nzPtvHWo0BtLHxXzbHS81R2pIi6PNSky8A1ymYjXsbbu8p'
    }
    params = {
        'per_page': 50
    }
    url = 'https://api.pexels.com/v1/curated'
    response = httpx.get(url, headers=headers, params=params)  # noqa
    if response.status_code == 200:
        data = response.json()
        return [{'url': data['photos'][i]['src']['original'], 'caption': data['photos'][i]['alt']} for i in
                range(0, len(data['photos']))]
    else:
        return []


def translate_txt(msg: str):
    translation = translate.Translator(from_lang='uz', to_lang='en')
    data = translation.translate(msg)
    return data


def writer(user: dict):
    with open('users.json', 'w') as file:
        json.dump(user, file, indent=3)


def read(tele_id: int):
    with open('users.json', 'r') as file:
        data = json.load(file)
        info = dict(data)
        for i in info['users']:
            if i == tele_id:
                writer(info)
                break
        else:
            info['users'].append(tele_id)
            writer(info)


def get_users():
    with open('users.json', 'r') as file:
        data = json.load(file)
        return data['users']

