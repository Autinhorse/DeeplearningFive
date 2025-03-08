import sys
import time
import threading
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QApplication

from FiveUI.BoardFive import BoardFive
from GameFive import GameFive
from Players.AutoPlayerArena import AutoPlayerArena, MatchResult
from Players.AutoPlayerArenaPool import AutoPlayerArenaPool
from Players.PlayerBase import RobotBase, PlayerColor
from Players.PlayerHuman import RobotHuman

from enum import Enum, auto

from Players.PlayerMCTS import RobotMCTS
from Players.PlayerRandom01 import RobotRandom01
from Players.PlayerRandom02 import RobotRandom02
from Players.PlayerRandom03 import RobotRandom03


class GameStatus(Enum):
    IDLE = 0
    BLACK = 1
    WHITE = 2



class MainWindow(QWidget):
    def __init__(self, size=15):
        super().__init__()
        self.thread = None
        self.size = size
        self.steps = 0
        self.status = GameStatus.IDLE

        self.player1 = None
        self.player2 = None
        self.currentPlayer = None
        self.game = GameFive(15)
        self.board = None

        self.initUI()

        # 用于控制线程的标志
        self.running = False



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
        if self.status!=GameStatus.IDLE:
            return

        # 棋盘部分
        # self.player1 = PlayerHuman(Player.BLACK)
        self.player1 = RobotMCTS(PlayerColor.BLACK)
        #self.player1.rate = 0
        self.player2 = RobotMCTS(PlayerColor.WHITE)
        #self.player2.rate = 1
        self.game.InitGame(size=15)
        self.player1.game = self.game
        self.player2.game = self.game

        self.board.reset_game()

        self.status = GameStatus.BLACK
        self.currentPlayer = self.player1
        self.info_label.setText("黑棋")
        self.CalculateNextMove()

        # 启动一个新的线程来执行任务
        self.thread = threading.Thread(target=self.run_task)
        self.running = True
        self.thread.start()


    def SaveGame(self):
        self.game.SaveGame()

    def LoadGame(self):
        self.game.LoadGame()
        self.board.reset_game()


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
            # print("Task executed at", time.ctime())

            if self.status == GameStatus.BLACK or self.status == GameStatus.WHITE:
                # 正在对弈中
                self.DoPlay()

            # 每秒执行5次
            time.sleep(0.2)  # 0.2 秒 * 5 = 1 秒

    def DoPlay(self):
        if self.currentPlayer.IsMachine():
            x, y = self.currentPlayer.GetNextMove()
        else:
            x, y = self.board.GetNextMove()

        if x==-2:
            # -2表示计算还没有结束
            return
        if x == -1:
            # 找不到可以走的位置了，GameOver
            self.info_label.setText("和棋")
            return

        self.game.steps += 1
        self.step_label.setText(f"步数: {self.game.steps}")
        #print("Step:",self.game.steps)
        result = self.game.DoMove(x=x, y=y, playerColor=self.currentPlayer.playerColor)
        #print("MovePiece:", y, x, self.currentPlayer.playerColor)
        self.board.UpdateBoard()
        if result:
            # 赢棋了
            if self.status == GameStatus.BLACK:
                self.info_label.setText("黑棋胜")
            else:
                self.info_label.setText("白棋胜")

            self.status = GameStatus.IDLE
            self.running = False
            return

        if self.status == GameStatus.BLACK:
            self.status =  GameStatus.WHITE
            self.info_label.setText("白棋")
            self.currentPlayer = self.player2
        else:
            self.status =  GameStatus.BLACK
            self.info_label.setText("黑棋")
            self.currentPlayer = self.player1
        self.CalculateNextMove()

    def CalculateNextMove(self):
        if self.currentPlayer.IsMachine():
            self.currentPlayer.CalculateNextMove()
        else:
            self.board.CalculateNextMove()

    def DoTest1(self):
        player1 = RobotRandom03(PlayerColor.BLACK)
        player2 = RobotMCTS(PlayerColor.WHITE)

        pool = AutoPlayerArenaPool(player1=player1, player2=player2, board=None, beginColor=PlayerColor.BLACK,
                                   processNumber=10, taskNumber=20)
        bw, ww, draw = pool.DoMatch()

        print("Test result: Black Win:", bw, "White Win:", ww, "Draw:",draw)

    def DoTestBundle(self):
        player1 = RobotRandom01(PlayerColor.BLACK)
        player2 = RobotRandom02(PlayerColor.WHITE)

        for i in range(0, 201):
            rate2 = 0.6325 + 0.0025 * i
            if rate2 > 1.0:
                break
            player2.rate = rate2
            pool = AutoPlayerArenaPool(player1=player1, player2=player2, board=None, beginColor=PlayerColor.BLACK,
                                       processNumber=10, taskNumber=10000)
            bw, ww, draw = pool.DoMatch()
            winRate = ww / bw
            print("Test result:", rate2, winRate)

    def DoTest(self):
        '''
        print("Test Begin!")
        player1=PlayerRandom02(Player.BLACK)
        player1.rate = 0.6
        player2=PlayerRandom02(Player.WHITE)
        player2.rate = 0.8
        pool = AutoPlayerArenaPool(player1=player1,player2=player2,board=None, beginColor=Player.BLACK, processNumber=10, taskNumber=2000)
        pool.BeginMatch()
        '''

        self.DoTest1()

        '''
        rate2 = 0.9
        delta = 0.02
        while True:
            rate2 += delta
            player2.rate = rate2
            pool = AutoPlayerArenaPool(player1=player1, player2=player2, board=None, beginColor=Player.BLACK,
                                       processNumber=10, taskNumber=2000)
            bw, ww = pool.BeginMatch()
            newRate = ww/bw
            if abs(newRate-winRate)<0.005:
                print("Done:",newRate,rate2)
                break

            if newRate<winRate:
                # 前进方向错误
                delta *= -0.9

            print(winRate,newRate,rate2, delta)
            winRate = newRate
        '''

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
