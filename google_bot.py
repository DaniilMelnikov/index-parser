from bs4 import BeautifulSoup
from selenium import webdriver
import re

from datetime import datetime, date

class GoogleBot():

    def __init__(self, url_list):
        self.url_list = url_list
        self.dict_month = {'янв': ['01', 'Jan'],
                'фев': ['02', 'Feb'],
                'мар': ['03', 'Mar'], 
                'апр': ['04', 'Apr'],
                'май': ['05', 'May'],
                'июн': ['06', 'Jun'],
                'июл': ['07', 'Jul'],
                'авг': ['08', 'Aug'],
                'сен': ['09', 'Sep'],
                'окт': ['10', 'Oct'],
                'ноя': ['11', 'Nov'],
                'дек': ['12', 'Dec'],
                }
        self.browser = webdriver.Edge()
        self.dict_url = {}
        self.date_now = datetime.now()

    def request_soup(self, url):
        """
        Открывает браузер
        """
        google_cache_url = f'http://webcache.googleusercontent.com/search?q=cache:{url}'
        self.browser.get(google_cache_url)
        return BeautifulSoup(self.browser.page_source, 'lxml')

    def collect_element(self, soup, url):
        """
        Функция собирает в dict_url время и проверяет прошёл ли месяц созранённой версии
        """
        span_list = soup.find_all('span')
        #Ищем в супе нужный span с датой
        for el in span_list:
            el = str(el)
            if 'GMT' in el:
                str_match = el
                break
        #выдёргиваем дату регулярным выражением и делим в список
        regex = r'\d+\s*\w+\s*\d+.+GMT*'
        matches = re.findall(regex, str(str_match), re.MULTILINE)    
        matches_list = matches[0].split(' ')
        #Проверяем верный ли месяц
        browser_month_lsit = self.dict_month[matches_list[1]]
        browser_month = browser_month_lsit[1]
        now_month = self.date_now.strftime('%b')
        current_month = browser_month == now_month

        list_first_date = self.date_now.strftime('%Y %m %d').split(' ')

        if not current_month:
            if list_first_date[1][0] == '0':
                list_first_date[1] = list_first_date[1][1]
            elif list_first_date[2][0] == '0':
                list_first_date[2] = list_first_date[2][1]
            first_date = date(int(list_first_date[0]), int(list_first_date[1]), int(list_first_date[2]))
            second_date = date(matches_list[2], browser_month_lsit[0], matches_list[0])
            different_date = first_date - second_date


        self.dict_url[url] = {
                'time': '',
                'current': True,
        }
        self.dict_url[url]['time'] = matches[0]
        self.dict_url[url]['current'] = current_month

    def iter_urls(self):
        for url in self.url_list:
            soup = self.request_soup(url)
            self.collect_element(soup, url)

        self.browser.close()

    def get_dict_urls(self):
        return self.dict_url
