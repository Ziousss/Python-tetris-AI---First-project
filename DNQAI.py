from HelperFunction.functions import Functions
import random
import time
from HelperFunction.collision import Collision

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
    #Looping through every bot
    for j in range(individuals):
        weights = population[j]["weights"]
        current_piece_type = random.choice(Pieces_list)
        current_piece = Functions(PIECES[current_piece_type],x=4,y=0)
        next_piece_type = random.choice(Pieces_list)
        next_piece = Functions(PIECES[next_piece_type],x=4,y=0)

        board = [[0 for _ in range(10)] for _ in range (20)]

        back_to_back = False
        total_score = 0
        count = 0

        #Game itself
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

            #Prepares for next piece
            current_piece = next_piece
            current_piece_type = next_piece_type
            next_piece_type = random.choice(Pieces_list)
            next_piece = Functions(PIECES[next_piece_type],x=4,y=0)
            count += 1 # values long game

            total_score += score + count

            if Functions.endgame(current_piece,board):
                break

        population[j]["fitness"] = total_score


    #Creates the new generation
    population = sorted(population, key=lambda x: x["fitness"], reverse=True)

    best_fit = population[0]["fitness"]
    avg_fit = sum(p["fitness"] for p in population) / len(population)

    with open("geneticAI.txt","a") as f:
        f.write(f"Generation {i}: Best = {best_fit:.2f}, Avg = {avg_fit:.2f}")

    print(f"Generation {i+1}: Best = {best_fit:.2f}, Avg = {avg_fit:.2f}\n")

    #Optional: prints in the terminal a game of the best and worst bot of this generation
    if i % 10 == 0:  # every 10 generations
        print(f"Displaying best AI of generation {i}...")
        Functions.play_with_weights(population[0]["weights"])
        print(f"Displaying worst AI of generation {i}...")
        Functions.play_with_weights(population[-1]["weights"])

    new_pop = population[:200]
    for _ in range(800):
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
    
    population = new_pop


