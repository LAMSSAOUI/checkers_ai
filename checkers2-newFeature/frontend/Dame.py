# from frontend.pion import Pion
from frontend.constants import GREY , SQUARE_SIZE 
import pygame
class Dame :
    PADDING = 15 
    OUTLINE = 2 
    def __init__(self ,x,y):
        self.x = x
        self.y = y 
        

    def drawDame(self, win ):
        # radius = SQUARE_SIZE // 2 - 15
        # pygame.draw.circle(win , GREY , (self.x , self.y) , radius + 2)
        
        # pygame.Color.update(GREY)
        # pygame.draw.circle(win , self.color , (self.x , self.y) , radius)
        # if self.pion.color == BLACK:
        #     self.pion.color = WHITE
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.DIAMETER)