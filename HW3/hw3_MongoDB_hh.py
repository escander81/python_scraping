from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_url = 'https://hh.ru'
vacancy = 'Python Developer'
page = 0
all_vacancies = []
params = {'text': vacancy,
          'area': 78,
          'experience': 'doesNotMatter',
          'order_by': 'relevance',
          'search_period': 0,
          'items_on_page': 20,
          'page': page}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/98.0.4758.141 YaBrowser/22.3.4.731 Yowser/2.5 Safari/537.36'}
response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
soup = bs(response.text, 'html.parser')

try:
    last_page = int(soup.find_all('a',{'data-qa':'pager-page'})[-1].text)
except:
    last_page = 1

for i in range(last_page):

    soup = bs(response.text, 'html.parser')

    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies:

        vacancy_info = {}
        vacancy_anchor = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"})
        vacancy_name = vacancy_anchor.getText()
        vacancy_info['name'] = vacancy_name

        vacancy_link = vacancy_anchor['href']
        vacancy_info['link'] = vacancy_link
        vacancy_info['site'] = main_url + '/'
        vacancy_salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})

        if vacancy_salary is None:
            min_salary = None
            max_salary = None
            currency = None
        else:
            vacancy_salary = vacancy_salary.getText()
            if vacancy_salary.startswith('до'):
                max_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                min_salary = None
                currency = vacancy_salary.split()[-1]

            elif vacancy_salary.startswith('от'):
                max_salary = None
                min_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

            else:
                max_salary = int("".join([s for s in vacancy_salary.split('–')[1] if s.isdigit()]))
                min_salary = int("".join([s for s in vacancy_salary.split('–')[0] if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

        vacancy_info['max_salary'] = max_salary
        vacancy_info['min_salary'] = min_salary
        vacancy_info['currency'] = currency

        all_vacancies.append(vacancy_info)

    params['page'] += + 1
    response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
    # print(len(all_vacancies))
pprint(all_vacancies)
