from Players.PlayerBase import RobotBase, RobotType


class RobotHuman(RobotBase):
    def __init__(self, color):
        super().__init__(color)
        self.isMachine = False
        self.uiBoard = None
        self.type = RobotType.Human

    def CalculateNextMove(self):
        """ 由子类实现的具体下棋逻辑 """
        self.nextMove = (-2, -2)