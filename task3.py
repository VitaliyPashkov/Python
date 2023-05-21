import sys  # sys нужен для передачи argv в QApplication
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic.properties import QtGui, QtCore
import datetime
from datetime import datetime
import design2
import re
import glob
#task 4
#

# Ввод имени файла с клавиатуры
def filter_task(filename):
    # task 4
    # Открываем файл на чтение
    with open(filename, 'r') as file:
        # Читаем содержимое файла в строку
        file_contents = file.read()

    # Определяем регулярное выражение для поиска дат
    date_regex = r'\d{2}-\d{2}-\d{4}'

    # Ищем все подстроки, удовлетворяющие регулярному выражению
    matches = re.findall(date_regex, file_contents)
    result = []
    # Выводим результаты на экран
    for match in matches:
        # Определяем позицию найденной подстроки
        match_pos = file_contents.find(match)

        # Определяем номер строки, в которой находится найденная подстрока
        line_num = file_contents.count('\n', 0, match_pos) + 1

        # Выводим результаты на экран
        result.append("Строка " + str(line_num) + ", позиция " + str(
            match_pos - file_contents.rfind('\n', 0, match_pos)) + ": найдено " + repr(match))
    return result

class ExampleApp(QtWidgets.QMainWindow, design2.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)

        self.action.triggered.connect(self.fileOpen)
        self.action_2.triggered.connect(self.logExport)
        self.action_3.triggered.connect(self.logAdd)
        self.action_4.triggered.connect(self.logShow)
        if not glob.glob(r'script18.log'):
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            msg.setText('Файл лога не найден. Файл будет создан автоматически кнопкой ОК')
            returnValue = msg.exec()
            if returnValue == QMessageBox.Ok:
                open('script18.log', 'w+')

    def fileOpen(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", None, "Text (*.txt)")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        print(file)
        if file:  # не продолжать выполнение, если пользователь не выбрал директорию
            now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            self.listWidget.addItem(f"Файл {file[0]} был обработан {now}\n")
            self.listWidget.addItems(filter_task("task 4.txt"))
            self.listWidget.addItem('')
            self.label_1 = QtWidgets.QLabel(f'{os.path.getsize(file[0])} байт\t\t\t\t')
            self.statusBar().addPermanentWidget(self.label_1)
            self.statusBar().showMessage(f"Обработан файл {file[0]}")

    def logExport(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", None, "Log files (*.log)")
        with open('script18.log', 'a') as f:
            for x in range(self.listWidget.count()):
                f.write(self.listWidget.item(x).text()+'\n')

    def logAdd(self):
        with open('script18.log', 'a') as f:
            for x in range(self.listWidget.count()):
                f.write(self.listWidget.item(x).text()+'\n')


    def logShow(self):
        msg = QMessageBox()
        msg.setWindowTitle("Внимание!")
        msg.setText('Вы действительно хотите открыть лог? Данные последних поисков будут потеряны!')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = msg.exec()
        if returnValue == QMessageBox.Yes:
            self.statusBar().showMessage(f"Открыт лог")
            print(sum(1 for line in open('script18.log')))
            self.listWidget.clear()
            with open('script18.log', 'r') as f:
                self.listWidget.addItems(f.readlines())


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  #

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

