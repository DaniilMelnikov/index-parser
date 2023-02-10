from PyQt5 import QtWidgets
from google_bot import GoogleBot
from ui_main import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QFileDialog
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

from yandex_bot import YandexBot


class main_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.setupUi(self)
        self.file_change.clicked.connect(self.openFileNameDialog)
        self.push_go.clicked.connect(self.startParser)
        self.setWindowTitle('Приложение')

        self.sheet_cache = object()
        self.url_listChache = []

    def startParser(self):
        url_book = self.file_url.text()
        book = load_workbook(url_book)
        self.sheet_cache = book.active
        for row in range(self.sheet_cache.max_row):
            self.url_listChache.append(self.sheet_cache[f'B{row+2}'].value)

        google_bot = GoogleBot(self.url_listChache)
        google_bot.iter_urls()
        result_google = google_bot.get_dict_urls()

        yandex_bot = YandexBot(self.url_listChache)
        yandex_bot.iter_urls()
        result_yandex = yandex_bot.get_dict_urls()

        self.__fillResult(result_google, 'D')
        self.__fillResult(result_yandex, 'E')
        
        book.save('test.xlsx')

    def __fillResult(self, result, str_column=None):
        true_fill = PatternFill('solid', fgColor='0000FF00')
        false_fill = PatternFill('solid', fgColor='00FF0000')
        for id, row in enumerate(range(self.sheet_cache.max_row)):
            self.sheet_cache[f'{str_column}{row+1}'].value = result[self.url_listChache[id]]['time']
            if result[self.url_listChache[id]]['current']:
                self.sheet_cache[f'{str_column}{row+1}'].fill = true_fill
            else:
                self.sheet_cache[f'{str_column}{row+1}'].fill = false_fill
            
    #Один файл
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.file_url.setText(fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    
app = QtWidgets.QApplication([])
application = main_window()
application.show()

 
sys.exit(app.exec())
