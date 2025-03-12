import time

from RobotArena.AutoRobotArena import AutoPlayerArena, MatchResult
from concurrent.futures import ProcessPoolExecutor, as_completed


class AutoRobotArenaPool:
    def __init__(self, player1, player2, game, board, beginColor, processNumber, taskNumber):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.beginColor = beginColor
        self.processNumber = processNumber
        self.taskNumber = taskNumber

        self.arenaPool = []
        self.arenaActive = []
        self.game = game
        for _ in range(processNumber):
            self.arenaPool.append(AutoPlayerArena(player1=player1,player2=player2,game=self.game,board=self.board, beginColor=self.beginColor))
            self.arenaActive.append(False)

        self.blackWin = 0
        self.whiteWin = 0
        self.draw = 0
        self.count = 0

    def DoTestTask(self):
        self.count+=1
        arena = AutoPlayerArena(player1=self.player1,player2=self.player2,game=self.game,board=self.board, beginColor=self.beginColor)
        arena.count = self.count
        arena.DoPlayAMatch()
        return arena.GetResult()

    def DoMatch(self):

        self.blackWin = 0
        self.whiteWin = 0
        self.draw = 0

        # 存储所有任务的计算结果
        task_results = {}

        start_time = time.time()

        # 使用 ProcessPoolExecutor 创建进程池
        with ProcessPoolExecutor(max_workers=self.processNumber) as executor:
            # 提交前 8 个任务
            future_to_task = [executor.submit(self.DoTestTask) for _ in range(self.processNumber)]


            # 处理任务，完成一个就提交一个新的
            next_task_id = self.processNumber  # 记录下一个要提交的任务 ID

            while future_to_task:
                for future in as_completed(future_to_task):
                    #print("Task completed")
                    result = future.result()  # 获取计算结果
                    if result == MatchResult.PLAYING:
                        continue
                    if result == MatchResult.BLACKWIN:
                        self.blackWin += 1
                    elif result == MatchResult.WHITEWIN:
                        self.whiteWin += 1
                    else:
                        self.draw += 1

                    # 如果还有剩余任务，提交给空闲进程
                    if next_task_id < self.taskNumber:
                        #print("Add new task")
                        new_future = executor.submit(self.DoTestTask)
                        future_to_task.append(new_future)
                        next_task_id += 1

                    # 移除已完成的任务
                    future_to_task.remove(future)

        end_time = time.time()

        print("Black Win:", self.blackWin, "White Win:", self.whiteWin, "Draw:", self.draw)
        print(f"\n🎉 所有任务计算完成！ ⏳总耗时：{end_time - start_time:.2f} 秒")

        return self.blackWin,self.whiteWin,self.draw