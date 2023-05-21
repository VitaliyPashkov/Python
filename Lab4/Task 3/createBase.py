import sys
import hashlib

# для настройки баз данных
from sqlalchemy import Column, ForeignKey, Integer, String

# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base

# для создания отношений между таблицами
from sqlalchemy.orm import relationship

# для настроек
from sqlalchemy import create_engine

# создание экземпляра declarative_base
Base = declarative_base()

# здесь добавим классы
class Author(Base):
    __tablename__ = 'Author'

    id = Column(Integer, primary_key=True)
    idAuthor = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    country = Column(String(250), nullable=False)
    years = Column(String(250))

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, country: {self.country}, years: {self.years}'

class Book(Base):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True)
    idAuthor = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    size = Column(String(250), nullable=False)
    Publishing = Column(String(250), nullable=False)
    yearsPublishing = Column(String(250))

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    Login = Column(String(250), nullable=False)
    Password = Column(String(250), nullable=False)

# создает экземпляр create_engine в конце файла
engine = create_engine('sqlite:///Lib-collection.db')

Base.metadata.create_all(engine)
