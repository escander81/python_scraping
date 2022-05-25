from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import csv

main_url = 'https://hh.ru'

params = {'area': '78',
          'text': 'Python developer'}
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.71 Safari/537.36 OPR/80.0.4170.40'}

response = requests.get(main_url+'/search/vacancy', params=params, headers=headers).text

html = ''
with open('page.html', 'r') as f:
    html = f.read()

soup = bs(html, 'html.parser')


for vac_anchor in soup.find_all('div', class_='vacancy-serp-item'):


    vac_title = vac_anchor.a.getText()
    vac_link = vac_anchor.a['href']
    # vac_info = vac_anchor.nextSibling
    vac_salary = vac_anchor.find('span', class_='bloko-header-section-3')
    vac_salary_sum = str(vac_salary).strip()\
        .replace('<span class="bloko-header-section-3" data-qa="vacancy-serp__vacancy-compensation">','')\
        .replace('<!-- --> <!-- -->', ' ')\
        .replace('</span>', '.')\
        .replace('<!-- -->', '')\
        .replace('..', '.')



    print(vac_title, vac_salary_sum, vac_link)