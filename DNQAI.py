from HelperFunction.functions import Functions
import random
import time
import copy
from HelperFunction.collision import Collision
import numpy

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

generation = 500
individuals = 1000

population = []
for _ in range(individuals):  
    weights = {
        "lines": random.uniform(-2, 2),
        "holes": random.uniform(-2, 2),
        "height": random.uniform(-2, 2),
        "bumpiness": random.uniform(-2, 2)
    }
    population.append({"weights": weights, "fitness": 0})



for i in range(generation):
    population = sorted(population, key=lambda x: x["fitness"], reverse=True)

    new_pop = population[:200]
    for i in range(800):
        i1 = random.randrange(0, 200)
        i2 = random.randrange(0, 200)
        weights = {
        "lines":(new_pop[i1]["weights"]["lines"] + new_pop[i2]["weights"]["lines"]) / 2,
        "holes": (new_pop[i1]["weights"]["holes"] + new_pop[i2]["weights"]["holes"]) / 2,
        "height": (new_pop[i1]["weights"]["height"] + new_pop[i2]["weights"]["height"]) / 2,
        "bumpiness": (new_pop[i1]["weights"]["bumpiness"] + new_pop[i2]["weights"]["bumpiness"]) / 2
        }

        for key in weights:
            if random.random() < 0.1:  # 10% chance to mutate
                weights[key] += random.uniform(-0.2, 0.2)

        new_pop.append({"weights":weights, "fitness": 0})



    for j in range(individuals):
        #Fait la boucle pour chaque individus dans la boucle
        current_piece_type = random.choice(Pieces_list)
        current_piece = Functions(PIECES[current_piece_type],x=4,y=0)
        next_piece_type = random.choice(Pieces_list)
        next_piece = Functions(PIECES[next_piece_type],x=4,y=0)

        board = numpy.zeros((20, 10), dtype=int)

        back_to_back = False
        total_score = 0

        while True:
            reward = 0
            score = 0

            #Calculates all possibilities
            if current_piece_type == 'O':
                max_rotations = 1
            elif current_piece_type == 'I':
                max_rotations = 2
            else:
                max_rotations = 4

            best_score = -float('inf')
            best_rotation = None
            best_position = None

            for rotations in range(max_rotations):
                temp_piece = Functions(PIECES[current_piece_type],x=4,y=0)

                for _ in range(rotations):
                    temp_piece.rotate_right()

                # Loop through columns and drop piece
                for column in range(0, 10 - len(temp_piece.shape[0]) + 1):
                    temp_board = [row[:] for row in board]
                    temp_piece.x = column
                    temp_piece.y = 0

                    while not Collision.collision_piece_bottom(temp_piece, temp_board):
                        piece_height = len(temp_piece.shape)
                        if temp_piece.y + piece_height >= 20:
                            break
                        temp_piece.y += 1

                # Lock piece & compute reward
                temp_board = Functions.lockBoard(temp_piece, temp_board)
                temp_board, lines_cleared = Functions.clear_lines(temp_board)
                state = Functions.make_state(temp_board, next_piece_type)
                score, back_to_back = Functions.score_count(lines_cleared, back_to_back)

                reward = Functions.compute_reward_geneticAI(current_piece, temp_board, lines_cleared, state, weights) + score

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
                count += 1

                total_score += score + count

                if Functions.endgame(current_piece,board):
                    break

            population[j]["fitness"] = total_score


