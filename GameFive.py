import json

from Players.PlayerBase import Player


class GameFive:
    def __init__(self,  size=15):
        self.steps = None
        self.current_player = None
        self.board = None
        self.size = None
        self.boardDis = None
        self.InitGame(size=size)

    # 下子，坐标x,y,
    def DoMove(self,x,y,playerColor):
        if self.board[y][x] !=Player.EMPTY:
            # 这个位置不是空的
            return

        # 落子
        self.board[y][x] = playerColor
        
        # 判断是否赢了
        direction = [(0, -1), (-1, -1), (-1, 0), (1, -1)]  # 搜索的四个方向
        for i in range(4):
            length = 1
            # 先逆向找到连续黑子棋子的开头
            deltay, deltax = direction[i]
            ny, nx = y, x
            while True:
                ny += deltay
                nx += deltax
                if ny < 0 or ny >= self.size or nx < 0 or nx >= self.size:
                    break
                if self.board[ny][nx] != playerColor:
                    # 这个位置不是相同棋子
                    break
                length += 1
            ny, nx = y, x
            # 再顺方向查找
            while True:
                ny -= deltay
                nx -= deltax
                if ny < 0 or ny >= self.size or nx < 0 or nx >= self.size:
                    break
                if self.board[ny][nx] != playerColor:
                    # 这个位置不是黑子了
                    break
                length += 1

            if length == 5:
                # 找到了连续的5个同颜色棋子，赢了
                return True

        # 修改周围空格信息
        for i in range(-2,3):
            if x+i<0 or x+i>=self.size:
                continue
            for j in range(-2,3):
                if y+j<0:
                    continue
                if y+j>=self.size:
                    break
                self.boardDis[y+j][x+i] = min(self.boardDis[y+j][x+i], max(abs(i),abs(j)))

        # 输出距离信息
        '''
        for i in range(self.size):
            for j in range(self.size):
                if self.boardDis[i][j]==100:
                    print(".",end='')
                elif self.boardDis[i][j]==0:
                    print("X", end='')
                elif self.boardDis[i][j]==1:
                    print("1", end='')
                elif self.boardDis[i][j] == 2:
                    print("2", end='')
            print("")
        '''
        return False

    def GetPieceOnPos(self,y,x):
        if y<0 or y>=self.size or x<0 or x>=self.size:
            return -1
        return self.board[y][x]

    def InitGame(self, size=15):
        self.size = size  # 棋盘大小，默认15x15

        # 这个是棋盘的数据，0表示空，1表示黑棋，2表示白棋
        self.board = [[Player.EMPTY] * size for _ in range(size)]

        # 因为希望将下的位置控制在已经有子的3格以内，但是如果每次都去判断哪些空位置周围3格以内有棋子算法开销过大
        # 所以使用了boardDis预处理数组，在每次下子的时候更新这个子周围的位置信息。
        # 初始化为100，每次下子，将下子位置更新为-1，然后更新周围7*7的矩形区域的空格位置，如果到这个棋子的距离更近，就更新数据
        self.boardDis = [[100] * size for _ in range(size)]
        self.current_player = 1  # 当前玩家，1为黑棋，2为白棋
        
        self.steps = 0  # 记录步数

    def SaveGame(self):
        print("Save Game")
        data = {
            'size': self.size,
            'board': self.board
        }
        with open('gamedata.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def LoadGame(self):
        print("Load Game")
        try:
            with open('gamedata.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.size = data['size']
            self.board = data['board']
            print("Board Size:",self.size)
            print("board:",len(self.board))

            self.ResetDisData()

        except FileNotFoundError:
            print("Error: The file 'gamedata.json' was not found.")
        except json.JSONDecodeError:
            print("Error: The file 'gamedata.json' is not a valid JSON file.")
        except KeyError as e:
            print(f"Error: Missing key {e} in the JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def ResetDisData(self):
        self.steps = 0
        # 修改周围空格信息
        self.boardDis = [[100 for _ in range(self.size)] for _ in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] != Player.EMPTY:
                    self.steps += 1
                    for i in range(-2, 3):
                        if x + i < 0 and x + i >= self.size:
                            continue
                        for j in range(-2, 3):
                            if y + j < 0:
                                continue
                            if y + j >= self.size:
                                break
                            self.boardDis[y + j][x + i] = min(self.boardDis[y + j][x + i], max(abs(i), abs(j)))
