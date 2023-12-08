from _2048_Game import Game
import numpy as np

class _2048_AI:
    def __init__(self,parent):
        self.parent = parent
        self.last_move = None
        self.snake_sequence = ((0,0), (0,1), (0,2), (0,3), 
                              (1,3), (1,2), (1,1), (1,0), 
                              (2,0), (2,1), (2,2), (2,3), 
                              (3,3), (3,2), (3,1), (3,0))
        self.snake_directions = ("invalid","right","right","right",
                                 "down",   "left" ,"left" ,"left",
                                 "down",   "right","right","right",
                                 "down",   "left", "left", "left")
    def valid_move(self,board,move):
        pieces = np.where(board!=0)
        pieces = [(pieces[0][j],pieces[1][j]) for j in range(len(pieces[0]))]
        for piece in pieces:
            if move == "left":
                if piece[1]!=0:
                    if board[piece[0],piece[1]] == board[piece[0],piece[1]-1]:
                        return True
                    if board[piece[0],piece[1]-1] == 0:
                        return True
            if move == "right":
                if piece[1]!=3:
                    if board[piece[0],piece[1]] == board[piece[0],piece[1]+1]:
                        return True
                    if board[piece[0],piece[1]+1] == 0:
                        return True
            if move == "up":
                if piece[0]!=0:
                    if board[piece[0],piece[1]] == board[piece[0]-1,piece[1]]:
                        return True
                    if board[piece[0]-1,piece[1]] == 0:
                        return True
        return False
    def find_move(self,game):
        if game.board[0,0] == 0:
            answer = "new game"
        else:
            chain_index = 0
            current_coordinates = self.snake_sequence[chain_index]
            value_at_previous_place = game.board[current_coordinates[0],current_coordinates[1]]
            verifying_snake = True
            state = "good"
            move = "blank"
            increase_found_in_snake = False
            while verifying_snake and state == "good":
                chain_index += 1
                current_coordinates = self.snake_sequence[chain_index]
                value_at_current_place = game.board[current_coordinates[0],current_coordinates[1]]
                if value_at_current_place > value_at_previous_place:
                    state = "invalid snake"
                    print("check 5")
                    increase_found_in_snake = True
                if value_at_current_place == value_at_previous_place:
                    if move == "blank":
                        current_place = self.snake_sequence[chain_index]
                        previous_place = self.snake_sequence[chain_index-1]
                        if current_place[1]>previous_place[1]:
                            move = "left"
                        elif current_place[1]<previous_place[1]:
                            move = "right"
                        else:
                            move = "up"
                        move_location = chain_index
                if value_at_current_place == 0:
                    verifying_snake = False
                value_at_previous_place = value_at_current_place
            if increase_found_in_snake:
                return "undo"
            number_of_numbers_on_the_board = np.sum(game.board!=0)
            pieces_in_snake = chain_index
            number_of_loose_pieces = number_of_numbers_on_the_board - pieces_in_snake
            print("move: " + str(move))
            print("number_of_loose_pieces: " + str(number_of_loose_pieces))
            snake_direction = self.snake_directions[chain_index]
            next_direction = self.snake_directions[move_location+1]
            print("self.snake_directions: " + str(self.snake_directions))
            print("self.snake_directions[4]: " + str(self.snake_directions[4]))
            print("chain_index: " + str(chain_index))
            print("move_location: " + str(move_location))
            print("snake_direction: " + str(snake_direction))
            print("next_direction: " + str(next_direction))
            if number_of_loose_pieces == 0 and move != "blank":
                if move in ("left","right") and next_direction == "down":
                    
                return move
            if number_of_loose_pieces > 1:
                return "undo"
            
            # find out where the loose piece is located
            # remove snake in temporary board to find loose pieces
            dummy_board = np.array(game.board)
            print("pieces_in_snake: " + str(pieces_in_snake))
            for i in range(pieces_in_snake):
                current_coordinates = self.snake_sequence[i]
                dummy_board[current_coordinates[0],current_coordinates[1]]=0
            loose_piece_locations = np.where(dummy_board != 0)
            loose_piece_locations = [(loose_piece_locations[0][j],loose_piece_locations[1][j]) for j in range(len(loose_piece_locations[0]))]
            
            for loose_piece_location in loose_piece_locations:
                print("----loose_piece_location: " + str(loose_piece_location))
                # determine if the location of the loose piece is ok based on the current move
                valid = True
                print("    current_coordinates: " + str(current_coordinates))
                print("    loose_piece_location: " + str(loose_piece_location))
                if move == "left":
                    print("    check 6.5")
                    if current_coordinates[0] == loose_piece_location[0]:
                        if current_coordinates[1] >= loose_piece_location[1]:
                            valid = False
                    else:
                        valid = False
                elif move == "right":
                    print("    check 6.6")
                    if current_coordinates[0] == loose_piece_location[0]:
                        if current_coordinates[1] <= loose_piece_location[1]:
                            valid = False
                    else:
                        valid = False
                elif move == "up":
                    print("    check 6.7")
                    if current_coordinates[1] == loose_piece_location[1]:
                        if current_coordinates[0] >= loose_piece_location[0]:
                            valid = False
                    else:
                        valid = False
                elif move == "blank":
                    print("    check 6.8")
                    # check if can combine loose block to last block in snake
                    current_coordinates = self.snake_sequence[chain_index]
                    previous_coordinates = self.snake_sequence[chain_index-1]
                    value_at_current_place = game.board[previous_coordinates[0],previous_coordinates[1]]
                    value_at_loose_piece = game.board[loose_piece_location[0],loose_piece_location[1]]
                    if value_at_current_place == value_at_loose_piece:
                        if previous_coordinates[1] == loose_piece_location[1]:
                            if previous_coordinates[0] <= loose_piece_location[0]:
                                return "up"
                        elif previous_coordinates[0] == loose_piece_location[0]:
                            if previous_coordinates[1] <= loose_piece_location[1]:
                                return "left"
                    
                    print("    check 6.9")
                    # move loose block based on location
                    if value_at_loose_piece < value_at_current_place:
                        if snake_direction == "right":
                            print("    check 7")
                            if current_coordinates[1] == loose_piece_location[1]: # if same column
                                if current_coordinates[0] < loose_piece_location[0]: # and loose piece is below
                                    move = "up"
                            elif current_coordinates[1] < loose_piece_location[1]: # if loose piece to the right
                                if current_coordinates[0] == loose_piece_location[0]: # and in same row
                                    move = "left"
                                # elif current_coordinates[0] < loose_piece_location[0]: # and loose is below
                                    # move = "up"
                        elif snake_direction == "left":
                            print("    check 8")
                            if current_coordinates[1] == loose_piece_location[1]: # if same column
                                if current_coordinates[0] < loose_piece_location[0]: # and loose piece is below
                                    move = "up"
                            elif current_coordinates[1] > loose_piece_location[1]: # if loose piece to the left
                                if current_coordinates[0] == loose_piece_location[0]: # and in same row
                                    move = "right"
                                # elif current_coordinates[0] < loose_piece_location[0]: # and loose is below
                                    # move = "up"                    
                        elif snake_direction == "down":
                            print("    check 9")
                            if previous_coordinates[1]==current_coordinates[1]:
                                if previous_coordinates[0] < current_coordinates[0]:
                                    move = "up"
                if valid and move != "blank":
                    print("    returning valid move")
                    if not self.valid_move(game.board,move):
                        move = "undo"
                    return move
                
        print("check 8")
        return "undo"