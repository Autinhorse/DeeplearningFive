from abc import ABC, abstractmethod
from enum import Enum, auto

class Player(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class PlayerBase(ABC):
    def __init__(self,playerColor):
        self.game = None
        self.playerColor = playerColor      # 1 执黑， 2 执白
        self.isMachine = True

    @abstractmethod
    def GetNextMove(self):
        """ 由子类实现的具体下棋逻辑 """
        pass

    def IsMachine(self):
        return self.isMachine

    def GetFirstMove(self):
        return 7,7

    def GetPossiblePos(self):
        print("GetPossiblePos")
        def manhattan_distance(x1, y1, x2, y2):
            return abs(x1 - x2) + abs(y1 - y2)

        def is_within_bounds(x, y, size):
            return 0 <= x < size and 0 <= y < size

        pos = []

        for y in range(self.game.size):
            for x in range(self.game.size):
                if self.game.boardDis[y][x] == 1 or self.game.boardDis[y][x] == 2:  # 当前位置是空位，并且2格以内有棋子
                    # print("Check:",y,x)
                    if self.playerColor == Player.BLACK:
                        # 执黑，需要判断禁手
                        self.game.board[y][x] = Player.BLACK  # 先在这个位置放上黑子
                        isForbidden = self.IsBlackForbidden(y=y, x=x)
                        self.game.board[y][x] = Player.EMPTY  # 取走刚刚放的黑子
                        if isForbidden:
                            # 黑棋的禁手，跳过
                            print("Forbidden:", y, x)
                            continue

                    # 是可能下子的位置
                    pos.append(((x, y), self.game.boardDis[y][x]))

        return pos

    # 这个函数判断一个位置对黑是不是禁手
    # 这里判断禁手的算法有一个缺陷。就是在判断禁手的时候，某些空位可能已经是禁手了，在后面这些位置应该被当作堵死不能下子的位置而不是空位的。
    # 但是这样禁手位置判断的前后顺序就会对结果产生影响，甚至必须反复判断几轮才能确定。这个开销比较大。
    # 因为我们主要是学习机器学习算法，这里就不搞这么复杂了，把常见禁手判断出来就好。这个问题会造成把一些不应该是禁手的位置判断成禁手，而不是
    # 反过来。所以不会下错。先这样吧。
    def IsBlackForbidden(self,x,y):
        # 判断禁手的标准比较复杂
        dir = [(0,-1),(-1,-1),(-1,0),(1,-1)]     # 搜索的四个方向

        if y == 8 and x == 5:
            test = 0
            test += 1
        # 先判断赢棋和长连
        # print("Check long link.")
        isMoreThanFive = False
        for i in range(4):
            length = 1
            # 先逆向找到连续黑子棋子的开头
            deltay, deltax = dir[i]
            ny, nx = y, x
            while True:
                ny += deltay
                nx += deltax
                if ny<0 or ny>=self.game.size or nx < 0 or nx >= self.game.size:
                    break
                if self.game.board[ny][nx]!=1:
                    # 这个位置不是黑子了
                    break
                length += 1
            ny, nx = y, x
            # 再顺方向查找
            while True:
                ny -= deltay
                nx -= deltax
                if ny < 0 or ny >= self.game.size or nx < 0 or nx >= self.game.size:
                    break
                if self.game.board[ny][nx] != Player.BLACK:
                    # 这个位置不是黑子了
                    break
                length += 1

            if length == 5:
                # 根据规则，只要能构成刚好5个，则是赢棋，不是禁手
                return False
            if length>5:
                # 先记录，防止其他方向上有刚好5个，造成赢棋
                isMoreThanFive = True
        if isMoreThanFive:
            return True

        # 然后判断双4
        # print("Check double link 4.")
        count4 = 0
        count4Dir = []
        models = [[1,1,0,1,1,0,1,1],[0,1,1,1,1],[1,1,1,1,0],[1,1,0,1,1],[1,1,1,0,1],[1,0,1,1,1]]
        for i in range(4):
            # 先逆向找到连续黑子棋子的开头
            deltay, deltax = dir[i]
            ny, nx = y, x
            pattern = []
            for j in range(-4, 5):
                pattern.append(self.game.GetPieceOnPos(y=y-deltay*j, x=x-deltax*j))
            for j in range(0, len(models)):
                model = models[j]
                match4 = False
                for k in range(0, 10-len(model)):
                    match = True
                    for l in range(0, len(model)):
                        if pattern[k+l]!=model[l]:
                            match = False
                            break
                    if match:
                        if j==0:
                            # 如果是第一个，表示在一行上完成了双4，直接禁手
                            return True
                        else:
                            match4 = True
                if match4:
                    # 匹配到了活4
                    count4 += 1
                    count4Dir.append(i)
                    break
        if count4>1:
            # 检测到了两个以上的活4
            return True

        # 然后判断双3
        # print("Check double link 3.")
        count3 = 0
        models = [[0, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0], [0, 1, 0, 1, 1, 0], [0, 1, 1, 0, 1, 0]]

        for i in range(4):
            if i in count4Dir:
                # 在这个方向上已经发现了活4，不需要再判断活3了（会重复判断）
                continue
            # 先逆向找到连续黑子棋子的开头
            deltay, deltax = dir[i]
            ny, nx = y, x
            pattern = []
            for j in range(-4, 5):
                pattern.append(self.game.GetPieceOnPos(y=y - deltay * j, x=x - deltax * j))
            for j in range(0, len(models)):
                model = models[j]
                match3 = False
                for k in range(0, 10 - len(model)):
                    match = True
                    for l in range(0, len(model)):
                        if pattern[k + l] != model[l]:
                            match = False
                            break
                    if match:
                        match3 = True
                        break

                if match3:
                    # 匹配到了活4
                    count3 += 1
                    break
        if count3 > 1:
            # 检测到了两个以上的活4
            return True

        return False