from GameFive.RobotFive.RobotFiveBase import RobotFiveBase, PlayerColor
import random

from RobotArena.RobotFactory import RobotType


class RobotFiveRandom01(RobotFiveBase):
    def __init__(self, color):
        super().__init__(color)
        self.distance = 2   # 下一步必须下在距离已经有的棋子多远的位置
        self.type = RobotType.FiveRandom01

    def CalculateNextMove(self):
        self.nextMove = (-2, -2) # -2, -2 表示还没有计算出结果
        # print("CalculateNextMove:",self.nextMove)

        if self.playerColor==PlayerColor.BLACK and self.game.steps == 0:
            # 是第一步开局，走在中心
            self.nextMove =  (7, 7)
            return

        """ 由子类实现的具体下棋逻辑 """
        pos = self.GetPossiblePos()

        if len(pos)==0:
            # 没找到可以走的位置，结束
            self.nextMove =  (-1, -1)
            return

        # 随机算法01，在所有可能的点中随机选一个
        self.nextMove, dis = pos[random.randint(0, len(pos)-1)]
        while self.playerColor == PlayerColor.BLACK:
            # 执黑，需要判断禁手
            y, x = self.nextMove
            self.calBoard[y][x] = PlayerColor.BLACK  # 先在这个位置放上黑子
            isForbidden = self.IsBlackForbidden(y=y, x=x)
            self.calBoard[y][x] = PlayerColor.EMPTY  # 取走刚刚放的黑子
            if not isForbidden:
                # 黑棋的禁手，跳过
                # print("Forbidden:", y, x)
                break
            if len(pos)==1:
                # 没找到可以走的位置，结束
                self.nextMove = (-1, -1)
                return
            # 再重新找一个位置
            self.nextMove, dis = pos[random.randint(0, len(pos) - 1)]


