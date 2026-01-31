import os
from States import GameStates

class Display:

    def DisplayBoard(self,BoardPositions):
        raise NotImplementedError
    
    def DisplayTurn(self,GameState):
        raise NotADirectoryError

class ConsoleDisplay(Display):
    @staticmethod
    def DisplayBoard(Board):

        symbolDictionary={
            "W":{
                "KING":"♔",
                "QUEEN":"♕",
                "TOWER":"♖",
                "BISHOP":"♗",
                "HORSE":"♘",
                "PAWN":"♙"
            },
            "B":{
                "KING":"♚",
                "QUEEN":"♛",
                "TOWER":"♜",
                "BISHOP":"♝",
                "HORSE":"♞",
                "PAWN":"♟"
            },
        }


        os.system("cls")

        for i in range(8):
            for j in range(8):
                squareContent=Board.getPiece((i,j))
                if(squareContent!=None):
                    print(symbolDictionary[squareContent.get_color()][squareContent.getType()],sep=None,end="\t")
                else:
                    print("□",sep=None,end="\t") if (i%2!=0 and j%2==0) or (i%2==0 and j%2!=0) else print("■",sep=None,end="\t")
                
            print("\n")

    @staticmethod
    def DisplayTurn(GameState):

        if GameState == GameStates.PLAYER_TURN:
            print("Player's turn")
        else:
            print("the bot is thinking...")

    @staticmethod
    def displayCoordError():

        print("invalid Coords.")

    @staticmethod
    def displayMovementError():

        print("Ilegal Movement")
