from Players.PlayerBase import PlayerBase


class PlayerHuman(PlayerBase):
    def __init__(self, color):
        super().__init__(color)
        self.isMachine = False

    def GetNextMove(self):
        """ 由子类实现的具体下棋逻辑 """
        pass