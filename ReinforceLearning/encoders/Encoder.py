class Encoder:
    # Get name of encoder
    def name(self):
        raise NotImplementedError()

    # Convert state of board to data
    def encode(self, game_state):
        raise NotImplementedError()

    # Get array index of point
    def encode_point(self,point):
        raise NotImplementedError()

    # Get point by array index
    def decode_point(self,index):
        raise NotImplementedError()

    # Number of point
    def num_points(self):
        raise NotImplementedError()

    # Shape after encode
    def shape(self):
        raise NotImplementedError()

