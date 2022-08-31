import requests
import json

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()
with open('token_disk.txt', 'r') as file_object:
    token_dick = file_object.read().strip()

ower_id = input('Введите id: ')
count = input('Введите количество фотографий: ')

URL = 'https://api.vk.com/method/photos.getAll/'
params = {
    'owner_id': ower_id,
    'access_token': token,
    'v':'5.131',
    'extended': 'likes',
    'album_id': 'profile',
    'count' : count
}
res = requests.get(URL, params=params,).json()
qwe = res['response']['items']


photo_list ={}
json_file = []
for n in qwe:
    likes = str(n['likes']['count'])
    date = str(n['date'])
    photo_url = n['sizes'][-1]['url']
    if likes not in photo_list.values():
        photo_list = {'likes': likes, 'url': photo_url}
        file = {'file_name': likes, 'size': n['sizes'][-1]['type']}
    else:
        photo_list = {'likes': likes + '_' + date, 'url': photo_url}
        file = {'file_name': likes + '_' + date, 'size': n['sizes'][-1]['type']}
    json_file.append(file)

    class YaUploader:
        def __init__(self, token: str):
            self.token = token_dick

        def upload(self, file_path: str):
            file_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_dick}'}
            params = {'url': file_path,  'path': photo_list['likes'], 'overwrite': 'true'}
            response = requests.post(file_url, headers=headers,params=params)
            if response.status_code == 202:
                print('Загрузка прошла успешно!')
            else:
                print(f'Ошибка загрузки! Код ошибки: {response.status_code}')

    if __name__ == '__main__':
        path_to_file = photo_list['url']
        uploader = YaUploader(token)
        result = uploader.upload(path_to_file)
        with open('file_info.json', 'w') as f:
            json.dump(json_file, f)