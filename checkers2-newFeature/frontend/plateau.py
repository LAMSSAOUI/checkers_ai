import pygame 
from frontend.constants import SILVER , BLACK , ROWS , COLS , SQUARE_SIZE , WHITE,blackPion , WhitePion , GREY , SILVER_DAME
from frontend.pion import Pion
import random
# from Backend.server import server
# from Backend.server import server
from copy import deepcopy


class Plateau :
    def __init__(self):
        self.plateau = []
        self.black_restant = self.white_restant = 12
        self.red_kings = self.white_kings = 0
        self.create_Plateau()
        

    # Draw just squares 

    def draw_squares(self , win):
        win.fill(SILVER)
        for row in range(ROWS):
            for col in range(row % 2 , COLS , 2):
                pygame.draw.rect(win , BLACK , (row*SQUARE_SIZE , col*SQUARE_SIZE , SQUARE_SIZE , SQUARE_SIZE ))

    # def print_board(self):
    #     for row in self.plateau:
    #         print(' '.join([str(p) if p else '.' for p in row]))
    # def print_board(self):
    #     print("  " + " ".join(str(col) for col in range(len(self.plateau[0]))))  # Print column headers
    #     for index, row in enumerate(self.plateau):
    #         print(str(index) + ' ' + ' '.join(['.' if p is None else str(p) for p in row]))

        
    #  draw just pieces 
            
    def create_Plateau(self):
        for row in range(ROWS):
            self.plateau.append([])
            for col in range(COLS):
                if col % 2 == (( row + 1 ) % 2 ) :
                    if row < 3 :
                        self.plateau[row].append(Pion(row , col , WhitePion))
                    elif row > 4 :
                        self.plateau[row].append(Pion(row , col , blackPion))
                        # self.plateau[row].append(Pion(row , col , GREY))
                    else :
                        self.plateau[row].append(0)
                else :
                    self.plateau[row].append(0)
    


    # draw all the squares and pieces 

    def draw(self , win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                # we should call the function here
                pion = self.plateau[row][col]
                if isinstance(pion, Pion):  # Check if pion is an instance of the Pion class
                    pion.draw(win)

                    

    def get_valid_moves(self, pion):
        ROWS = 7
        moves = {}
        r = pion.row 
        COLS = 7
        # print('the row of pion is ', r)
        # col = pion.col
        col = pion.col 

        # start_ligne_black = r 
        # stop_ligne_black = r - 1
        # step_ligne_black = -1
        # start_ligne_white = r
        # stop_ligne_white = r + 1
        # step_ligne_white = 1
        # nbr_pion_should_be_deleted = []
        # print('la couleur du pion is', pion.color)


        if pion is not None and pion.color == BLACK:
            # print('la valeur de pion.dame is ', pion.dame)
            # Define directions in which the BLACK piece can move
            directions = [(-1, -1), (-1, 1)]  # Up-left and up-right
            for d_row, d_col in directions:
                # Check immediate next position
                next_row, next_col = r + d_row, col + d_col
                if 0 <= next_row <= ROWS and 0 <= next_col <= COLS:
                    next_pion = self.get_pion(next_row, next_col)
                    if next_pion == 0:
                        moves[(next_row, next_col)] = (next_pion, next_row, next_col, False)
                    elif next_pion is not None and  next_pion.color == WHITE:
                        jump_row, jump_col = next_row + d_row, next_col + d_col
                        if 0 <= jump_row <= ROWS and 0 <= jump_col <= COLS:
                            jump_pion = self.get_pion(jump_row, jump_col)
                            if jump_pion == 0:
                                moves[(jump_row, jump_col)] = (jump_pion, next_row, next_col, True)
                                # print('we inter in this case')


        if pion is not None and pion.color == GREY:
            ROWS = 7
            COLS = 7
            r = pion.row
            col = pion.col

            for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)] :
                d_row, d_col = direction
                for distance in range(1, 8):  
                    dest_row, dest_col = r + distance * d_row, col + distance * d_col
                    if 0 <= dest_row <= ROWS and 0 <= dest_col <= COLS:
                        current_pion = self.get_pion(dest_row, dest_col)
                        if current_pion == 0:
                            moves[(dest_row, dest_col)] = (current_pion, [dest_row], [dest_col], False)
                        elif  current_pion.color == WHITE:
                            skip_row = current_pion.row
                            skip_col = current_pion.col
                            if 0 <= skip_row <= ROWS and 0 <= skip_col <= COLS:
                                posibility = self.get_pion(skip_row, skip_col)
                                if posibility == 0 :
                                    moves[(skip_row, skip_col)] = (posibility,current_pion.row, current_pion.col, current_pion.color, True)
                        else :
                            break


        if pion is not None and pion.color == WHITE:
            # print('la valeur de pion.dame is ', pion.dame)
            # Define directions in which the WHITE piece can move
            directions = [(1, -1), (1, 1)]  # Down-left and down-right
            for d_row, d_col in directions:
                # Check immediate next position
                next_row, next_col = r + d_row, col + d_col
                if 0 <= next_row <= ROWS and 0 <= next_col <= COLS:
                    next_pion = self.get_pion(next_row, next_col)
                    if next_pion == 0 or next_pion is None:
                        # Position is empty, can move
                        moves[(next_row, next_col)] = (next_pion, next_row, next_col, False)
                    elif next_pion.color == BLACK:
                        # Check if a jump is possible
                        jump_row, jump_col = next_row + d_row, next_col + d_col
                        if 0 <= jump_row <= ROWS and 0 <= jump_col <= COLS:
                            jump_pion = self.get_pion(jump_row, jump_col)
                            if jump_pion == 0:
                                # Can jump over the opponent's piece
                                moves[(jump_row, jump_col)] = (jump_pion, next_row, next_col, True)
                                # print('we inter in this case')
    
                

       


        if pion is not None and pion.color == SILVER_DAME:
            ROWS = 7
            COLS = 7
            r = pion.row
            col = pion.col

            for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)] :
                d_row, d_col = direction
                for distance in range(1, 8):  
                    dest_row, dest_col = r + distance * d_row, col + distance * d_col
                    if 0 <= dest_row <= ROWS and 0 <= dest_col <= COLS:
                        current_pion = self.get_pion(dest_row, dest_col)
                        if current_pion == 0:
                            moves[(dest_row, dest_col)] = (current_pion, [dest_row], [dest_col], False)
                        elif  current_pion.color == WHITE:
                            skip_row = current_pion.row
                            skip_col = current_pion.col
                            if 0 <= skip_row <= ROWS and 0 <= skip_col <= COLS:
                                posibility = self.get_pion(skip_row, skip_col)
                                if posibility == 0 :
                                    moves[(skip_row, skip_col)] = (posibility,current_pion.row, current_pion.col, current_pion.color, True)
                        else :
                            break
        return moves
                

    
 
    def get_pion(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.plateau[row][col]
        else:
            return None
    
    def get_pion_color(self , row , col):
        pion = self.get_pion(row, col)
        if pion is not None and pion != 0:
            pion_color = pion.color
            return pion_color
        else:
            return None
    

    # def changerPosition(self, piece, row, col):
    #     # Server = server(screen)
    #     if not isinstance(piece, Pion):  # Replace 'Piece' with the actual class name of your game pieces
    #         print(f"Error: Expected a Piece object, but got {type(piece)}")
    #         return
       
    #     if piece.dame:
    #         direction_row = 1 if row > piece.row else -1
    #         direction_col = 1 if col > piece.col else -1
    #         temp_row, temp_col = piece.row, piece.col
    #         while temp_row != row or temp_col != col:
    #             temp_row += direction_row
    #             temp_col += direction_col
    #             temp_piece = self.get_pion(temp_row, temp_col)
    #             temp_color = self.get_pion_color(temp_row, temp_col)
    #             print('temp_col', temp_color)
    #             if temp_piece != 0 is not None and temp_color == WHITE:
    #                 self.supprimer(temp_row, temp_col, WHITE)
    #             elif temp_color is None:
    #                 self.plateau[piece.row][piece.col], self.plateau[temp_row][temp_col] = self.plateau[temp_row][temp_col], self.plateau[piece.row][piece.col]
    #                 piece.move(temp_row, temp_col)
    #                 print(f"No piece at position ({temp_row}, {temp_col}) or out of board bounds.")
    #                 break

    #     if abs(row - piece.row) == 2 :
    #         # Calculate the coordinates of the skipped piece
    #         skipped_row = (row + piece.row) // 2
    #         skipped_col = (col + piece.col) // 2
    #         # Delete the skipped piece
    #         self.supprimer(skipped_row, skipped_col, self.get_pion_color(skipped_row, skipped_col))

    #     self.plateau[piece.row][piece.col], self.plateau[row][col] = self.plateau[row][col], self.plateau[piece.row][piece.col]
    #     piece.move(row, col)
    #     if not isinstance(piece, Pion):
    #         print(f"Error: Expected a Pion object, but got {type(piece)}")
    #         return

    #     # Check if the destination is within the board bounds
    #     if not (0 <= row < ROWS and 0 <= col < COLS):
    #         print(f"Attempted move out of board bounds to ({row}, {col})")
    #         return

    #     # Check if the destination is empty
    #     # destination_pion = self.get_pion(row, col)
    #     # if destination_pion is not None:
    #     #     print(f"Destination ({row}, {col}) is not empty: {destination_pion}")
    #     #     return

    #     # Clear the current position
    #     self.plateau[piece.row][piece.col] = 0
    #     print(f"Cleared position ({piece.row}, {piece.col})")

    #     # Move the piece to the new position
    #     self.plateau[row][col] = piece
    #     print(f"Moved piece to ({row}, {col})")

    #     piece.row, piece.col = row, col  # Update the piece's position attributes

    #     if (row == 7 and piece.color == WHITE) or (row == 0 and piece.color == BLACK):
    #         piece.make_dame()
    #         print(f"Piece promoted to dame at ({row}, {col})")

    #     # self.plateau[piece.row][piece.col], self.plateau[row][col] = self.plateau[row][col], self.plateau[piece.row][piece.col]
    #     piece.move(piece.row, piece.col)

    #     if row == 7 or row == 0:
    #         piece.make_dame()
    #         if piece.color == WHITE:
    #             # piece.color = GREY
    #             self.white_kings += 1
    #         else:
    #             self.red_kings += 1 

    #     # change_turn()


    def changerPosition(self, piece, row, col):
        if not isinstance(piece, Pion):
            print(f"Error: Expected a Pion object, but got {type(piece)}")
            return

        if piece.dame:
            direction_row = 1 if row > piece.row else -1
            direction_col = 1 if col > piece.col else -1
            temp_row, temp_col = piece.row, piece.col
            while temp_row != row or temp_col != col:
                temp_row += direction_row
                temp_col += direction_col
                temp_piece = self.get_pion(temp_row, temp_col)
                temp_color = self.get_pion_color(temp_row, temp_col)
                # print('temp_col', temp_color)
                if temp_piece != 0 is not None and temp_color == WHITE:
                    self.supprimer(temp_row, temp_col, WHITE)
                elif temp_color is None:
                    if 0 <= temp_row < len(self.plateau) and 0 <= temp_col < len(self.plateau[temp_row]):
                        self.plateau[piece.row][piece.col], self.plateau[temp_row][temp_col] = self.plateau[temp_row][temp_col], self.plateau[piece.row][piece.col]
                        piece.move(temp_row, temp_col)
                        print(f"No piece at position ({temp_row}, {temp_col}) or out of board bounds.")
                        break

        if abs(row - piece.row) == 2:
            # Calculate the coordinates of the skipped piece
            skipped_row = (row + piece.row) // 2
            skipped_col = (col + piece.col) // 2
            # Delete the skipped piece
            self.supprimer(skipped_row, skipped_col, self.get_pion_color(skipped_row, skipped_col))

        # Visual update: Move the piece on the screen
        # Update the position of the piece on the screen
        # Something like: piece.move_visual(row, col)
        # This function should update the visual representation of the piece's position
        self.plateau[piece.row][piece.col], self.plateau[row][col] = self.plateau[row][col], self.plateau[piece.row][piece.col]
        piece.move(row, col)

        if (row == 7 and piece.color == WHITE) or (row == 0 and piece.color == BLACK):
            piece.make_dame()
            print(f"Piece promoted to dame at ({row}, {col})")

        # Clear the current position
        self.plateau[piece.row][piece.col] = 0
        print(f"Cleared position ({piece.row}, {piece.col})")

        # Move the piece to the new position
        self.plateau[row][col] = piece
        print(f"Moved piece to ({row}, {col})")

        piece.row, piece.col = row, col  # Update the piece's position attributes
        print('the piece.row is ', piece.row)
        print('the piece.col is ', piece.col)


        
        # self.draw()
        if row == 7 or row == 0:
            piece.make_dame()
            if piece.color == WHITE:
                # piece.color = GREY
                self.white_kings += 1
            else:
                self.red_kings += 1

        # change_turn()




    # def changerPosition(self, piece, row, col):
    #     if not isinstance(piece, Pion):
    #         print(f"Error: Expected a Pion object, but got {type(piece)}")
    #         return

    #     # Check if the destination is within the board bounds
    #     if not (0 <= row < ROWS and 0 <= col < COLS):
    #         print(f"Attempted move out of board bounds to ({row}, {col})")
    #         return

    #     # Check if the destination is empty or if capturing
    #     destination_pion = self.get_pion(row, col)
    #     if destination_pion is not None :
    #         print(f"Destination ({row}, {col}) is not empty: {destination_pion}")
    #         return

    #     # Handle normal move or capture
    #     if abs(row - piece.row) == 2:
    #         # Calculate the coordinates of the skipped piece
    #         skipped_row = (row + piece.row) // 2
    #         skipped_col = (col + piece.col) // 2
    #         # Remove the skipped piece
    #         self.supprimer(skipped_row, skipped_col, self.get_pion_color(skipped_row, skipped_col))

    #     # Clear the current position
    #     self.plateau[piece.row][piece.col] = None
    #     print(f"Cleared position ({piece.row}, {piece.col})")

    #     # Move the piece to the new position
    #     self.plateau[row][col] = piece
    #     print(f"Moved piece to ({row}, {col})")

    #     # Update the piece's position attributes
    #     piece.row, piece.col = row, col

    #     # Check for promotion to dame
    #     if (row == 7 and piece.color == WHITE) or (row == 0 and piece.color == BLACK):
    #         piece.make_dame()
    #         print(f"Piece promoted to dame at ({row}, {col})")
    #         if piece.color == WHITE:
    #             self.white_kings += 1
    #         else:
    #             self.red_kings += 1
        
        
    def print_board_state(self):
        for row in self.plateau:
            # print('row =', row ) 
            print(['1' if pion else '0' for pion in row])

    def supprimer (self  , row , col , color):
        self.plateau[row][col] = 0 
        print('la couleur de pion skipped from plateau ' , color)
        if color == WHITE:
            self.white_restant =  self.white_restant-1
            print('the number now of white_restant is' , self.white_restant)
        if color == BLACK:
            self.black_restant =  self.black_restant-1
            print('the number now of black_restant is' , self.black_restant)

   

    # def ai_move(self):
    #     print('########## we enter here in ai move #############')
    #     if not self.winner():  # Check if the game is still ongoing
    #         best_move = self.choose_best_move(WHITE)
    #         print('######## the best move is ######## ', best_move)
    #         if best_move:
    #             from_pos, to_pos = best_move
    #             piece = self.get_pion(*from_pos)
    #             self.changerPosition(piece, *to_pos[:2])
    #             if self.winner():
    #                 print(f"Game Over. Winner: {self.winner()}")
    #         else:
    #             print("No valid moves for AI")
    #     else:
    #         print(f"Game Over. Winner: {self.winner()}")


    def ai_move(self , win ):
        # first = 0
        # from Backend.server import server 
        # print('########## we enter here in ai move #############')
        if self.black_restant != 0 and self.white_restant != 0 :  
            # initial_state = deepcopy(self.plateau)
            best_move = self.monte_carlo_Algorithme(WHITE)  
            print('######## the best move is ######## ', best_move)
            # self.plateau = deepcopy(initial_state)
            if best_move:

                row, col = best_move.row , best_move.col
                print('from_pos and from_pos is ', row , col)
                from_piece = self.get_pion(row , col)
                # row , col = from_pos
                # r1 , c1 = to_pos
                
                print('row and col of the from piece', row , col)
                valid_moves_for_this_pion = self.get_valid_moves(best_move)
                print('valid_moves_for_this_pion' , valid_moves_for_this_pion)
                keys = list(valid_moves_for_this_pion.keys())
                print('my keys of destination now are ',keys[0][0],keys[0][1])  
                row_des = keys[0][0]
                col_des = keys[0][1]
                # piece = self.get_pion(row , col)
                # print('this is piece', piece)
                # if piece  :
                self.changerPosition( from_piece, row_des , col_des)
                    # self.plateau[r1].append(Pion(r1 , c1 , WHITE))
                    # if self.winner():
                    #     print(f"Game Over. Winner: {self.winner()}")
                # else:
                #     print("No piece at the starting position which is ", row , col)
                return row , col 
            else:
                print("No valid moves for AI")
        else:
            print(f"Game Over. Winner: {self.winner()}")
       


    # def ai_move(self):
    #     print('########## we enter here in ai move #############')
    #     if not self.winner():  # Check if the game is still ongoing
    #         best_move = self.choose_best_move(WHITE)  # Assuming WHITE is the AI color
    #         print('######## the best move is ######## ', best_move)
    #         if best_move:
    #             from_pos, to_pos = best_move
    #             piece = self.get_pion(*from_pos)
    #             if piece:
    #                 self.changerPosition(piece, *to_pos)
    #                 if self.winner():
    #                     print(f"Game Over. Winner: {self.winner()}")
    #             else:
    #                 print("No piece at the starting position")
    #         else:
    #             print("No valid moves for AI")
    #     else:
    #         print(f"Game Over. Winner: {self.winner()}")
            

    def winner(self):
        if self.black_restant == 0:
            return WHITE
        elif self.white_restant == 0:
            return BLACK
        return None 
    

    # def simulate_game(self, player_color):
    #     # Simulate a random game from the current state
    #     current_board = self.plateau
    #     current_player = player_color
    #     move_count = 0
    #     while not self.winner() and move_count < 100:  # Limiting move count to prevent infinite loops
    #         valid_moves = self.get_all_valid_moves(current_player)
    #         if not valid_moves:
    #             break
    #         move = random.choice(list(valid_moves.keys()))
    #         self.changerPosition(self.get_pion(*move[0]), *move[1][:2])
    #         current_player = 'white' if current_player == 'black' else 'black'
    #         move_count += 1
    #     return self.winner()

    def simulate_game(self, player_color):
        # Simulate a random game from the current state
        current_board = self.plateau
        current_player = player_color
        move_count = 0
        while not self.winner() and move_count < 3:  # Limiting move count to prevent infinite loops
            valid_moves = self.get_all_valid_moves(current_player)
            if not valid_moves:
                break
            move = random.choice(list(valid_moves.keys()))
            start_pos, end_pos = move, random.choice(list(valid_moves[move].keys()))
            self.changerPosition(self.get_pion(*start_pos), *end_pos[:2])
            current_player = WHITE if current_player == BLACK else BLACK
            move_count += 1
        return self.winner()

    def monte_carlo_tree_search(self, player_color, iterations=3):
        wins = 0
        for _ in range(iterations):
            winner = self.simulate_game(player_color)
            if winner == player_color:
                wins += 1

        
        return wins / iterations

    # def choose_best_move(self, player_color):
    #     # print(' ########## we are in best moves  function  ###########')
    #     valid_moves = self.get_all_valid_moves(player_color)
    #     print(' $$$$$  this is all moves in choose best move function $$$$$$ \n', valid_moves)
    #     best_move = None
    #     best_score = -1
    #     for move, details in valid_moves.items():
    #         print('move is ',move)
    #         # Simulate making the move
    #         original_piece = self.get_pion(*move[0])
    #         self.changerPosition(original_piece, *move[1][:2])
    #         score = self.monte_carlo_tree_search(player_color)
    #         # Undo the move
    #         self.changerPosition(self.get_pion(*move[1][:2]), *move[0])
    #         if score > best_score:
    #             best_score = score
    #             best_move = move
    #     return best_move
    def jouer_aleatoirement(self):
        import random
        players = ['WHITE', 'BLACK']
        return random.choice(players)

    def monte_carlo_Algorithme(self, player_color):
        valid_moves = self.get_all_valid_moves(player_color)
        print('valid moves in monte carlos algorithme ', valid_moves.items())
        choix = None
        max_score = 0
        # temp_plateau = deepcopp
        keys = [(item[0] , item[1]) for item in valid_moves]
        print('the keys are ', keys)
        # for start_pos, moves in valid_moves.items():
        for pion in keys :
            Gain = 0 
            print('le pion now is ', pion)
            pion = self.get_pion(pion[0], pion[1])
            valid_move = self.get_valid_moves(pion)
            print('la valid move is ', valid_move)
            # random 
            memoriserTableau = deepcopy(self.plateau)
            for _ in range (3) :
                takeWinner = self.jouer_aleatoirement()
                print('take winner now is ', takeWinner)
                if takeWinner == 'WHITE' :
                    Gain = Gain + 1
                    print('la valeur de Gain is now ', Gain)
                    self.tableau = deepcopy(memoriserTableau)
            if Gain>max_score :
                max_score = Gain
                choix = pion 
            print('la valeur de gain is ', Gain)
        

        return choix
    

    def get_all_valid_moves(self, player_color):
        moves = {}
        for row in range(ROWS):
            for col in range(COLS):
                pion = self.plateau[row][col]
                if pion != 0 and pion.color == player_color:
                    valid_moves = self.get_valid_moves(pion)
                    if valid_moves:
                        moves[(row, col)] = valid_moves
        return moves
    # def get_all_valid_moves(self, player_color):
    #     moves = {}
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             pion = self.get_pion(row, col)
    #             if pion is not None and pion.color == player_color:
    #                 valid_moves = self.get_valid_moves(pion)
    #                 if valid_moves:
    #                     moves[(row, col)] = valid_moves
    #     return moves






    #   original_piece = self.get_pion(*start_pos)
    #         for end_pos, move_details in moves.items():
    #             # Simulate the move
    #             self.changerPosition(  original_piece, *end_pos[:2])
    #             print('second argument in choose best move  ', *end_pos[:2])
    #             score = self.monte_carlo_tree_search(player_color)
    #             # Undo the move
    #             # self.changerPosition(self.get_pion(*end_pos[:2]), *start_pos )

    #             if score > best_score:
    #                 best_score = score
    #                 best_move = (start_pos, end_pos)

    





#  