
from enum import Enum
import copy



class RobotType(Enum):
    FiveHuman = 0
    FiveRandom01 = 1
    FiveRandom02 = 2
    FiveRandom03 = 3
    FiveMCTS    = 4

    CheckersHuman = 20
    CheckersRandom01 = 21
    CheckersMCTS = 22
    CheckersRating = 23

class RobotFactory:
    @staticmethod
    def CopyRobot(robot):
        from GameFive.RobotFive.FiveHuman import RobotFiveHuman
        from GameFive.RobotFive.RobotFiveMCTS import RobotFiveMCTS
        from GameFive.RobotFive.RobotFiveRandom01 import RobotFiveRandom01
        from GameFive.RobotFive.RobotFiveRandom02 import RobotFiveRandom02
        from GameFive.RobotFive.RobotFiveRandom03 import RobotFiveRandom03
        from GameCheckers.RobotCheckers.RobotCheckersHuman import RobotCheckersHuman
        from GameCheckers.RobotCheckers.RobotCheckersMCTS import RobotCheckersMCTS
        from GameCheckers.RobotCheckers.RobotCheckersRandom01 import RobotCheckersRandom01
        from GameCheckers.RobotCheckers.RobotCheckersRating import RobotCheckersRating

        newRobot = None
        if robot.type == RobotType.FiveHuman:
            newRobot = RobotFiveHuman(robot.playerColor)
        elif robot.type == RobotType.FiveMCTS:
            newRobot = RobotFiveMCTS(robot.playerColor)
        elif robot.type == RobotType.FiveRandom01:
            newRobot = RobotFiveRandom01(robot.playerColor)
        elif robot.type == RobotType.FiveRandom02:
            newRobot = RobotFiveRandom02(robot.playerColor)
            newRobot.rate = robot.rate
        elif robot.type == RobotType.FiveRandom03:
            newRobot = RobotFiveRandom03(robot.playerColor)
        elif robot.type == RobotType.CheckersHuman:
            newRobot = RobotCheckersHuman(robot.playerColor)
        elif robot.type == RobotType.CheckersRandom01:
            newRobot = RobotCheckersRandom01(color=robot.playerColor,rate=robot.rate)
        elif robot.type == RobotType.CheckersMCTS:
            newRobot = RobotCheckersMCTS(robot.playerColor)
        elif robot.type  == RobotType.CheckersRating:
            newRobot = RobotCheckersRating(robot.playerColor)
        return newRobot

    def CreateRobot(robotType,playerColor):
        from GameFive.RobotFive.FiveHuman import RobotFiveHuman
        from GameFive.RobotFive.RobotFiveMCTS import RobotFiveMCTS
        from GameFive.RobotFive.RobotFiveRandom01 import RobotFiveRandom01
        from GameFive.RobotFive.RobotFiveRandom02 import RobotFiveRandom02
        from GameFive.RobotFive.RobotFiveRandom03 import RobotFiveRandom03
        from GameCheckers.RobotCheckers.RobotCheckersHuman import RobotCheckersHuman
        from GameCheckers.RobotCheckers.RobotCheckersMCTS import RobotCheckersMCTS
        from GameCheckers.RobotCheckers.RobotCheckersRandom01 import RobotCheckersRandom01
        from GameCheckers.RobotCheckers.RobotCheckersRating import RobotCheckersRating

        newRobot = None
        if robotType == RobotType.FiveHuman:
            newRobot = RobotFiveHuman(playerColor)
        elif robotType == RobotType.FiveMCTS:
            newRobot = RobotFiveMCTS(playerColor)
        elif robotType == RobotType.FiveRandom01:
            newRobot = RobotFiveRandom01(playerColor)
        elif robotType == RobotType.FiveRandom02:
            newRobot = RobotFiveRandom02(playerColor)
            newRobot.rate = 0.8
        elif robotType == RobotType.FiveRandom03:
            newRobot = RobotFiveRandom03(playerColor)
        elif robotType == RobotType.CheckersHuman:
            newRobot = RobotCheckersHuman(playerColor)
        elif robotType == RobotType.CheckersRandom01:
            newRobot = RobotCheckersRandom01(color=playerColor,rate=0.8)
        elif robotType == RobotType.CheckersMCTS:
            newRobot = RobotCheckersMCTS(playerColor)
        elif robotType == RobotType.CheckersRating:
            newRobot = RobotCheckersRating(playerColor)
        return newRobot