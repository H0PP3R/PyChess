#Get buttons working, better system of piece pos (self.dict), player change
import pygame as pg,sys
from pygame.locals import *
import sys
import os

class main:
    def __init__(self):
        self.board = None
        self.GUI = None
        self.selectedB4 = False
        self.color = ""
        self.crnt_player = "White"
        self.crnt_side = []
        self.running = True

    def main_loop(self):
        while self.running:
            self.ev = pg.event.get()
            for event in self.ev:
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.pos = pg.mouse.get_pos()
                    print(self.pos)
                    self.onclick()
                pg.display.flip()
        if self.running == False:
            pg.display.quit()
                
    def onclick(self):
        #Convert the coordinates suitable for 2d array
        x = (self.pos[0]//self.GUI.SQ_DIM)
        y = (self.pos[1]//self.GUI.SQ_DIM)
        print(y,x)
        print("current player:"+self.crnt_player)
        #changes of player
        if self.crnt_player == "White":
            self.crnt_side = self.pieces.white_pieces
        else:
            self.crnt_side = self.pieces.black_pieces
        #navigation
        if x>=8:
            if y == 1:
                print("saving...")
                self.navigation.game_save()
            elif y == 3:
                print("loading...")
                self.navigation.game_load()
            elif y == 5:
                print("exiting...")
                self.navigation.game_exit()
                
        if self.selectedB4 == False:
            if x <8:
                if (self.piece_at(y,x) in self.crnt_side) or self.piece_at(y,x) == 0:
                    self.select_piece(y,x)
        else:
            self.select_destination(y,x)
        
    def select_piece(self,y,x):
        #Check if the mouse clicked outside the chessboard
        if self.pos[0] > self.GUI.SQ_DIM*8:
            return
        #Highlight a selected piece
        if self.piece_at(y,x) == 0:
            pass
        elif self.piece_at(y,x) != 0:
            print("highlight selected: "+self.piece_at(y,x))
            self.board.prv_pos_update(x,y)
            self.GUI.highlight(y,x)
            self.selectedB4 = True
            #Calculate possible moves
            self.calc.calcMoves(y,x)
            
    def select_destination(self,y,x):
        self.color = self.colour_at(x,y)
        if y < 8 and y > -1 and x < 8 and x > -1:
            #If same piece is picked, de highlight
            if self.piece_at(y,x) == self.piece_at(self.prv_pos_at(1),self.prv_pos_at(0)):
                pass
            #If another destination picked, move
            elif self.color != self.GUI.BLACK and self.color != self.GUI.WHITE and self.color != self.GUI.OLIVEGREEN:
                self.Update_board(y,x)
            self.selectedB4 = False
            self.GUI.draw_board()
            
    def add_board(self,board):
        self.board = board

    def add_GUI(self,GUI):
        self.GUI = GUI
        self.pieces = self.GUI.pieces
        self.dict = self.GUI.pieces.dict

    def add_calc(self,calc):
        self.calc = calc

    def add_pieces(self,pieces):
        self.pieces = pieces

    def add_navigation(self,navigation):
        self.navigation = navigation

    def UpdateMain(self,new_board):
        self.board.piece_pos = new_board

    def UpdatePlayer(self,new_player):
        self.crnt_player = new_player
        
    def piece_at(self,y,x):
        return self.board.piece_pos[y][x]

    def prv_pos_at(self,item):
        return self.board.prv_pos[item]

    def colour_at(self,x,y):
        return self.GUI.window.get_at(((x*self.GUI.SQ_DIM)+2, (y*self.GUI.SQ_DIM)+2))
        
    def Update_board(self,y,x):
        self.board.UpdatePos(y,x)
        
class navigation:
    def __init__(self,GUI):
        self.GUI = GUI
        self.main = self.GUI.main
        self.GUI.draw_button("save",self.GUI.SQ_DIM*8,self.GUI.SQ_DIM)
        self.GUI.draw_button("load",self.GUI.SQ_DIM*8,self.GUI.SQ_DIM*3)
        self.GUI.draw_button("exit",self.GUI.SQ_DIM*8,self.GUI.SQ_DIM*5)

    def game_save(self):
        self.piece_pos = self.GUI.main.board.piece_pos
        file = open("Save file.txt","w")
        for line in self.piece_pos:
            for item in line:
                file.write(str(item)+",")
            file.write("\n")
        file.write(self.main.crnt_player)
        file.close()
        
    def game_load(self):
        self.board = self.GUI.main.board
        lda = []
        file = open("Save file.txt","r")
        file_lines = file.readlines()
        for line in file_lines:
            line_list = line.rstrip("\n").split(",")
            if line_list != ["Black"] and line_list != ["White"]:
                line_list.pop()
                #Change string 0 to iteger
                for i in range(0,8):
                    if line_list[i]== '0':
                        line_list[i] = 0
                lda.append(line_list)
            else:
                self.main.UpdatePlayer(line)
        file.close()
        self.board.UpdateBoard(lda)
        self.GUI.draw_board()
        
    def game_exit(self):
        self.main.running = False
        
class board:
    def __init__(self,main):
        self.main = main
        self.pieces = self.main.pieces
        self.prv_pos = []
        self.dict = self.pieces.dict
        A = ["bRook","bKnight","bBishop","bQueen","bKing","bBishop","bKnight","bRook"]
        B = ["bPawn","bPawn","bPawn","bPawn","bPawn","bPawn","bPawn","bPawn"]
        C = [0,0,0,0,0,0,0,0]
        D = [0,0,0,0,0,0,0,0]
        E = [0,0,0,0,0,0,0,0]
        F = [0,0,0,0,0,0,0,0]
        G = ["wPawn","wPawn","wPawn","wPawn","wPawn","wPawn","wPawn","wPawn"]
        H = ["wRook","wKnight","wBishop","wQueen","wKing","wBishop","wKnight","wRook"]
        self.piece_pos= [A,B,C,D,E,F,G,H]
        #Pawn Original position array
        self.wPawn_orig_pos = [[6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[6,7]]
        self.bPawn_orig_pos = [[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7]]
        
    def prv_pos_update(self,x,y):
        self.prv_pos = [x,y]

    def UpdateBoard(self,new_board):
        self.piece_pos = new_board
        self.main.UpdateMain(self.piece_pos)

    def UpdatePos(self,y,x):
        self.piece_pos[y][x] = self.piece_pos[self.prv_pos[1]][self.prv_pos[0]]
        self.piece_pos[self.prv_pos[1]][self.prv_pos[0]] = 0
        self.ChangePlayer()

    def ChangePlayer(self):
        #Changes players
        if self.main.crnt_player == "White":
            self.main.crnt_player = "Black"
        else:
            self.main.crnt_player = "White"
#IMAGES
class pieces:
    def __init__(self):
        self.wPawn = pg.image.load("./Chess Sprites/WPawn.png")
        self.wKing = pg.image.load("./Chess Sprites/WKing.png")
        self.wQueen = pg.image.load("./Chess Sprites/WQueen.png")
        self.wBishop = pg.image.load("./Chess Sprites/WBishop.png")
        self.wRook = pg.image.load("./Chess Sprites/WRook.png")
        self.wKnight = pg.image.load("./Chess Sprites/WHorse.png")
        self.bPawn = pg.image.load("./Chess Sprites/BPawn.png")
        self.bKing = pg.image.load("./Chess Sprites/BKing.png")
        self.bQueen = pg.image.load("./Chess Sprites/BQueen.png")
        self.bBishop = pg.image.load("./Chess Sprites/BBishop.png")
        self.bRook = pg.image.load("./Chess Sprites/BRook.png")
        self.bKnight = pg.image.load("./Chess Sprites/BHorse.png")
        self.square = pg.image.load("./Chess Sprites/squaremove.png")
        self.dict = {"wPawn":self.wPawn,"wKing":self.wKing,"wQueen":self.wQueen,"wBishop":self.wBishop,"wRook":self.wRook,"wKnight":self.wKnight,
                    "bPawn":self.bPawn,"bKing":self.bKing,"bQueen":self.bQueen,"bBishop":self.bBishop,"bRook":self.bRook,"bKnight":self.bKnight}
        self.black_pieces = ["bKing","bQueen","bBishop","bRook","bKnight","bPawn"]
        self.white_pieces = ["wKing","wQueen","wBishop","wRook","wKnight","wPawn"]

class GUI:
    def __init__(self,main):
        self.SQ_DIM = 50
        self.main = main
        self.pieces = self.main.pieces
        self.dict = self.pieces.dict
        self.board = self.main.board
        
        #COLOURS
        self.OLIVEGREEN = (85, 107, 47)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)

        #Window & Button dimensions
        self.WINDOW_WIDTH = 500
        self.WINDOW_HEIGHT = 400
        self.BUTTON_WIDTH = 100
        self.BUTTON_HEIGHT = 50

        #board colour array
        self.b = self.BLACK
        self.w = self.WHITE
        a = [self.b,self.w,self.b,self.w,self.b,self.w,self.b,self.w,]
        b = [self.w,self.b,self.w,self.b,self.w,self.b,self.w,self.b,]
        c = [self.b,self.w,self.b,self.w,self.b,self.w,self.b,self.w,]
        d = [self.w,self.b,self.w,self.b,self.w,self.b,self.w,self.b,]
        e = [self.b,self.w,self.b,self.w,self.b,self.w,self.b,self.w,]
        f = [self.w,self.b,self.w,self.b,self.w,self.b,self.w,self.b,]
        g = [self.b,self.w,self.b,self.w,self.b,self.w,self.b,self.w,]
        h = [self.w,self.b,self.w,self.b,self.w,self.b,self.w,self.b,]
        self.sq_colour =[a,b,c,d,e,f,g,h]
        
    def add_calc(self,calc):
        self.calc = self.main.calc
        
    def draw_window(self):
        self.window = pg.display.set_mode([self.WINDOW_WIDTH,self.WINDOW_HEIGHT])
        self.window.fill(self.OLIVEGREEN)
        
    def draw_button(self,text,X,Y):
        pg.font.init()
        pg.draw.rect(self.window,self.WHITE,(X,Y,self.BUTTON_WIDTH,self.BUTTON_HEIGHT),2)
        pg.draw.rect(self.window,self.BLACK,(X+2,Y+2,self.BUTTON_WIDTH-4,self.BUTTON_HEIGHT-4),0)
        self.buttonfont = pg.font.Font(None,24)
        self.label = self.buttonfont.render(text,1,self.WHITE)
        self.window.blit(self.label,(X+25,Y+10))
    
    def draw_board(self):
        X = 0
        Y = 0
        Ycounter = False
        sqcounter = False
        #Draw the board
        for i in range(0,8):
            for j in range(0,8):
                pg.draw.rect(self.window, self.sq_colour[i][j],(X,Y,self.SQ_DIM,self.SQ_DIM),0)
                if self.main.piece_at(i,j) == 0:
                    pass
                else:
                    self.window.blit(self.dict[self.main.piece_at(i,j)],(X,Y))
                
                #Change of X coord
                if X >(self.SQ_DIM*6):
                    X = 0
                    Ycounter = True
                    sqcounter = True
                else:
                    X +=(self.SQ_DIM)
                    
                #Change of Y coord
                if Ycounter == True:
                    Y +=self.SQ_DIM
                    Ycounter = False
                else:
                    pass
                
    def highlight(self,y,x):
        self.window.blit(self.pieces.square,(x*self.SQ_DIM,y*self.SQ_DIM))
        self.window.blit(self.dict[self.main.piece_at(y,x)],(x*self.SQ_DIM,y*self.SQ_DIM))

    def DisplayMoves(self):
        self.moves = self.calc.FinMoves
        for i in range(0,len(self.moves)):
            self.window.blit(self.pieces.square,(self.moves[i][1]*self.SQ_DIM,self.moves[i][0]*self.SQ_DIM))
            if self.main.piece_at(self.moves[i][0],self.moves[i][1]) != 0:
                self.window.blit(self.dict[self.main.piece_at(self.moves[i][0],self.moves[i][1])],
                                 (self.moves[i][1]*self.SQ_DIM,self.moves[i][0]*self.SQ_DIM))   
class calc:
    def __init__(self,main):
        self.main = main
        self.FinMoves = []
        self.GUI = self.main.GUI
        self.board = self.main.board
        self.pieces = self.main.pieces
        
    def calcMoves(self,y,x):
        moves = []
        self.crnt_side = self.main.crnt_side
        #Probable next moves for:
        #Knights
        if self.main.piece_at(y,x) == "wKnight" or self.main.piece_at(y,x) == "bKnight":
            moves = [[y-2,x+1],[y-2,x-1],[y-1,x-2],[y+1,x-2],
                     [y-1,x+2],[y+1,x+2],[y+2,x-1],[y+2,x+1]]
            
        #Bishops
        elif self.main.piece_at(y,x) == "wBishop" or self.main.piece_at(y,x) == "bBishop":
            self.diagonals(y,x,moves)

        #Rooks
        elif self.main.piece_at(y,x) == "wRook" or self.main.piece_at(y,x) == "bRook":
            self.straights(y,x,moves)

        #Queens
        elif self.main.piece_at(y,x) == "wQueen" or self.main.piece_at(y,x) == "bQueen":
            self.diagonals(y,x,moves)
            self.straights(y,x,moves)

        #Kings
        elif self.main.piece_at(y,x) == "wKing" or self.main.piece_at(y,x) == "bKing":
            moves = [[y-1,x],[y+1,x],[y,x+1],[y,x-1],
                     [y+1,x+1],[y+1,x-1],[y-1,x-1],[y-1,x+1]]

        #wPawns
        elif self.main.piece_at(y,x) == "wPawn":
            if self.main.piece_at(y-1,x) == 0:
                moves.append([y-1,x])
                if [y,x] in self.board.wPawn_orig_pos:
                    if self.main.piece_at(y-2,x) == 0:
                        moves.append([y-2,x])
            if x+1 < 8:
                if self.main.piece_at(y-1,x+1) in self.pieces.black_pieces:
                    moves.append([y-1,x+1])
            if x-1 > -1:
                if self.main.piece_at(y-1,x-1) in self.pieces.black_pieces:
                    moves.append([y-1,x-1])
                

        #bPawns
        elif self.main.piece_at(y,x) == "bPawn":
            if self.main.piece_at(y+1,x) == 0:
                moves.append([y+1,x])
                if [y,x] in self.board.bPawn_orig_pos:
                    if self.main.piece_at(y+2,x) == 0:
                        moves.append([y+2,x])
            if x+1 < 8:
                if self.main.piece_at(y+1,x+1) in self.pieces.white_pieces:
                    moves.append([y+1,x+1])
            if x-1 >-1:
                if self.main.piece_at(y+1,x-1) in self.pieces.white_pieces:
                    moves.append([y+1,x-1])
        self.ValidateMoves(moves,y,x)

    def straights(self,y,x,moves):
        for i in range(1,9):
            if y-i>-1:
                if self.main.piece_at(y-i,x) in self.crnt_side:
                    break
                elif self.main.piece_at(y-i,x) == 0:
                    moves.append([y-i,x])
                else:
                    moves.append([y-i,x])
                    break
        for i in range(1,9):
            if y+i<8:
                if self.main.piece_at(y+i,x) in self.crnt_side:
                    break
                elif self.main.piece_at(y+i,x) == 0:
                    moves.append([y+i,x])
                else:
                    moves.append([y+i,x])
                    break
        for i in range(1,9):
            if x+i<8:
                if self.main.piece_at(y,x+i) in self.crnt_side:
                    break
                elif self.main.piece_at(y,x+i) == 0:
                    moves.append([y,x+i])
                else:
                    moves.append([y,x+i])
                    break
        for i in range(1,9):
            if x-i>-1:
                if self.main.piece_at(y,x-i) in self.crnt_side:
                    break
                elif self.main.piece_at(y,x-i) == 0:
                    moves.append([y,x-i])
                else:
                    moves.append([y,x-i])
                    break

    def diagonals(self,y,x,moves):
        for i in range(1,9):
            if y-i>-1 and x-i >-1:
                if self.main.piece_at(y-i,x-i) in self.crnt_side:
                    break
                elif self.main.piece_at(y-i,x-i) == 0:
                    moves.append([y-i,x-i])
                else:
                    moves.append([y-i,x-i])
                    break    
        for i in range(1,9):
            if y-i>-1 and x+i < 8:
                if self.main.piece_at(y-i,x+i) in self.crnt_side:
                    break
                elif self.main.piece_at(y-i,x+i) == 0:
                    moves.append([y-i,x+i])
                else:
                    moves.append([y-i,x+i])
                    break
        for i in range(1,9):
            if y+i <8 and x-i >-1:
                if self.main.piece_at(y+i,x-i) in self.crnt_side:
                    break
                elif self.main.piece_at(y+i,x-i) == 0:
                    moves.append([y+i,x-i])
                else:
                    moves.append([y+i,x-i])
                    break
        for i in range(1,9):
            if y+i <8 and x+i <8:
                if self.main.piece_at(y+i,x+i) in self.crnt_side:
                    break
                elif self.main.piece_at(y+i,x+i) == 0:
                    moves.append([y+i,x+i])
                else:
                    moves.append([y+i,x+i])
                    break
                
    def ValidateMoves(self,moves,y,x):
        self.FinMoves = []
        MidMoves = []
        for i in range(0,len(moves)):
            if moves[i][0] > 7 or moves[i][0] < 0 or moves[i][1] <0 or moves[i][1] > 7:
                pass
            else:
                MidMoves.append(moves[i])
        #code for filtering out valid moves that is over a piece of the same color
        for i in range(0,len(MidMoves)):
            if self.main.piece_at(MidMoves[i][0],MidMoves[i][1]) not in self.crnt_side or  self.main.piece_at(MidMoves[i][0],MidMoves[i][1]) == 0:
                self.FinMoves.append(MidMoves[i])
        print(self.FinMoves)
        print(len(self.FinMoves))
        self.GUI.DisplayMoves()

        
#Initialising objects
main = main()
pieces = pieces()
main.add_pieces(pieces)
board = board(main)
main.add_board(board)
GUI = GUI(main)
main.add_GUI(GUI)
calc = calc(main)
main.add_calc(calc)
GUI.add_calc(calc)
GUI.draw_window()
navigation = navigation(GUI)
main.add_navigation(navigation)
GUI.draw_board()
main.main_loop()
