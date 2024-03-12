import os
import sqlite3

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QColor, QPalette, QFont, QIcon
from PyQt5 import QtGui
from PyQt5 import QtCore

from registration_window import RegistrationWindow
from select_level import SelectLevel


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))

        self.setWindowTitle('Окно входа')
        self.setGeometry(450, 200, 1020, 600)
        self.setFixedSize(1020, 600)

        self.count_clicks = 0

        background_label = QLabel(self)
        background_pixmap = QPixmap(os.path.join('pictures', 'Задний фон2.jpg'))
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

        self.current_text_login_button = "Бацæуын"
        self.login_button = QPushButton(self)
        self.login_button.setText(self.current_text_login_button)
        self.login_button.setGeometry(380, 375, 260, 35)
        self.login_button.setStyleSheet(
            f"QPushButton{{border-image: url('pictures/Rectangle3.png'); color: white;}}")
        self.login_button.clicked.connect(self.login)

        self.current_text_open_registration_window = "Регистраци скæнын"
        self.open_registration_window = QPushButton(self)
        self.open_registration_window.setText(self.current_text_open_registration_window)
        self.open_registration_window.setGeometry(380, 420, 260, 35)
        self.open_registration_window.setStyleSheet(
            f"QPushButton{{border-image: url('pictures/Rectangle3.png'); color: white;}}")
        self.open_registration_window.clicked.connect(self.startRegistrationWindow)

        font = QFont()
        font2 = QFont()
        font.setFamily("VAG World")
        font2.setFamily("VAG World")
        font.setPointSize(12)
        font2.setPointSize(24)
        font.setBold(True)
        font2.setBold(True)
        self.login_button.setFont(font)
        self.open_registration_window.setFont(font)
        self.name_label.setFont(font2)

        self.name_input.textChanged.connect(self.update_background)
        self.password_input.textChanged.connect(self.update_background)

        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(220, 220, 220))

        self.name_input.setPalette(palette)
        self.password_input.setPalette(palette)

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
            self.current_text_login_button = "Бацæуын"
            self.current_text_open_registration_window = "Регистраци скæнын"
            self.current_password_placeholder_text = "Сусæ дзырд"
            self.current_placeholder_text = "Ном"
            self.name_label_text = "Уæ бон хорз!"
        else:
            self.current_image_image_button = "Ossetia.png"
            self.current_text_login_button = "Войти"
            self.current_text_open_registration_window = "Зарегистрироваться"
            self.current_password_placeholder_text = "Пароль"
            self.current_placeholder_text = "Имя"
            self.name_label_text = "Добро пожаловать!"

        self.image_button.setIcon(QIcon(os.path.join('pictures', self.current_image_image_button)))
        self.name_label.setText(self.name_label_text)
        self.login_button.setText(self.current_text_login_button)
        self.open_registration_window.setText(self.current_text_open_registration_window)
        self.password_input.setPlaceholderText(self.current_password_placeholder_text)
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

    def login(self):
        name = self.name_input.text()
        password = self.password_input.text()

        if name and password:
            self.cursor.execute('SELECT id, name FROM users WHERE name = ? AND password = ?', (name, password))
            user_data = self.cursor.fetchone()

            if user_data:
                user_id, existing_user = user_data
                self.name_input.clear()
                self.password_input.clear()

                QMessageBox.information(self, 'Вход успешен', f'Пользователь {name} авторизован')

                self.id_ak = user_id

                self.startSelectLevel()
                self.close()
            else:
                QMessageBox.warning(self, 'Неверное имя или пароль',
                                    'Пользователь с указанным именем и паролем не найден.')
        else:
            QMessageBox.warning(self, 'Введите имя и пароль', 'Пожалуйста, введите имя и пароль.')

    def startSelectLevel(self):
        self.select_level = SelectLevel(self.id_ak)
        self.select_level.show()

    def startRegistrationWindow(self):
        self.name_input.clear()
        self.password_input.clear()
        self.registration_window = RegistrationWindow(self)
        self.registration_window.show()
        self.close()
