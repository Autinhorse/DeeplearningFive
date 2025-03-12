from GameCheckers.RobotCheckers.RobotCheckersBase import RobotCheckersBase, PlayerColor
import random

from RobotArena.RobotFactory import RobotType


class RobotCheckersRandom01(RobotCheckersBase):
    def __init__(self, color, rate):
        super().__init__(color)
        self.type = RobotType.CheckersRandom01
        self.rate = rate

    def CalculateNextMove(self):
        #print("RobotCheckersRandom01:CalculateNextMove")
        self.nextMove = None # -2, -2 表示还没有计算出结果
        # print("CalculateNextMove:",self.nextMove)

        """ 由子类实现的具体下棋逻辑 """
        pos = self.GetAllPossibleMove()

        if len(pos)==0:
            # 正常下棋是不会有平局的，但是机器下，可能完全堵死
            self.nextMove = (-1,-1,-1,-1)
            return

        pos1 = []
        pos2 = []
        for item in pos:
            if abs(item[0]-item[2])==2:
                pos2.append(item)
            else:
                pos1.append(item)

        #print(len(pos2),len(pos1))
        if len(pos2)>0 and random.randint(0,10000) < self.rate*10000:
            self.nextMove = pos2[random.randint(0, len(pos2) - 1)]
        elif len(pos1)>0:
            self.nextMove = pos1[random.randint(0, len(pos1) - 1)]
        else:
            self.nextMove = pos2[random.randint(0, len(pos2) - 1)]


        # 随机算法01，在所有可能的点中随机选一个
        # self.nextMove = pos[random.randint(0, len(pos)-1)]



