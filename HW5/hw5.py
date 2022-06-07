from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains
# import time
from datetime import date, timedelta
from pprint import pprint


def check_letter(mongo_d, va_date):
    """
    Функция проверяет наличие вакансии в БД,
    что бы исключить повтор записей.
    """

    if bool(mongo_d.find_one({'$and': [{'Mail_Sender': va_date['Mail_Sender']}, {'Send_Date': va_date['Send_Date']}]})):
        return True

    return False


# study.ai_172@mail.ru
# NextPassword172#

client = MongoClient('127.0.0.1', 27017)
db = client['mailru']
mail = db.mailru

mail.delete_many({})

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(10)
action = ActionChains(driver)

driver.get('https://mail.ru')

elem = driver.find_element(By.CLASS_NAME, 'email-input')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)

elem = driver.find_element(By.CLASS_NAME, 'password-input')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)

temp = []
first_check = driver.find_elements(By.XPATH, "//div[@class='dataset__items']//a[contains(@class, 'llc')]")
last_check = None

"""
Делаем прокрутку входящих сообщений,
собирая все ссылки на сообщения,
включая повторы.
"""
while first_check != last_check:

    last_check = driver.find_elements(By.XPATH, "//div[@class='dataset__items']//a[contains(@class, 'llc')]")
    for _el in last_check:
        temp.append(_el.get_attribute('href'))
    action.move_to_element(last_check[-1])
    action.perform()
    first_check = driver.find_elements(By.XPATH, "//div[@class='dataset__items']//a[contains(@class, 'llc')]")

"""
Убираем повторы.
"""

mem = set(temp)

""" 
В множестве mem может попасть пустой элемент,
поэтому необходимо удалить его для возможности
обработки писем
"""

if None in mem:
    mem.remove(None)


for el in mem:
    temp_mail = dict()

    driver.get(el)

    mail_send = driver.find_element(By.XPATH, "//div[@class='letter__author']/span")
    temp_mail["Mail_Sender"] = " - ".join([mail_send.get_attribute('title'), mail_send.text])

    date_send = driver.find_element(By.XPATH, "//div[@class='letter__date']").text.replace(
        "Сегодня,", f"{date.today()}"
    ).replace(
        "Вчера,", f"{date.today() - timedelta(days=1)}"
    )
    temp_mail["Send_Date"] = date_send

    thread = driver.find_element(By.XPATH, "//h2[@class='thread__subject']").text
    temp_mail["Thread"] = thread

    letter = driver.find_element(By.XPATH, "//div[contains(@class,'letter-body')]").text
    temp_mail["Letter"] = letter

    if check_letter(mail, temp_mail) is False:
        mail.insert_one(temp_mail)

for letter in mail.find({}):
    pprint(letter)
    
