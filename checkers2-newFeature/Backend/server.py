import pygame 
from frontend.constants import BLACK , WHITE , BLUE , SQUARE_SIZE , GREY , SILVER , SILVER_DAME
from frontend.plateau import Plateau
from frontend.pion import Pion

class server :
    def __init__(self,win ):
        self.selected = None 
        # self.ai_selected = None
        self.plateau = Plateau()
        self.turn = None
        self.turnK = GREY
        self.valid_moves = {}
        self.win = win 
        self.first = True
        self.continue_turn = False
    
    def setfirst (self , att):
        self.first = att

    def setTurn(self , turn ):
        self.turn = turn
    
    def setTurnK(self , turnk) :
        self.turnk = turnk

    def set_valid_moves(self, row_des, col_des):
        self.row_des = row_des
        self.col_des = col_des
        self.valid_moves = {(row_des, col_des)}  # Update valid_moves with row_des and col_des

    def get_valid_moves(self):
        return self.valid_moves
    
    def add_to_valid_moves(self, key, value):
        self.valid_moves[key] = value


    
    def update(self):
        self.plateau.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # # 1 underscore mean private
    def _initialization(self):
        self.selected = None 
        self.plateau = Plateau()
        self.turn = None 
        self.valid_moves = {}

    def reset(self):
        self._initialization()

  
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        else:
            pion = self.plateau.get_pion(row, col)
            if self.first:
                self.setTurnK(GREY if (isinstance(pion, Pion) and pion.color == SILVER) else SILVER)
                self.setTurn(pion.color) if isinstance(pion, Pion) else None
                # self.setTurn(if (isinstance(pion, Pion)  and pion.color)
                self.first = False
            
       

            if  isinstance(pion, Pion) and pion != 0 and (pion.color == self.turn or pion.color == self.turnk):
            # if isinstance(pion, Pion) and pion != 0 and (pion.color == self.turn or pion.color == self.turnk or pion.color == SILVER_DAME) :
                self.selected = pion
                self.valid_moves = self.plateau.get_valid_moves(pion)
                print('valid moves are ', self.valid_moves)
                return True

        return False


    def _move(self, row, col):
        piece = self.plateau.get_pion(row, col)
        if  piece == 0 and (row, col) in self.valid_moves:
            move_info = self.valid_moves[(row, col)]
            # Extract move information
            moved_pawn, r, c, is_skip = move_info[:4] if len(move_info) == 4 else move_info[:5]
            color = None if len(move_info) == 4 else move_info[3]
            # print('before change position ')
            self.plateau.changerPosition(self.selected, row, col)
            # print('after change position')
            if is_skip:
                self.handle_captures(r, c, color)
                # After a capture, check for additional valid capture moves
                self.selected = self.plateau.get_pion(row, col)  # Update selected to the new position
                additional_moves = self.plateau.get_valid_moves(self.selected)
                additional_capture_moves = {move: details for move, details in additional_moves.items() if details[-1]}

                if additional_capture_moves:
                    print('Additional capture moves available, BLACK retains the turn.')
                    # Keep the piece selected for further moves
                    return True
                else:
                    print('No additional capture moves, turn changes.')
            # Change turn if no capture was made or no additional captures are possible
   
            self.change_turn()
            self.selected = None  # Deselect piece after turn change or move
            return True
        else:
            print('Invalid move!')
            return False


    def handle_captures(self, r, c, color):
        # Assuming this method handles the removal of captured pieces
        if isinstance(r, (list, tuple)) and isinstance(c, (list, tuple)):
            for skip_row, skip_col in zip(r, c):
                self.plateau.supprimer(skip_row, skip_col, color)
        else:
            self.plateau.supprimer(r, c, color)


    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)




    def change_turn(self):
        # Check if the turn should continue for BLACK after a capture
        if hasattr(self, 'continue_turn') and self.continue_turn:
            # Reset the flag for the next action
            self.continue_turn = False
            print("BLACK retains the turn after a capture.")
            return  # Do not change the turn

        self.valid_moves = {}

        # Assuming SILVER_DAME is treated as a special case of BLACK
        if self.turn == WHITE:
            self.turn = BLACK
            self.turnk = GREY  # Assuming turnk is used to allow SILVER_DAME to move with BLACK
        elif self.turn == BLACK:
            self.turn = WHITE
            self.turnk = SILVER_DAME  # Resetting turnk as it's now WHITE's turn

        # Additional logic to handle GREY if necessary
        elif self.turnK == GREY:
            self.turnK = SILVER_DAME
            self.turn = WHITE
        elif self.turnK == SILVER_DAME:
            self.turnK = GREY
            self.turn = BLACK



    def get_turn(self):
        if self.turn == BLACK:
            return 'BLACK'
        elif self.turn == WHITE:
            return 'WHITE'
        elif self.turnK == GREY:
            return "Grey's turn (Silver Dame with Black)"
        elif self.turnK == SILVER_DAME:
            return "Silver Dame's turn (with White)"
        else:
            return "Unknown turn state"

   

      


    def winner(self):
        return self.plateau.winner()
    

    




    

