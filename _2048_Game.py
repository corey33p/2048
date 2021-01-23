import numpy as np
import random

class Game:
    def __init__(self,board=None):
        self.console_print = True
        self.new_game(board)
    def print_board(self):
        print("----------")
        print("move #" + str(self.number_of_moves))
        print("score: " + str(self.score))
        print(str(self.board))
    def undo(self):
        self.board,self.previous_board = self.previous_board,self.board
        if self.console_print: self.print_board()
    def new_game(self,board=None):
        if board is not None:
            assert np.all(board.shape == (4,4))
            self.board = board
        else:
            self.board = np.zeros((4,4),np.int32)
            self.random_spawn()
            self.random_spawn()
        self.number_of_moves = 0
        self.score = 0
        self.previous_board = np.copy(self.board)
        if self.console_print: self.print_board()
    def random_spawn(self):
        empty_spots = np.argwhere(self.board == 0)
        random_spot = random.choice(empty_spots)
        if random.uniform(0,1) < .1:
            self.board[random_spot[0],random_spot[1]] = 4
        else:
            self.board[random_spot[0],random_spot[1]] = 2
    def move(self,direction):
        valid_direction = direction in ("up","right","down","left")
        if valid_direction:
            if direction == "up":
                move_direction = np.array([-1,0])
            elif direction == "right":
                move_direction = np.array([0,1])
            elif direction == "down":
                move_direction = np.array([1,0])
            elif direction == "left":
                move_direction = np.array([0,-1])
            something_moved = True
            board_copy = np.array(self.board)
            while something_moved:
                # input("loop")
                something_moved = False
                nonzero_locations = np.argwhere(self.board!=0)
                for nonzero_location in nonzero_locations: # iterate all the nonempty tiles
                    # print("----nonzero_location: " + str(nonzero_location))
                    # print("----loop")
                    current_location = nonzero_location
                    quit_loop = False
                    while 1:
                        # print("--------loop")
                        current_location = current_location + move_direction
                        for coordinate in current_location: # check if new location valid, if not, move back and break loop
                            if coordinate < 0 or coordinate > 3: 
                                current_location = current_location - move_direction
                                quit_loop = True
                                break
                        if quit_loop:
                            break
                        if self.board[current_location[0],current_location[1]] != 0:
                            current_location = current_location - move_direction
                            break
                        # print("--------current_location: " + str(current_location))
                    if np.any(current_location != nonzero_location):
                        # print("----self.board:\n" + str(self.board))
                        # print("----swapping")
                        self.board[current_location[0],current_location[1]],self.board[nonzero_location[0],nonzero_location[1]]=self.board[nonzero_location[0],nonzero_location[1]],self.board[current_location[0],current_location[1]]
                        something_moved = True
                        self.board = np.copy(self.board)
                        # print("----self.board:\n" + str(self.board))
        # print("board_copy55:\n" + str(board_copy))
        # print("self.board55:\n" + str(self.board))
        self.consolidate(direction)
        # print("board_copy66:\n" + str(board_copy))
        # print("self.board66:\n" + str(self.board))
        something_changed = not np.all(board_copy == self.board)
        if something_changed:
            # print("here77")
            self.previous_board = board_copy
            self.random_spawn()
            self.number_of_moves += 1
            if self.console_print: self.print_board()
    def consolidate(self,direction):
        print("consolidating")
        valid_direction = direction in ("up","right","down","left")
        if valid_direction:
            if direction in ("left","right"):
                if direction == "left":
                    for row in range(4):
                        for col in range(1,4):
                            if self.board[row,col-1]==self.board[row,col]:
                                if self.board[row,col] != 0:
                                    self.board[row,col-1] = np.sum(self.board[row,col]+self.board[row,col-1])
                                    self.score += self.board[row,col-1]
                                    self.board[row,col]=0
                                    self.board[row,col:]=np.roll(self.board[row,col:],-1,axis=0)
                else:
                    for row in range(4):
                        for col in range(2,-1,-1):
                            # print("what up")
                            if self.board[row,col]==self.board[row,col+1]:
                                if self.board[row,col] != 0:
                                    self.board[row,col+1] = np.sum(self.board[row,col]+self.board[row,col+1])
                                    self.score += self.board[row,col+1]
                                    self.board[row,col]=0
                                    self.board[row,:col]=np.roll(self.board[row,:col],1,axis=0)
            else:
                if direction == "up":
                    for col in range(4):
                        for row in range(1,4):
                            if self.board[row-1,col]==self.board[row,col]:
                                if self.board[row,col] != 0:
                                    self.board[row-1,col] = np.sum(self.board[row,col]+self.board[row-1,col])
                                    self.score += self.board[row-1,col]
                                    self.board[row,col]=0
                                    self.board[row:,col]=np.roll(self.board[row:,col],-1,axis=0)
                else:
                    for col in range(4):
                        for row in range(2,-1,-1):
                            if self.board[row,col]==self.board[row+1,col]:
                                if self.board[row,col] != 0:
                                    self.board[row+1,col] = np.sum(self.board[row,col]+self.board[row+1,col])
                                    self.score += self.board[row+1,col]
                                    self.board[row,col]=0
                                    self.board[:row,col]=np.roll(self.board[:row,col],1,axis=0)
        # print("here")

# game = Game()
# # game.board = np.array([[2,0,2,0],
                       # # [0,2,0,2],
                       # # [2,0,2,0],
                       # # [0,2,0,2]])
# # game.board = np.array([[0,0,2,0],
                       # # [0,0,0,0],
                       # # [0,0,0,0],
                       # # [0,0,0,0]])
# # game.board = np.array([[2,2,2,2],
                       # # [0,0,0,0],
                       # # [0,0,0,0],
                       # # [0,0,0,0]])
# game.board = np.array([[0,8,0,0],
                       # [0,8,0,0],
                       # [0,8,0,0],
                       # [0,8,0,0]])
# print("game.board:\n" + str(game.board))
# game.move("up")
# print("game.board:\n" + str(game.board))
