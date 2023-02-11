
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver

from datetime import datetime


class MainBot():

    def __init__(self, bd: object):
        self.bd = bd
        self.date_now = datetime.now()


    def setup_browser(self):
        """
        Стартует браузер в дочерних ботах
        """
        # options = webdriver.ChromeOptions()
        # options.add_extension('anticaptcha-plugin_v0.63.zip')

        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "eager"

        service = Service(executable_path='chromedriver/chromedriver.exe')
        browser = webdriver.Chrome(service=service, desired_capabilities=capa)

        return browser


    def setup_date_now(self):
        """
        Дата записывается только здесь, указателем передаётся в дочерний бот
        """
        return self.date_now


    def get_url(self):
        return self.bd.select_checked_url()


    def update_result(self, url, bot, data):
        self.bd.add_result(url, bot, data)


    def get_all(self):
        return self.bd.select_all()

