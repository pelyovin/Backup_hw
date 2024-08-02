import requests
import json
import yadisk
from datetime import datetime
from tqdm import tqdm


class Reserv:
    URL_TO_GET_PHOTOS = ('https://api.vk.com/method/photos.get')

    def __init__(self, access_token, vk_id):
        self.access_token = access_token
        self.vk_id = vk_id

    def get_photos(self):
        params = {
            'access_token': self.access_token,
            'owner_id': self.vk_id,
            'album_id': 'profile',
            'extended': 1,
            'v': '5.199'
        }
        response = requests.get(self.URL_TO_GET_PHOTOS, params=params)
        return response.json()

    def file_info(self):
        info = []
        for i in self.get_photos()['response']['items']:
            info.append(
                {"file_name": f'{i["likes"]["count"]}_{datetime.fromtimestamp(i["date"]).strftime("%Y-%m-%d")}.png',
                 "size": "z"})
        with open('file_info.json', 'w') as f:
            json.dump(info, f)

    def to_download(self):
        photos_dict = {}
        for i in self.get_photos()['response']['items']:
            for j in i['sizes']:
                if j['type'] == 'z':
                    photos_dict[f'{i["likes"]["count"]}_{datetime.fromtimestamp(i["date"]).strftime("%Y-%m-%d")}.png'] = \
                    j['url']
        return photos_dict

    def download_photos(self):
        client = yadisk.Client(token="")
        with client:
            if client.exists('photos') and client.is_dir('photos'):
                pass
            else:
                client.mkdir('photos')
            for key, value in tqdm(self.to_download().items()):
                if not client.exists('photos/' + key):
                    client.upload_url(value, 'photos/' + key)


access_token = ''
vk_id = '155780177'

one = Reserv(access_token, vk_id)
one.file_info()
one.download_photos()