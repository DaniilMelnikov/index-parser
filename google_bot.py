from bs4 import BeautifulSoup

from seleniumwire import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service

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

        options = webdriver.ChromeOptions()
        options.add_extension('anticaptcha-plugin_v0.63.zip')

        self.capa = DesiredCapabilities.CHROME
        self.capa["pageLoadStrategy"] = "eager"

        service = Service(executable_path='chromedriver/chromedriver.exe')
        self.browser = webdriver.Chrome(service=service, options=options, desired_capabilities=self.capa)

        self.dict_url = {}
        self.date_now = datetime.now()

    def request_soup(self, url):
        """
        Открывает браузер
        """
        google_cache_url = f'http://webcache.googleusercontent.com/search?q=cache:{url}'
        self.browser.get(google_cache_url)
        
        captcha = False

        for request in self.browser.requests:
            if request.response:
                if request.response.status_code == 404:
                    self.dict_url[url] = {
                        'time': 'Ошибка 404',
                        'current': False,
                    }
                    self.browser.close()
                    self.browser = webdriver.Chrome(desired_capabilities=self.capa)
                    return False
                if request.response.status_code == 429:
                    soup = BeautifulSoup(self.browser.page_source, 'lxml')
                    captcha = soup.find("form", {"id": "captcha-form"})

        if captcha:

            while captcha:
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                captcha = soup.find("form", {"id": "captcha-form"})

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
            first_date = date(int(list_first_date[0]), int(list_first_date[1]), int(list_first_date[2]))
            second_date = date(int(matches_list[2]), int(browser_month_lsit[0]), int(matches_list[0]))
            different_date = first_date - second_date

            if different_date.days < 30:
                current_month = True

        self.dict_url[url] = {
                'time': matches[0],
                'current': current_month,
        }

    def iter_urls(self):
        for url in self.url_list:
            soup = self.request_soup(url)
            if soup:
                self.collect_element(soup, url)

        self.browser.close()

    def get_dict_urls(self):
        return self.dict_url