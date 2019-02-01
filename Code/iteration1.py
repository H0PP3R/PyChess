#help hhahahaha
import pygame, sys
from pygame.locals import *
import os

#Define constants
#GLOBALS
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

#COLOURS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
OLIVEGREEN = (85, 107, 47)

#IMAGES
wPawn = pygame.image.load("./Chess Sprites/WPawn.png")
wKing = pygame.image.load("./Chess Sprites/WKing.png")
wQueen = pygame.image.load("./Chess Sprites/WQueen.png")
wBishop = pygame.image.load("./Chess Sprites/WBishop.png")
wRook = pygame.image.load("./Chess Sprites/WRook.png")
wKnight = pygame.image.load("./Chess Sprites/WHorse.png")
bPawn = pygame.image.load("./Chess Sprites/BPawn.png")
bKing = pygame.image.load("./Chess Sprites/BKing.png")
bQueen = pygame.image.load("./Chess Sprites/BQueen.png")
bBishop = pygame.image.load("./Chess Sprites/BBishop.png")
bRook = pygame.image.load("./Chess Sprites/BRook.png")
bKnight = pygame.image.load("./Chess Sprites/BHorse.png")
square = pygame.image.load("./Chess Sprites/squaremove.png")

#Starting board array
A = [bRook,bKnight,bBishop,bQueen,bKing,bBishop,bKnight,bRook]
B = [bPawn,bPawn,bPawn,bPawn,bPawn,bPawn,bPawn,bPawn]
C = [0,0,0,0,0,0,0,0]
D = [0,0,0,0,0,0,0,0]
E = [0,0,0,0,0,0,0,0]
F = [0,0,0,0,0,0,0,0]
G = [wPawn,wPawn,wPawn,wPawn,wPawn,wPawn,wPawn,wPawn]
H = [wRook,wKnight,wBishop,wQueen,wKing,wBishop,wKnight,wRook]
piece_pos= [A,B,C,D,E,F,G,H]
            
class board:
    def __init__(self):
        self.board = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])

    def drawbutton(self,text,X,Y):
        pygame.draw.rect(self.board,BLACK,(X,Y,BUTTON_WIDTH,BUTTON_HEIGHT),0)
        self.buttonfont = pygame.font.Font(None,24)
        self.label = self.buttonfont.render(text,1,WHITE)
        self.board.blit(self.label,(X+25,Y+10))
    
    def draw(self):
        pygame.font.init()
    
        #Draw the window
        self.board.fill(OLIVEGREEN)
        self.X = 0
        self.Y = 0
        self.Ycounter = False
        self.sqcounter = False
        self.colour = WHITE
        #Draw the board
        for i in range(0,8):
            for j in range(0,8):
                pygame.draw.rect(self.board, self.colour,(self.X,self.Y,50,50),0)
                if piece_pos[i][j] == 0:
                    pass
                else:
                    self.board.blit(piece_pos[i][j],(self.X,self.Y))
                #Change of X coord
                if self.X >300:
                    self.X = 0
                    self.Ycounter = True
                    self.sqcounter = True
                else:
                    self.X +=50
                    
                #Change of Y coord
                if self.Ycounter == True:
                    self.Y +=50
                    self.Ycounter = False
                else:
                    pass
                
                #Change of colour
                if self.sqcounter == True:
                    self.sqcounter = False
                else:
                    if self.colour == BLACK:
                        self.colour = WHITE
                    else:
                        self.colour = BLACK
        self.drawbutton("save",400,50)
        self.drawbutton("load",400,150)
        self.drawbutton("exit",400,250)
        pygame.display.flip()
    
board = board()
board.draw()
