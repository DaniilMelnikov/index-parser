# **Парсер индексации страниц**


## Задача
1. Написать автоматизированную программу, которая будет проверять индексацию страниц.
2. Помечать поле в excel файле зелёным цветом, если 
````сегодняшняя_дата - дата_сохранённой_страницы < 30````
, иначе красным.
3. Автоматизировать решение капчи Yandex и Google.

## Установка
Чтобы пользоваться программой нужно сделать несколько манипуляций:
1. Установить Python минимум 3.9.13.
2. Установить библиотеку для виртуального окружения
````
pip install virtualenv
 ````
3. Открыть cmd на правах администратора.
4. Перейти в папку, куда скачали проект, например:
````
cd C:\Users\user_name\Desktop\my_project
````
5. Создать папку виртуального окружения
````
python -m  venv name-env
````
где ````name-env```` название будщей папки виртуального окружения

6. Запустить виртуальное окружение (можно запустить cmd в VScode) 
````
name-env\Scripts\activate
````
должна появиться такая строчка:
````
(name-env) C:\User\my_name\Desktop\my_project>
````
7. Установить зависимости проекта
````
pip install -r requirements.txt
````
Могут появиться ошибки, вручную pip'аем зависимости с ошибками.

8. Качаем webdriver для Chrome.

Смотрим версию Chrome браузера в справках
![Версия браузера](/img-readme/chrome-version.png)

Качаем драйвер подходящая нашей версии
[Скачать WebdriverChrome](https://chromedriver.chromium.org/downloads)

9. Извлекаем драйвер в папку ````chromedriver````.

10. В файле .env в директории проекта заполняем переменную SECRET_KEY ключом AntiCaptcha.

11. Запускаем программу.
````
python parser_sdata.py
````


## Как использовать?

1. Нужно создать excel файл с урлами начало поле B2 и заполняем ниже столбик: B3, B4, B5, ..., Bn.
![Пример Excel](/img-readme/example-excel.png)

Проблема решается, подробнее в [Смотреть issue](https://github.com/DaniilMelnikov/index-parser/issues/1)

2. Далее указать в окне программы путь до файла.

3. Программа сама всё сделает, лишь иногда нужно решать капчу.

Можно написать файл test.py в корне проекта:

````
from models.url_model import UrlModel
from bots.google_bot import GoogleBot
from bots.yandex_bot import YandexBot

#Поместите здесь свои urls для проверки
urls= [


]

#Создаём бд
url_bd = UrlModel('test')

#Заполняем таблицу урлами
url_bd.load_url(urls)

#Создаём гугл бота
google_bot = GoogleBot(url_bd)

#Запускаем итерацию
google_bot.iter_urls()

#Создаём яндекс бота
yandex_bot = YandexBot(url_bd)

#Запускаем итерацию
yandex_bot.iter_urls()

````