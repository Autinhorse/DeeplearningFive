import numpy as np
import pickle

from keras import Sequential
from keras.layers import Conv2D, Flatten, Dense, MaxPooling2D, Dropout
from tensorflow_estimator.python.estimator.estimator import maybe_overwrite_model_dir_and_session_config

from GameCheckers.RobotCheckers.RobotCheckersBase import PieceType


class GameState(object):
    def __init__(self):
        pass

class GameCheckersTraining(object):

    def __init__(self):
        self.board = None
        self.moveRec = None

    def GenerateGameFromRecord(self, gameRecord):
        boards = []
        moves = []
        # 初始化棋盘
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        for i in range(3):
            for j in range(0, 8, 2):
                self.board[i][j + (1 - i % 2)] = 1
                self.board[7 - i][7 - j - (1 - i % 2)] = 2
        self.moveRec = gameRecord
        player = 2
        for record in gameRecord:
            self.moveRec = record
            boards.append(self.EncodeBoard(board=self.board,next_player = player))
            moves.append(self.EncodeMove(record))
            y = record[0]
            x = record[1]
            for i in range(2, len(record), 2):
                y1 = record[i]
                x1 = record[i+1]
                self.board[y][x] = 0
                self.board[y1][x1] = player
                if abs(y1 - y)==2:
                    self.board[int((y+y1)/2)][int((x+x1)/2)] = 0
                x = x1
                y = y1
            player = 3 - player
        return np.array(boards), np.array(moves)

    def EncodeBoard(self, board, next_player):
        board_matrix = np.zeros((8, 8))
        for r in range(8):
            for c in range(8):
                if board[r][c]!=0:
                    if board[r][c] == next_player:
                        board_matrix[r, c] = 1
                    else:
                        board_matrix[r, c] = -1
        return board_matrix

    def EncodeMove(self, moves):
        move = np.zeros((8*8))
        move[int(moves[0])*8+int(moves[1])] = -1
        move[int(moves[-2])*8+int(moves[-1])] = 1

        return move


class TrainData:
    def __init__(self):
        self.records = None

    def LoadData(self):
        '''if (i + 1) % fileSize == 0:
            with open(f"data{i + 1}.pkl", 'wb') as f:
                pickle.dump(records, f)
            records.clear()'''

        with open('data10.pkl', 'rb') as f:
            self.records = pickle.load(f)

    def SaveTrainData(self):
        self.LoadData()

        print("Records Loaded:",len(self.records))

        bs = []
        ms = []
        game = GameCheckersTraining()
        for record in self.records:
            boards, moves = game.GenerateGameFromRecord(record)
            bs.append(boards)
            ms.append(moves)

        x = np.concatenate(bs)
        y = np.concatenate(ms)

        np.save("TrainData\data10-boards.npy", x)
        np.save("TrainData\data10-moves.npy", y)

    def Train(self, file):

        X = np.load("TrainData\\"+file+"-boards.npy")
        Y = np.load("TrainData\\"+file+"-moves.npy")

        samples = X.shape[0]
        size = 8
        input_shape = (size, size, 1)
        X = X.reshape((samples, size, size, 1))
        train_samples = int(0.9*samples)

        X_train, X_test = X[:train_samples], X[train_samples:]
        Y_train, Y_test = Y[:train_samples], Y[train_samples:]

        model = Sequential()
        model.add(Conv2D(filters=48, kernel_size=(3, 3), activation='relu', padding='same',input_shape=input_shape))
        model.add(Dropout(0.5))
        model.add(Conv2D(48,(3,3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))
        model.add(Flatten())
        model.add(Dense(512, activation='sigmoid'))
        model.add(Dropout(0.5))
        model.add(Dense(size*size, activation='softmax'))
        model.summary()

        model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

        model.fit(X_train, Y_train, batch_size=64, epochs=100, verbose=1, validation_data=(X_test, Y_test))
        score = model.evaluate(X_test, Y_test, verbose=0)
        print("Test loss:", score[0])
        print("Test accuracy:", score[1])




