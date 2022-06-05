from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient


def get_html(f_url, f_link=None):

    f_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

    if f_link is None:
        resp = requests.get(f_url, headers=f_header)
        f_dom = html.fromstring(resp.text)
        return f_dom

    resp = requests.get(f_url + f_link, headers=header)
    f_dom = html.fromstring(resp.text)
    avtor = f_dom.xpath("//span[@itemprop='name']/text()")

    return avtor


client = MongoClient('127.0.0.1', 27017)
db = client['news']
d_news = db.news
d_news.delete_many({})

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 OPR/80.0.4170.40'}
url = 'https://lenta.ru'
dom = get_html(url)

news = dom.xpath("//time[@class='g-time']/../text()")
link = dom.xpath("//time[@class='g-time']/../@href")
date = dom.xpath("//time[@class='g-time']/@datetime")

for i in range(10):
    news_dict = dict()
    news_dict['1_Date'] = date[i]
    news_dict['2_News'] = news[i].replace('\xa0', ' ')
    news_dict['3_Link'] = url + link[i]
    news_dict['4_Avtor'] = get_html(url, link[i])

    d_news.insert_one(news_dict)

for d_mongo in d_news.find({}):
    pprint(d_mongo)