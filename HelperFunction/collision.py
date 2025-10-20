import copy

class Collision():
    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y
            
    #Checks if the piece can rotate right
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
    
    #Checks if the piece can rotate left   
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

    #Checks if the piece can fall
    def collision_piece_bottom(piece, board):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell != 1: 
                    continue

                y = piece.y + i
                x = piece.x + j

                if y + 1 >= len(board):
                    return True
                
                if x < 0 or x >= len(board[0]): 
                    return True

                if y < 0:
                    continue

                if board[y + 1][x] == 1:
                    return True

        return False
  
    #Checks for collision with the right side
    def collision_sides_right(piece, board):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    if piece.x + j >= len(board[0]) or piece.x + j < 0:
                        return True  
                    
                    if 0 <= piece.y + i < len(board):
                        if board[piece.y + i][piece.x + j] == 1:
                            return True
        return False 

    #Checks for collision with the right side
    def collision_sides_left(piece, board):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    if piece.x + j - 1 < 0:
                        return True  
                    if piece.y + i < len(board):
                        if board[piece.y + i][piece.x + j - 1] == 1:
                            return True
        return False 