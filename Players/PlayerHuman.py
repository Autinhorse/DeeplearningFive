from Players.PlayerBase import PlayerBase


class PlayerHuman(PlayerBase):
    def __init__(self, color):
        super().__init__(color)
        self.isMachine = False
        self.uiBoard = None

    def CalculateNextMove(self):
        """ 由子类实现的具体下棋逻辑 """
        self.nextMove = (-2, -2)