import copy
import random

from GameCheckers.GameCheckers import GameCheckers
from GameCheckers.RobotCheckers.RobotCheckersRandom01 import RobotCheckersRandom01
from GameCheckers.RobotCheckers.RobotCheckersBase import RobotCheckersBase, PlayerColor, PieceType
import multiprocessing
import time

from GameFive.RobotFive.RobotFiveRandom03 import RobotFiveRandom03
from RobotArena.RobotFactory import RobotType


class RobotCheckersRating(RobotCheckersBase):
    def __init__(self, color):
        super().__init__(color)
        self.distance = 1   # 下一步必须下在距离已经有的棋子多远的位置
        self.type = RobotType.CheckersRating

        self.pos = None

        self.name = "PlayerMCTS"

        self.useThread = False
        if self.useThread:
            self.manager = multiprocessing.Manager()
            self.result = self.manager.dict()  # 用于存储进程处理后的结果
            self.result['result'] = None
        else:
            self.manager = None
            self.result = {}
            self.result["result"] = []


    def CalculateNextMove(self):
        # -2, -2 表示还没有计算出结果
        self.result['result'] = None

        """ 由子类实现的具体下棋逻辑 """
        self.pos = self.GetAllPossibleMove()

        if len(self.pos)==0:
            # 没找到可以走的位置，结束
            self.result['result'] = (-1,-1,-1,-1)
            return

        # 评估函数，对于每一个可能下的位置，对落子以后的局面使用评估函数进行评估，找出最优选择。
        # 可以发挥到评估N步以后的结果。这是传统AI下棋使用的方法。关键在于评估函数的质量。
        # 因为计算需要时间比较久，启动另外一个进程并行计算
        board = copy.deepcopy(self.game.board)

        if self.useThread:
            p = multiprocessing.Process(target=self.worker,args=(self.result,board,self.pos,self.playerColor,self.game.steps))
            p.start()
        else:
            RobotCheckersRating.worker(result=self.result,board=board,pos=self.pos,playerColor=self.playerColor,steps=self.game.steps)

    @staticmethod
    def worker(result,board,pos,playerColor,steps):
        rowValues = [0, 0, 1, 1, 2, 5, 10, 25]

        def GetRatingOfBoard():
            blackValue = 0
            whiteValue = 0

            def GetPieceType(y, x):
                if y < 0 or y > 7 or x < 0 or x > 7:
                    return None
                return game.board[y][x]
            value1 = 0
            for y, x in game.blackPieces:
                if game.board[y][x] == PieceType.BlackKing:
                    value1 = rowValues[7]
                else:
                    value1 = rowValues[y]
                leftUp = GetPieceType(y + 1, x - 1)
                rightUp = GetPieceType(y + 1, x + 1)
                leftDown = GetPieceType(y - 1, x - 1)
                rightDown = GetPieceType(y - 1, x + 1)
                if ((leftUp == PieceType.WhiteKing or leftUp == PieceType.WhiteNormal) and rightDown == PieceType.Empty) \
                        or ((rightUp == PieceType.WhiteKing or rightUp == PieceType.WhiteNormal) and leftDown == PieceType.Empty) \
                        or (leftUp == PieceType.Empty and rightDown == PieceType.WhiteKing) \
                        or (rightUp == PieceType.Empty and leftDown == PieceType.WhiteKing):
                    # 如果这个棋子可能被吃，则价值减半
                    value1 /= 2
                if x==0 or x==7:
                    value1 += 3
                blackValue += value1

            for y, x in game.whitePieces:
                if game.board[y][x] == PieceType.WhiteKing:
                    value1 = rowValues[7]
                else:
                    value1 = rowValues[7 - y]
                leftUp = GetPieceType(y - 1, x - 1)
                rightUp = GetPieceType(y - 1, x + 1)
                leftDown = GetPieceType(y + 1, x - 1)
                rightDown = GetPieceType(y + 1, x + 1)
                if ((leftUp == PieceType.BlackKing or leftUp == PieceType.BlackNormal) and rightDown == PieceType.Empty) \
                        or (
                        (
                                rightUp == PieceType.BlackKing or rightUp == PieceType.BlackNormal) and leftDown == PieceType.Empty) \
                        or (leftUp == PieceType.Empty and rightDown == PieceType.BlackKing) \
                        or (rightUp == PieceType.Empty and leftDown == PieceType.BlackKing):
                    # 如果这个棋子可能被吃，则价值减半
                    value1 /= 2
                if x==0 or x==7:
                    value1 += 3
                whiteValue += value1
            return blackValue - whiteValue
        # -----------------------------------------------------------------------------------------------------------------------------
        start_time = time.time()

        bestMove, bestRate = None, -1
        player1 = RobotCheckersRandom01(PlayerColor.BLACK,0.8)
        player2 = RobotCheckersRandom01(PlayerColor.WHITE,0.8)

        # 这里创建一个游戏的目的实际就是利用DoMova函数判断一下是不是这步就赢了
        game = GameCheckers()
        player1.game = game
        player2.game = game
        maxFlag = 1 if playerColor == PlayerColor.BLACK else -1

        maxValue = -1000000
        bestMove = None

        for nextMove in pos:
            game.SetBoard(copy.deepcopy(board))
            game.ResetData()

            isWin = game.DoMove(nextMove=nextMove,playerColor=playerColor)
            if isWin:
                # 这个点赢了，直接退出
                bestMove = nextMove
                break
            # 取得所有可能的走法
            # pos = player1.GetAllPossibleMove() if playerColor == PlayerColor.BLACK else player2.GetAllPossibleMove()

            value = GetRatingOfBoard()*maxFlag
            if value>maxValue:
                maxValue = value
                bestMove = nextMove

        rate = 0
        if steps>50:
            rate = 200
        if steps>75:
            rate = 400
        if steps>100:
            rate = 500
        if steps>150:
            rate = 600
        if steps>200:
            rate = 800
        if random.randint(0,1000)<rate:
            result['result'] = pos[random.randint(0,len(pos)-1)]
        else:
            result['result'] = bestMove
        end_time = time.time()
        #print(f"Worker process finished and set the event   ⏳总耗时：{end_time - start_time:.2f} 秒")



    def GetNextMove(self):
        return self.result['result']
