import sys
import time
import threading
import logging

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QApplication

from FiveUI.BoardFive import BoardFive
from GameFive import GameFive
from Players.PlayerBase import PlayerBase, Player
from Players.PlayerRandom01 import PlayerRandom01
from Players.PlayerHuman import PlayerHuman

from enum import Enum, auto

class GameStatus(Enum):
    IDLE = 0
    BLACK = 1
    WHITE = 2

class MainWindow(QWidget):
    def __init__(self, size=15):
        super().__init__()
        self.size = size
        self.steps = 0
        self.status = GameStatus.IDLE

        self.player1 = None
        self.player2 = None
        self.game = GameFive(15)
        self.board = None

        self.initUI()

        # 用于控制线程的标志
        self.running = False

        # 启动一个新的线程来执行任务
        self.thread = threading.Thread(target=self.run_task)

    def initUI(self):
        self.setWindowTitle('五子棋')
        self.setFixedSize(self.size * 40 + 2 * 20 + 180, self.size * 40 + 2 * 60)  # 固定窗口大小

        main_layout = QHBoxLayout()

        # 棋盘部分
        self.board = BoardFive(game=self.game, parent=self)
        main_layout.addWidget(self.board)

        # 控制面板
        control_layout = QVBoxLayout()

        self.step_label = QLabel(f"步数: {self.steps}", self)
        control_layout.addWidget(self.step_label)

        self.info_label = QLabel("等待开始", self)
        control_layout.addWidget(self.info_label)

        start_button = QPushButton("开始", self)
        start_button.setFixedWidth(100)  # 设置按钮宽度
        start_button.clicked.connect(self.StartGame)
        control_layout.addWidget(start_button)

        end_button = QPushButton("结束", self)
        end_button.setFixedWidth(100)  # 设置按钮宽度
        end_button.clicked.connect(QApplication.quit)
        control_layout.addWidget(end_button)

        save_button = QPushButton("保存", self)
        save_button.setFixedWidth(100)  # 设置按钮宽度
        save_button.clicked.connect(self.SaveGame)
        control_layout.addWidget(save_button)

        load_button = QPushButton("加载", self)
        load_button.setFixedWidth(100)  # 设置按钮宽度
        load_button.clicked.connect(self.LoadGame)
        control_layout.addWidget(load_button)

        test_button = QPushButton("测试", self)
        test_button.setFixedWidth(100)  # 设置按钮宽度
        test_button.clicked.connect(self.DoTest)
        control_layout.addWidget(test_button)

        spacer = control_layout.addStretch(1)  # 添加弹性空间以保持按钮靠上

        main_layout.addLayout(control_layout)
        self.setLayout(main_layout)
        self.show()

    def StartGame(self):
        # 棋盘部分
        self.player1 = PlayerRandom01(Player.BLACK)
        self.player2 = PlayerRandom01(Player.WHITE)
        self.game.InitGame(size=15)
        self.player1.game = self.game
        self.player2.game = self.game

        self.board.reset_game()

        self.status = GameStatus.BLACK
        self.info_label.setText("黑棋")

        self.running = True
        self.thread.start()


    def SaveGame(self):
        self.game.SaveGame()

    def LoadGame(self):
        self.game.LoadGame()
        self.board.reset_game()

    def DoTest(self):
        print("Do Test")
        self.running = False
        # pos = self.player1.GetPossiblePos()
        # print("Result:", len(pos))
        # for (x,y),d in pos:
        #    print(y,x,d)
        player = self.player1 if self.status == GameStatus.BLACK else self.player2

        x, y = player.GetNextMove()
        if x==-1:
            # 找不到可以走的位置了，GameOver
            self.info_label.setText("和棋")
            return

        self.game.steps += 1
        self.step_label.setText(f"步数: {self.game.steps}")
        result = self.game.DoMove(x=x,y=y,playerColor=player.playerColor)
        print("MovePiece:",y,x,player.playerColor)
        self.board.UpdateBoard()
        if result:
            # 赢棋了
            if player.playerColor==Player.BLACK:
                self.info_label.setText("黑棋胜")
            else:
                self.info_label.setText("白棋胜")
            return

        if self.status == GameStatus.BLACK:
            self.status =  GameStatus.WHITE
            self.info_label.setText("白棋")
        else:
            self.status =  GameStatus.BLACK
            self.info_label.setText("黑棋")

    def start_task(self):
        if not self.running:
            self.running = True
            self.button.setText("Stop")
            # 启动一个新的线程来执行任务
            self.thread = threading.Thread(target=self.run_task)
            self.thread.start()
        else:
            self.running = False
            self.button.setText("Start")

    def run_task(self):
        while self.running:
            # 执行你的操作
            print("Task executed at", time.ctime())
            # 每秒执行5次
            time.sleep(0.2)  # 0.2 秒 * 5 = 1 秒



        # 线程结束时重置按钮文本
        # self.button.setText("Start")

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
