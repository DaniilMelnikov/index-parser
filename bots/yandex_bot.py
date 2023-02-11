import sys
import os
sys.path.append(os.getcwd())

from bs4 import BeautifulSoup

from seleniumwire import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from datetime import date
import urllib.request
import re
from main_bot import MainBot

from captcha.yandex_captcha import img_captcha
from data.month_yandex import dict_month_yandex

class YandexBot(MainBot):

    def __init__(self, url_list, mode=False):
        super().__init__(url_list)

        self.browser = super().setup_browser()
        self.date_now = super().setup_date_now()


        if mode:
            self.dict_url = super().write_json('yandex')
        else:
            self.dict_url = {}

        self.cache_url = ''

    def __request_soup(self, url, mode_url=True):
        if mode_url:
            yandex_url = f'https://yandex.ru/search/?text=url%3A{url}'
        else:
            yandex_url = url
        self.browser.get(yandex_url)

        soup = BeautifulSoup(self.browser.page_source, 'lxml')

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

        root = soup.find("div", {"id": "root"})
        if root:
            try:
                WebDriverWait(self.browser, 5).until(lambda x: x.find_element(By.CLASS_NAME, "CheckboxCaptcha-Anchor").click())
            except:
                pass
            try:
                WebDriverWait(self.browser, 5).until(lambda x: x.find_element(By.CLASS_NAME, 'AdvancedCaptcha-Image'))
            except:
                pass
            img = self.browser.find_element(By.CLASS_NAME, 'AdvancedCaptcha-Image')
            src = img.get_attribute('src')
            urllib.request.urlretrieve(src, "img/captcha.jpeg")

            current_api = img_captcha()
            if not current_api:
                print('Придётся самому вводить капчу!!!')
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
        try:
            regex = r'\:\"*(https:\/\/yandexwebcache.net.+keyno=[0-9]*)\"*'
            matches  = re.findall(regex, str(str_match), re.MULTILINE)
            return matches[0].replace('amp;', '')
        except:
            return False
    
    def __collect_element(self, soup):
        cache_id = soup.find("div", {"id": "yandex-cache-hdr"})
        if cache_id:
            span_list = cache_id.find_all('span')
            for el in span_list:
                el = str(el)
                if 'GMT' in el:
                    str_match = el
                    break
        else:
            self.dict_url[self.cache_url] = {
                    'time': 'Нет элемента yandex-cache-hdr',
                    'current': 'Ошибка в программе',
            }

        #выдёргиваем дату регулярным выражением и делим в список
        regex = r'\d+\s*\w+\s*\d+.+GMT*'
        matches = re.findall(regex, str(str_match), re.MULTILINE)    
        matches_list = matches[0].split(' ')
        #Проверяем верный ли месяц
        browser_month = matches_list[1][0:3]
        browser_month_list = dict_month_yandex[browser_month]
        now_month = self.date_now.strftime('%b')
        current_month = browser_month == now_month

        list_first_date = self.date_now.strftime('%Y %m %d').split(' ')
        if not current_month:
            first_date = date(int(list_first_date[0]), int(list_first_date[1]), int(list_first_date[2]))
            second_date = date(int(matches_list[2]), int(browser_month_list), int(matches_list[0]))
            different_date = first_date - second_date

            if different_date.days < 30:
                current_month = True

        self.dict_url[self.cache_url] = {
                'time': matches[0],
                'current': current_month,
        }

        
    def iter_urls(self):
        try:
            for url in self.url_list:
                self.cache_url = url
                soup_first = self.__request_soup(self.cache_url)
                url = self.__collect_url_search(soup_first)
                if url:
                    soup_second = self.__request_soup(url, False)
                if soup_second:
                    self.__collect_element(soup_second)
        except:
            self.get_dict_urls()



        self.browser.close()

    def get_dict_urls(self):
        super().save_json(self.dict_url, 'yandex')
        return self.dict_url