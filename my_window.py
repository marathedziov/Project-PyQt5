import os
import sqlite3
from random import shuffle
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QMessageBox, QInputDialog, QProgressBar
from PyQt5.QtGui import QFont, QPainter, QPixmap, QColor, QIcon
from PyQt5 import QtGui


class MyWindow(QMainWindow):
    def __init__(self, select_level, id_ak):
        super().__init__()
        self.id_ak = id_ak
        self.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))
        self.select_level = select_level
        self.user_points = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Собери животное из частей")
        self.points = 0
        self.id_of_dataBase = 0
        self.number_of_question = 1
        self.con = sqlite3.connect("DataBase.sqlite")
        self.cur = self.con.cursor()
        self.Data = self.cur.execute("""SELECT * FROM BaseAlData""").fetchall()
        self.con.close()
        self.text_questions = self.Data[0 + self.id_of_dataBase][0]
        self.text_questions = self.text_questions.split(", ")
        self.one_ans = self.Data[0 + self.id_of_dataBase][1]
        self.one_ans = self.one_ans.split(", ")
        self.two_ans = self.Data[0 + self.id_of_dataBase][2]
        self.two_ans = self.two_ans.split(", ")
        self.three_ans = self.Data[0 + self.id_of_dataBase][3]
        self.three_ans = self.three_ans.split(", ")
        self.four_ans = self.Data[0 + self.id_of_dataBase][4]
        self.four_ans = self.four_ans.split(", ")

        self.correct_answers = self.one_ans.copy()

        self.correct_answer_count = 0

        self.setGeometry(650, 200, 660, 660)
        self.setFixedSize(660, 640)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(10, 600, 150, 30)
        self.pbar.setTextVisible(False)
        self.updateProgressBar()

        self.points_label = QLabel(self)
        self.points_label.setGeometry(10, 600, 150, 30)
        self.points_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(10)
        font.setBold(True)
        self.points_label.setFont(font)
        self.updatePointsLabel()

        self.question = QLabel(self)
        self.question.setGeometry(10, 10, 650, 50)
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(20)
        font.setBold(True)
        self.question.setFont(font)

        self.button1 = QPushButton(self)
        self.button1.setGeometry(15, 90, 150, 30)
        self.button1.clicked.connect(lambda: self.checkAnswer(self.button1.text()))
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(11)
        font.setBold(True)
        self.button1.setFont(font)

        self.button2 = QPushButton(self)
        self.button2.setGeometry(175, 90, 150, 30)
        self.button2.clicked.connect(lambda: self.checkAnswer(self.button2.text()))
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(11)
        font.setBold(True)
        self.button2.setFont(font)

        self.button3 = QPushButton(self)
        self.button3.setGeometry(335, 90, 150, 30)
        self.button3.clicked.connect(lambda: self.checkAnswer(self.button3.text()))
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(11)
        font.setBold(True)
        self.button3.setFont(font)

        self.button4 = QPushButton(self)
        self.button4.setGeometry(495, 90, 150, 30)
        self.button4.clicked.connect(lambda: self.checkAnswer(self.button4.text()))
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(11)
        font.setBold(True)
        self.button4.setFont(font)

        self.back_button = QPushButton("Вернуться в меню", self)
        self.back_button.setGeometry(500, 600, 150, 30)
        self.back_button.clicked.connect(self.returnToSelectLevel)
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(10)
        font.setBold(True)
        self.back_button.setFont(font)

        self.images = ['level1/1_1_img.png', 'level1/1_2_img.png', 'level1/1_3_img.png', 'level1/1_4_img.png',
                       'level1/1_5_img.png',
                       'level1/1_6_img.png', 'level1/1_7_img.png', 'level1/1_8_img.png']
        self.current_image_index = 0

        self.myWidget = MyWidget(self)
        self.myWidget.setGeometry(50, 150, 550, 380)

        self.question_index = 0
        self.answer_index = 0
        self.wrong_answer_count = 0

        self.updateQuestion()

    def checkAnswer(self, answer):
        if self.question_index < len(self.text_questions):
            if answer == self.correct_answers[self.question_index]:
                self.addImage()
                self.wrong_answer_count = 0
                self.correct_answer_count += 1
            else:
                self.wrongAnswer()
                self.wrong_answer_count += 1
                if self.user_points != 0:
                    self.user_points -= 5
                self.updatePointsLabel()
                if self.wrong_answer_count == 2:
                    if self.user_points != 0:
                        self.user_points -= 5
                    self.showRestartMessage()
                    self.updatePointsLabel()

        if self.correct_answer_count == 8:
            self.checkWord()

    def updateQuestion(self):
        self.question.setText(self.text_questions[self.question_index])
        self.correct_answer = self.correct_answers[self.question_index]
        answer_buttons = [self.one_ans[self.answer_index], self.two_ans[self.answer_index],
                          self.three_ans[self.answer_index], self.four_ans[self.answer_index]]
        shuffle(answer_buttons)
        self.button1.setText(answer_buttons[0])
        self.button2.setText(answer_buttons[1])
        self.button3.setText(answer_buttons[2])
        self.button4.setText(answer_buttons[3])

    def addImage(self):
        if self.current_image_index < len(self.images):
            self.myWidget.addImage(self.images[self.current_image_index])
            self.current_image_index += 1
            self.myWidget.update()

        self.question_index += 1
        self.answer_index += 1

        if self.question_index < len(self.text_questions):
            self.updateQuestion()

    def wrongAnswer(self):
        if self.question_index < len(self.text_questions):
            msg = QMessageBox()
            msg.setWindowTitle("Неправильный ответ")
            msg.setText("Неправильно! -5 очков, попробуй еще раз!")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))
            msg.exec()

    def showRestartMessage(self):
        msg = QMessageBox()
        msg.setWindowTitle("Игра перезапускается")
        msg.setText("Вы дважды подряд дали неправильный ответ! -5 очков. Игра начнется заново.")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))
        msg.exec()
        self.restartGame()

    def restartGame(self):
        self.question_index = 0
        self.answer_index = 0
        self.wrong_answer_count = 0
        self.correct_answer_count = 0
        self.current_image_index = 0
        self.myWidget.clearImages()
        self.updateQuestion()

    def checkWord(self):
        while True:
            user_input, ok_pressed = QInputDialog.getText(self, "Проверка слова", "Введите слово на осетинском:")
            if not ok_pressed:
                break

            if user_input.lower().strip() == "фыс":
                self.showSuccessMessage()
                self.updateDatabasePoints()
                break
            else:
                self.showFailureMessage()

    def updatePointsLabel(self):
        self.points_label.setText(f"Очки: {self.user_points}")
        self.updateProgressBar()

    def updateProgressBar(self):
        self.pbar.setValue(self.user_points)

        if self.user_points >= 75:
            green_color = QColor(0, 215, 0)
            color_style = f"QProgressBar::chunk {{ background: {green_color.name()}; }}"
        elif self.user_points >= 50:
            yellow_color = QColor(255, 255, 0)
            color_style = f"QProgressBar::chunk {{ background: {yellow_color.name()}; }}"
        else:
            color_style = "QProgressBar::chunk { background: red; }"

        self.pbar.setStyleSheet(color_style)

    def updateDatabasePoints(self):
        self.con = sqlite3.connect("DataBase.sqlite")
        self.cur = self.con.cursor()

        user_id = self.id_ak

        additional_points = self.user_points

        query_current_points = "SELECT points FROM Users WHERE id = ?"
        current_points = self.cur.execute(query_current_points, (user_id,)).fetchone()[0]

        if current_points < additional_points:
            query_update_points = "UPDATE Users SET points = ? WHERE id = ?"
            self.cur.execute(query_update_points, (additional_points, user_id))

        self.con.commit()
        self.con.close()

    def showSuccessMessage(self):
        msg = QMessageBox()
        msg.setWindowTitle("Уровень пройден")
        msg.setText("Поздравляю! Вы прошли уровень!")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))
        msg.exec()
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)

    def showFailureMessage(self):
        msg = QMessageBox()
        msg.setWindowTitle("Неправильный ответ")
        msg.setText("Вы ввели неправильное слово. Попробуйте еще раз.")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon(os.path.join('pictures', 'logo.png')))
        msg.exec()

    def returnToSelectLevel(self):
        self.restartGame()
        self.select_level.show()
        self.close()


class MyWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_info = []

    def addImage(self, image_path):
        self.image_info.append((0, 0, image_path))

    def clearImages(self):
        self.image_info = []

    def paintEvent(self, event):
        qp = QPainter(self)

        for x, y, image_path in self.image_info:
            pixmap = QPixmap(image_path)
            qp.drawPixmap(x, y, pixmap)
