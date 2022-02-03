import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget


class CoffeeWindow(QWidget):
    def __init__(self, *info):
        super().__init__()
        uic.loadUi('about.ui', self)
        self.info = list(*info)
        self.align_text()

        self.init_ui()

    def align_text(self):
        text = self.info[4]
        new_text = ['']
        if text:
            text = text.split()
            for word in text:
                new_text[-1] += ' ' + word
                if len(new_text[-1]) > 40:
                    new_text.append('')
        self.info[4] = '\n'.join(new_text)

    def init_ui(self):
        self.setGeometry(300, 300, 250, 400)
        self.setWindowTitle('Информация о кофе')
        self.setLayout(self.gridLayout)
        labels = [self.label_2, self.label_4, self.label_6,
                  self.label_8, self.label_10, self.label_12, self.label_14]
        for i in range(len(labels)):
            labels[i].setText(str(self.info[i]))


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.init_ui()

    def init_ui(self):
        self.db = sqlite3.connect('coffee.db')
        self.cur = self.db.cursor()

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Каталог кофе')
        self.setLayout(self.verticalLayout)
        self.listWidget.itemClicked.connect(self.clicked)

        self.load_table()

    def load_table(self):
        self.listWidget.clear()
        data = self.cur.execute(f'''SELECT * from coffee''').fetchall()

        self.coffee_list = dict()
        for i in range(len(data)):
            info = data[i]
            name = info[1]
            self.coffee_list[name] = info
            item = QListWidgetItem(name)
            self.listWidget.addItem(item)

    def clicked(self):
        name = self.sender().currentItem().text()
        info = self.coffee_list[name]
        self.coffee_window = CoffeeWindow(info)
        self.coffee_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())
