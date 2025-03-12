import copy

from GameFive.GameFive import GameFive
from RobotArena.AutoRobotArenaPool import AutoRobotArenaPool
from GameFive.RobotFive.RobotFiveBase import RobotFiveBase, PlayerColor
import multiprocessing
import time

from GameFive.RobotFive.RobotFiveRandom03 import RobotFiveRandom03
from RobotArena.RobotFactory import RobotType


class RobotFiveMCTS(RobotFiveBase):
    def __init__(self, color):
        super().__init__(color)
        self.distance = 1   # 下一步必须下在距离已经有的棋子多远的位置
        self.tryNumber = 200
        self.type = RobotType.FiveMCTS

        self.done_event = multiprocessing.Event()

        self.pos = None

        self.name = "PlayerMCTS"

        self.manager = multiprocessing.Manager()
        self.result = self.manager.dict()  # 用于存储进程处理后的结果
        self.result['result'] = (-2,-2)


    def CalculateNextMove(self):
        # -2, -2 表示还没有计算出结果
        self.result['result'] = (-2,-2)

        if self.playerColor==PlayerColor.BLACK and self.game.steps == 0:
            # 是第一步开局，走在中心
            self.result['result'] = (7,7)
            return

        """ 由子类实现的具体下棋逻辑 """
        self.pos = self.GetPossiblePos()

        if len(self.pos)==0:
            # 没找到可以走的位置，结束
            self.result['result'] = (-1,-1)
            return

        # 蒙特卡罗算法，对于每一个可能的选择，随机试下tryNumber盘，评估每一个点的质量
        # 因为计算需要时间比较久，启动另外一个进程并行计算
        board = copy.deepcopy(self.game.board)

        #p = multiprocessing.Process(target=self.worker, args=(self.procResult,))
        p = multiprocessing.Process(target=self.worker,args=(self.result,board,self.pos,self.playerColor,self.tryNumber))

        p.start()

    @staticmethod
    def worker(result,board,pos,playerColor,tryNumber):

        start_time = time.time()

        bestX, bestY, bestRate = -1, -1, 0
        player1 = RobotFiveRandom03(PlayerColor.BLACK)
        player2 = RobotFiveRandom03(PlayerColor.WHITE)

        # 这里创建一个游戏的目的实际就是利用DoMova函数判断一下是不是这步就赢了
        game = GameFive()

        for (y, x), dis in pos:
            if playerColor == PlayerColor.BLACK and not game.isFreeMode:
                # 非业余模式，执黑，需要判断禁手
                board[y][x] = PlayerColor.BLACK  # 先在这个位置放上黑子
                isForbidden = RobotFiveMCTS.IsBlackForbiddenStatic(board, y=y, x=x)
                board[y][x] = PlayerColor.EMPTY
                if isForbidden:
                    # 黑棋的禁手，跳过
                    continue

            game.SetBoard(board)
            isWin = game.DoMove(y=y, x=x,playerColor=playerColor)
            if isWin:
                # 这个点赢了，直接退出
                bestX = x
                bestY = y
                break

            # 调用线程池模拟继续下
            pool = AutoRobotArenaPool(player1=player1, player2=player2, board=board, beginColor=playerColor,
                                      processNumber=10, taskNumber=tryNumber)
            bw, ww, draw = pool.DoMatch()
            rate = bw / ww if playerColor == PlayerColor.BLACK else ww / bw
            #print("Pos:",y,x,"Rate:",rate)
            if rate > bestRate:
                #print("Is Best Rate")
                bestRate = rate
                bestX = x
                bestY = y

            # 把刚刚下的子去掉
            board[y][x] = PlayerColor.EMPTY

        result['result'] = (bestX, bestY)

        end_time = time.time()
        #print(f"Worker process finished and set the event   ⏳总耗时：{end_time - start_time:.2f} 秒")

    @staticmethod
    def IsBlackForbiddenStatic(board,y,x):

        def GetPieceOnCalBoardPos(y,x):
            if y < 0 or y >= size or x < 0 or x >= size:
                return -1
            return board[y][x]

        size = len(board)
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
                if ny<0 or ny>=size or nx < 0 or nx >= size:
                    break
                if board[ny][nx]!=PlayerColor.BLACK:
                    # 这个位置不是黑子了
                    break
                length += 1
            ny, nx = y, x
            # 再顺方向查找
            while True:
                ny -= deltay
                nx -= deltax
                if ny < 0 or ny >= size or nx < 0 or nx >= size:
                    break
                if board[ny][nx] != PlayerColor.BLACK:
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
                pattern.append(GetPieceOnCalBoardPos(y=y-deltay*j, x=x-deltax*j))
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
                pattern.append(GetPieceOnCalBoardPos(y=y - deltay * j, x=x - deltax * j))
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

    def GetNextMove(self):
        return self.result['result']