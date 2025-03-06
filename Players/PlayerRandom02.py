from Players.PlayerBase import PlayerBase, Player
import random

class PlayerRandom02(PlayerBase):
    def __init__(self, color):
        super().__init__(color)

    def GetNextMove(self):

        if self.playerColor==Player.BLACK and self.game.steps == 0:
            # 是第一步开局，走在中心
            return 7, 7

        """ 由子类实现的具体下棋逻辑 """
        pos = self.GetPossiblePos()
        print("GetNextMove:", len(pos))
        if len(pos)==0:
            # 没找到可以走的位置，结束
            return -1, -1

        # 随机算法02
        # 因为返回的可能的点中，有间隔1和间隔2的，一般逻辑，挨着下比跳着下多一些，所以这里调整概率
        # 80%概率下在一个格子远的位置，20%概率下在两个格子远的位置。这里额80%和20%是拍脑袋想出来的。后面会研究怎么用算法评估。
        (x,y), dis = pos[random.randint(0, len(pos)-1)]

        return x, y

        # print("Result:", len(pos))
        # for (x,y),d in pos:
        #    print(y,x,d)


