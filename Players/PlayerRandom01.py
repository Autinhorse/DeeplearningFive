from Players.PlayerBase import PlayerBase, Player
import random

class PlayerRandom01(PlayerBase):
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

        # 随机算法01，在所有可能的点中随机选一个
        (x,y), dis = pos[random.randint(0, len(pos)-1)]

        return x, y

        # print("Result:", len(pos))
        # for (x,y),d in pos:
        #    print(y,x,d)


