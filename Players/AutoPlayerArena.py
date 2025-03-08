import copy

from GameFive import GameFive
from enum import Enum

from Players.PlayerBase import PlayerColor, RobotBase


class MatchResult(Enum):
    PLAYING = 0
    BLACKWIN = 1
    WHITEWIN = 2
    DRAW = 3

class AutoPlayerArena:
    def __init__(self, player1, player2, board=None, beginColor=PlayerColor.BLACK):
        self.player1 = RobotBase.CopyRobot(player1)
        self.player2 = RobotBase.CopyRobot(player2)
        self.beginColor = beginColor
        self.currentColor = beginColor
        self.currentPlayer = player1 if beginColor == PlayerColor.BLACK else player2
        self.game = GameFive(15)

        self.player1.game = self.game
        self.player2.game = self.game
        self.board = board
        self.result = MatchResult.PLAYING

    def DoPlayAMatch(self):
        self.game.InitGame(size=15)
        if self.board is not None:
            self.game.board = copy.deepcopy(self.board)
            self.game.ResetDisData()
        self.currentColor = self.beginColor
        self.currentPlayer = self.player1 if self.beginColor == PlayerColor.BLACK else self.player2

        self.currentPlayer.CalculateNextMove()
        while True:
            x, y = self.currentPlayer.GetNextMove()
            if x==-2:
                # 还没影结果
                continue
            if x==-1:
                # 无棋可走
                print("Set Draw")
                self.result = MatchResult.DRAW
                break

            result = self.game.DoMove(x=x, y=y, playerColor=self.currentPlayer.playerColor)
            self.game.steps += 1
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

    def GetResult(self):
        # print("GetResult:",self.result)
        return self.result


