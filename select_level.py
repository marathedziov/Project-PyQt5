import os

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QAction, QTextBrowser, QWidget, QVBoxLayout, \
    QTableWidget, QTableWidgetItem
from PyQt5 import QtGui, QtCore

from my_window import MyWindow
from my_second_window import MySecondWindow


class LeaderboardDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))
        self.setWindowTitle('Список лидеров')
        self.setGeometry(300, 100, 650, 450)
        self.setFixedSize(650, 450)
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('DataBase.sqlite')
        db.open()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Name", "Points LVL 1", "Points LVL 2"])
        table.setColumnWidth(0, 400)

        query = QSqlQuery(db)
        query.prepare("SELECT name, points, points2 FROM users ORDER BY (points + points2) DESC")
        query.exec_()

        row = 0
        while query.next():
            name = query.value(0)
            points = query.value(1)
            points2 = query.value(2)

            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(str(points)))
            table.setItem(row, 2, QTableWidgetItem(str(points2)))

            row += 1

        layout.addWidget(table, 1)
        self.setLayout(layout)


class SelectLevel(QMainWindow):
    def __init__(self, id_ak):
        super().__init__()
        self.id_ak = id_ak
        self.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))
        self.initUI()
        self.about_dialog = None

    def initUI(self):
        self.setWindowTitle("Окно выбора уровня")
        self.setGeometry(450, 200, 1020, 600)
        self.setFixedSize(1020, 600)

        menubar = self.menuBar()

        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.showAboutDialog)
        menubar.addAction(about_action)

        leaderboard_action = QAction("Список лидеров", self)
        leaderboard_action.triggered.connect(self.showLeaderboard)
        menubar.addAction(leaderboard_action)

        image_label = QLabel(self)
        pixmap = QtGui.QPixmap(os.path.join('pictures', 'r1.png'))
        image_label.setPixmap(pixmap)
        image_label.setGeometry(455, 35, 540, 540)

        image_label2 = QLabel(self)
        pixmap = QtGui.QPixmap(os.path.join('pictures', 'Vector.png'))
        image_label2.setPixmap(pixmap)
        image_label2.setGeometry(5, 310, 300, 300)

        label = QLabel("Выберите уровень", self)
        label.setGeometry(25, 120, 400, 60)
        label.setAlignment(QtCore.Qt.AlignCenter)
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(25)
        font.setBold(True)
        label.setFont(font)

        first_button = QPushButton("Первый уровень", self)
        first_button.setGeometry(85, 200, 285, 40)
        first_button.setStyleSheet(
            f"QPushButton{{border-image: url('pictures/Rectangle2.png');}}")
        first_button.clicked.connect(self.startFirstGame)
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(14)
        font.setBold(True)
        first_button.setFont(font)

        second_button = QPushButton("Второй уровень", self)
        second_button.setGeometry(85, 260, 285, 40)
        second_button.setStyleSheet(
            f"QPushButton{{border-image: url('pictures/Rectangle2.png');}}")
        second_button.clicked.connect(self.startSecondGame)
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(14)
        font.setBold(True)
        second_button.setFont(font)

    def showAboutDialog(self):
        if not self.about_dialog:
            self.about_dialog = QTextBrowser()
            self.about_dialog.setWindowTitle("О программе")
            self.about_dialog.setGeometry(300, 100, 650, 450)
            self.about_dialog.setFixedSize(650, 450)
            self.about_dialog.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))
            text = open('file.txt', 'r', encoding='utf-8').read()
            self.about_dialog.setPlainText(text)
            font = QFont()
            font.setFamily("VAG World")
            font.setPointSize(11)
            font.setBold(True)
            self.about_dialog.setFont(font)
        self.about_dialog.show()

    def showLeaderboard(self):
        self.leaderboard_dialog = LeaderboardDialog()
        self.leaderboard_dialog.show()

    def startFirstGame(self):
        self.firs_level = MyWindow(self, self.id_ak)
        self.firs_level.show()
        self.close()

    def startSecondGame(self):
        self.second_level = MySecondWindow(self, self.id_ak)
        self.second_level.show()
        self.close()
