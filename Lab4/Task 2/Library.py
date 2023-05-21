from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableView, QVBoxLayout, QInputDialog, \
    QMessageBox
from PyQt5.QtCore import pyqtSignal
import sqlalchemy as db
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.orm import Session, sessionmaker
import sys
import uuid
import hashlib
import json
import xml.etree.ElementTree as ET
import re
import sqlite3

#________________________________________________________________________________________#

class LibraryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Library.ui", self)
        self.addA = AuthorForm()
        self.addB = BookForm()
        self.actionAuthor.triggered.connect(self.open_addA)
        self.actionBook.triggered.connect(self.open_addB)
        self.actionjson.triggered.connect(self.save_json)
        self.actionXML.triggered.connect(self.save_XML)
        self.AuthorsBornInXY.clicked.connect(self.years_sort)
        self.AythorsWithNBooks.clicked.connect(self.book_sort)
        self.RussianBooks.clicked.connect(self.country_sort)
        self.CountPages.clicked.connect(self.pages_sort)
        self.addA.Author_data[str, str, str, str].connect(self.addAuthor)
        self.addB.Book_data[str, str, str, str, str].connect(self.addBook)
        self.listAuthors.clear()

        db = sqlite3.connect('Lab-database.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM author")
        for i in cursor.fetchall():
            self.listAuthors.addItem(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}")

        cursor.execute("SELECT * FROM books")
        for i in cursor.fetchall():
            self.listBook.addItem(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}")
        db.commit()
        cursor.close()

    def addAuthor(self, idA, name, country, years):
        self.listAuthors.clear()
        db = sqlite3.connect('Lab-database.db')
        cursor = db.cursor()
        sqlite_insert_with_param = """INSERT INTO author
                                                  (idAuthor, name, country, years)
                                                  VALUES (?, ?, ?, ?);"""
        data_tuple = (idA, name, country, years)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        cursor.execute("SELECT * FROM author")
        for i in cursor.fetchall():
            self.listAuthors.addItem(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}")
        db.commit()
        cursor.close()

    def addBook(self, idB, name, size, publishing, year):
        self.listAuthors.clear()
        db = sqlite3.connect('Lab-database.db')
        cursor = db.cursor()
        sqlite_insert_with_param = """INSERT INTO books
                                          (idAuthor, name, size, publishing, yearsPublishing)
                                          VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (idB, name, size, publishing, year)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        cursor.execute("SELECT * FROM books")
        for i in cursor.fetchall():
            self.listBook.addItem(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}")
        db.commit()
        cursor.close()

    def open_addA(self):
        self.addA.show()

    def open_addB(self):
        self.addB.show()

    def open_Auth(self):
        self.Auth.show()
        self.close()

    def save_json(self):
        data = self.listAuthors.currentItem().text().split()
        author = {
            "Name": data[1] + data[2],
            "Country" : data[3],
            "Years": data[4]
        }
        with open('my.json', 'a') as file:
            json.dump(author, file, indent=2)

    def save_XML(self):
        data = self.listAuthors.currentItem().text().split()
        author = ET.Element('author')
        s_elem1 = ET.SubElement(author, 'Name')
        s_elem2 = ET.SubElement(author, 'Country')
        s_elem3 = ET.SubElement(author, 'Year')
        s_elem1.text = data[1] + data[2]
        s_elem2.text = data[3]
        s_elem3.text = data[4]
        b_xml = ET.tostring(author)
        with open("my.xml", "ab") as f:
            f.write(b_xml)

    def years_sort(self):
        self.listAuthors.clear()
        db = sqlite3.connect('Lab-database.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM author")
        for i in cursor.fetchall():
            if(int(f"{i[3]}".split(':')[0]) >= 1800 and int(f"{i[3]}".split(':')[0]) <= 1890):
                self.listAuthors.addItem(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}")
        db.commit()
        cursor.close()

    def book_sort(self):
        self.listBook.clear()
        db = sqlite3.connect('Lab-database.db')
        cursor_1 = db.cursor()
        cursor_1.execute("SELECT * FROM author")
        cursor_2 = db.cursor()
        cursor_2.execute("SELECT * FROM books")
        countBooks = 0;
        for i in cursor_1.fetchall():
            countBooks = 0
            for j in cursor_2.fetchall():
                if i[0] == j[0]:
                    countBooks += 1
                if countBooks > 5:
                    self.listBook.addItem(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}")
                    countBooks = 0
        db.commit()
        cursor_1.close()
        cursor_2.close()

    def country_sort(self):
        self.listBook.clear()
        db = sqlite3.connect('Lab-database.db')
        cursor_1 = db.cursor()
        cursor_1.execute("SELECT * FROM author")
        cursor_2 = db.cursor()
        cursor_2.execute("SELECT * FROM books")
        for i in cursor_1.fetchall():
            if i[2] == "Россия":
                for j in cursor_2.fetchall():
                    if i[0] == j[0]:
                        self.listBook.addItem(f"{j[0]}\t{j[1]}\t{j[2]}\t{j[3]}\t{j[4]}")
        db.commit()
        cursor_1.close()
        cursor_2.close()

    def pages_sort(self):
        self.listBook.clear()
        db = sqlite3.connect('Lab-database.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM books")
        for i in cursor.fetchall():
            if int(i[2]) > 100:
                self.listBook.addItem(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}")
        db.commit()
        cursor.close()

    #________________________________________________________________________________________#

class AuthorForm(QMainWindow):
    Author_data = pyqtSignal(str, str, str, str)
    def __init__(self):
        super().__init__()
        uic.loadUi("AuthorForm.ui", self)
        self.pushAuthor.clicked.connect(self.send_data)

    def send_data(self):
        pattern = re.compile("\d{1,4}:\d{1,4}")
        if pattern.match(self.lineYears.text()):
            self.Author_data.emit(self.lineID.text(), self.lineName.text(), self.lineCountry.text(), self.lineYears.text())
            self.close()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Неверный формат ввода в поле "Годы жизни"')
            msg.setWindowTitle("Error")
            msg.exec_()

#________________________________________________________________________________________#

class BookForm(QMainWindow):
    Book_data = pyqtSignal(str, str, str, str, str)
    def __init__(self):
        super().__init__()
        uic.loadUi("BookForm.ui", self)
        self.pushBook.clicked.connect(self.send_data)

    def send_data(self):
        self.Book_data.emit(self.lineID.text(), self.lineName.text(), self.lineSize.text(), self.linePublic.text(), self.lineYear.text())
        self.close()

#___________________________________________________________________________________________#

class AuthorizationForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("AuthorizationForm.ui", self)
        self.Lib = LibraryWindow()
        self.pushIn.clicked.connect(self.make_Authorization)

    def make_Authorization(self):
        db = sqlite3.connect('Lab-database.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        openWindow = False
        for i in cursor.fetchall():
            if i[1] == self.lineLogin.text():
                if(i[2] == hashlib.sha1(f"{self.linePassword.text()}".encode()).hexdigest()):
                    self.Lib.show()
                    openWindow = True
                    self.close()
        if(openWindow == False):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Вы ввели неверые данные!')
            msg.setWindowTitle("Error")
            msg.exec_()
        db.commit()
        cursor.close()

#___________________________________________________________________________________________#

if __name__ == "__main__":
    Authoriz = QApplication(sys.argv)
    ex = AuthorizationForm()
    ex.show()
    sys.exit(Authoriz.exec())
