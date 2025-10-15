from collision import Collision

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
    # Make a copy of the board so we don't modify the original
        temp_board = [row[:] for row in board]

        # Overlay the piece
        if piece:
            shape = piece.shape
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell == 1:
                        board_y = piece.y + i
                        board_x = piece.x + j
                        if 0 <= board_y < len(temp_board) and 0 <= board_x < len(temp_board[0]):
                            temp_board[board_y][board_x] = 1

        # Print the board
        for row in temp_board:
            line = ''.join('#' if cell == 1 else '.' for cell in row)
            print(line)
    
    def print_board(piece, board):
        temp_board = [row[:] for row in board]

        if piece:
            shape = piece.shape
            x, y = piece.x, piece.y
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell == 1:
                        if 0 <= y + i < len(temp_board) and 0 <= x + j < len(temp_board[0]):
                            temp_board[y + i][x + j] = 1

        for row in temp_board:
            line = ''
            for cell in row:
                if cell == 1 or cell == 1:
                    line += 1
                else:
                    line += 0
        return temp_board

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
        # Game over if newly spawned piece collides immediately
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    if piece.y + i < 0 or piece.y + i >= 20:
                        return True
                    if board[piece.y + i][piece.x + j] == 1:
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
        height = state[:10]  # list of 10 heights
        holes = Functions.count_holes(board)          # number of empty cells with blocks above
        bumpiness = Functions.bumpiness(height)      # sum of height differences between adjacent columns
        
        reward = 0

        # Game over penalty
        if Functions.endgame(current_piece,board):
            reward -= 500

        # Reward for line clears
        if lines_cleared == 1:
            reward += 100
        elif lines_cleared == 2:
            reward += 300
        elif lines_cleared == 3:
            reward += 500
        elif lines_cleared == 4:
            reward += 800  # Tetris

        # Penalties for bad board features
        reward -= (0.5 * holes + 0.3 * bumpiness + 0.2 * max(height))

        return reward
    
    
    def score_count(line_count, back_to_back):
        score = 0
        if line_count == 1:
            score += 100
            back_to_back = False
        if line_count == 2:
            score += 300
            back_to_back = False
        if line_count == 3:
            score += 500
            back_to_back = False
        if line_count == 4:
            score += 800
            if back_to_back:
                score += 800
            back_to_back = True
        return score, back_to_back
    
    def bumpiness(state):
        total = 0
        for item in range(9):
            total += abs(state[item] - state[item+1])
        return total