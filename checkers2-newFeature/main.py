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
        # print('the turn now from main file is ',turn )
        # new = deepcopy(plateau)
        # plateau.print_board() 
        # print("Board state before move:")
        # plateau.print_board_state()
        if turn == 'WHITE' :
            # print('########## we are in white #############')
            plateau.ai_move(screen) 
            # print('the r1 and c1 ', r1  , c1 )
            # Server._move(r1 , c1)
            # print("Board state after move:")
            # plateau.print_board_state()
            Server.change_turn

        # plateau.draw(screen)
        
            


        

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


    
