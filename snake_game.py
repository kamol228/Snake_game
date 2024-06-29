from PyQt5.QtWidgets import *
import sys
import random
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.board = Board(self)
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet("border : 4px groove purple;")
        self.board.msg2statusbar[str].connect(self.statusbar.showMessage)
        self.setCentralWidget(self.board)
        self.setWindowTitle('Snake')
        self.setGeometry(200, 200, 720, 504)
        self.butstart = QPushButton('Begin', self)
        self.butstart.resize(80, 30)
        self.butstart.move(20, 0)
        self.butstart.clicked.connect(self.board.start)
        self.butrestart = QPushButton('Restart', self)
        self.butrestart.resize(120, 30)
        self.butrestart.move(220, 0)
        self.butrestart.clicked.connect(self.board.restart)
        self.butstop = QPushButton('Stop', self)
        self.butstop.resize(80, 30)
        self.butstop.move(120, 0)
        self.butstop.clicked.connect(self.board.pause)
        self.show()


class Board(QFrame, QGraphicsItem):
    msg2statusbar = pyqtSignal(str)
    shirinablocka = 60
    vyisotablocka = 40

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.endgame = False
        self.timer = QBasicTimer()
        self.snake = [[45, 35], [45, 36]]
        self.len_x_head = self.snake[0][0]
        self.len_y_head = self.snake[0][1]
        self.food = []
        self.bad_bonus = []
        self.good_bonus = []
        self.board = []
        self.direction = 1
        self.drop_food()
        self.drop_good_bonus()
        self.drop_bad_bonus()
        self.setFocusPolicy(Qt.StrongFocus)
        self.grow_snake = False
        self.speed = 100
        self.stenyifirst = [[6, 13], [6, 14], [6, 15], [6, 16], [6, 17], [6, 18], [6, 19], [6, 20],
                        [6, 21], [9, 12], [10, 12], [11, 12], [12, 12], [13, 12], [14, 12],
                        [15, 12], [16, 12], [17, 12], [22, 16], [22, 17], [22, 18], [22, 19],
                        [22, 20], [22, 21], [22, 22], [22, 23], [22, 24], [25, 15], [26, 15],
                        [27, 15], [28, 15], [29, 15], [30, 15], [31, 15], [32, 15], [33, 15],
                        [35, 8], [36, 8], [37, 8], [38, 8], [39, 8], [40, 8],
                        [41, 8], [42, 8], [43, 8], [44, 8], [45, 8], [46, 8], [47, 8], [48, 8],
                        [38, 19], [38, 20], [38, 21], [38, 22], [38, 23], [38, 24],
                        [38, 25], [38, 26], [38, 27], [41, 18], [42, 18], [43, 18], [44, 18],
                        [45, 18], [46, 18], [47, 18], [48, 18], [49, 18], [8, 33], [9, 33],
                        [10, 33], [11, 33], [12, 33], [13, 33], [14, 33], [15, 33], [16, 33],
                        [17, 33], [18, 33], [19, 33], [20, 33], [21, 33]]

        self.stenyisecond = [[2, 28], [3, 28], [4, 28], [5, 28], [6, 28], [7, 27], [8, 26],
                        [8, 25], [8, 24], [9, 23], [9, 22], [10, 21], [9, 20], [9, 19],
                        [8, 18], [8, 17], [8, 16], [7, 15], [6, 14], [5, 14], [4, 14],
                        [3, 14], [2, 14], [11, 20], [11, 19], [12, 18], [12, 17], [12, 16],
                        [11, 22], [11, 23], [12, 24], [12, 25], [12, 26], [13, 27],
                        [14, 27], [15, 27], [16, 27], [17, 27], [18, 27], [19, 27], [20, 27], [21, 27], [22, 27],
                        [23, 27], [24, 27], [25, 27], [26, 27], [27, 27], [32, 27],
                        [33, 27], [34, 27], [35, 27], [36, 27], [37, 27], [38, 27], [39, 27], [40, 27], [41, 27],
                        [42, 27], [43, 27], [44, 27], [45, 27], [46, 27], [13, 15],
                        [14, 15], [15, 15], [16, 15], [17, 15], [18, 15], [19, 15], [20, 15], [21, 15], [22, 15],
                        [23, 15], [24, 15], [25, 15], [26, 15], [27, 15], [28, 15], [29, 15], [30, 15], [31, 15],
                        [32, 15],
                        [33, 15], [34, 15], [35, 15], [36, 15], [37, 15], [38, 15], [39, 15], [40, 15], [41, 15],
                        [42, 15], [43, 15], [44, 15], [45, 15], [46, 15], [47, 26], [47, 25], [47, 24], [48, 23],
                        [48, 22],
                        [49, 21], [48, 20], [48, 19], [47, 18], [47, 17], [47, 16], [50, 23], [50, 22], [50, 20],
                        [50, 19], [51, 26], [51, 25], [51, 24], [51, 18], [51, 17], [51, 16],
                        [52, 15], [52, 27], [53, 28], [54, 28], [55, 28], [56, 28], [53, 14],
                        [54, 14], [55, 14], [56, 14],
                        [24, 22], [24, 21], [24, 20], [25, 22], [25, 21], [25, 20], [26, 22], [26, 21], [26, 20],
                        [27, 22], [27, 21], [27, 20], [28, 22], [28, 21], [28, 20], [29, 22], [29, 21], [29, 20],
                        [30, 22], [30, 21], [30, 20], [31, 22], [31, 21], [31, 20], [32, 22], [32, 21], [32, 20],
                        [33, 22], [33, 21], [33, 20], [34, 22], [34, 21], [34, 20], [35, 22], [35, 21], [35, 20]]

    def run(self):
        pass

    def start(self):
        if not self.endgame and not self.timer.isActive():
            self.msg2statusbar.emit(str(len(self.snake) - 2))
            self.timer.start(self.speed, self)

    def pause(self):
        if self.timer.isActive():
            self.timer.stop()

    def restart(self):
        self.snake = [[45, 35], [45, 36]]
        self.len_x_head = self.snake[0][0]
        self.len_y_head = self.snake[0][1]
        self.food = []
        self.bad_bonus = []
        self.good_bonus = []
        self.board = []
        self.direction = 1
        self.drop_food()
        self.drop_bad_bonus()
        self.drop_good_bonus()
        self.setFocusPolicy(Qt.StrongFocus)
        self.grow_snake = False
        self.setStyleSheet("background-color : white;")
        self.endgame = False

    def kvadrat_width(self):
        return self.contentsRect().width() / Board.shirinablocka

    def kvadrat_height(self):
        return self.contentsRect().height() / Board.vyisotablocka

    def paintskake(self, painter):
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.vyisotablocka * self.kvadrat_height()
        for position in self.snake:
            self.draw_snake_square(painter, rect.left() + position[0] * self.kvadrat_width(),
                                   boardtop + position[1] * self.kvadrat_height())
        for position in self.food:
            self.draw_food_square(painter, rect.left() + position[0] * self.kvadrat_width(),
                                  boardtop + position[1] * self.kvadrat_height())

        for position in self.bad_bonus:
            self.draw_bad_bonus_square(painter, rect.left() + position[0] * self.kvadrat_width(),
                                       boardtop + position[1] * self.kvadrat_height())

        for position in self.good_bonus:
            self.draw_bonus_good_square(painter, rect.left() + position[0] * self.kvadrat_width(),
                                        boardtop + position[1] * self.kvadrat_height())

    def draw_flag(self, qp):
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(0, 35, 700, 12)
        qp.setBrush(QColor(190, 0, 0))
        qp.drawRect(0, 36, 12, 500)
        qp.setBrush(QColor(180, 0, 0))
        qp.drawRect(0, 468, 700, 12)
        qp.setBrush(QColor(190, 0, 0))
        qp.drawRect(696, 35, 12, 500)

    def draw_stenyi_1ur(self, ip):
        ip.setBrush(QColor(190, 0, 0))
        ip.drawRect(71, 156, 12, 108)
        ip.drawRect(263, 192, 12, 108)
        ip.drawRect(455, 228, 12, 108)
        ip.drawRect(109, 144, 108, 12)
        ip.setBrush(QColor(190, 0, 0))
        ip.drawRect(301, 180, 108, 12)
        ip.drawRect(493, 216, 108, 12)
        ip.drawRect(421, 96, 168, 12)
        ip.drawRect(96, 396, 168, 12)

    def draw_stenyi_2ur(self, ip2):
        ip2.setBrush(QColor(190, 0, 0))
        ip2.drawRect(120, 252, 12, 12)
        ip2.drawRect(108, 228, 12, 24)
        ip2.drawRect(132, 228, 12, 24)
        ip2.drawRect(120, 252, 12, 12)
        ip2.drawRect(108, 264, 12, 24)
        ip2.drawRect(132, 264, 12, 24)
        ip2.drawRect(144, 192, 12, 36)
        ip2.drawRect(96, 192, 12, 36)
        ip2.drawRect(144, 288, 12, 36)
        ip2.drawRect(96, 288, 12, 36)
        ip2.drawRect(84, 324, 12, 12)
        ip2.drawRect(84, 180, 12, 12)
        ip2.drawRect(24, 168, 60, 12)
        ip2.drawRect(24, 336, 60, 12)
        ip2.drawRect(156, 180, 408, 12)
        ip2.drawRect(156, 324, 180, 12)
        ip2.drawRect(384, 324, 180, 12)
        ip2.setBrush(QColor(190, 0, 0))
        ip2.drawRect(588, 252, 12, 12)
        ip2.drawRect(576, 228, 12, 24)
        ip2.drawRect(600, 228, 12, 24)
        ip2.drawRect(576, 264, 12, 24)
        ip2.drawRect(600, 264, 12, 24)
        ip2.drawRect(612, 192, 12, 36)
        ip2.drawRect(564, 192, 12, 36)
        ip2.drawRect(612, 288, 12, 36)
        ip2.drawRect(564, 288, 12, 36)
        ip2.drawRect(624, 324, 12, 12)
        ip2.drawRect(624, 180, 12, 12)
        ip2.drawRect(636, 168, 48, 12)
        ip2.drawRect(636, 336, 48, 12)
        ip2.setBrush(QColor(0, 0, 0))
        ip2.drawRect(288, 240, 144, 36)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        self.draw_flag(painter)
        self.paintskake(painter)
        if int(len(self.snake) - 2) >= 10 and int(len(self.snake) - 2) < 15:
            self.draw_stenyi_1ur(painter)
        if int(len(self.snake) - 2) >= 15:
            self.draw_stenyi_2ur(painter)
        painter.end()

    def keyPressEvent(self, event):
        z = event.key()

        if z == Qt.Key_Left:
            if self.direction != 2:
                self.direction = 1

        elif z == Qt.Key_Right:
            if self.direction != 1:
                self.direction = 2

        elif z == Qt.Key_Down:
            if self.direction != 4:
                self.direction = 3

        elif z == Qt.Key_Up:
            if self.direction != 3:
                self.direction = 4

        elif event.key() == Qt.Key_E:
            self.start()

        elif event.key() == Qt.Key_R:
            self.restart()

        elif event.key() == Qt.Key_Space:
            self.pause()

        elif event.key() == Qt.Key_Escape:
            self.close()

    def draw_snake_square(self, painter, x, y):
        Green = '#66ff00'
        color = QColor(Green)
        painter.fillRect(x + 1, y + 1, self.kvadrat_width() - 2,
                         self.kvadrat_height() - 2, color)

    def draw_food_square(self, painter, x, y):
        Red = '#ff4d00'
        color = QColor(Red)
        painter.fillRect(x + 1, y + 1, self.kvadrat_width() - 2,
                         self.kvadrat_height() - 2, color)

    def draw_bad_bonus_square(self, painter, x, y):
        Gold = '#FFD700'
        color = QColor(Gold)
        painter.fillRect(x + 1, y + 1, self.kvadrat_width() - 2,
                         self.kvadrat_height() - 2, color)

    def draw_bonus_good_square(self, painter, x, y):
        Blue = '#008080'
        color = QColor(Blue)
        painter.fillRect(x + 1, y + 1, self.kvadrat_width() - 2,
                         self.kvadrat_height() - 2, color)

    def move_snake(self):
        if self.direction == 1:
            self.len_x_head, self.len_y_head = self.len_x_head - 1, self.len_y_head
            if self.len_x_head < 1:
                self.msg2statusbar.emit(str("Snake crashed"))
                self.setStyleSheet("background-color : black;")
                self.timer.stop()
                self.update()
                self.endgame = True
        if self.direction == 2:
            self.len_x_head, self.len_y_head = self.len_x_head + 1, self.len_y_head
            if self.len_x_head == Board.shirinablocka - 2:
                self.msg2statusbar.emit(str("Snake crashed"))
                self.setStyleSheet("background-color : black;")
                self.timer.stop()
                self.update()
                self.endgame = True
        if self.direction == 3:
            self.len_x_head, self.len_y_head = self.len_x_head, self.len_y_head + 1
            if self.len_y_head == Board.vyisotablocka - 1:
                self.msg2statusbar.emit(str("Snake crashed"))
                self.setStyleSheet("background-color : black;")
                self.timer.stop()
                self.update()
                self.endgame = True
        if self.direction == 4:
            self.len_x_head, self.len_y_head = self.len_x_head, self.len_y_head - 1
            if self.len_y_head < 4:
                self.msg2statusbar.emit(str("Snake crashed"))
                self.setStyleSheet("background-color : black;")
                self.timer.stop()
                self.endgame = True

        head = [self.len_x_head, self.len_y_head]
        self.snake.insert(0, head)

        if not self.grow_snake:
            self.snake.pop()
        else:
            self.msg2statusbar.emit(str(len(self.snake) - 2))
            self.grow_snake = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
            self.is_food_collision()
            self.is_bad_bonus_collision()
            self.is_good_bonus_collision()
            self.is_suicide()
            self.update()

    def is_suicide(self):
        for i in range(1, len(self.snake)):
            if self.snake[i] == self.snake[0]:
                self.msg2statusbar.emit(str("Snake suicided"
                                            ""))
                self.setStyleSheet("background-color : brown;")
                self.timer.stop()
                self.update()
                self.endgame = True
        if 10 <= int(len(self.snake) - 2) < 15:
            for x in self.stenyifirst:
                if self.len_x_head == x[0] and self.len_y_head == x[1]:
                    self.msg2statusbar.emit(str("Snake suicided"
                                                ""))
                    self.setStyleSheet("background-color : brown;")
                    self.timer.stop()
                    self.update()
                    self.endgame = True
        if int(len(self.snake) - 2) >= 15:
            for x in self.stenyisecond:
                if self.len_x_head == x[0] and self.len_y_head == x[1]:
                    self.msg2statusbar.emit(str("Snake suicided"
                                                ""))
                    self.setStyleSheet("background-color : brown;")
                    self.timer.stop()
                    self.update()
                    self.endgame = True

    def drop_bad_bonus(self):
        if 0 <= (len(self.snake) - 2) < 10:
            x = random.randint(4, 57)
            y = random.randint(7, 36)
            for position in self.snake:
                if position == [x, y]:
                    self.drop_bad_bonus()
            self.bad_bonus.append([x, y])
        if len(self.snake) == 10 or len(self.snake) == 15:
            x = random.randint(50, 57)
            y = random.randint(33, 36)
            for position12 in self.snake:
                if position12 == [x, y]:
                    self.drop_bad_bonus()
            self.bad_bonus.append([x, y])
        else:
            if 10 <= (len(self.snake) - 2) < 15:
                x = random.randint(4, 57)
                y = random.randint(7, 36)
                if [x, y] in self.ksteni1:
                    self.drop_bad_bonus()
                else:
                    for position12 in self.snake:
                        if position12 == [x, y]:
                            self.drop_bad_bonus()
                    self.bad_bonus.append([x, y])
            if 15 <= (len(self.snake) - 2) < 30:
                x = random.randint(4, 57)
                y = random.randint(7, 36)
                if [x, y] in self.ksteni1:
                    self.drop_bad_bonus()
                else:
                    for position12 in self.snake:
                        if position12 == [x, y]:
                            self.drop_bad_bonus()
                    self.bad_bonus.append([x, y])

    def is_bad_bonus_collision(self):
        for position1 in self.bad_bonus:
            if position1 == self.snake[0]:
                self.bad_bonus.remove(position1)
                self.drop_bad_bonus()
                self.visok_speed()

    def visok_speed(self):
        self.timer.start(50, self)

    def medl_speed(self):
        self.timer.start(100, self)

    def drop_food(self):
        if (len(self.snake) - 2) == 25:
            self.win_game()
        if 0 <= (len(self.snake) - 2) < 10 and (len(self.snake) - 2) != 8:
            x = random.randint(4, 57)
            y = random.randint(7, 36)
            for position in self.snake:
                if position == [x, y]:
                    self.drop_food()
            self.food.append([x, y])
        if (len(self.snake) - 2) == 8 or (len(self.snake) - 2) == 13:
            x = random.randint(53, 57)
            y = random.randint(32, 36)
            for position in self.snake:
                if position == [x, y]:
                    self.drop_food()
            self.food.append([x, y])
        else:
            if 10 <= (len(self.snake) - 2) < 15:
                x = random.randint(4, 57)
                y = random.randint(7, 36)
                if [x, y] in self.stenyifirst:
                    self.drop_food()
                else:
                    for position12 in self.snake:
                        if position12 == [x, y]:
                            self.drop_foos()
                    self.food.append([x, y])
            if 15 <= (len(self.snake) - 2) < 25:
                x = random.randint(4, 57)
                y = random.randint(7, 36)
                if [x, y] in self.stenyifirst:
                    self.drop_food()
                else:
                    for position12 in self.snake:
                        if position12 == [x, y]:
                            self.drop_food()
                    self.food.append([x, y])

    def is_food_collision(self):
        for position in self.food:
            if position == self.snake[0]:
                self.food.remove(position)
                self.drop_food()
                self.grow_snake = True

    def drop_good_bonus(self):
        if 0 <= (len(self.snake) - 2) < 10:
            x = random.randint(4, 57)
            y = random.randint(7, 36)
            for position in self.snake:
                if position == [x, y]:
                    self.drop_good_bonus()
            self.good_bonus.append([x, y])
        if len(self.snake) == 10 or len(self.snake) == 15:
            x = random.randint(50, 57)
            y = random.randint(33, 36)
            for position12 in self.snake:
                if position12 == [x, y]:
                    self.drop_good_bonus()
            self.good_bonus.append([x, y])
        else:
            if 10 <= (len(self.snake) - 2) < 15:
                x = random.randint(4, 57)
                y = random.randint(7, 36)
                if [x, y] in self.ksteni1:
                    self.drop_good_bonus()
                else:
                    for position12 in self.snake:
                        if position12 == [x, y]:
                            self.drop_good_bonus()
                    self.good_bonus.append([x, y])
            if 15 <= (len(self.snake) - 2) < 25:
                x = random.randint(4, 57)
                y = random.randint(7, 36)
                if [x, y] in self.stenyifirst:
                    self.drop_good_bonus()
                else:
                    for position12 in self.snake:
                        if position12 == [x, y]:
                            self.drop_good_bonus()
                    self.good_bonus.append([x, y])

    def is_good_bonus_collision(self):
        for position1 in self.good_bonus:
            if position1 == self.snake[0]:
                self.good_bonus.remove(position1)
                self.drop_good_bonus()
                self.medl_speed()

    def win_game(self):
        self.timer.stop()
        self.setStyleSheet("background-color : yellow;")
        self.msg2statusbar.emit(str("You are winner!"))


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    sys.exit(app.exec_())