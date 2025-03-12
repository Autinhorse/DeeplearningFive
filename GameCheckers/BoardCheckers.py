import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRectF

from GameCheckers.RobotCheckers.RobotCheckersBase import PieceType, PlayerColor


class BoardCheckers(QWidget):
    def __init__(self,game,parent):
        super().__init__()
        self.initUI()
        self.game = game
        self.parent = parent
        # self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.possible_moves = []
        # self.initialize_pieces()
        self.crown_pixmap = QPixmap("crown.png")  # 加载王冠图像
        self.nextMove = None
        self.waitingPlayer = None


    def initUI(self):
        self.setWindowTitle('西洋跳棋')
        self.setGeometry(100, 100, 600, 600)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawBoard(qp)
        self.drawPieces(qp)
        if self.selected_piece is not None:
            self.drawPossibleMoves(qp)
        qp.end()

    def drawBoard(self, qp):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    qp.setBrush(QColor(255, 206, 158))  # 浅色格
                else:
                    qp.setBrush(QColor(209, 139, 71))  # 深色格
                qp.drawRect(col * 75, row * 75, 75, 75)

    def drawPieces(self, qp):
        for row in range(8):
            for col in range(8):
                #print(row,col,self.game.board[row][col])
                if self.game.board[row][col] != PieceType.Empty:
                    color = QColor(Qt.black) if self.game.board[row][col] == PieceType.BlackKing or self.game.board[row][col] == PieceType.BlackNormal else QColor(Qt.white)
                    qp.setBrush(color)
                    center_x = int(col * 75 + 37.5)
                    center_y = int(row * 75 + 37.5)
                    qp.drawEllipse(QPoint(center_x, center_y), 30, 30)
                    if self.game.board[row][col]==PieceType.BlackKing or self.game.board[row][col]==PieceType.WhiteKing:
                        #ellipse_rect = QRectF(center_x, center_y, 72, 72)
                        crown_rect = self.crown_pixmap.rect()
                        crown_rect.moveCenter(QPoint(center_x, center_y))  # 将王冠图像的中心对齐到椭圆中心
                        qp.drawPixmap(crown_rect, self.crown_pixmap)

    def drawPossibleMoves(self, qp):
        for item in self.possible_moves:
            move = []
            l = len(item)
            ty = item[l-2]
            tx = item[l-1]
            move.append(ty)
            move.append(tx)

            center_x = int(move[1] * 75 + 37.5)
            center_y = int(move[0] * 75 + 37.5)
            qp.setBrush(QColor(0, 255, 0, 128))
            qp.drawEllipse(QPoint(center_x, center_y), 15, 15)

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        col, row = x // 75, y // 75
        if self.selected_piece is None:
            if self.game.board[row][col] != PieceType.Empty and self.waitingPlayer is not None:
                if (self.waitingPlayer.playerColor==PlayerColor.BLACK and (self.game.board[row][col]==PieceType.BlackKing or self.game.board[row][col]==PieceType.BlackNormal))\
                    or (self.waitingPlayer.playerColor==PlayerColor.WHITE and (self.game.board[row][col]==PieceType.WhiteKing or self.game.board[row][col]==PieceType.WhiteNormal)):
                    self.selected_piece = (row, col)
                    #print("Select:",self.selected_piece)
                    self.possible_moves = self.waitingPlayer.GetPossibleMoveOfPiece(row,col)
                    #print("Possible_move:",self.possible_moves)
                    self.update()
        else:
            #print("SelectTarget:",row,col)
            for item in self.possible_moves:
                #print("Item:",item)
                l = len(item)
                if row==item[l-2] and col==item[l-1]:
                    self.nextMove = self.selected_piece  + item
                    self.possible_moves = []
                    self.selected_piece = None
                    break

    def get_possible_moves(self, row, col, playerColor):
        moves = self.game.GetPossibleMoveOfPiece(row, col, playerColor)

        return moves

    def move_piece(self, from_pos, to_pos):
        self.nextMove = (from_pos[0], from_pos[1], to_pos[0], to_pos[1])

    def UpdateBoard(self):
        self.update()

    def reset_game(self):
        self.parent().step_label.setText(f"步数: {self.game.steps}")
        self.update()

    def CalculateNextMove(self):
        self.nextMove = None

    def GetNextMove(self):
        return self.nextMove