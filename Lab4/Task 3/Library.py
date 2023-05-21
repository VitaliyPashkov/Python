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
from createBase import Author, User, Book, Base

#________________________________________________________________________________________#

class LibraryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Library.ui", self)
        self.addA = AuthorForm()
        self.addB = BookForm()
        self.actionCreate.triggered.connect(self.createBase)
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
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.commit()
        for i in session.query(Author).all():
            self.listAuthors.addItem(f"{i.idAuthor}\t{i.name}\t{i.country}\t{i.years}")
        for i in session.query(Book).all():
            self.listBook.addItem(f"{i.idAuthor}\t{i.name}\t{i.size}\t{i.Publishing}\t{i.yearsPublishing}")

    def createBase(self):
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        user = User(Login="Никита", Password=hashlib.sha1(b'123').hexdigest())
        session.add(user)
        session.commit()

    def addAuthor(self, idA, name, country, years):
        self.listAuthors.clear()
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        author = Author(idAuthor=idA, name=name, country=country, years=years)
        session.add(author)
        session.commit()
        for i in session.query(Author).all():
            self.listAuthors.addItem(f"{i.idAuthor}\t{i.name}\t{i.country}\t{i.years}")

    def addBook(self, idB, name, size, publishing, year):
        self.listBook.clear()
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        book = Book(idAuthor=idB, name=name, size=size, Publishing=publishing, yearsPublishing=year)
        session.add(book)
        session.commit()
        for i in session.query(Book).all():
            self.listBook.addItem(f"{i.idAuthor}\t{i.name}\t{i.size}\t{i.Publishing}\t{i.yearsPublishing}")

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
            "Name": data[1],
            "Country" : data[2],
            "Years": data[3]
        }
        with open('my.json', 'a') as file:
            json.dump(author, file, indent=2)

    def save_XML(self):
        data = self.listAuthors.currentItem().text().split()
        author = ET.Element('author')
        s_elem1 = ET.SubElement(author, 'Name')
        s_elem2 = ET.SubElement(author, 'Country')
        s_elem3 = ET.SubElement(author, 'Year')
        s_elem1.text = data[1]
        s_elem2.text = data[2]
        s_elem3.text = data[3]
        b_xml = ET.tostring(author)
        with open("my.xml", "ab") as f:
            f.write(b_xml)

    def years_sort(self):
        self.listAuthors.clear()
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.commit()
        for i in session.query(Author).all():
            if(int(f"{i.years}".split(':')[0]) >= 1800 and int(f"{i.years}".split(':')[0]) <= 1890):
                self.listAuthors.addItem(f"{i.idAuthor}\t{i.name}\t{i.country}\t{i.years}")

    def book_sort(self):
        self.listBook.clear()
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.commit()
        countBooks = 0;
        for i in session.query(Author).all():
            countBooks = 0
            for j in session.query(Book).all():
                if i.idAuthor == j.idAuthor:
                    countBooks += 1
                if countBooks > 5:
                    self.listAuthors.addItem(f"{i.idAuthor}\t{i.name}\t{i.country}\t{i.years}")
                    countBooks = 0

    def country_sort(self):
        self.listBook.clear()
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.commit()
        for i in session.query(Author).all():
            if(i.country == "Россия"):
                for j in session.query(Book).all():
                    if i.idAuthor == j.idAuthor:
                        self.listBook.addItem(f"{j.idAuthor}\t{j.name}\t{j.size}\t{j.Publishing}\t{j.yearsPublishing}")

    def pages_sort(self):
        self.listBook.clear()
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.commit()
        for i in session.query(Book).all():
            if int(i.size) > 100:
                self.listBook.addItem(f"{i.idAuthor}\t{i.name}\t{i.size}\t{i.Publishing}\t{i.yearsPublishing}")

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
        engine = db.create_engine('sqlite:///Lib-collection.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.commit()
        openWindow = False
        for i in session.query(User).all():
            if i.Login == self.lineLogin.text() and i.Password == hashlib.sha1(f"{self.linePassword.text()}".encode()).hexdigest():
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

#___________________________________________________________________________________________#

if __name__ == "__main__":
    Authoriz = QApplication(sys.argv)
    ex = AuthorizationForm()
    ex.show()
    sys.exit(Authoriz.exec())
