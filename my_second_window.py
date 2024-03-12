import os
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QMessageBox, QInputDialog, QProgressBar
from PyQt5.QtGui import QFont, QPainter, QPen, QColor, QBrush, QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5 import QtGui


class MySecondWindow(QMainWindow):
    def __init__(self, select_level, id_ak):
        super().__init__()
        self.id_ak = id_ak
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.select_level = select_level
        self.user_points = 100
        self.user_id = 1
        self.initUI()
        self.media_player = QMediaPlayer()
        self.current_audio_file = None
        self.correct_answer_count = 0

    def initUI(self):
        self.setWindowTitle("Собери животное из геометрических фигур")
        self.lst = ['1', '3', '2', '5', '1', '4', '3']
        sound_folder = os.path.join(os.path.dirname(__file__), 'level2', 'sound')

        self.audio_files = [
            os.path.join(sound_folder, "circle.mp3"),
            os.path.join(sound_folder, "oval.mp3"),
            os.path.join(sound_folder, "square.mp3"),
            os.path.join(sound_folder, "triangle.mp3"),
            os.path.join(sound_folder, "circle.mp3"),
            os.path.join(sound_folder, "rectangle.mp3"),
            os.path.join(sound_folder, "oval.mp3"),
            os.path.join(sound_folder, "oval.mp3")
        ]

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
        self.question.setGeometry(5, 10, 655, 50)
        self.question.setAlignment(Qt.AlignCenter)
        self.question.setText("Послушай диктора и выбери фигуру, которую он произнес")
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(16)
        font.setBold(True)
        self.question.setFont(font)

        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)

        self.button1 = QPushButton(self)
        self.button1.setGeometry(20, 75, 100, 100)
        self.button1.setStyleSheet(f"QPushButton{{border-image: url({'level2/circle.png'});}}"
                                   "QPushButton:hover { border: 5px solid black; }")
        self.button1.clicked.connect(self.button1_click)

        self.button2 = QPushButton(self)
        self.button2.setGeometry(150, 75, 100, 100)
        self.button2.setStyleSheet(f"QPushButton{{border-image: url({'level2/square.png.'});}}"
                                   "QPushButton:hover { border: 5px solid black; }")
        self.button2.clicked.connect(self.button2_click)

        self.button3 = QPushButton(self)
        self.button3.setGeometry(280, 75, 100, 100)
        self.button3.setStyleSheet(f"QPushButton{{border-image: url({'level2/oval.png'});}}"
                                   "QPushButton:hover { border: 5px solid black; }")

        self.button3.clicked.connect(self.button3_click)

        self.button4 = QPushButton(self)
        self.button4.setGeometry(410, 75, 100, 100)
        self.button4.setStyleSheet(f"QPushButton{{border-image: url({'level2/rectangle.png'});}}"
                                   "QPushButton:hover { border: 5px solid black; }")
        self.button4.clicked.connect(self.button4_click)

        self.button5 = QPushButton(self)
        self.button5.setGeometry(540, 75, 100, 100)
        self.button5.setStyleSheet(f"QPushButton{{border-image: url({'level2/triangle.png'});}}"
                                   "QPushButton:hover { border: 5px solid black; }")
        self.button5.clicked.connect(self.button5_click)

        self.speaker_button = QPushButton("Послушать диктора", self)
        self.speaker_button.setGeometry(205, 535, 250, 30)
        self.speaker_button.clicked.connect(self.playAudio)
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(12)
        font.setBold(True)
        self.speaker_button.setFont(font)

        self.back_button = QPushButton("Вернуться в меню", self)
        self.back_button.setGeometry(500, 600, 150, 30)
        self.back_button.clicked.connect(self.returnSelectLevel)
        font = QFont()
        font.setFamily("VAG World")
        font.setPointSize(10)
        font.setBold(True)
        self.back_button.setFont(font)

        self.question_index = 0
        self.answer_index = 0
        self.wrong_answer_count = 0

    def button1_click(self):
        self.button = '1'
        self.checkAnswer(self.button)

    def button2_click(self):
        self.button = '2'
        self.checkAnswer(self.button)

    def button3_click(self):
        self.button = '3'
        self.checkAnswer(self.button)

    def button4_click(self):
        self.button = '4'
        self.checkAnswer(self.button)

    def button5_click(self):
        self.button = '5'
        self.checkAnswer(self.button)

    def checkAnswer(self, num_button):
        if self.question_index < len(self.lst):
            if num_button == self.lst[self.question_index]:
                self.draw()
                self.wrong_answer_count = 0
                self.correct_answer_count += 1
            else:
                self.wrongAnswer()
                self.wrong_answer_count += 1
                if self.user_points != 0:
                    self.user_points -= 5
                self.updatePointsLabel()
                if self.wrong_answer_count == 3:
                    if self.user_points != 0:
                        self.user_points -= 5
                    self.showRestartMessage()
                    self.updatePointsLabel()
                    self.restartGame()

        if self.correct_answer_count == 7:
            self.checkWord()

    def draw(self):
        self.answer_index += 1
        self.question_index += 1
        blue_color = QColor(0, 0, 180)
        black_color = QColor(0, 0, 0)
        green_color = QColor(0, 100, 0)
        red_color = QColor(215, 0, 0)
        brown_color = QColor(139, 69, 19)

        if self.question_index == 1:
            self.canvas.shapes.append(('circle', blue_color, 181, 211, 100, 100))
        elif self.question_index == 2:
            self.canvas.shapes.append(('oval', green_color, 290, 320, 150, 70))
        elif self.question_index == 3:
            self.canvas.shapes.append(('rectangle', brown_color, 482, 290, 35, 35))
        elif self.question_index == 4:
            self.canvas.shapes.append(('triangle', green_color, [QPoint(176, 250), QPoint(176, 270), QPoint(145, 265)]))
        elif self.question_index == 5:
            self.canvas.shapes.append(('circle2', black_color, 201, 241, 23, 23))
        elif self.question_index == 6:
            self.canvas.shapes.append(('rectangle', brown_color, 250, 445, 140, 30))
        elif self.question_index == 7:
            self.canvas.shapes.append(('oval', red_color, 230, 280, 260, 160))

        self.canvas.update()

    def wrongAnswer(self):
        if self.question_index < len(self.lst):
            msg = QMessageBox()
            msg.setWindowTitle("Неправильный ответ")
            msg.setText("Неправильно -5 очков, попробуй еще раз!")
            msg.setIcon(QMessageBox.Warning)
            icon_pixmap = QPixmap('logo.png')
            msg.setWindowIcon(QIcon(icon_pixmap))
            msg.exec()

    def showRestartMessage(self):
        msg = QMessageBox()
        msg.setWindowTitle("Игра перезапускается")
        msg.setText("Вы трижды подряд дали неправильный ответ! -5 очков. Игра начнется заново.")
        msg.setIcon(QMessageBox.Warning)
        icon_pixmap = QPixmap('logo.png')
        msg.setWindowIcon(QIcon(icon_pixmap))
        msg.exec()

    def restartGame(self):
        self.question_index = 0
        self.answer_index = 0
        self.wrong_answer_count = 0
        self.correct_answer_count = 0
        self.canvas.shapes = []

    def checkWord(self):
        while True:
            user_input, ok_pressed = QInputDialog.getText(self, "Проверка слова", "Введите слово на осетинском:")
            if not ok_pressed:
                break

            if user_input.lower().strip() == "цъиу":
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

        query_current_points = "SELECT points2 FROM Users WHERE id = ?"
        current_points = self.cur.execute(query_current_points, (user_id,)).fetchone()[0]

        if current_points < additional_points:
            query_update_points = "UPDATE Users SET points2 = ? WHERE id = ?"
            self.cur.execute(query_update_points, (additional_points, user_id))

        self.con.commit()
        self.con.close()

    def showSuccessMessage(self):
        msg = QMessageBox()
        msg.setWindowTitle("Уровень пройден")
        msg.setText("Поздравляю! Вы прошли уровень!")
        msg.setIcon(QMessageBox.Information)
        icon_pixmap = QPixmap('logo.png')
        msg.setWindowIcon(QIcon(icon_pixmap))
        msg.exec()
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        self.button5.setEnabled(False)
        self.speaker_button.setEnabled(False)

    def showFailureMessage(self):
        msg = QMessageBox()
        msg.setWindowTitle("Неправильный ответ")
        msg.setText("Вы ввели неправильное слово. Попробуйте еще раз.")
        msg.setIcon(QMessageBox.Warning)
        icon_pixmap = QPixmap('logo.png')
        msg.setWindowIcon(QIcon(icon_pixmap))
        msg.exec()

    def returnSelectLevel(self):
        self.restartGame()
        self.select_level.show()
        self.close()

    def playAudio(self):
        media_content = QMediaContent(QUrl.fromLocalFile(self.audio_files[self.question_index]))
        self.media_player.setMedia(media_content)
        self.media_player.play()


class Canvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.shapes = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for shape in self.shapes:
            pen = QPen(shape[1])
            pen.setWidth(4)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            if shape[0] == 'circle':
                painter.drawEllipse(shape[2], shape[3], shape[4], shape[5])
            elif shape[0] == 'circle2':
                painter.setBrush(QBrush(shape[1]))
                painter.drawEllipse(shape[2], shape[3], shape[4], shape[5])
            elif shape[0] == 'square':
                painter.drawRect(shape[2], shape[3], shape[4], shape[5])
            elif shape[0] == 'triangle':
                painter.drawPolygon(shape[2])
            elif shape[0] == 'oval':
                painter.drawEllipse(shape[2], shape[3], shape[4], shape[5])
            elif shape[0] == 'rectangle':
                painter.drawRect(shape[2], shape[3], shape[4], shape[5])
