import copy

class Collision():
    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y
            
    #Checks if u can rotate right without going outside of the board
    def collision_rotation_right(piece, board):
        temp_piece = copy.deepcopy(piece)
        
        rotate = True
        temp_piece.rotate_right()
        for i, row in enumerate(temp_piece.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    if temp_piece.y + i >= len(board) or temp_piece.x + j >= 10 or temp_piece.x + j < 0 or temp_piece.y + i < 0:
                        rotate = False 
                        break
                    if board[temp_piece.y+i][temp_piece.x+j] == 1:
                        return True
            if not rotate:
                return True
        if rotate:
            return False
    
    #Checks if u can rotate left   
    def collision_rotation_left(piece, board):
        temp_piece = copy.deepcopy(piece)
        
        rotate = True
        temp_piece.rotate_left()
        for i, row in enumerate(temp_piece.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    if temp_piece.y + i >= len(board) or temp_piece.x + j >= 10 or temp_piece.x + j < 0 or temp_piece.y + i < 0:
                        rotate = False
                        break
                    if board[temp_piece.y+i][temp_piece.x+j] == 1:
                        return True
            if not rotate:
                return True
        if rotate:
            return False   


    def collision_piece_bottom(piece, board):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    # Check if piece itself is already out of bounds
                    if piece.y + i >= len(board):
                        return True
                        
                    # Check if next position would be out of bounds
                    if piece.y + i + 1 >= len(board):
                        return True
                    
                    # Check for collision with other pieces
                    if piece.x + j >= 10 or piece.x + j < 0:
                        return True
                        
                    if board[piece.y + i + 1][piece.x + j] == 1:
                        return True
        return False
        
    #Checks for collision with the right side of the board when going right
    def collision_sides(piece, board):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    # right boundary
                    if piece.x + j >= len(board[0]) or piece.x + j < 0:
                        return True  # collision
                    # cell occupied
                    if 0 <= piece.y + i < len(board):
                        if board[piece.y + i][piece.x + j] == 1:
                            return True
        return False  # no collision

    def collision_sides_left(piece, board):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    if piece.x + j - 1 < 0:
                        return True  # collision
                    if piece.y + i < len(board):
                        if board[piece.y + i][piece.x + j - 1] == 1:
                            return True
        return False  # no collision