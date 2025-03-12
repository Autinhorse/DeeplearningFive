import copy
import time

from GameCheckers.GameCheckers import GameCheckers
from GameFive.GameFive import GameFive
from enum import Enum

from GameFive.RobotFive.RobotFiveBase import PlayerColor, RobotFiveBase
from RobotArena.RobotFactory import RobotFactory


class MatchResult(Enum):
    PLAYING = 0
    BLACKWIN = 1
    WHITEWIN = 2
    DRAW = 3

class AutoPlayerArena:
    def __init__(self, player1, player2,game,board=None, beginColor=PlayerColor.BLACK):
        self.player1 = RobotFactory.CopyRobot(player1)
        self.player2 = RobotFactory.CopyRobot(player2)
        self.beginColor = beginColor
        self.currentColor = beginColor
        self.currentPlayer = player1 if beginColor == PlayerColor.BLACK else player2
        self.game = copy.deepcopy(game) #GameCheckers() #GameFive()

        self.player1.game = self.game
        self.player2.game = self.game
        self.board = board
        self.result = MatchResult.PLAYING

        self.count = 0

    def DoPlayAMatch(self):
        #start_time = time.time()
        records = []
        self.game.InitGame()
        if self.board is not None:
            self.game.board = copy.deepcopy(self.board)
            self.game.ResetData()
        self.currentColor = self.beginColor
        self.currentPlayer = self.player1 if self.beginColor == PlayerColor.BLACK else self.player2

        self.currentPlayer.CalculateNextMove()
        while True:
            nextMove = self.currentPlayer.GetNextMove()
            if nextMove is None:
                # 还没影结果
                continue
            if nextMove[0]==-1:
                # 无棋可走
                #print("Set Draw")
                self.result = MatchResult.DRAW
                break

            result = self.game.DoMove(nextMove=nextMove, playerColor=self.currentPlayer.playerColor)
            records.append((self.currentPlayer.playerColor,nextMove))
            self.game.steps += 1
            print("Step:",self.game.steps)
            print(records)
            # print("Step:",self.game.steps,"Pos:",y,x,"Color:",self.currentPlayer.playerColor)
            if result:
                # 赢棋了
                if self.currentColor == PlayerColor.BLACK:
                    self.result = MatchResult.BLACKWIN
                else:
                    self.result = MatchResult.WHITEWIN
                break

            if self.currentColor == PlayerColor.BLACK:
                self.currentColor = PlayerColor.WHITE
                self.currentPlayer = self.player2
            else:
                self.currentColor = PlayerColor.BLACK
                self.currentPlayer = self.player1
            self.currentPlayer.CalculateNextMove()
        #end_time = time.time()
        #print(f"\n🎉 所有任务计算完成！ ⏳总耗时：{end_time - start_time:.2f} 秒")
        # print("Complete a game!",self.count)

    def GetResult(self):
        # print("GetResult:",self.result)
        return self.result


