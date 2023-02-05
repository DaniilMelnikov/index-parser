from bs4 import BeautifulSoup
from seleniumwire import webdriver
import re
from datetime import datetime, date

from warning_dialog import result_window

class YandexBot():

    def __init__(self, url_list):
        self.cache_url = ''
        self.url_list = url_list
        self.dict_month = {'Jan': '01',
                'Feb': '02',
                'Mar': '03', 
                'Apr': '04',
                'May': '05',
                'Jun': '06',
                'Jul': '07',
                'Aug': '08',
                'Sep': '09',
                'Oct': '10',
                'Nov': '11',
                'Dec': '12',
                }
        self.browser = webdriver.Edge()
        self.dict_url = {}
        self.date_now = datetime.now()

    def __request_soup(self, url, mode_url=True):
        if mode_url:
            yandex_url = f'https://yandex.ru/search/?text=url%3A{url}'
        else:
            yandex_url = url
        self.browser.get(yandex_url)

        soup = BeautifulSoup(self.browser.page_source, 'lxml')

        root = soup.find("div", {"id": "root"})
        while root:
            soup = BeautifulSoup(self.browser.page_source, 'lxml')
            root = soup.find("div", {"id": "root"})
            
        return BeautifulSoup(self.browser.page_source, 'lxml')

    def __collect_url_search(self, soup):
        """
        Функция ищет урл сохранённой страницы
        """
        button_list = soup.find_all('button')
        for button in button_list:
            button = str(button)
            if 'yandexwebcache.net' in button:
                str_match = button
                break
        
        regex = r'\:\"*(https:\/\/yandexwebcache.net.+keyno=[0-9]*)\"*'
        matches  = re.findall(regex, str(str_match), re.MULTILINE)
        return matches[0].replace('amp;', '')
    
    def __collect_element(self, soup):
        cache_id = soup.find("div", {"id": "yandex-cache-hdr"})
        span_list = cache_id.find_all('span')
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
        browser_month = matches_list[1][0:3]
        browser_month_list = self.dict_month[browser_month]
        now_month = self.date_now.strftime('%b')
        current_month = browser_month == now_month

        list_first_date = self.date_now.strftime('%Y %m %d').split(' ')

        if not current_month:
            if list_first_date[1][0] == '0':
                list_first_date[1] = list_first_date[1][1]
            elif list_first_date[2][0] == '0':
                list_first_date[2] = list_first_date[2][1]
            
            if browser_month_list[0] == '0':
                browser_month_list = browser_month_list[1]

            first_date = date(int(list_first_date[0]), int(list_first_date[1]), int(list_first_date[2]))
            second_date = date(int(matches_list[2]), int(browser_month_list[0]), int(matches_list[0]))
            different_date = first_date - second_date

            if different_date.days < 30:
                current_month = True

        self.dict_url[self.cache_url] = {
                'time': matches[0],
                'current': current_month,
        }

        
    def iter_urls(self):
        for url in self.url_list:
            self.cache_url = url
            soup_first = self.__request_soup(self.cache_url)
            url = self.__collect_url_search(soup_first)
            soup_second = self.__request_soup(url, False)
            self.__collect_element(soup_second)


        self.browser.close()

    def get_dict_urls(self):
        return self.dict_url