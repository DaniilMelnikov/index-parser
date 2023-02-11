from typing import Any, Dict, List

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver

from datetime import datetime

import json



class MainBot():
    def __init__(self, url_list: List[str]):
        self.url_list = url_list

        # options = webdriver.ChromeOptions()
        # options.add_extension('anticaptcha-plugin_v0.63.zip')

        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "eager"

        service = Service(executable_path='chromedriver/chromedriver.exe')
        self.browser = webdriver.Chrome(service=service, desired_capabilities=capa)

        self.date_now = datetime.now()


    def setup_browser(self):
        """
        Стартует браузер в дочерних ботах
        """
        return self.browser


    def setup_date_now(self):
        """
        Дата записывается только здесь, указателем передаётся в дочерний бот
        """
        return self.date_now


    def save_json(self, data :Dict[str, Any], bots: str):
        """
        Сохраняет пройденный путь ботами
        """
        with open(f'bots\\data\\{bots}.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)


    def write_json(self, bots: str) -> Dict[str, Any]:
        """
        Записывает обратно сохранённые при ошибке данные
        """
        with open(f'bots\\data\\{bots}.json') as json_file:
            data = json.load(json_file)
            if data:
                dict_url = {}
                count = 0
                for url in data:
                    count += 1
                    dict_url[url] = {
                        'time': data[url]['time'],
                        'current': data[url]['current'],
                    }
                self.url_list = self.url_list[count:]
            return dict_url
