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
import pymongo

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

        db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        current_db = db_client["Lab-database"]
        collection = current_db["authors"]
        for i in collection.find():
            self.listAuthors.addItem(f"{i['idAuthor']}\t{i['name']}\t{i['country']}\t{i['years']}")

        collection = current_db["books"]
        for i in collection.find():
            self.listBook.addItem(f"{i['idAuthor']}\t{i['name']}\t{i['size']}\t{i['publishing']}\t{i['yearsPublishing']}")

    def addAuthor(self, idA, name, country, years):
        self.listAuthors.clear()
        db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        current_db = db_client["Lab-database"]
        collection = current_db["authors"]
        author = {
            'idAuthor': idA,
            'name': name,
            'country': country,
            'years': years
        }
        collection.insert_one(author)
        for i in collection.find():
            self.listAuthors.addItem(f"{i['idAuthor']}\t{i['name']}\t{i['country']}\t{i['years']}")

    def addBook(self, idB, name, size, publishing, year):
        self.listBook.clear()
        db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        current_db = db_client["Lab-database"]
        collection = current_db["books"]
        book = {
            'idAuthor': idB,
            'name': name,
            'size': size,
            'publishing': publishing,
            'yearsPublishing': year
        }
        collection.insert_one(book)
        for i in collection.find():
            self.listBook.addItem(
                f"{i['idAuthor']}\t{i['name']}\t{i['size']}\t{i['publishing']}\t{i['yearsPublishing']}")

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
        db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        current_db = db_client["Lab-database"]
        collection = current_db["authors"]
        for i in collection.find():
            if (int(f"{i['years']}".split(':')[0]) >= 1800 and int(f"{i['years']}".split(':')[0]) <= 1890):
                self.listAuthors.addItem(f"{i['idAuthor']}\t{i['name']}\t{i['country']}\t{i['years']}")

    def book_sort(self):
        self.listBook.clear()
        db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        current_db = db_client["Lab-database"]
        collectionA = current_db["authors"]
        collectionB = current_db["books"]
        count_books = 0
        for i in collectionA.find():
            for j in collectionB.find({'idAuthor': i['idAuthor']}):
                count_books += 1
            if count_books >= 5:
                self.listAuthors.addItem(f"{i['idAuthor']}\t{i['name']}\t{i['country']}\t{i['years']}")
            count_books = 0


    def country_sort(self):
        self.listBook.clear()
        db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        current_db = db_client["Lab-database"]
        collectionA = current_db["authors"]
        collectionB = current_db["books"]
        for i in collectionA.find({'country': 'Россия'}):
            for j in collectionB.find({'idAuthor': i['idAuthor']}):
                self.listBook.addItem(
                    f"{j['idAuthor']}\t{j['name']}\t{j['size']}\t{j['publishing']}\t{j['yearsPublishing']}")

    def pages_sort(self):
        self.listBook.clear()
        db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        current_db = db_client["Lab-database"]
        collection = current_db["books"]
        for i in collection.find():
            if int(i['size']) >= 100:
                self.listBook.addItem(
                    f"{i['idAuthor']}\t{i['name']}\t{i['size']}\t{i['publishing']}\t{i['yearsPublishing']}")

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
        db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        current_db = db_client["Lab-database"]
        collection = current_db["users"]
        openWindow = collection.find_one({'login': self.lineLogin.text(), 'password': hashlib.sha1(f"{self.linePassword.text()}".encode()).hexdigest()})

        if(openWindow == None):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Вы ввели неверые данные!')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self.Lib.show()
            self.close()

#___________________________________________________________________________________________#

if __name__ == "__main__":
    Authoriz = QApplication(sys.argv)
    ex = AuthorizationForm()
    ex.show()
    sys.exit(Authoriz.exec())
