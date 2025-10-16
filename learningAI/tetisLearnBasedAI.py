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
current_piece = Functions(PIECES[random.choice(Pieces_list)],x=4,y=0)
next_piece = Functions(PIECES[random.choice(Pieces_list)],x=4,y=0)

Q_table = {}

actions = [
    (0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0), (9,0),
    (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1),
    (0,2), (1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2), (9,2),
    (0,3), (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3), (8,3), (9,3)
    ]

learning_rate = 0.7
discount_factor = 0.99
exploration_prob = 1
number = 50000

episode = 0

#for loop that goes until 10000
for _ in range(number):
    board = [[0 for _ in range(10)] for _ in range (20)]

    current_piece_type = random.choice(Pieces_list)
    current_piece = Functions(PIECES[current_piece_type],x=4,y=0)
    next_piece_type = random.choice(Pieces_list)
    next_piece = Functions(PIECES[next_piece_type],x=4,y=0)

    back_to_back = False
    total_score = 0

    while not Functions.endgame(current_piece, board):
        current_state = Functions.make_state(board, current_piece_type)
        current_state_tuple = tuple(current_state)

        if current_state_tuple not in Q_table:
            Q_table[current_state_tuple] = [0.0]*len(actions)

        valid_move = []

        for move,rotate in actions:
            valid = True
            temp_piece = copy.deepcopy(current_piece)
            temp_piece.x = move
            temp_piece.y = 0
            for _ in range(rotate):
                if not Collision.collision_rotation_right(temp_piece,board):
                    temp_piece.rotate_right()
                else:
                    valid = False
                    break
            if valid and not Collision.collision_sides(temp_piece,board) and (move,rotate) not in valid_move:
                valid_move.append((move,rotate))



        if random.random() <= exploration_prob:
            action_index = random.randint(0,len(valid_move)-1)
            chosen_action = valid_move[action_index]
        else:
            valid_indices = [actions.index(a) for a in valid_move]
            q_values = [Q_table[current_state_tuple][i] for i in valid_indices]
            action_index = valid_indices[q_values.index(max(q_values))]
            chosen_action = actions[action_index]

        def_move = chosen_action[0]
        def_rotation = chosen_action[1]
        for _ in range(def_rotation):
            current_piece.rotate_right()
        current_piece.x = def_move

        while not Collision.collision_piece_bottom(current_piece,board):
            current_piece.y += 1
        
        board = Functions.lockBoard(current_piece,board)
        board, line_cleared = Functions.clear_lines(board)
        new_state = Functions.make_state(board, next_piece_type)
        new_state_tuple = tuple(new_state)

        if new_state_tuple not in Q_table:
            Q_table[new_state_tuple] = [0.0]*40

        score,back_to_back = Functions.score_count(line_cleared,back_to_back)
        reward = Functions.compute_reward(current_piece,board, line_cleared, current_state)

        Q_table[current_state_tuple][action_index] = Q_table[current_state_tuple][action_index] + learning_rate*(reward+discount_factor*max(Q_table[new_state_tuple]) - Q_table[current_state_tuple][action_index])

        current_piece = next_piece
        current_piece_type = next_piece_type
        next_piece_type = random.choice(Pieces_list)
        next_piece = Functions(PIECES[next_piece_type],x=4,y=0)

        total_score += score

    episode += 1
    exploration_prob = (max(0.05,exploration_prob*0.999))
    print(f"{episode}")
    if episode%50 == 0:
        with open("score_LearnAI50.txt","a") as f:
            f.write(f"Episode {episode}, total score = {total_score}\n")
