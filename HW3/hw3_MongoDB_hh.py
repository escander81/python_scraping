from pymongo import MongoClient
import requests as rq
from bs4 import BeautifulSoup
from pprint import pprint


def zp_check(value):
    z_min = None
    z_max = None
    ue = None

    try:
        value = value.getText().replace('\u202f', '').split()
        if value[0] == 'от':
            z_min = float(value[1])
            ue = value[2]
        elif value[0] == 'до':
            z_max = float(value[1])
            ue = value[2]
        else:
            z_min = float(value[0])
            z_max = float(value[2])
            ue = value[3]

    finally:

        return z_min, z_max, ue


def check_vacancy(mongo_d, va_date):
    """
    Функция проверяет наличие вакансии в БД,
    что бы исключить повтор записей.
    """

    dat_b = mongo_d['headhunter']
    hh = dat_b.headhunter

    if bool(hh.find_one({'$and': [{'1_Name': va_date['1_Name']}, {'5_Link': va_date['5_Link']}]})):
        return True

    return False


def mongo_index(mongo_d):
    """
    Поиск последний созданый индекс в базе данных Index
    и добавление вновь созданного
    """
    max_index = 0
    dat_bas = mongo_d['index']

    for elem in dat_bas.index.find():
        if elem['index'] > max_index:
            max_index = elem['index']

    dat_bas.index.insert_one({'index': max_index + 1})

    return max_index + 1


def find_vac(mongo_d, value):
    """
    Поиск вакансий с ЗП выше требуемой (value)
    """
    temp = mongo_d.find({'$or': [
        {'2_Min_ZP': {'$gte': value}},
        {'3_Max_ZP': {'$gte': value}}
    ]})

    return temp


client = MongoClient('127.0.0.1', 27017)
db = client['headhunter']
db_vacancy = db.headhunter

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 OPR/80.0.4170.40'}
url = "https://hh.ru"
params = {'text': None,
          'area': 113, 'search_field': 'description', 'page': 0}

i = 0

params['text'] = input('Введите название проффессии: ')

response = rq.get(url + '/search/vacancy/', params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')

db_vacancy.delete_many({})  # Предварительная чистка БД hh для обучения
client['index'].index.delete_many({})  # Предварительная чистка БД index для обучения

try:
    page = int(dom.find_all('span', {'class': 'pager-item-not-in-short-range'})[-1].getText())
except:
    page = 1

while i < page:

    vacansies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for vacansy in vacansies:
        vac_dict = dict()

        name = vacansy.find('a').getText()
        link = vacansy.find('a')['href']
        zp = vacansy.find('div', {'class': 'vacancy-serp-item__sidebar'})

        vac_dict['_id'] = mongo_index(client)
        vac_dict['1_Name'] = name
        vac_dict['2_Min_ZP'], vac_dict['3_Max_ZP'], vac_dict['4_UE'] = zp_check(zp)
        vac_dict['5_Link'] = link[:link.index('?')]

        if check_vacancy(client, vac_dict) is False:
            db_vacancy.insert_one(vac_dict)

    i += 1
    params['page'] = i
    response = rq.get(url + '/search/vacancy/', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')

z_p = float(input('Введите желаемую ЗП: '))

for item in find_vac(db_vacancy, z_p):
    pprint(item)
    
