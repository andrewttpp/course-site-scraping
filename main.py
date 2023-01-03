import requests
import os
from bs4 import BeautifulSoup


def pars_page(number_page: int):
    # создадим переменную с url нашего сайта
    url = f'https://cattish.ru/breed/page/{number_page}'

    # добавим заголовки для идентификации нашего запроса, чтобы показать сайту,
    # что мы не бот, а обычный пользователь
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.818 Yowser/2.5 Safari/537.36'
    }

    # создадим объект requests, который будет сохранять в себе html код страницы
    req = requests.get(url=url, headers=headers)

    # сохраним наш код в файл html с кодировкой, чтобы не дергать наш сайт запросами
    # выполняем 1 раз для записи
    with open(f'index_{number_page}.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    # откроем наш файл
    with open(f'index_{number_page}.html', 'r', encoding='utf-8') as file:
        data = file.read()

    # создадим объект обработчика BeautifulSoup и в качестве параметров передадим
    # нашу html страницу, сохраненную в переменную data, и парсер lxml
    soup = BeautifulSoup(data, 'lxml')

    # создадим 3 списка: для названий пород кошек, описания и ссылок на фото
    cats_breed_names = []
    cats_descriptions = []
    cats_links = []

    # получим названия пород всех кошек со страницы
    cats_breed = soup.find_all('h3', class_='entry-title mh-posts-list-title')

    # пробегаемся по отсортированному коду
    for cat_breed in cats_breed:
        # получим названия пород методом получения значения параметра title
        cat_name = cat_breed.find('a', rel='bookmark').get('title')

        # добавим полученное имя в список
        cats_breed_names.append(cat_name)

    # получим описание пород всех кошек со страницы
    cats_description = soup.find_all('div', class_='mh-excerpt')

    # пробегаемся по отсортированному коду
    for cat_desc in cats_description:
        # получим названия пород методом получения значения тега p
        cat_description = cat_desc.find('p').text

        # добавим полученное описание в список
        cats_descriptions.append(cat_description)

    # получим все ссылки на фото со страницы
    cats_link = soup.find_all('a', class_='mh-thumb-icon mh-thumb-icon-small-mobile')

    # пробегаемся по отсортированному коду
    for cat_links in cats_link:
        # получим ссылку на фото каждой породы
        cat_link = cat_links.find('img').get('data-src')

        # добавим ссылки в список
        cats_links.append(cat_link)

    # создадим для каждой породы отдельную папку (до этого создал внутри проекта папку cats)
    for i in range(len(cats_breed_names)):

        # зададим название нашей папки по названию породы из нашего списка
        new_folder = fr'C:\Users\USER\PycharmProjects\pythonProject1\cats\{cats_breed_names[i]}'

        # создадим нашу новую папку, если папки с таким названием нет в каталоге
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        # сохраним наше фото в переменную, а затем запишем его в двоичном формате
        downloaded_photo = requests.get(f'{cats_links[i]}').content
        with open(f'cats/{cats_breed_names[i]}/{cats_breed_names[i]}.jpg', 'wb') as file:
            file.write(downloaded_photo)

        # создадим txt файл с описанием породы и добавим в папку с данной породой
        with open(f'cats/{cats_breed_names[i]}/{cats_breed_names[i]}.txt', 'w', encoding='utf-8') as file:
            file.write(cats_descriptions[i])


if __name__ == '__main__':
    # соберем со всех страниц всю информацию с помощью цикла
    for page in range(7):
        pars_page(page + 1)
