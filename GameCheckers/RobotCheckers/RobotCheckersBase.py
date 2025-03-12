import copy
from abc import ABC, abstractmethod
from enum import Enum


class PlayerColor(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class PieceType(Enum):
    Empty = 0
    WhiteNormal = 1
    WhiteKing = 2
    BlackNormal = 3
    BlackKing = 4



class RobotCheckersBase(ABC):

    def __init__(self,playerColor):
        self.game = None
        self.playerColor = playerColor      # 1 执黑， 2 执白
        self.isMachine = True
        self.nextMove = None

        self.type = None

    @abstractmethod
    def CalculateNextMove(self):
        """ 由子类实现的具体下棋逻辑 """
        pass

    def GetNextMove(self):
        return self.nextMove

    def IsMachine(self):
        return self.isMachine

    def GetWhiteEatChain(self,y,x,chain,pos):
        if x > 1 and y > 1:
            if (self.game.board[y - 1][x - 1] == PieceType.BlackKing or self.game.board[y - 1][
                x - 1] == PieceType.BlackNormal) \
                    and self.game.board[y - 2][x - 2] == PieceType.Empty:
                # 左下吃子
                if (y - 2, x - 2) not in chain:
                    newChain = copy.deepcopy(chain)
                    newChain += (y - 2, x - 2)
                    pos.append(newChain)
                    self.GetWhiteEatChain( y=y-2, x=x-2, chain=newChain, pos=pos)

        if x < self.game.size - 2 and y > 1:
            if (self.game.board[y - 1][x + 1] == PieceType.BlackKing or self.game.board[y - 1][
                x + 1] == PieceType.BlackNormal) \
                    and self.game.board[y - 2][x + 2] == PieceType.Empty:
                # 左下吃子
                if (y - 2, x + 2) not in chain:
                    newChain = copy.deepcopy(chain)
                    newChain += (y - 2, x + 2)
                    pos.append(newChain)
                    self.GetWhiteEatChain(y=y - 2, x=x + 2, chain=newChain, pos=pos)

        if self.game.board[y][x] == PieceType.WhiteKing and y < 6:
            if x > 1:
                if (self.game.board[y + 1][x - 1] == PieceType.BlackKing or self.game.board[y + 1][
                    x - 1] == PieceType.BlackNormal) \
                        and self.game.board[y + 2][x - 2] == PieceType.Empty:
                    # 左下吃子
                    if (y + 2, x - 2) not in chain:
                        newChain = copy.deepcopy(chain)
                        newChain += (y + 2, x - 2)
                        pos.append(newChain)
                        self.GetWhiteEatChain(y=y + 2, x=x - 2, chain=newChain, pos=pos)

            if x < self.game.size - 2:
                if (self.game.board[y + 1][x + 1] == PieceType.BlackKing or self.game.board[y + 1][
                    x + 1] == PieceType.BlackNormal) \
                        and self.game.board[y + 2][x + 2] == PieceType.Empty:
                    # 左下吃子
                    if (y + 2, x + 2) not in chain:
                        newChain = copy.deepcopy(chain)
                        newChain += (y + 2, x + 2)
                        pos.append(newChain)
                        self.GetWhiteEatChain(y=y + 2, x=x + 2, chain=newChain, pos=pos)

    def GetBlackEatChain(self, y, x, chain, pos):
        if x > 1 and y < 6:
            if (self.game.board[y + 1][x - 1] == PieceType.WhiteKing or self.game.board[y + 1][
                x - 1] == PieceType.WhiteNormal) \
                    and self.game.board[y + 2][x - 2] == PieceType.Empty:
                # 左下吃子
                if (y + 2, x - 2) not in chain:
                    newChain = copy.deepcopy(chain)
                    newChain += (y + 2, x - 2)
                    pos.append(newChain)
                    self.GetBlackEatChain(y=y + 2, x=x - 2, chain=newChain, pos=pos)

        if x < self.game.size - 2 and y < 6:
            if (self.game.board[y + 1][x + 1] == PieceType.WhiteKing or self.game.board[y + 1][
                x + 1] == PieceType.WhiteNormal) \
                    and self.game.board[y + 2][x + 2] == PieceType.Empty:
                # 左下吃子
                if (y + 2, x + 2) not in chain:
                    newChain = copy.deepcopy(chain)
                    newChain += (y + 2, x + 2)
                    pos.append(newChain)
                    self.GetBlackEatChain(y=y + 2, x=x + 2, chain=newChain, pos=pos)

        if self.game.board[y][x] == PieceType.BlackKing and y != 0:
            if x > 1 and y>1:
                if (self.game.board[y - 1][x - 1] == PieceType.WhiteKing or self.game.board[y - 1][x - 1] == PieceType.WhiteNormal )\
                        and self.game.board[y - 2][x - 2] == PieceType.Empty:
                    # 左下吃子
                    if (y - 2, x - 2) not in chain:
                        newChain = copy.deepcopy(chain)
                        newChain += (y - 2, x - 2)
                        pos.append(newChain)
                        self.GetBlackEatChain(y=y - 2, x=x - 2, chain=newChain, pos=pos)

            if x <self.game.size-2 and y > 1:
                if (self.game.board[y - 1][x + 1] == PieceType.WhiteKing or self.game.board[y - 1][
                    x + 1] == PieceType.WhiteNormal) \
                        and self.game.board[y - 2][x + 2] == PieceType.Empty:
                    # 左下吃子
                    if (y - 2, x + 2) not in chain:
                        newChain = copy.deepcopy(chain)
                        newChain += (y - 2, x + 2)
                        pos.append(newChain)
                        self.GetBlackEatChain(y=y - 2, x=x + 2, chain=newChain, pos=pos)

    # 查找一个棋子可能走的位置
    def GetPossibleMoveOfPiece(self, y, x):
        pos = []

        if (self.game.board[y][x]==PieceType.WhiteNormal or self.game.board[y][x]==PieceType.WhiteKing) and y!=0:
            # 向下走
            if x>0:
                if self.game.board[y-1][x-1]==PieceType.Empty:
                    # 左下
                    pos.append((y-1, x-1))
            if x<self.game.size-1:
                if self.game.board[y-1][x+1]==PieceType.Empty:
                    # 左下
                    pos.append((y-1, x+1))
            chain=()
            self.GetWhiteEatChain(y=y,x=x,chain=chain,pos=pos)

        if self.game.board[y][x]==PieceType.WhiteKing and y!=7:
            # 国王可以往回走
            if x>0:
                if self.game.board[y+1][x-1]==PieceType.Empty:
                    # 左下
                    pos.append((y+1, x-1))
            if x<self.game.size-1:
                if self.game.board[y+1][x+1]==PieceType.Empty:
                    # 左下
                    pos.append((y+1, x+1))

            chain = ()
            self.GetWhiteEatChain(y=y, x=x, chain=chain, pos=pos)

        if (self.game.board[y][x]==PieceType.BlackNormal or self.game.board[y][x]==PieceType.BlackKing) and y!=7:
            # 向下走
            if x>0:
                if self.game.board[y+1][x-1]==PieceType.Empty:
                    # 左下
                    pos.append((y+1, x-1))
            if x<self.game.size-1:
                if self.game.board[y+1][x+1]==PieceType.Empty:
                    # 左下
                    pos.append((y+1, x+1))
            chain = ()
            self.GetBlackEatChain(y=y, x=x, chain=chain, pos=pos)

        if self.game.board[y][x]==PieceType.BlackKing and y!=0:
            # 国王可以往回走
            if x>0:
                if self.game.board[y-1][x-1]==PieceType.Empty:
                    # 左下
                    pos.append((y-1, x-1))
            if x<self.game.size-1:
                if self.game.board[y-1][x+1]==PieceType.Empty:
                    # 左下
                    pos.append((y-1, x+1))
            chain = ()
            self.GetBlackEatChain(y=y, x=x, chain=chain, pos=pos)
        return pos

    def GetAllPossibleMove(self):
        result = []
        #print("GetAllPossibleMove:",self.playerColor)
        if self.playerColor is PlayerColor.BLACK:
            for y,x in self.game.blackPieces:
                pos = self.GetPossibleMoveOfPiece(y,x)
                for item in pos:
                    item = (y,x)+item
                    if item not in result:
                        result.append(item)
        else:
            for y, x in self.game.whitePieces:
                pos = self.GetPossibleMoveOfPiece(y, x)
                for item in pos:
                    item = (y,x)+item
                    if item not in result:
                        result.append(item)

        #("All Possible Result:",result)
        return result
