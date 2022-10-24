from bs4 import BeautifulSoup
import requests
import lxml
import os
from time import sleep


def create_url(request):
    data = []

    for n in range(1, 10):
        print("Parsing ", n, " page")
        request.replace(' ', '%20')
        url = f'https://yandex.ru/images/search?text={request}&p={n}'
        r = requests.get(url)
        sleep(2)
        soup = BeautifulSoup(r.text, 'lxml')
        tmp = soup.find_all('img', class_='serp-item__thumb justifier__thumb')
        for img in tmp:
            tmp_url = 'https:' + img.get('src')
            yield (tmp_url)


def create_dir(src):
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    folder_name = os.path.join('dataset', src)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def download_img(img_url, img_name, img_path):
    response = requests.get(img_url)
    file_name = os.path.join('dataset', img_path, img_name+'.jpg')
    file = open(file_name, "wb")
    file.write(response.content)
    file.close()


def run(class_name):
    create_dir(class_name)
    number = 0
    for item in create_url(class_name):
        download_img(item, str(number).zfill(4), class_name)
        number += 1
        if (number % 10 == 0):
            print('downloded: ', number)
