import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design


class StringFormatter:
    def __init__(self, text):
        self.text = text

    def remove_short_words(self, n):
        words = self.text.split()
        filtered_words = [word for word in words if len(word) >= n]
        self.text = ' '.join(filtered_words)

    def replace_digits(self):
        self.text = ''.join(['*' if char.isdigit() else char for char in self.text])

    def insert_spaces(self):
        self.text = ' '.join(list(self.text))

    def sort_by_length(self):
        words = self.text.split()
        sorted_words = sorted(words, key=lambda x: len(x))
        self.text = ' '.join(sorted_words)

    def sort_lexicographically(self):
        words = self.text.split()
        sorted_words = sorted(words)
        self.text = ' '.join(sorted_words)


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow, StringFormatter):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.pushButton.released.connect(self.press_button)
        self.checkBox_4.stateChanged.connect(self.check_box_is_checked)

    def press_button(self):
        formatter = StringFormatter(self.lineEdit_2.text())
        if (self.checkBox.isChecked()):
            formatter.remove_short_words(int(self.spinBox.text()))
        if (self.checkBox_2.isChecked()):
            formatter.replace_digits()
        if (self.checkBox_3.isChecked()):
            formatter.insert_spaces()
        if (self.checkBox_4.isChecked()):
            if (self.radioButton.isChecked()):
                formatter.sort_by_length()
            elif (self.radioButton_2.isChecked()):
                formatter.sort_lexicographically()
        self.lineEdit.setText(formatter.text)

    def check_box_is_checked(self, state):
        if state:
            self.radioButton.setEnabled(True)
            self.radioButton_2.setEnabled(True)
        else:
            self.radioButton.setEnabled(False)
            self.radioButton_2.setEnabled(False)







def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  #

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
