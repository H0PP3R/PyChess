#sound
import pygame as pg,sys
from pygame.locals import *
from pygame import mixer
import os
import sys
import time

class main:
    def __init__(self):
        self.board = None
        self.GUI = None
        self.selectedB4 = False
        self.check = False
        self.checkmate = False
        self.color = ""
        self.crnt_player = "White"
        self.crnt_side = []
        self.running = True
        self.winner = False

    def main_loop(self):
        self.sound.play_sound("start")
        while self.running:
            if self.winner == False:
                self.ev = pg.event.get()
                for event in self.ev:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.pos = pg.mouse.get_pos()
                        self.onclick()
            else:
                self.GUI.draw_EndScreen(self.calc.winner)
                time.sleep(3)
                self.sound.play_sound("checkmate")
                self.running = False
            pg.display.flip()
        if self.running == False:
            pg.display.quit()
                
    def onclick(self):
        #Convert the coordinates suitable for 2d array
        x = (self.pos[0]//self.GUI.SQ_DIM)
        y = (self.pos[1]//self.GUI.SQ_DIM)
        print(y,x)
        #changes of player
        if self.crnt_player == "White":
            self.crnt_side = self.pieces.white_pieces
        else:
            self.crnt_side = self.pieces.black_pieces
        #navigation
        if x>=8:
            if y == 1:
                print("saving...")
                self.sound.play_sound("click")
                self.navigation.game_save()
            elif y == 3:
                print("loading...")
                self.sound.play_sound("click")
                self.navigation.game_load()
            elif y == 5:
                print("exiting...")
                self.sound.play_sound("click")
                self.navigation.game_exit()
                
        if self.selectedB4 == False:
            self.calc.checkKing()
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
                self.sound.play_sound("move")
                #Update current king's danger situation
                self.calc.checkKing()
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

    def add_sound(self,sound):
        self.sound = sound

    def UpdateMain(self,new_board):
        self.board.piece_pos = new_board
        
    def piece_at(self,y,x):
        return self.board.piece_pos[y][x]

    def prv_pos_at(self,item):
        return self.board.prv_pos[item]

    def colour_at(self,x,y):
        return self.GUI.window.get_at(((x*self.GUI.SQ_DIM)+2, (y*self.GUI.SQ_DIM)+2))
        
    def Update_board(self,y,x):
        self.board.UpdatePos(y,x)

    def UpdatePlayer(self,new_player):
        self.crnt_player = new_player

    def UpdateMoves(self,moves):
        self.moves = moves

    def UpdateWinner(self):
        self.winner = True
        
class navigation:
    def __init__(self,GUI):
        self.GUI = GUI
        self.main = self.GUI.main
        self.GUI.draw_StatusBar("")
        self.GUI.draw_button("save",self.GUI.SQ_DIM*8,self.GUI.SQ_DIM)
        self.GUI.draw_button("load",self.GUI.SQ_DIM*8,self.GUI.SQ_DIM*3)
        self.GUI.draw_button("exit",self.GUI.SQ_DIM*8,self.GUI.SQ_DIM*5)

    def Update_StatusBar(self,text):
        self.GUI.draw_StatusBar(text)

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


class sound:
    def __init__(self):
        mixer.init()
        self.Drop = pg.mixer.Sound("./Sounds/ChessDrop.wav")
        self.Move = pg.mixer.Sound("./Sounds/ChessMove.wav")
        self.Win = pg.mixer.Sound("./Sounds/YEAH.wav")
        self.Click = pg.mixer.Sound("./Sounds/Click.wav")
        self.Splat = pg.mixer.Sound("./Sounds/Splat2.wav")
        

    def play_sound(self,sound):
        if sound == "start":
            crnt_sound = self.Drop
        elif sound == "move":
            crnt_sound = self.Move
        elif sound == "checkmate":
            crnt_sound = self.Win
        elif sound == "click":
            crnt_sound = self.Click
        elif sound == "death":
            crnt_sound = self.Splat
        crnt_sound.play()

class GUI:
    def __init__(self,main):
        pg.font.init()
        self.buttonfont = pg.font.Font(None,24)
        self.SQ_DIM = 50
        self.main = main
        self.pieces = self.main.pieces
        self.dict = self.pieces.dict
        self.board = self.main.board
        self.party = pg.image.load("./Chess Sprites/celebrate_party.jpg")
        self.blood_splatter= pg.image.load("./Chess Sprites/Blood.png")
        
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
        self.sq_colour = self.WHITE

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

    def draw_StatusBar(self,text):
        pg.draw.rect(self.window,self.RED,(self.SQ_DIM*8,0,self.BUTTON_WIDTH,self.BUTTON_HEIGHT),0)
        self.label = self.buttonfont.render(text,1,self.WHITE)
        self.window.blit(self.label,(self.SQ_DIM*8+20,10))
                         
    def draw_button(self,text,X,Y):
        pg.draw.rect(self.window,self.WHITE,(X,Y,self.BUTTON_WIDTH,self.BUTTON_HEIGHT),2)
        pg.draw.rect(self.window,self.BLACK,(X+2,Y+2,self.BUTTON_WIDTH-4,self.BUTTON_HEIGHT-4),0)
        self.label = self.buttonfont.render(text,1,self.WHITE)
        self.window.blit(self.label,(X+25,Y+10))
    
    def draw_board(self):
        X = 0
        Y = 0
        Ycounter = False
        sqcounter = False
        #Draw the board
        print("GUI update")
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
        self.moves = self.calc.moves
        for i in range(0,len(self.moves)):
            self.window.blit(self.pieces.square,(self.moves[i][1]*self.SQ_DIM,self.moves[i][0]*self.SQ_DIM))
            if self.main.piece_at(self.moves[i][0],self.moves[i][1]) != 0:
                self.window.blit(self.dict[self.main.piece_at(self.moves[i][0],self.moves[i][1])],
                                 (self.moves[i][1]*self.SQ_DIM,self.moves[i][0]*self.SQ_DIM))

    def draw_EndScreen(self,winner):
        self.window.fill(self.WHITE)
        self.label = self.buttonfont.render(winner,1,self.BLACK)
        self.window.blit(self.label,(0,0))
        self.window.blit(self.party,(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2))
        pg.display.flip()

    def Death_Animation(self,y,x):
        self.window.blit(self.blood_splatter,(x*self.SQ_DIM,y*self.SQ_DIM))
        pg.display.flip()
        self.main.sound.play_sound("death")
        time.sleep(1)
        
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
        #Play deathsounds
        if self.piece_pos[y][x] != 0:
            self.main.GUI.Death_Animation(y,x)
        self.piece_pos[y][x] = self.piece_pos[self.prv_pos[1]][self.prv_pos[0]]
        self.piece_pos[self.prv_pos[1]][self.prv_pos[0]] = 0
        #Check if the player has won
        self.main.calc.win(y,x)
        self.ChangePlayer()

    def ChangePlayer(self):
        #Changes players
        if self.main.crnt_player == "White":
            self.main.crnt_player = "Black"
        else:
            self.main.crnt_player = "White"
    
class calc:
    def __init__(self,main):
        self.main = main
        self.GUI = self.main.GUI
        self.board = self.main.board
        self.pieces = self.main.pieces
        self.moves = []
        self.checking = False
        self.King = False
        self.KingPos = []
        self.OppKingPos = []
        self.crnt_king = False
        self.crnt_InCheck = False
        self.OppMoves = []
        self.KingPosMoves = []
       
    def calcMoves(self,y,x):
        self.moves = []
        KingTemp = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
        KnightTemp = [[2,1],[2,-1],[1,2],[-1,2],[-2,1],[-2,-1],[-1,-2],[1,-2]]
        #Probable next moves for:
        #Knights
        if self.main.piece_at(y,x) == "wKnight" or self.main.piece_at(y,x) == "bKnight":
            self._discrt(y,x,KnightTemp)
            
        #Bishops
        elif self.main.piece_at(y,x) == "wBishop" or self.main.piece_at(y,x) == "bBishop":
            self._diagonals(y,x)

        #Rooks
        elif self.main.piece_at(y,x) == "wRook" or self.main.piece_at(y,x) == "bRook":
            self._straights(y,x)

        #Queens
        elif self.main.piece_at(y,x) == "wQueen" or self.main.piece_at(y,x) == "bQueen":
            self._diagonals(y,x)
            self._straights(y,x)

        #Kings
        elif self.main.piece_at(y,x) == "wKing" or self.main.piece_at(y,x) == "bKing":
            self._discrt(y,x,KingTemp)

        elif self.main.piece_at(y,x) == "wPawn" or self.main.piece_at(y,x) == "bPawn":
            self.Pawn_Moves(y,x)

        #Final operation different depending on whether system is checking    
        if self.checking == False:
            self.GUI.DisplayMoves()
        elif self.checking == True:
            self.crnt_InCheck = False
            if self.KingPos in self.moves:
                print("King in Check")
                self.crnt_InCheck = True

    def Pawn_Moves(self,y,x):
        if self.main.piece_at(y,x) =="wPawn":
            Pawn_orig_pos = self.board.wPawn_orig_pos
            v = -1
        else:
            Pawn_orig_pos = self.board.bPawn_orig_pos
            v = 1
    
        if self.main.piece_at(y+v,x) == 0:
            self.moves.append([y+v,x])
            if [y,x] in Pawn_orig_pos:
                if self.main.piece_at(y+(2*v),x) == 0:
                    self.moves.append([y+(2*v),x])
        for i in range(0,2):
            h = 1
            if i == 1:
                h = -1
            if x+h < 8 and x+h >-1:
                if self.main.piece_at(y+v,x+h) not in self.crnt_side and self.main.piece_at(y+v,x+h) != 0:
                    self.moves.append([y+v,x+h])

    def _cont(self,y,x,v,h):
        hrange = int(3.5*(1+h)-(h*x))
        vrange = int(3.5*(1+v)-(v*y))
        if h == 0:
            rnge = vrange
        elif v == 0:
            rnge = hrange
        else:#neither 0 - diagonal
            rnge = min(hrange,vrange)
        #'float' object is not callable
        for i in range(1,rnge+1):
            if self.main.piece_at(y+i*v,x+i*h) in self.crnt_side:
                break
            elif self.main.piece_at(y+i*v,x+i*h) == 0:
                self.moves.append([y+i*v,x+i*h])
            else:#reached an opposing piece
                self.moves.append([y+i*v,x+i*h])
                break

    def _discrt(self,y,x,template):
        for move in template:
            if y+move[0] <8 and y+move[0] >-1 and x+move[1] <8 and x+move[1] > -1:
                if self.main.piece_at(y+move[0],x+move[1]) in self.crnt_side:
                    pass
                elif self.main.piece_at(y+move[0],x+move[1]) == 0:
                    self.moves.append([y+move[0],x+move[1]])
                else:
                    self.moves.append([y+move[0],x+move[1]])
                
    def _straights(self,y,x):
       self._cont(y,x,1,0)
       self._cont(y,x,-1,0)
       self._cont(y,x,0,1)
       self._cont(y,x,0,-1)

    def _diagonals(self,y,x):
        self._cont(y,x,1,1)
        self._cont(y,x,-1,1)
        self._cont(y,x,1,-1)
        self._cont(y,x,-1,-1)

    def checkKing(self):
        self.crnt_InCheck = False
        self.InCheck = False
        self.crnt_side = self.main.crnt_side
        #Sides change when checking where the opposite side will go
        if self.crnt_side == self.pieces.white_pieces:
            self.opp_side = self.pieces.black_pieces
        else:
            self.opp_side = self.pieces.white_pieces
            
        #Find where the king is
        for i in range(0,8):
            for j in range(0,8):
                if self.main.piece_at(i,j) == self.crnt_side[0]:
                    self.KingPos = [i,j]
                elif self.main.piece_at(i,j) == self.opp_side[0]:
                    self.OppKingPos = [i,j]
        self.checking = True

        for i in range(0,8):
            for j in range(0,8):
                if self.main.piece_at(i,j) in self.opp_side:
                    self.crnt_piece_pos = [i,j]
                    self.crnt_side = self.opp_side
                    self.calcMoves(i,j)
                    if self.crnt_InCheck == True:
                        self.InCheck = True
        self.checking = False
        self.crnt_side = self.main.crnt_side
        
        if self.InCheck == True:
            self.main.navigation.Update_StatusBar("CHECK!")
        else:
            self.main.navigation.Update_StatusBar("")

    def win(self,y,x):
        if [y,x] == self.OppKingPos:
            print("GAME OVER")
            self.winner = (self.main.crnt_player+" wins") 
            print(self.winner)
            self.main.UpdateWinner()
#Initialising objects
main = main()
pieces = pieces()
sound = sound()
main.add_pieces(pieces)
main.add_sound(sound)
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
