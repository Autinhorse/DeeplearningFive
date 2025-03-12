import copy

from GameCheckers.GameCheckers import GameCheckers
from GameCheckers.RobotCheckers.RobotCheckersRandom01 import RobotCheckersRandom01
from RobotArena.AutoRobotArena import MatchResult
from RobotArena.AutoRobotArenaPool import AutoRobotArenaPool
from GameCheckers.RobotCheckers.RobotCheckersBase import RobotCheckersBase, PlayerColor
import multiprocessing
import time

from GameFive.RobotFive.RobotFiveRandom03 import RobotFiveRandom03
from RobotArena.RobotFactory import RobotType


class RobotCheckersMCTS(RobotCheckersBase):
    def __init__(self, color):
        super().__init__(color)
        self.distance = 1   # 下一步必须下在距离已经有的棋子多远的位置
        self.tryNumber = 50
        self.type = RobotType.CheckersMCTS

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

        # 蒙特卡罗算法，对于每一个可能的选择，随机试下tryNumber盘，评估每一个点的质量
        # 因为计算需要时间比较久，启动另外一个进程并行计算
        board = copy.deepcopy(self.game.board)

        if self.useThread:
            p = multiprocessing.Process(target=self.worker,args=(self.result,board,self.pos,self.playerColor,self.tryNumber,True))
            p.start()
        else:
            RobotCheckersMCTS.worker(result=self.result,board=board,pos=self.pos,playerColor=self.playerColor,tryNumber=self.tryNumber,useThread=False)

    @staticmethod
    def worker(result,board,pos,playerColor,tryNumber,useThread):
        print("Worker process started:", pos)
        start_time = time.time()

        bestMove, bestRate = None, -1
        player1 = RobotCheckersRandom01(PlayerColor.BLACK,0.8)
        player2 = RobotCheckersRandom01(PlayerColor.WHITE,0.8)

        # 这里创建一个游戏的目的实际就是利用DoMova函数判断一下是不是这步就赢了
        game = GameCheckers()
        player1.game = game
        player2.game = game

        bestRate = -1000000
        bestMove = None

        for move in pos:
            game.SetBoard(copy.deepcopy(board))
            game.ResetData()

            isWin = game.DoMove(nextMove=move,playerColor=playerColor)
            if isWin:
                # 这个点赢了，直接退出
                bestMove = move
                break
            bw, ww, draw = 0, 0, 0
            if useThread:
                # 调用线程池模拟继续下
                pool = AutoRobotArenaPool(player1=player1, player2=player2, game=GameCheckers(), board=board, beginColor=playerColor,
                                          processNumber=1, taskNumber=tryNumber)
                bw, ww, draw = pool.DoMatch()
            else:
                print("Try next move:", move, tryNumber)
                tempBoard = copy.deepcopy(game.board)

                for i in range(tryNumber):
                    game.SetBoard(copy.deepcopy(tempBoard))
                    game.ResetData()

                    # 注意这里currentColor和playerColor是反的，因为在外面已经替playerColor走了一步了。
                    currentColor = PlayerColor.WHITE if playerColor == PlayerColor.BLACK else PlayerColor.BLACK
                    currentPlayer = player2 if playerColor == PlayerColor.BLACK else player2

                    currentPlayer.CalculateNextMove()
                    result1 = MatchResult.DRAW
                    while True:
                        nextMove = currentPlayer.GetNextMove()
                        if nextMove is None:
                            # 还没影结果
                            continue

                        if nextMove[0] == -1:
                            # 无棋可走
                            # print("Set Draw")
                            result1 = MatchResult.DRAW
                            break

                        result1 = game.DoMove(nextMove=nextMove, playerColor=currentPlayer.playerColor)
                        # print("Step:",self.game.steps,"Pos:",y,x,"Color:",self.currentPlayer.playerColor)
                        if result1:
                            # 赢棋了
                            if currentColor == PlayerColor.BLACK:
                                result1 = MatchResult.BLACKWIN
                            else:
                                result1 = MatchResult.WHITEWIN
                            break

                        if currentColor == PlayerColor.BLACK:
                            currentColor = PlayerColor.WHITE
                            currentPlayer = player2
                        else:
                            currentColor = PlayerColor.BLACK
                            currentPlayer = player1
                        currentPlayer.CalculateNextMove()
                    time.sleep(0.1)

                    if result1 == MatchResult.DRAW:
                       draw += 1
                    elif result1 == MatchResult.BLACKWIN:
                       bw += 1
                    else:
                        ww += 1

            if bw !=0 and ww !=0:
                rate = bw / ww if playerColor == PlayerColor.BLACK else ww / bw
            else:
                rate = 0
            print("Move:",move,rate)
            if rate > bestRate:
                bestRate = rate
                bestMove = move
                print("Is Best Rate:", bestMove)

            result['result'] = bestMove

        print("Final Best Move:", bestMove, result['result'], bestRate)

        end_time = time.time()
        #print(f"Worker process finished and set the event   ⏳总耗时：{end_time - start_time:.2f} 秒")

    def GetNextMove(self):
        return self.result['result']