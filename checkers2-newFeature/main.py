import pygame 
from frontend.constants import WIDTH , HEIGHT  , SQUARE_SIZE ,  SILVER_DAME , WHITE
from Backend.server import server
from frontend.plateau import Plateau
from copy import deepcopy





screen = pygame.display.set_mode((800 , 800))


class GameDisplay:
    def __init__(self, screen, server):
        self.screen = screen
        self.server = server

    def display_winner(self, winner_color):
        font = pygame.font.Font(None, 90)
        # Determine the winner's name based on the color
        if winner_color == (0, 0, 0):  # Assuming (0, 0, 0) represents Black
            winner_text = "Black Wins!"
        elif winner_color == (255, 255, 255):  # Assuming (255, 255, 255) represents White
            winner_text = "White Wins!"
        else:
            winner_text = "Draw!"  # Default message or for other cases

        text = font.render(winner_text, True, (255, 255, 255))  # White color for the text
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(10000) 


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    Server = server(screen)
    game_display = GameDisplay(screen, server)
    plateau = Plateau()
    ai_moved = False


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print('position clicked is ', pos)
                row, col = get_row_col_from_mouse(pos)
                print('by row and col ', row, col)
                Server.select(row, col)

        turn = Server.get_turn()
        if turn == 'WHITE' and not ai_moved :
            piece , row_des , col_des , valid_moves = plateau.ai_move(screen) 
            print('from main this is what you should change ', piece , row_des , col_des)
            # Server.ai_selected = True
            # piece1 = plateau.get_pion( row_des , col_des)
            # print('this is piece in main', piece1)
            # Server.set_valid_moves(row_des , col_des)
            print('this is valid_moves ',valid_moves)
            for key, value in valid_moves.items():
                Server.add_to_valid_moves(key , value)
                # Use key and value to add to valid_moves using the setter method
                # add_to_valid_moves(key, value)

            moves = Server.get_valid_moves()
            print('my moves now ', moves)
            Server.select(piece.row , piece.col)
            plateau.changerPosition(piece , row_des , col_des)
            Server._move(row_des , col_des)
            # piece.move(row_des , col_des )
            ai_moved = True    
            Server.change_turn
            


        

        Server.update()

        winner_color = Server.winner()
        # print('the winner color is ', winner_color)
        if winner_color:
            game_display.display_winner(winner_color)
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


    
