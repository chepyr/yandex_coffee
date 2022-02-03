import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget

DATABASE = sqlite3.connect('coffee.db')
CURSOR = DATABASE.cursor()


class AddEditWindow(QWidget):
    def __init__(self, info=None, parent_window=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.info = info
        if info is None:
            self.info = ['' for i in range(7)]
        self.init_ui()
        self.pushButton.clicked.connect(self.save)
        self.parent_window = parent_window

    def init_ui(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Информация о кофе')
        self.setLayout(self.gridLayout)
        self.line_edits = [self.lineEdit, self.lineEdit_2, self.lineEdit_3,
                           self.lineEdit_4, self.textEdit, self.lineEdit_6, self.lineEdit_7]
        for i in range(len(self.line_edits)):
            self.line_edits[i].setText(str(self.info[i]))

    def save(self):
        CURSOR.execute(f"""DELETE from coffee WHERE ID = '{self.info[0]}'""")
        for line_edit_num in range(len(self.line_edits)):
            line_edit = self.line_edits[line_edit_num]
            if line_edit == self.textEdit:
                text = line_edit.toPlainText()
            else:
                text = line_edit.text()
            self.info[line_edit_num] = text
        data = [self.info[i] for i in range(7)]
        CURSOR.execute(f"""INSERT INTO coffee VALUES({data[0]}, '{data[1]}', '{data[2]}',
        '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}')""")
        DATABASE.commit()

        if self.parent_window is not None:
            self.parent_window.update_info()

        self.close()


class CoffeeWindow(QWidget):
    def __init__(self, info=None, parent_window=None):
        super().__init__()
        uic.loadUi('about.ui', self)
        self.pushButton.clicked.connect(self.edit_coffee)
        self.info = list(info)
        self.align_text()
        self.init_about_ui()
        self.parent_window = parent_window

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

    def edit_coffee(self):
        self.edit_window = AddEditWindow(info=self.info, parent_window=self.parent_window)
        self.edit_window.show()
        self.close()

    def init_about_ui(self):
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
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Каталог кофе')
        self.setLayout(self.verticalLayout)
        self.listWidget.itemClicked.connect(self.clicked)

        self.load_table()
        self.pushButton.clicked.connect(self.add_new_item)

    def add_new_item(self):
        self.add_coffee_window = AddEditWindow(parent_window=self)
        self.add_coffee_window.show()

    def load_table(self):
        self.listWidget.clear()
        data = CURSOR.execute(f'''SELECT * from coffee''').fetchall()

        self.coffee_list = dict()
        for i in range(len(data)):
            info = data[i]
            name = info[1]
            self.coffee_list[name] = info
            item = QListWidgetItem(name)
            self.listWidget.addItem(item)

    def update_info(self):
        self.load_table()

    def clicked(self):
        name = self.sender().currentItem().text()
        info = self.coffee_list[name]
        self.coffee_window = CoffeeWindow(info=info, parent_window=self)
        self.coffee_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())
