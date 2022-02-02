import requests
import json
from requests.structures import CaseInsensitiveDict 
from config import *
import os
from datetime import datetime
import asyncio


headers = CaseInsensitiveDict()
headers['Authorization'] = Authorization


def make_folders(path: str):
    if not os.path.exists(path + 'Images/screenshots/'):
        os.makedirs(path + 'Images/screenshots/')
    return path + 'Images/', path + 'Images/screenshots/'

img_path, screenshot_path = make_folders(path)


def get_all_message():
    def write_history(js):
        try:
            for message in js:
                with open('history.txt', 'a', encoding='utf-8') as file:
                    file.write('\n')
                    if message['content'] != '':
                        file.write(message['timestamp'][:-13].replace('T', ' ') + '-' + message['author']['username'] + ': ' + message['content'])
                    else:
                        file.write(message['timestamp'][:-13].replace('T', ' ') + '-' + message['author']['username'] + ': ' + message['attachments'][0]['url'])
        except Exception as ex:
            print(ex)

    url = 'https://discord.com/api/v9/channels/' + Chanel + ' /messages?limit=100'
    while True:
        res = requests.get(url, headers=headers)
        js = json.loads(res.text)
        write_history(js)
        url = 'https://discord.com/api/v9/channels/' + Chanel + ' /messages?before='+ js[99]['id'] +'&limit=100'


def get_all_pics():
    for_unknown = (i for i in range(1000))

    def get_img_data(js: dict):
        links = []
        titles = []
        timestamps = []
        for i in js['messages']:
            try:
                links.append(i[0]['attachments'][0]['url'])
                titles.append(i[0]['attachments'][0]['filename'])
                timestamps.append(i[0]['timestamp'])
            except Exception as ex:
                    print('Ошибка при получении ссылки/имени/даты - ' + str(ex.__class__.__name__) + '(' + str(ex) + ')')    
                    with open('errors.txt', 'a', encoding='utf-8') as file:
                        file.write('\nОшибка при получении ссылки/имени/даты - ' + str(ex.__class__.__name__) + '(' + str(ex) + ')' + ' json: ' + json.dumps(js))
        return links, titles, timestamps

    def download_imgs(data: tuple):
        for i in range(len(data[0])):
            try:
                res = requests.get(data[0][i])
            except Exception as ex:
                print('Ошибка при скачивании картинки - ' + str(ex.__class__.__name__) + '(' + str(ex) + ')')
                with open('errors.txt', 'a', encoding='utf-8') as file:
                    file.write('\nОшибка при скачивании картинки - ' + str(ex.__class__.__name__) + '(' + str(ex) + ')' + ' url: ' + data[0][i])
            try:
                if data[1][i].startswith('unknown'):
                    with open(screenshot_path + 'unknown_' + str(next(for_unknown)) + '.png', 'wb') as file:
                        file.write(res.content)
                        os.utime(file.name, 
                                (datetime.timestamp(datetime.strptime(data[2][i], '%Y-%m-%dT%H:%M:%S.%f%z')), 
                                datetime.timestamp(datetime.strptime(data[2][i], '%Y-%m-%dT%H:%M:%S.%f%z'))))
                else:
                    with open(img_path + data[1][i], 'wb') as file:
                        file.write(res.content)
                        os.utime(file.name, 
                                (datetime.timestamp(datetime.strptime(data[2][i], '%Y-%m-%dT%H:%M:%S.%f%z')), 
                                datetime.timestamp(datetime.strptime(data[2][i], '%Y-%m-%dT%H:%M:%S.%f%z'))))
                print('Загружено ' + str(next(total_count)) + ' - ' + data[1][i] + ' (' + thread.name + ')' + '(' + str(threading.active_count()) + ')')
            except Exception as ex:
                print('Ошибка при сохранении файла - ' + str(ex.__class__.__name__) + '(' + str(ex) + ')')
                with open('errors.txt', 'a', encoding='utf-8') as file:
                    file.write('\nОшибка при сохранении файла - ' + str(ex.__class__.__name__) + '(' + str(ex) + '):'
                              '\n   ' + data[0][i] + 
                              '\n   ' + data[1][i] + 
                              '\n   ' + data[2][i] 
                              )

    def main(start: int, end: int):
        for i in range(start, end, 25):
            try:
                if i == 0:
                    url = 'https://discord.com/api/v9/guilds/' + Server + ' /messages/search?has=image'
                else:
                    url = 'https://discord.com/api/v9/guilds/' + Server + ' /messages/search?has=image&offset=' + str(i) 
                res = requests.get(url, headers=headers)
                js = json.loads(res.text)
                len(js['messages'])
                download_imgs(get_img_data(js))
            except Exception as ex:
                print('Ошибка при получении данных - ' + str(i) + ' ' + str(ex.__class__.__name__) + '(' + str(ex) + ')')
                with open('errors.txt', 'a', encoding='utf-8') as file:
                    file.write('\nОшибка при получении данных - ' + str(i) + ' ' + str(ex.__class__.__name__) + '(' + str(ex) + ')' + ' json: ' + json.dumps(js))
            

    url = 'https://discord.com/api/v9/guilds/' + Server + ' /messages/search?has=image'
    res = requests.get(url, headers=headers)
    js = json.loads(res.text)
    total_num = js['total_results']
    print('Найдено - ' + str(total_num) + ' изображений')
    total_count = (i for i in range(1, total_num))
    for i in range(5):
        thread = threading.Thread(target=main, args=((total_num // 5) * i, (total_num // 5) * i + (total_num // 5),))
        thread.start()
        time.sleep(2)
        

    if total_num % 5 != 0:
        thread = threading.Thread(target=main, args=((total_num // 5) * 4 + (total_num // 5), (total_num // 5) * 4 + (total_num // 5) + (total_num % 5),))
        thread.start()

    
    
    

get_all_pics()




