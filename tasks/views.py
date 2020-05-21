from django.shortcuts import render
from django.db import connection
from .models import hotelrooms
from django.db.models import Count
import fake_useragent
import requests
from bs4 import BeautifulSoup as bs


# Задание №1
def task1():
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS hotelrooms(id int, room_id int, hotel_id int, price int)")
    cursor.fetchone()

    cursor1 = connection.cursor()
    cursor1.execute("SELECT hotel_id FROM hotelrooms GROUP BY hotel_id HAVING COUNT(room_id) < 20")
    cursor1.fetchone()


# Задание №2
def task2():
    hotelrooms.objects.values("hotel_id").annotate(rooms=Count("room_id")).filter(rooms__lt=20)


# Задание №3
def get_html(url):
    user_agent = fake_useragent.UserAgent()
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers)
    return r.text


def get_all_links(html):
    soup = bs(html, 'lxml')
    ads = soup.find_all('div', {'class': 'col-lg-12 col-md-6 col-sm-6 col-xs-12 travel-box-container'})[0:4]

    all_links = []

    for index, ad in enumerate(ads):
        link = 'https://www.lueftner-cruises.com' + ad.find('a', class_='btn btn-primary btn-block visible-xs-block').get('href')
        all_links.append(link)

    return all_links


def get_page_data(html):
    soup = bs(html, 'lxml')

    name = soup.find('div', class_='cruise-headline').find('h1').text

    days = soup.find('div', class_='col-xs-12 col-sm-6 col-lg-5').find('p', class_='cruise-duration pull-right').text.replace(' Days', '')

    itinerary = []
    itinerary1 = soup.find('div', class_='panel-group accordion route').find_all('div', class_='panel panel-default')
    for i in itinerary1:
        a = i.find('span', class_='route-city').text.replace('\n                                ', '')
        itinerary.append(a)

    date = []
    date1 = soup.find('div', class_='panel-group accordion price accordeon-data-price').find_all('div', class_='panel panel-default accordeon-panel-default')
    for i in date1:
        a = i.find('span', class_='price-duration').text
        date.append(a)

    ship = []
    ship1 = soup.find('div', class_='panel-group accordion price accordeon-data-price').find_all('div', class_='panel panel-default accordeon-panel-default')
    for i in ship1:
        a = i.find('span', class_='table-ship-name fakelink').text
        ship.append(a)

    price = []
    price1 = soup.find('div', class_='panel-group accordion price accordeon-data-price').find_all('div', class_='panel panel-default accordeon-panel-default')

    for i in price1:
        a = i.find('span', class_='big-table-font').text.replace('\n', '')
        price.append(a)

    dates = []
    for a, b, c in zip(date, ship, price):
        dates.append([{a: {'ship': b, 'price': c}}])

    data = [{'name': name,
            'days': days,
             'itinerary': itinerary,
             'dates': dates}]

    return data


def main(request):
    url = 'https://www.lueftner-cruises.com/en/river-cruises/cruise.html'

    all_links = get_all_links(get_html(url))
    data_new = []
    for link in all_links:
        html = get_html(link)
        data = get_page_data(html)
        data_new.append(data)

    context = {"data": data_new}

    return render(request, 'tasks/base.html', context)


if __name__ == '__main__':
    main()


""" Задание 4
Если данные из предыдущего задания будут в виде xml файла,
то необходимо будет использовать библиотеку ElementTree (import xml.etree.ElementTree).
Для начала мы создаем корневой элемент при помощи функции Element.
Далее, мы создаем элемент назначения и добавляем его к root.
Далее, мы создаем SubElements, выполнив парсинг назначения объекта Element в SubElement наряду с именем.
Далее, для каждого SubElement, мы назначаем их текстовые свойства, для передачи значения.
В конце скрипта мы создаем ElementTree и используем его для написания XML в файле.
"""




