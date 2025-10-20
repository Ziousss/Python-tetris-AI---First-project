from HelperFunction.collision import Collision
import random
import time

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
        (0,1,1),
        (1,1,0)
    ],
    'Z': [
        (1,1,0),
        (0,1,1)
    ]
}

class Functions():
    def __init__(self, shape, x=0, y=0):
        self.shape = shape
        self.x = x
        self.y = y

    def rotate_right(self):     
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def rotate_left(self):
        rotated = list(zip(*self.shape))  
        rotated_left = rotated[::-1]      
        self.shape = [list(row) for row in rotated_left]

    def print_board_terminal(piece, board):
        temp_board = [row[:] for row in board]

        if piece:
            shape = piece.shape
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell == 1:
                        board_y = piece.y + i
                        board_x = piece.x + j
                        if 0 <= board_y < len(temp_board) and 0 <= board_x < len(temp_board[0]):
                            temp_board[board_y][board_x] = 1

        for row in temp_board:
            line = ''.join('#' if cell == 1 else '.' for cell in row)
            print(line)
    
    def lockBoard(piece, board):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell != 1:
                    continue

                if 0 <= piece.y + i < len(board) and 0 <= piece.x + j < len(board[0]):
                    board[piece.y + i][piece.x + j] = 1
                else:
                    pass
        return board
        
    def move_right(piece):
        piece.x += 1

    def move_left(piece):
        piece.x -= 1

    def endgame(piece, board):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell != 1:
                    continue
                y = piece.y + i
                x = piece.x + j
                
                if board[0][j] == 1:
                    return True

                # Check if piece overlaps with existing blocks
                if 0 <= y < len(board) and 0 <= x < len(board[0]):
                    if board[y][x] == 1:
                        return True
        return False


    
    def moveDown(piece,board):
        if not Collision.collision_piece_bottom(piece, board):
            piece.y += 1
        
    def clear_lines(board):
        new_board = []
        lines_cleared = 0
        for row in board:
            if all(cell == 1 for cell in row):
                lines_cleared += 1 
            else:
                new_board.append(row)

        for _ in range(lines_cleared):
            new_board.insert(0,[0 for _ in range(len(board[0]))])
        return new_board, lines_cleared
    

    def soft_down(piece,board):
        if not Collision.collision_piece_bottom(piece,board):
            piece.y += 1

    def step(action,piece,board):
        if action == "left":
            if not Collision.collision_sides_left(piece,board):    
                Functions.move_left(piece)
        elif action == "right":
            if not Collision.collision_sides_right(piece,board):
                Functions.move_right(piece)
        elif action == "down":
            if not Collision.collision_piece_bottom(piece,board):
                Functions.soft_down(piece,board)
                
        elif action == "rotate_right":
            if not Collision.collision_rotation_right(piece,board):
                Functions.rotate_right(piece)
        elif action == "rotate_left":
            if not Collision.collision_rotation_left(piece,board):
                Functions.rotate_left(piece)

    def make_state(board,piece_type):
        state = []
        for i in range(10):
            for j in range(20):
                if board[j][i] == 1:
                    state.append(20 - j)
                    break
            else:
                state.append(0)

        new_list = [0]*7
        new_list[Pieces_list.index(piece_type)] = 1

        state.extend(new_list)
        return state

    def max_difference(state):
        maximum = 0
        minimum = 100
        for item in state:
            if item > maximum:
                maximum = item
            if item < minimum:
                minimum = item
        return maximum - minimum

    def count_holes(board):
        total = 0
        for i in range(10):
            found_block = False
            for j in range(20):
                if board[j][i] == 1:
                    found_block = True
                if found_block and board[j][i] == 0:
                    total += 1
        return total
    

    def compute_reward(current_piece,board, lines_cleared,state):
        # Extract board features
        height = state[:10] 
        holes = Functions.count_holes(board)         
        bumpiness = Functions.bumpiness(height)      
        
        reward = 0
        reward -= (0.5 * holes + 0.3 * bumpiness + 0.2 * max(height))

        if Functions.endgame(current_piece,board):
            reward -= 500

        if lines_cleared == 1:
            reward += 100
        elif lines_cleared == 2:
            reward += 300
        elif lines_cleared == 3:
            reward += 700
        elif lines_cleared == 4:
            reward += 1200  # Tetris

        return reward
    
    def compute_reward_geneticAI(current_piece, board, lines_cleared, state, weights):
        # Extract board features
        height = state[:10] 
        holes = Functions.count_holes(board)         
        bumpiness = Functions.bumpiness(height)      
        
        reward = 0
        reward = (lines_cleared * weights["lines"] - holes * weights["holes"] - bumpiness * weights["bumpiness"] - max(height) * weights["height"])

        if Functions.endgame(current_piece,board):
            reward -= 500
        return reward
    
    
    def score_count(line_count, back_to_back, board, level):
        score = 0
        is_empty = all(cell == 0 for row in board for cell in row)

        if line_count == 1:
            score += 800*level if is_empty else 100*level
            back_to_back = False
        elif line_count == 2:
            score += 1200*level if is_empty else 300*level
            back_to_back = False
        elif line_count == 3:
            score += 1800*level if is_empty else 500*level
            back_to_back = False
        elif line_count == 4:  # Tetris
            score += 2000*level if is_empty else 800*level
            if back_to_back:  # Back-to-back bonus
                score += 1200*level
            back_to_back = True
        else:
            back_to_back = False

        return score, back_to_back

    
    def bumpiness(state):
        total = 0
        for item in range(9):
            total += abs(state[item] - state[item+1])
        return total
    
    def play_with_weights(weights):

        current_piece_type = random.choice(Pieces_list)
        current_piece = Functions(PIECES[current_piece_type], x=4, y=0)
        next_piece_type = random.choice(Pieces_list)
        next_piece = Functions(PIECES[next_piece_type], x=4, y=0)
        board = [[0 for _ in range(10)] for _ in range(20)]
        
        back_to_back = False
        total_score = 0
        total_lines_cleared = 0
        pieces_placed = 0
        
        while True:
            # Calculates all possibilities
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
                temp_piece = Functions(PIECES[current_piece_type], x=4, y=0)
                
                for _ in range(rotations):
                    temp_piece.rotate_right()
                
                for column in range(0, 10 - len(temp_piece.shape[0]) + 1):
                    temp_board = [row[:] for row in board]
                    temp_piece.x = column
                    temp_piece.y = 0
                    
                    while not Collision.collision_piece_bottom(temp_piece, temp_board):
                        piece_height = len(temp_piece.shape)
                        if temp_piece.y + piece_height >= 20:
                            break
                        temp_piece.y += 1

                    temp_board = Functions.lockBoard(temp_piece, temp_board)
                    temp_board, lines_cleared = Functions.clear_lines(temp_board)
                    state = Functions.make_state(temp_board, next_piece_type)
                    score, back_to_back_temp = Functions.score_count(lines_cleared, back_to_back)
                    
                    reward = Functions.compute_reward_geneticAI(temp_piece, temp_board, lines_cleared, state, weights) + score
                    
                    if reward > best_score:
                        best_score = reward
                        best_rotation = rotations
                        best_position = column
            
            # Applies the best move
            for _ in range(best_rotation):
                current_piece.rotate_right()
            current_piece.x = best_position
            
            while not Collision.collision_piece_bottom(current_piece, board):
                current_piece.y += 1
                Functions.print_board_terminal(current_piece,board)
                time.sleep(0.01)

            board = Functions.lockBoard(current_piece, board)
            board, lines_cleared = Functions.clear_lines(board)
            
            score, back_to_back = Functions.score_count(lines_cleared, back_to_back)
            pieces_placed += 1
            total_score += score + pieces_placed  
            total_lines_cleared += lines_cleared
            
            current_piece = next_piece
            current_piece_type = next_piece_type
            next_piece_type = random.choice(Pieces_list)
            next_piece = Functions(PIECES[next_piece_type], x=4, y=0)
            
            if Functions.endgame(current_piece, board):
                break
