from bs4 import BeautifulSoup

from seleniumwire import webdriver

import re
from datetime import date

from main_bot import MainBot

from data.month_google import dict_month_google


class GoogleBot(MainBot):

    def __init__(self, url_list, mode=False):
        super().__init__(url_list)

        self.browser = super().setup_browser()
        self.date_now = super().setup_date_now()

        
        if mode:
            self.dict_url = super().write_json('google')
        else:
            self.dict_url = {}

        
    def __request_soup(self, url):
        """
        Открывает браузер
        """
        google_cache_url = f'http://webcache.googleusercontent.com/search?q=cache:{url}'
        self.browser.get(google_cache_url)

        self.__current_status(url)
        
        return BeautifulSoup(self.browser.page_source, 'lxml')


    def __current_status(self, url):
        """
        Проверка страницы на статус и обработка капчи
        """
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
        

    def __collect_element(self, soup, url):
        """
        Функция собирает в dict_url время и проверяет прошёл ли месяц сохранённой версии
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
        browser_month_lsit = dict_month_google[matches_list[1]]
        browser_month = browser_month_lsit[1]
        now_month = self.date_now.strftime('%b')
        current_month = browser_month == now_month

        list_first_date = self.date_now.strftime('%Y %m %d').split(' ')

        if not current_month:
            first_date = date(
                int(list_first_date[0]), 
                int(list_first_date[1]), 
                int(list_first_date[2])
                )
            second_date = date(
                int(matches_list[2]), 
                int(browser_month_lsit[0]), 
                int(matches_list[0])
                )
            different_date = first_date - second_date

            if different_date.days < 30:
                current_month = True

        self.dict_url[url] = {
                'time': matches[0],
                'current': current_month,
        }
    

    def iter_urls(self):
        try:
            for url in self.url_list:
                soup = self.__request_soup(url)
                if soup:
                    self.__collect_element(soup, url)
        except:
            self.get_dict_urls()
            
        
        self.browser.close()


    def get_dict_urls(self):
        super().save_json(self.dict_url, 'google')
        return self.dict_url
