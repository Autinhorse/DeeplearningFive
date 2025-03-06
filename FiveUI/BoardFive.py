import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint

from Players.PlayerBase import Player


class BoardFive(QWidget):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.game = game
        self.grid_size = 40  # 每个格子的大小
        self.margin = 20  # 边距
        self.initUI()
        self.nextMove = (-1, -1)

    def initUI(self):
        self.setWindowTitle('五子棋')
        self.setGeometry(300, 300, self.game.size * self.grid_size + 2 * self.margin,
                         self.game.size * self.grid_size + 2 * self.margin)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制网格
        for i in range(self.game.size):
            painter.drawLine(self.margin+(int)(self.grid_size/2), self.margin + i * self.grid_size+(int)(self.grid_size/2),
                             self.margin + (self.game.size-1) * self.grid_size+(int)(self.grid_size/2), self.margin + i * self.grid_size+(int)(self.grid_size/2))
            painter.drawLine(self.margin + i * self.grid_size+(int)(self.grid_size/2), self.margin+(int)(self.grid_size/2),
                             self.margin + i * self.grid_size+(int)(self.grid_size/2), self.margin + (self.game.size-1) * self.grid_size+(int)(self.grid_size/2))

        # 绘制棋子
        cn = 0
        for y in range(self.game.size):
            for x in range(self.game.size):
                if self.game.board[y][x] != Player.EMPTY:
                    cn += 1
                    if self.game.board[y][x] == Player.BLACK:
                        # 黑子
                        color = QColor(Qt.black)
                        painter.setBrush(color)
                        painter.setPen(QPen(color, 1))
                        painter.drawEllipse(QPoint((int)(self.margin + (x + 1) * self.grid_size - self.grid_size / 2),
                                                   (int)(self.margin + (y + 1) * self.grid_size - self.grid_size / 2)), 18, 18)
                    elif self.game.board[y][x] == Player.WHITE:
                        # 白子
                        # 设置填充颜色
                        fill_color = QColor(Qt.white)
                        painter.setBrush(fill_color)

                        # 设置边框颜色和宽度
                        border_color = QColor(Qt.black)  # 你可以选择你喜欢的颜色
                        pen = QPen(border_color, 2)  # 2 是边框的宽度
                        painter.setPen(pen)

                        # 计算棋子的中心位置
                        center_x = int(self.margin + (x + 1) * self.grid_size - self.grid_size / 2)
                        center_y = int(self.margin + (y + 1) * self.grid_size - self.grid_size / 2)

                        # 绘制带边框的圆形
                        painter.drawEllipse(QPoint(center_x, center_y), 18, 18)
        # print("Piece Number:",cn)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            x = round((pos.x() - self.margin-self.grid_size/2) / self.grid_size)
            y = round((pos.y() - self.margin-self.grid_size/2) / self.grid_size)
            print("Mouse Press:",y,x)
            if 0 <= x < self.game.size and 0 <= y < self.game.size:
                if self.game.board[y][x] != Player.EMPTY:
                    return
                print("Click:",y,x)
                self.nextMove = (x, y)

                #self.game.board[y][x] = self.current_player
                #self.game.DoMove(y=y, x=x, playerColor=self.current_player)
                #self.current_player = 3 - self.current_player
                #self.parent().steps += 1
                #self.parent().step_label.setText(f"步数: {self.game.steps}")
                #self.update()

    def CalculateNextMove(self):
        self.nextMove = (-2, -2)

    def GetNextMove(self):
        return self.nextMove

    def SetStepNumber(self, step):
        self.parent().step_label.setText(f"步数: {step}")

    def UpdateBoard(self):
        self.update()

    def reset_game(self):
        self.parent().step_label.setText(f"步数: {self.game.steps}")
        self.update()




