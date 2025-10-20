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
        (0,1,1),
        (1,1,0)
    ],
    'Z': [
        (1,1,0),
        (0,1,1)
    ]
}

generation = 100
individuals = 200
mutation = 0.15
mutation_step = 0.2

level = 1
lines_required = level*5

population = []

for _ in range(individuals):  
    weights = {
        "lines": random.uniform(0.5, 2),
        "holes": random.uniform(0, 2),
        "height": random.uniform(0, 2),
        "bumpiness": random.uniform(0, 2)
    }
    population.append({"weights": weights, "fitness": 0})


for i in range(generation):
    # Looping through every bot

    for j in range(individuals):
        weights = population[j]["weights"]

        current_piece_type = random.choice(Pieces_list)
        current_piece = Functions(PIECES[current_piece_type], x=4, y=0)
        next_piece_type = random.choice(Pieces_list)
        next_piece = Functions(PIECES[next_piece_type], x=4, y=0)
        second_next_piece_type = random.choice(Pieces_list)
        second_next_piece = Functions(PIECES[next_piece_type], x=4, y=0)

        board = [[0 for _ in range(10)] for _ in range(20)]

        back_to_back = False
        total_score = 0
        human_score = 0
        count = 0

        # Game itself
        while True:
            reward = 0
            score = 0
            count = 0
            best_score = -float('inf')
            best_rotation = None
            best_position = None
            fake_level = level
            fake_line_required = lines_required

            if current_piece_type == "O":
                max_rotation = 1
            elif current_piece_type == "I":
                max_rotation = 2
            else:
                max_rotation = 4

            for rotation in range(max_rotation):
                temp_piece_1 = Functions(PIECES[current_piece_type],x=4,y=0)
                
                for _ in range(rotation):
                    temp_piece_1.rotate_right()

                for column in range(0, 10 - len(temp_piece_1.shape[0]) + 1):
                    temp_board_1 = [row[:] for row in board]
                    temp_piece_1.x = column
                    temp_piece_1.y = 0

                    while not Collision.collision_piece_bottom(temp_piece_1,temp_board_1):
                        temp_piece_1.y += 1 

                    temp_board_1 = Functions.lockBoard(temp_piece_1, temp_board_1)
                    temp_board_1, lines_cleared_1 = Functions.clear_lines(temp_board_1)
                    score_1, back_to_back_temp = Functions.score_count(lines_cleared_1,back_to_back,temp_board_1,fake_level)
            
                    if fake_line_required > fake_level * 10:
                            fake_level+= 1

                    if next_piece_type == "O":
                        next_max_rotation = 1
                    elif next_piece_type == "I":
                        next_max_rotation = 2
                    else:
                        next_max_rotation = 4

                    for next_rotation in range(next_max_rotation):
                        temp_piece_2 = Functions(PIECES[next_piece_type],x=4,y=0)
                        
                        for _ in range(next_rotation):
                            temp_piece_2.rotate_right()
                        for next_column in range(0, 10 - len(temp_piece_2.shape[0]) + 1):
                            temp_board_2 = [row[:] for row in temp_board_1]
                            temp_piece_2.x = next_column
                            temp_piece_2.y = 0

                            while not Collision.collision_piece_bottom(temp_piece_2,temp_board_2):
                                temp_piece_2.y += 1 

                            temp_board_2 = Functions.lockBoard(temp_piece_2,temp_board_2)
                            temp_board_2, lines_cleared_2 = Functions.clear_lines(temp_board_2)
                            score_2, _ = Functions.score_count(lines_cleared_2,back_to_back_temp,temp_board_2,fake_level)

                            total_lines = lines_cleared_2 + lines_cleared_1
                            temp_total_score = score_1 + score_2

                            state = Functions.make_state(temp_board_2, second_next_piece_type)
                            reward = Functions.compute_reward(temp_piece_2,temp_board_2,total_lines,state) + temp_total_score

                            if reward > best_score:
                                best_score = reward
                                best_rotation = rotation
                                best_position = column
            
            #Applies the best one
            for _ in range(best_rotation):
                current_piece.rotate_right()
            current_piece.x = best_position

            while not Collision.collision_piece_bottom(current_piece,board):
                current_piece.y += 1
                count += 1
                Functions.print_board_terminal(current_piece,board)
                
            board = Functions.lockBoard(current_piece,board)
            board,line_cleared_def = Functions.clear_lines(board)

            current_piece = next_piece
            current_piece_type = next_piece_type
            next_piece_type = second_next_piece_type
            next_piece = second_next_piece
            second_next_piece_type = random.choice(Pieces_list)
            second_next_piece = Functions(PIECES[second_next_piece_type],x=4,y=0)


            score,back_to_back = Functions.score_count(line_cleared_def, back_to_back, board, level)
            total_score += score 
            human_score += score
            human_score += count*2

            lines_required += line_cleared_def

            if lines_required > level*10:
                level += 1 


            if Functions.endgame(current_piece,board):
                break

        population[j]["fitness"] = total_score

        print("ok")



        with open(f"human_score.txt","a") as f:
            f.write(f"individual {j} has human score {human_score}\n")

    # Creates the new generation
    best_fit = population[0]["fitness"]
    avg_fit = sum(p["fitness"] for p in population) / len(population)

    with open("genetic_generation_AI.txt", "a") as f:
        f.write(f"Generation {i}: Best = {best_fit:.2f}, best weight = {population[0]["weights"]}, best fitness = {population[0]["fitness"]}, Avg = {avg_fit:.2f}\n")

    population.sort(key=lambda x: x["fitness"], reverse=True)
    new_pop = population[:int(individuals*0.1)]


    for _ in range(int(individuals*0.8)):
        i1 = random.randrange(0, len(new_pop))
        i2 = random.randrange(0, len(new_pop))
        if random.random()<0.5:
            weights = {
                "lines": (new_pop[i1]["weights"]["lines"] + new_pop[i2]["weights"]["lines"]) / 2,
                "holes": (new_pop[i1]["weights"]["holes"] + new_pop[i2]["weights"]["holes"]) / 2,
                "height": (new_pop[i1]["weights"]["height"] + new_pop[i2]["weights"]["height"]) / 2,
                "bumpiness": (new_pop[i1]["weights"]["bumpiness"] + new_pop[i2]["weights"]["bumpiness"]) / 2
            }
        else:
            weights = random.choice([new_pop[i1]["weights"], new_pop[i2]["weights"]]).copy()

        for key in weights:
            if random.random() < mutation:
                weights[key] += random.uniform(-mutation_step, mutation_step)
        
        weights["lines"] = max(weights["lines"],0)

        new_pop.append({"weights": weights, "fitness": 0})
    
    for _ in range(int(individuals*0.1)): 
        weights = {
            "lines": random.uniform(0.5, 2),
            "holes": random.uniform(0, 2),
            "height": random.uniform(0, 2),
            "bumpiness": random.uniform(0, 2)
        }
        new_pop.append({"weights": weights, "fitness": 0})

    population = new_pop

    mutation = max(mutation*0.995,0.05)
    mutation_step = max(mutation_step*0.998,0.1)

print("Training complete!")
print(f"Best weights: {population[0]['weights']}")