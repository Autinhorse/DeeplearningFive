from GameFive.RobotFive.RobotFiveBase import RobotFiveBase
from RobotArena.RobotFactory import RobotType


class RobotFiveHuman(RobotFiveBase):
    def __init__(self, color):
        super().__init__(color)
        self.isMachine = False
        self.uiBoard = None
        self.type = RobotType.FiveHuman

    def CalculateNextMove(self):
        """ 由子类实现的具体下棋逻辑 """
        self.nextMove = (-2, -2)