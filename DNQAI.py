from HelperFunction.functions import Functions
import random
import time
import copy
from HelperFunction.collision import Collision

board = [[0 for _ in range(10)] for _ in range (20)]
Pieces_list = ['I','L','J','O','T','S','Z']
PIECES = {
    'I': [
        (1,1,1,1)
    ],
    'J': [
        (0, 1),
        (0, 1),
        (1, 1)         
    ],
    'L': [
        (1, 0),
        (1, 0),
        (1, 1)
    ],
    'O': [
        (1,1),
        (1,1)
    ],
    'T': [
        (1,1,1),
        (0,1,0)
    ],
    'S': [
        (0,1,1,0),
        (1,1,0)
    ],
    'Z': [
        (1,1,0),
        (0,1,1)
    ]
}

generation = 100
individuals = 1000

weights = {
    "lines": random.uniform(-5,5),
    "holes": random.uniform(-5,5),
    "height": random.uniform(-5,5),
    "bumpiness": random.uniform(-5,5)
}




for i in range(generation):
    #prend les 500 meilleurs et les reproduit



    for i in range(individuals):
        #Fait la boucle pour chaque individus dans la boucle
        current_piece_type = random.choice(Pieces_list)
        current_piece = Functions(PIECES[current_piece_type],x=4,y=0)
        next_piece_type = random.choice(Pieces_list)
        next_piece = Functions(PIECES[next_piece_type],x=4,y=0)


        while True:
            reward = 0
            score = 0

            best_score = -float('inf')
            best_position = None
            best_rotation = None

            #Calculates all possibilities
            for rotations in range(4):
                temp_piece = copy.deepcopy(current_piece)
                temp_piece.x = 0
                temp_piece.y = 0
                for _ in range(rotations):
                    temp_piece.rotate_right()

                for column in range(0,10-len(temp_piece.shape[0])+1):
                    temp_board = [row[:] for row in board]
                    temp_piece.x = column
                    temp_piece.y = 0

                    while not Collision.collision_piece_bottom(temp_piece,temp_board):
                        piece_height = len(temp_piece.shape)
                        if temp_piece.y + piece_height >= 20:
                            break
                        temp_piece.y += 1
                        
                    temp_board = Functions.lockBoard(temp_piece,temp_board)
                    temp_board, lines_cleared = Functions.clear_lines(temp_board)
                    state = Functions.make_state(temp_board,next_piece_type)
                    score, back_to_back = Functions.score_count(lines_cleared,back_to_back)

                    reward = Functions.compute_reward_geneticAI(current_piece,temp_board,lines_cleared,state, weights) + score
                    if reward > best_score:
                        best_score = reward
                        best_rotation = rotations
                        best_position = column
            
            #Applies the best one
            for _ in range(best_rotation):
                current_piece.rotate_right()
            current_piece.x = best_position

            while not Collision.collision_piece_bottom(current_piece,board):
                current_piece.y += 1
                score += 2
                
        
            board = Functions.lockBoard(current_piece,board)
            board,_ = Functions.clear_lines(board)

            #Updates the Q_table and the pieces
            current_piece = next_piece
            current_piece_type = next_piece_type
            next_piece_type = random.choice(Pieces_list)
            next_piece = Functions(PIECES[next_piece_type],x=4,y=0)

            total_score += score

            if Functions.endgame(current_piece,board):
                break


