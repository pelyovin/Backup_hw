import requests
import json
import yadisk
from datetime import datetime
from tqdm import tqdm


class Backup:
    URL_TO_GET_PHOTOS = ('https://api.vk.com/method/photos.get')
    access_token_vk = '<Сервисный ключ доступа приложения>'

    def __init__(self, token_ya_disk, vk_id):
        self.token_ya_disk = token_ya_disk
        self.vk_id = vk_id

    def get_photos(self):
        """Метод делает запрос к апи ВК и возвращает json ответ"""
        params = {
            'access_token': self.access_token_vk,
            'owner_id': self.vk_id,
            'album_id': 'profile',
            'extended': 1,
            'v': '5.199'
        }
        response = requests.get(self.URL_TO_GET_PHOTOS, params=params)
        return response.json()

    def file_info(self):
        """Метод формирует json файл с информацией о фотографиях с указанием названия и типа размера"""
        info = []
        for i in self.get_photos()['response']['items']:
            info.append(
                {"file_name": f'{i["likes"]["count"]}_{datetime.fromtimestamp(i["date"]).strftime("%Y-%m-%d")}.png',
                 "size": "z"})
        with open('file_info.json', 'w') as f:
            json.dump(info, f)

    def to_download(self):
        """Метод формирует словарь с названием фото и ссылок на них для дальнейшего скачивания"""
        ph_dict = {}
        for i in self.get_photos()['response']['items']:
            for j in i['sizes']:
                if j['type'] == 'z':
                    ph_dict[f'{i["likes"]["count"]}_{datetime.fromtimestamp(i["date"]).strftime("%Y-%m-%d")}.png'] = \
                        j['url']
        return ph_dict

    def download_photos(self):
        """Метод сохраняет фотографии из ВК на Я. диск"""
        client = yadisk.Client(token=self.token_ya_disk)
        with client:
            if client.exists('photos') and client.is_dir('photos'):
                pass
            else:
                client.mkdir('photos')
            for key, value in tqdm(self.to_download().items()):
                if not client.exists('photos/' + key):
                    client.upload_url(value, 'photos/' + key)


token_ya_disk = input('Введите токен с Полигона Яндекс.Диска: ')
vk_id = input('Введите ваш ВК id: ')

one = Backup(token_ya_disk, vk_id)
one.file_info()
one.download_photos()
