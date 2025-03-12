import json

from GameCheckers.RobotCheckers.RobotCheckersBase import PieceType
from GameCheckers.RobotCheckers.RobotCheckersBase import PlayerColor


class GameCheckers:
    def __init__(self, size=8):
        self.steps = 0
        self.size = size
        self.current_player = None
        self.board = None
        self.blackPieces = []
        self.whitePieces = []
        self.InitGame()

        self.record = []

    # 下子，坐标x,y。
    # 返回值True，表示赢了，棋局结束。False表示还需要继续下。
    def DoMove(self, nextMove, playerColor):
        #print("DoMove:",playerColor,nextMove,len(nextMove))
        self.steps += 1
        y = nextMove[0]
        x = nextMove[1]
        i = 1
        while i*2<len(nextMove):
            ty = nextMove[i*2]
            tx = nextMove[i*2+1]
            #print("MoevTo:",i,y,x,ty,tx)
            # 移动棋子
            self.board[ty][tx] = self.board[y][x]
            if self.board[ty][tx] == PieceType.BlackNormal or self.board[ty][tx]==PieceType.BlackKing:
                self.blackPieces.remove((y,x))
                self.blackPieces.append((ty,tx))
            else:
                self.whitePieces.remove((y,x))
                self.whitePieces.append((ty,tx))

            if self.board[ty][tx]==PieceType.BlackNormal and ty==7:
                self.board[ty][tx] = PieceType.BlackKing
            if self.board[ty][tx] == PieceType.WhiteNormal and ty == 0:
                self.board[ty][tx] = PieceType.WhiteKing
            self.board[y][x] = PieceType.Empty

            # 判断吃子
            if abs(ty - y) == 2:
                # 走了两个格子，说明吃子了
                my = y + 1 if ty > y else y - 1
                mx = x + 1 if tx > x else x - 1
                self.board[my][mx] = PieceType.Empty
                targetPieces = self.whitePieces if playerColor == PlayerColor.BLACK else self.blackPieces
                targetPieces.remove((my, mx))
                if len(targetPieces) == 0:
                    return True

            y, x = ty, tx
            i += 1



        return False

    def GetPieceOnPos(self, y, x):
        if y < 0 or y >= self.size or x < 0 or x >= self.size:
            return -1
        return self.board[y][x]

    def InitGame(self):
        # print("InitGame")
        # 这个是棋盘的数据，0表示空，1表示黑棋，2表示白棋
        self.board = [[PieceType.Empty] * self.size for _ in range(self.size)]
        self.blackPieces.clear()
        self.whitePieces.clear()
        for i in range(3):
            for j in range(0,8,2):
                self.board[i][j+(1-i%2)] = PieceType.BlackNormal
                self.blackPieces.append((i,j+(1-i%2)))
                self.board[7-i][7-j-(1-i%2)] = PieceType.WhiteNormal
                self.whitePieces.append((7-i,7-j-(1-i%2)))

        self.current_player = PlayerColor.BLACK  # 当前玩家，1为黑棋，2为白棋

        self.steps = 0  # 记录步数

    def SetBoard(self, board):
        self.board = board
        self.ResetData()

    def SaveGame(self):
        print("Save Game")
        data = {
            'size': self.size,
            'board': self.board
        }
        with open('../gamedata.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def LoadGame(self):
        print("Load Game")
        try:
            with open('../gamedata.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.size = data['size']
            self.board = data['board']
            self.ResetData()
            print("Board Size:", self.size)
            print("board:", len(self.board))

            # self.ResetDisData()

        except FileNotFoundError:
            print("Error: The file 'gamedata.json' was not found.")
        except json.JSONDecodeError:
            print("Error: The file 'gamedata.json' is not a valid JSON file.")
        except KeyError as e:
            print(f"Error: Missing key {e} in the JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def ResetData(self):
        self.blackPieces.clear()
        self.whitePieces.clear()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == PieceType.BlackNormal or self.board[i][j] == PieceType.BlackKing:
                    self.blackPieces.append((i, j))
                if self.board[i][j] == PieceType.WhiteNormal or self.board[i][j] == PieceType.WhiteKing:
                    self.whitePieces.append((i, j))
        self.steps = len(self.blackPieces) + len(self.whitePieces)


