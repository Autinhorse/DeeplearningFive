from Players.PlayerBase import RobotBase, PlayerColor, RobotType
import random

class RobotRandom02(RobotBase):
    def __init__(self, color):
        super().__init__(color)
        self.rate = 1.0
        self.distance = 2   # 下一步必须下在距离已经有的棋子多远的位置
        self.type = RobotType.Random02

    def CalculateNextMove(self):

        if self.playerColor==PlayerColor.BLACK and self.game.steps == 0:
            # 是第一步开局，走在中心
            self.nextMove =  (7, 7)
            return

        """ 由子类实现的具体下棋逻辑 """
        pos = self.GetPossiblePos()
        #print("GetNextMove:", len(pos))
        if len(pos)==0:
            # 没找到可以走的位置，结束
            self.nextMove = (-1, -1)
            return

        # 随机算法02
        # 因为返回的可能的点中，有间隔1和间隔2的，一般逻辑，挨着下比跳着下多一些，所以这里调整概率
        # 80%概率下在一个格子远的位置，20%概率下在两个格子远的位置。这里额80%和20%是拍脑袋想出来的。后面会研究怎么用算法评估。
        pos1 = []
        pos2 = []
        for (x,y),dis in pos:
            if dis == 1:
                pos1.append((x, y))
            else:
                pos2.append((x, y))
        if len(pos2)>0:
            if random.randint(0, 999) <= self.rate*1000:
                self.nextMove = pos1[random.randint(0, len(pos1)-1)]
            else:
                self.nextMove = pos2[random.randint(0, len(pos2) - 1)]
        else:
            self.nextMove = pos1[random.randint(0, len(pos1) - 1)]

        # print("NextPos:",self.nextMove, "Dis:", dis, "Color:",self.playerColor,"Rate:",self.rate)



