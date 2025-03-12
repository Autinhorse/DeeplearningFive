import random
import sys
import time
import threading
import pickle

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QApplication

from GameCheckers.BoardCheckers import BoardCheckers
from GameCheckers.GameCheckers import GameCheckers
from GameCheckers.RobotCheckers.RobotCheckersHuman import RobotCheckersHuman
from GameCheckers.RobotCheckers.RobotCheckersMCTS import RobotCheckersMCTS
from GameCheckers.RobotCheckers.RobotCheckersRandom01 import RobotCheckersRandom01
from GameCheckers.RobotCheckers.RobotCheckersRating import RobotCheckersRating
from GameFive.Five import GameStatus
from RobotArena.AutoRobotArena import MatchResult
from RobotArena.AutoRobotArenaPool import AutoRobotArenaPool
from GameCheckers.RobotCheckers.RobotCheckersBase import PlayerColor


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
        self.game = GameCheckers()
        self.board = None

        self.initUI()

        # 用于控制线程的标志
        self.running = False

    def initUI(self):
        self.setWindowTitle('西洋跳棋')
        self.setFixedSize(self.size * 40 + 2 * 20 + 180, self.size * 40 + 2 * 60)  # 固定窗口大小

        main_layout = QHBoxLayout()

        # 棋盘部分
        self.board = BoardCheckers(game=self.game, parent=self)
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
        self.player1 = RobotCheckersRandom01(PlayerColor.BLACK, 0.9)
        #self.player1 = RobotCheckersMCTS(PlayerColor.BLACK)
        #self.player1.rate = 0
        #self.player2 = RobotCheckersMCTS(PlayerColor.WHITE)
        #self.player2 = RobotCheckersRandom01(PlayerColor.WHITE, 0.8)
        #self.player2 = RobotCheckersHuman(PlayerColor.WHITE)
        self.player2 = RobotCheckersRating(PlayerColor.WHITE)

        #self.player2.rate = 1
        self.game.InitGame()
        self.player1.game = self.game
        self.player2.game = self.game

        #self.board.reset_game()

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
        self.LoadData()

        #self.game.LoadGame()
        #self.board.reset_game()


    def start_task(self):
        print("start_task")
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
        print("run_task")
        while self.running:
            # 执行你的操作
            # print("Task executed at", time.ctime())

            if self.status == GameStatus.BLACK or self.status == GameStatus.WHITE:
                # 正在对弈中
                self.DoPlay()

            # 每秒执行5次
            time.sleep(0.5)  # 0.2 秒 * 5 = 1 秒

    def DoPlay(self):
        #print("DoPlay")
        if self.currentPlayer.IsMachine():
            nextMove = self.currentPlayer.GetNextMove()
        else:
            self.board.waitingPlayer = self.currentPlayer
            nextMove = self.board.GetNextMove()

        if nextMove is None:
            return
        print("DoPlay:",nextMove)
        self.board.waitingPlayer = None

        if nextMove[0]==-1:
            # 全堵死了
            # 找不到可以走的位置了，GameOver
            self.info_label.setText("和棋")
            return

        print("NextMove:",nextMove, self.currentPlayer.playerColor)
        self.game.steps += 1
        self.step_label.setText(f"步数: {self.game.steps}")
        #print("Step:",self.game.steps)
        result = self.game.DoMove(nextMove=nextMove, playerColor=self.currentPlayer.playerColor)
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

    def DoGenerateGame(self):
        gameNumber = 100
        gameIndex = 0
        fileSize = 10

        records = []
        for i in range(gameNumber):
            print("Game:",i+1)
            #随机分配机器人
            if random.randint(0,100)>50:
                player1 = RobotCheckersRandom01(PlayerColor.BLACK, 0.9)
                player2 = RobotCheckersRating(PlayerColor.WHITE)
            else:
                player2 = RobotCheckersRandom01(PlayerColor.BLACK, 0.9)
                player1 = RobotCheckersRating(PlayerColor.WHITE)

            # self.player2.rate = 1
            game =GameCheckers()
            player1.game = game
            player2.game = game

            # self.board.reset_game()

            status = GameStatus.BLACK
            currentPlayer = player1

            gameResult = MatchResult.DRAW
            record = []
            while True:
                currentPlayer.CalculateNextMove()
                nextMove = currentPlayer.GetNextMove()
                record.append(nextMove)
                print("Next Move:",nextMove,currentPlayer)
                if nextMove[0] == -1:
                    # 全堵死了
                    # 找不到可以走的位置了，GameOver
                    break

                game.steps += 1
                result = game.DoMove(nextMove=nextMove, playerColor=currentPlayer.playerColor)

                if result:
                    # 赢棋了
                    if status == GameStatus.BLACK:
                        gameResult = MatchResult.BLACKWIN
                    else:
                        gameResult = MatchResult.WHITEWIN
                    break

                if status == GameStatus.BLACK:
                    status = GameStatus.WHITE
                    currentPlayer = player2
                else:
                    status = GameStatus.BLACK
                    currentPlayer = player1

            records.append(record)
            if (i+1) % fileSize == 0:
                with open(f"data{i+1}.pkl", 'wb') as f:
                    pickle.dump(records, f)
                records.clear()


    def DoTest1(self):
        #player1 = RobotCheckersRandom01(PlayerColor.BLACK, 0.8)
        player1 = RobotCheckersRandom01(PlayerColor.BLACK, 0.9)
        player2 = RobotCheckersRating(PlayerColor.WHITE)

        pool = AutoRobotArenaPool(player1=player1, player2=player2, game=GameCheckers(), board=None, beginColor=PlayerColor.BLACK,
                                   processNumber=10, taskNumber=20)
        bw, ww, draw = pool.DoMatch()

        print("Test result: Black Win:", bw, "White Win:", ww, "Draw:",draw)

    def DoTestBundle(self):
        player1 = RobotCheckersRandom01(PlayerColor.BLACK, 0.8)
        player2 = RobotCheckersRandom01(PlayerColor.WHITE, 0.8)

        for i in range(80, 101):
            rate2 = i/100

            player2.rate = rate2
            pool = AutoRobotArenaPool(player1=player1, player2=player2, game=GameCheckers(), board=None, beginColor=PlayerColor.BLACK,
                                       processNumber=10, taskNumber=1000)
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

        #self.DoTest1()
        # self.DoTestBundle()
        self.DoGenerateGame()
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

    def LoadData(self):
        # 从文件中读取
        with open('data10.pkl', 'rb') as f:
            records = pickle.load(f)
        print("Records:",len(records))
        for record in records:
            print("Record:",len(record))

class Checkers():
    def __init__(self):
        pass

    def StartGame(self):
        app = QApplication(sys.argv)
        ex = MainWindow()
        sys.exit(app.exec_())