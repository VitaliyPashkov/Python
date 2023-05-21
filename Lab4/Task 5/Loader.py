import urllib

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import threading
import requests
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os


# https://puzzleit.ru/files/puzzles/246/246151/_original.jpg
# https://slovnet.ru/wp-content/uploads/2018/11/21-42.jpg
# https://phonoteka.org/uploads/posts/2021-07/1625696792_1-phonoteka-org-p-spanch-bob-art-krasivo-1.jpg

class Loader(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("DownloadForm.ui", self)
        self.progressBar.setValue(0)
        self.progressBar_2.setValue(0)
        self.progressBar_3.setValue(0)
        self.Start.clicked.connect(self.download)
        self.lineEdit.setText("https://puzzleit.ru/files/puzzles/246/246151/_original.jpg")
        self.lineEdit_2.setText("https://slovnet.ru/wp-content/uploads/2018/11/21-42.jpg")
        self.lineEdit_3.setText("https://phonoteka.org/uploads/posts/2021-07/1625696792_1-phonoteka-org-p-spanch-bob-art-krasivo-1.jpg")

    def download(self):
        a = datetime.datetime.now()
        t1 = threading.Thread(target=self.starting, args=(self.lineEdit.text(), 1))
        t1.start()
        t1.join()
        self.progressBar.setValue(100)
        b = datetime.datetime.now()
        c1 = (b-a).total_seconds()
        a = datetime.datetime.now()
        t2 = threading.Thread(target=self.starting, args=(self.lineEdit_2.text(), 2))
        t2.start()
        t2.join()
        self.progressBar_2.setValue(100)
        b = datetime.datetime.now()
        c2 = (b-a).total_seconds()
        a = datetime.datetime.now()
        t3 = threading.Thread(target=self.starting, args=(self.lineEdit_3.text(), 3))
        t3.start()
        t3.join()
        self.progressBar_3.setValue(100)
        b = datetime.datetime.now()
        c3 = (b-a).total_seconds()
        x = [self.lineEdit.text().split('/')[-1], self.lineEdit_2.text().split('/')[-1], self.lineEdit_3.text().split('/')[-1]]
        y = [c1, c2, c3]
        f, ax = plt.subplots(1, 2)
        f.set_size_inches(7, 4)
        f.set_facecolor("#eee")
        ax[0].bar(x, y)
        ax[0].grid()
        files = [self.lineEdit.text().split('/')[-1], self.lineEdit_2.text().split('/')[-1], self.lineEdit_3.text().split('/')[-1]]
        sizes = [os.path.getsize(files[0]), os.path.getsize(files[1]), os.path.getsize(files[2])]
        ax[1].pie(sizes, labels=files)
        ax[1].grid()
        plt.show()

    def starting(self, url, numProgressBar):
        local_filename = url.split('/')[-1]
        i = 0
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    f.write(chunk)
                    i += 2
                    if(numProgressBar == 1):
                        self.progressBar.setValue(i)
                    elif(numProgressBar == 2):
                        self.progressBar_2.setValue(i)
                    else:
                        self.progressBar_3.setValue(i)
        return local_filename


if __name__ == "__main__":
    load = QApplication(sys.argv)
    ex = Loader()
    ex.show()
    sys.exit(load.exec())