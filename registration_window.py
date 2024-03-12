import os
import sqlite3

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QColor, QPalette, QFont, QIcon
from PyQt5 import QtGui
from PyQt5 import QtCore

from select_level import SelectLevel


class RegistrationWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))

        self.setWindowTitle('Окно регистрации')
        self.login_window = login_window
        self.setGeometry(450, 200, 1020, 600)
        self.setFixedSize(1020, 600)

        self.count_clicks = 0

        background_label = QLabel(self)
        background_pixmap = QPixmap(os.path.join('pictures', 'Задний фон.jpg'))
        background_label.setPixmap(background_pixmap)
        background_label.setGeometry(0, 0, 1020, 600)

        self.name_label = QLabel(self)
        self.name_label_text = "Уæ бон хорз!"
        self.name_label.setText(self.name_label_text)
        self.name_label.setGeometry(330, 235, 360, 40)
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setStyleSheet("color: orange;")

        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(380, 285, 260, 30)
        self.current_placeholder_text = "Ном"
        self.name_input.setPlaceholderText(self.current_placeholder_text)
        self.name_input.setFont(QFont("VAG World", 14))
        self.name_input.setAlignment(QtCore.Qt.AlignCenter)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(380, 325, 260, 30)
        self.current_password_placeholder_text = "Сусæг дзырд"
        self.password_input.setPlaceholderText(self.current_password_placeholder_text)
        self.password_input.setFont(QFont("VAG World", 14))
        self.password_input.setAlignment(QtCore.Qt.AlignCenter)

        self.password_input2 = QLineEdit(self)
        self.password_input2.setEchoMode(QLineEdit.Password)
        self.password_input2.setGeometry(380, 365, 260, 30)
        self.current_password_placeholder_text2 = "Сбæлвырд кæнын"
        self.password_input2.setPlaceholderText(self.current_password_placeholder_text2)
        self.password_input2.setFont(QFont("VAG World", 14))
        self.password_input2.setAlignment(QtCore.Qt.AlignCenter)

        self.current_text_register_button = "Регистраци скæнын"
        self.register_button = QPushButton(self)
        self.register_button.setText(self.current_text_register_button)
        self.register_button.setGeometry(380, 415, 260, 35)
        self.register_button.setStyleSheet(
            f"QPushButton{{border-image: url('pictures/Rectangle3.png'); color: white;}}")
        self.register_button.clicked.connect(self.register)

        self.current_text_open_login_button = "Фæстæмæ"
        self.open_login_button = QPushButton(self)
        self.open_login_button.setText(self.current_text_open_login_button)
        self.open_login_button.setGeometry(380, 460, 260, 35)
        self.open_login_button.setStyleSheet(
            f"QPushButton{{border-image: url('pictures/Rectangle3.png'); color: white;}}")
        self.open_login_button.clicked.connect(self.startLoginWindow)

        font = QFont()
        font2 = QFont()
        font.setFamily("VAG World")
        font2.setFamily("VAG World")
        font.setPointSize(12)
        font2.setPointSize(24)
        font.setBold(True)
        font2.setBold(True)
        self.register_button.setFont(font)
        self.open_login_button.setFont(font)
        self.name_label.setFont(font2)

        self.name_input.textChanged.connect(self.update_background)
        self.password_input.textChanged.connect(self.update_background)
        self.password_input2.textChanged.connect(self.update_background)

        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(220, 220, 220))

        self.name_input.setPalette(palette)
        self.password_input.setPalette(palette)
        self.password_input2.setPalette(palette)

        self.conn = sqlite3.connect('DataBase.sqlite')
        self.cursor = self.conn.cursor()

        self.image_button = QPushButton(self)
        self.image_button.setGeometry(950, 15, 50, 50)
        self.current_image_image_button = "Russia.png"
        self.image_button.setIcon(QIcon(os.path.join('pictures', self.current_image_image_button)))
        self.image_button.setIconSize(QSize(50, 50))
        self.image_button.clicked.connect(self.change_image)
        self.image_button.setStyleSheet("background-color: transparent; border: none;")

    def change_image(self):
        self.count_clicks += 1
        if self.count_clicks % 2 == 0:
            self.current_image_image_button = "Russia.png"
            self.current_text_open_login_button = "Фæстæмæ"
            self.current_text_register_button = "Регистраци скæнын"
            self.current_password_placeholder_text = "Сусæг дзырд"
            self.current_password_placeholder_text2 = "Сбæлвырд кæнын"
            self.current_placeholder_text = "Ном"
            self.name_label_text = "Уæ бон хорз!"
        else:
            self.current_image_image_button = "Ossetia.png"
            self.current_text_open_login_button = "Назад"
            self.current_text_register_button = "Зарегистрировать"
            self.current_password_placeholder_text = "Пароль"
            self.current_password_placeholder_text2 = "Подтвердить пароль"
            self.current_placeholder_text = "Имя"
            self.name_label_text = "Добро пожаловать!"

        self.image_button.setIcon(QIcon(os.path.join('pictures', self.current_image_image_button)))
        self.open_login_button.setText(self.current_text_open_login_button)
        self.register_button.setText(self.current_text_register_button)
        self.name_label.setText(self.name_label_text)
        self.password_input.setPlaceholderText(self.current_password_placeholder_text)
        self.password_input2.setPlaceholderText(self.current_password_placeholder_text2)
        self.name_input.setPlaceholderText(self.current_placeholder_text)

    def update_background(self):
        if not self.name_input.text():
            self.name_input.setPlaceholderText(self.current_placeholder_text)
        else:
            self.name_input.setPlaceholderText("")

        if not self.password_input.text():
            self.password_input.setPlaceholderText(self.current_password_placeholder_text)
        else:
            self.password_input.setPlaceholderText("")

    def register(self):
        name = self.name_input.text()
        password = self.password_input.text()
        password2 = self.password_input2.text()

        if name and password and password2:
            self.cursor.execute('SELECT name FROM users WHERE name = ?', (name,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                QMessageBox.warning(self, 'Пользователь c зарегистрирован',
                                    'Пользователь с таким именем уже зарегистрирован.')
            else:
                if password == password2:
                    self.cursor.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, password))
                    self.conn.commit()
                    self.name_input.clear()
                    self.password_input.clear()
                    self.password_input2.clear()

                    self.cursor.execute('SELECT id, name FROM users WHERE name = ? AND password = ?', (name, password))
                    user_data = self.cursor.fetchone()
                    user_id, existing_user = user_data

                    QMessageBox.information(self, 'Регистрация успешна', f'Пользователь {name} зарегистрирован')

                    self.id_ak = user_id

                    self.startSelectLevel()
                    self.close()
                else:
                    QMessageBox.warning(self, 'Пароли не совпадают', 'Пожалуйста, убедитесь, что пароли идентичны.')
        else:
            QMessageBox.warning(self, 'Введите имя и пароль', 'Пожалуйста, введите имя и пароль.')

    def startLoginWindow(self):
        self.name_input.clear()
        self.password_input.clear()
        self.password_input2.clear()
        self.close()
        self.login_window.show()

    def startSelectLevel(self):
        self.select_level = SelectLevel(self.id_ak)
        self.select_level.show()
