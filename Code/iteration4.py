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

SQ_DIM = 50 #Square dimensions if the GUI is to change e.g. phone

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
black_pieces = [bPawn,bKing,bQueen,bBishop,bRook,bKnight]
white_pieces = [wPawn,wKing,wQueen,wBishop,wRook,wKnight]

#Starting board array
A = [bRook,bKnight,bBishop,bQueen,bKing,bBishop,bKnight,bRook]
B = [bPawn,bPawn,bPawn,bPawn,bPawn,bPawn,bPawn,bPawn]
C = [0,0,0,0,0,0,0,0]
D = [0,0,0,0,0,0,0,0]
E = [0,0,0,0,wQueen,0,0,0]
F = [0,0,0,0,0,0,0,0]
G = [wPawn,wPawn,wPawn,wPawn,wPawn,wPawn,wPawn,wPawn]
H = [wRook,wKnight,wBishop,wQueen,wKing,wBishop,wKnight,wRook]
piece_pos= [A,B,C,D,E,F,G,H]

#Pawn Original position array
wPawn_orig_pos = [[6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[6,7]]
bPawn_orig_pos = [[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7]]

class board:
    def __init__(self):
        self.board = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
        self.prv_pos = []
        self.selectedB4 = False
        self.color = ""
        self.crnt_player = "White"

    #Put in button class later  
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
        self.sq_colour = WHITE
        #Draw the board
        for i in range(0,8):
            for j in range(0,8):
                pygame.draw.rect(self.board, self.sq_colour,(self.X,self.Y,SQ_DIM,SQ_DIM),0)
                if piece_pos[i][j] == 0:
                    pass
                else:
                    self.board.blit(piece_pos[i][j],(self.X,self.Y))
                #Change of X coord
                if self.X >(SQ_DIM*6):
                    self.X = 0
                    self.Ycounter = True
                    self.sqcounter = True
                else:
                    self.X +=(SQ_DIM)
                    
                #Change of Y coord
                if self.Ycounter == True:
                    self.Y +=SQ_DIM
                    self.Ycounter = False
                else:
                    pass
                
                #Change of colour
                if self.sqcounter == True:
                    self.sqcounter = False
                else:
                    if self.sq_colour == BLACK:
                        self.sq_colour = WHITE
                    else:
                        self.sq_colour = BLACK
            self.drawbutton("save",SQ_DIM*8,SQ_DIM)
            self.drawbutton("load",SQ_DIM*8,SQ_DIM*3)
            self.drawbutton("exit",SQ_DIM*8,SQ_DIM*5)

    #Welcome to Hell: The Longest Function/What I cry over the most
    def onclick(self,pos):
        #Convert the coordinates suitable for 2d array
        x = (pos[0]//SQ_DIM)
        y = (pos[1]//SQ_DIM)
        print(y,x)
        #Check if there is an already selected piece
        if self.selectedB4 == False:
            #Check if the mouse clicked outside the chessboard
            if pos[0] > SQ_DIM*8:
                return
            #Highlight a selected piece
            if piece_pos[y][x] == 0:
                pass
            elif piece_pos[y][x] != 0:
                self.prv_pos = [x, y]
                self.color = self.board.get_at((self.prv_pos[0]*SQ_DIM, self.prv_pos[1]*SQ_DIM))
                self.board.blit(square,(x*SQ_DIM,y*SQ_DIM))
                self.board.blit(piece_pos[y][x],(x*SQ_DIM,y*SQ_DIM))
                self.selectedB4 = True
                #Calculate possible moves
                self.calcMoves(y,x)
        #Deselect piece
        else:
            self.color = self.board.get_at(((x * SQ_DIM)+2, (y * SQ_DIM)+2))
            print("self color")
            print(self.color)
            #If same piece is picked, de highlight
            if piece_pos[y][x] == piece_pos[self.prv_pos[1]][self.prv_pos[0]]:
                self.draw()
            #If another destination picked, move
            elif self.color != BLACK and self.color != WHITE and self.color != OLIVEGREEN:
                self.MovePiece(y,x)
            else:
                self.draw()
            self.selectedB4 = False
            
    def calcMoves(self,y,x):
        moves = []
        #Probable next moves for:
        #Knights
        if piece_pos[y][x] in black_pieces:
            player_col = "Black"
            crnt_side = black_pieces
        elif piece_pos[y][x] in white_pieces:
            player_col = "White"
            crnt_side = white_pieces
            
        if piece_pos[y][x] == wKnight or piece_pos[y][x] == bKnight:
            print("Knight")
            moves = [[y-2,x+1],[y-2,x-1],[y-1,x-2],[y+1,x-2],
                     [y-1,x+2],[y+1,x+2],[y+2,x-1],[y+2,x+1]]
            
        #Bishops
        elif piece_pos[y][x] == wBishop or piece_pos[y][x] == bBishop:
            print("Bishop")
            self.diagonals(y,x,moves,crnt_side)

        #Rooks
        elif piece_pos[y][x] == wRook or piece_pos[y][x] == bRook:
            print("Rook")
            self.straights(y,x,moves,crnt_side)

        #Queens
        elif piece_pos[y][x] == wQueen or piece_pos[y][x] == bQueen:
            print("Queen")
            self.diagonals(y,x,moves,crnt_side)
            self.straights(y,x,moves,crnt_side)

        #Kings
        elif piece_pos[y][x] == wKing or piece_pos[y][x] == bKing:
            print("King")
            moves = [[y-1,x],[y+1,x],[y,x+1],[y,x-1],
                     [y+1,x+1],[y+1,x-1],[y-1,x-1],[y-1,x+1]]

        #wPawns
        elif piece_pos[y][x] == wPawn:
            print("pawn")
            if piece_pos[y-1][x] == 0:
                moves.append([y-1,x])
            if [y,x] in wPawn_orig_pos:
                moves.append([y-2,x])
            if piece_pos[y-1][x-1] in black_pieces:
                moves.append([y-1,x-1])
            if x+1 >7:
                pass
            else:
                if piece_pos[y-1][x+1] in black_pieces:
                    moves.append([y-1,x+1])

        #bPawns
        elif piece_pos[y][x] == bPawn:
            print("pawn")
            if piece_pos[y+1][x] == 0:
                moves.append([y+1,x])
            if [y,x] in bPawn_orig_pos:
                moves.append([y+2,x])
            if piece_pos[y+1][x-1] in white_pieces:
                moves.append([y+1,x-1])
            if x+1 >7:
                pass
            else:
                if piece_pos[y+1][x+1] in white_pieces:
                    moves.append([y+1,x+1])
        print(moves)
        self.ValidateMoves(player_col,moves)

    def straights(self,y,x,moves,crnt_side):
        for i in range(1,9):
            if y-i>-1:
                if piece_pos[y-i][x] in crnt_side:
                    break
                elif piece_pos[y-i][x] == 0:
                    moves.append([y-i,x])
                else:
                    moves.append([y-i,x])
                    break
        for i in range(1,9):
            if y+i<8:
                if piece_pos[y+i][x] in crnt_side:
                    break
                elif piece_pos[y+i][x] == 0:
                    moves.append([y+i,x])
                else:
                    moves.append([y+i,x])
                    break
        for i in range(1,9):
            if x+i<8:
                if piece_pos[y][x+i] in crnt_side:
                    break
                elif piece_pos[y][x+i] == 0:
                    moves.append([y,x+i])
                else:
                    moves.append([y,x+i])
                    break
        for i in range(1,9):
            if x-i>-1:
                if piece_pos[y][x-i] in crnt_side:
                    break
                elif piece_pos[y][x-i] == 0:
                    moves.append([y,x-i])
                else:
                    moves.append([y,x-i])
                    break

    def diagonals(self,y,x,moves,crnt_side):
        for i in range(1,9):
            if y-i>-1 or x-i >-1:
                if piece_pos[y-i][x-i] in crnt_side:
                    break
                elif piece_pos[y-i][x-i] == 0:
                    moves.append([y-i,x-i])
                else:
                    moves.append([y-i,x-i])
                    break    
        for i in range(1,9):
            if y-i>-1 or x+i < 8:
                if piece_pos[y-i][x+i] in crnt_side:
                    break
                elif piece_pos[y-i][x+i] == 0:
                    moves.append([y-i,x+i])
                else:
                    moves.append([y-i,x+i])
                    break
        for i in range(1,9):
            if y+i <8 or x-i >-1:
                if piece_pos[y+i][x-i] in crnt_side:
                    break
                elif piece_pos[y+i][x-i] == 0:
                    moves.append([y+i,x-i])
                else:
                    moves.append([y+i,x-i])
                    break
        for i in range(1,9):
            if y+i <8 or x+i <8:
                if piece_pos[y+i][x+i] in crnt_side:
                    break
                elif piece_pos[y+i][x+i] == 0:
                    moves.append([y+i,x+i])
                else:
                    moves.append([y+i,x+i])
                    break
    def ValidateMoves(self,player_col,moves):
        FinMoves = []
        MidMoves = []
        for i in range(0,len(moves)):
            if moves[i][0] > 7 or moves[i][0] < 0 or moves[i][1] <0 or moves[i][1] > 7:
                pass
            else:
                MidMoves.append(moves[i])
        #code for filtering out valid moves that is over a piece of the same color
        if player_col == "Black":
            for i in range(0,len(MidMoves)):
                if piece_pos[MidMoves[i][0]][MidMoves[i][1]] in white_pieces or  piece_pos[MidMoves[i][0]][MidMoves[i][1]] == 0:
                    FinMoves.append(MidMoves[i])
        else:
            for i in range(0,len(MidMoves)):
                if piece_pos[MidMoves[i][0]][MidMoves[i][1]] in black_pieces or  piece_pos[MidMoves[i][0]][MidMoves[i][1]] == 0:
                    FinMoves.append(MidMoves[i])
        print(FinMoves)
        print(len(FinMoves))
        self.DisplayMoves(FinMoves)

    def DisplayMoves(self,FinMoves):
        for i in range(0,len(FinMoves)):
            self.board.blit(square,(FinMoves[i][1]*SQ_DIM,FinMoves[i][0]*SQ_DIM))
            if piece_pos[FinMoves[i][0]][FinMoves[i][1]] != 0:
                self.board.blit(piece_pos[FinMoves[i][0]][FinMoves[i][1]],(FinMoves[i][1]*SQ_DIM,FinMoves[i][0]*SQ_DIM))     

    def MovePiece(self,y,x):    
        piece_pos[y][x] = piece_pos[self.prv_pos[1]][self.prv_pos[0]]
        piece_pos[self.prv_pos[1]][self.prv_pos[0]] = 0
        self.draw()
board = board()
board.draw()

while True:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
            board.onclick(pos)
    pygame.display.flip()
