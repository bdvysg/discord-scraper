import requests
import json
from requests.structures import CaseInsensitiveDict 
from config import *
import os
from datetime import datetime

headers = CaseInsensitiveDict()
headers['Authorization'] = Authorization



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


def get_all_message():
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
            links.append(i[0]['attachments'][0]['url'])
            titles.append(i[0]['attachments'][0]['filename'])
            timestamps.append(i[0]['timestamp'])
        return links, titles, timestamps

    def download_imgs(data: tuple):
        try:
            assert(len(data[0]) == len(data[1]) == len(data[2]), 'Не соответствие данных(ссылка, имя, дата создание)')  
            for i in range(len(data[0])):
                res = requests.get(data[0][i])
                if data[1][i].startswith('unknown'):
                    with open('C:/Users/bdvys/Desktop/discord parser/images/screenshots/' + 'unknown_' + str(next(for_unknown)) + '.png', 'wb') as file:
                        file.write(res.content)
                        os.utime(file.name, 
                                (datetime.timestamp(datetime.strptime(data[2][i], '%Y-%m-%dT%H:%M:%S.%f%z')), 
                                 datetime.timestamp(datetime.strptime(data[2][i], '%Y-%m-%dT%H:%M:%S.%f%z'))))
                else:
                    with open('C:/Users/bdvys/Desktop/discord parser/images/' + data[1][i], 'wb') as file:
                        file.write(res.content)
                        os.utime(file.name, 
                                (datetime.timestamp(datetime.strptime(data[2][i], '%Y-%m-%dT%H:%M:%S.%f%z')), 
                                 datetime.timestamp(datetime.strptime(data[2][i], '%Y-%m-%dT%H:%M:%S.%f%z'))))
                print('Загружено - ' + data[1][i])
        except Exception as ex:
            print(ex)
  
    url = 'https://discord.com/api/v9/guilds/' + Server + ' /messages/search?has=image'
    res = requests.get(url, headers=headers)
    js = json.loads(res.text)
    total_num = js['total_results']
    for i in range(0, total_num, 50):
        download_imgs(get_img_data(js))
        url = 'https://discord.com/api/v9/guilds/' + Server + ' /messages/search?has=image&offset=' + str(i)
        res = requests.get(url, headers=headers)
        js = json.loads(res.text)

get_all_pics()


