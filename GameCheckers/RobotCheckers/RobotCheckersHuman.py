from GameCheckers.RobotCheckers.RobotCheckersBase import RobotCheckersBase
from RobotArena.RobotFactory import RobotType


class RobotCheckersHuman(RobotCheckersBase):
    def __init__(self, color):
        super().__init__(color)
        self.isMachine = False
        self.uiBoard = None
        self.type = RobotType.CheckersHuman

    def CalculateNextMove(self):
        """ 由子类实现的具体下棋逻辑 """
        self.nextMove = None