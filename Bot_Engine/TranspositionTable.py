import random
from Utils.GenerateIndividualBitboard import generateIndividualBitboard
from Bot_Engine.constants import IDX_BLACK_BITBOARD,IDX_WHITE_BITBOARD,IDX_OCCUPIED
from Bot_Engine.ZoobristHash import ZoobristHash

class TranspositionTable:

    def __init__(self,seed=53808):
        self.zoobrist=ZoobristHash(seed)
        self.table={}

    def isStateInTable(self,State,colorFlag):
        zooHash=self.zoobrist.compute_zoobristHash(State,colorFlag)

        return (zooHash in self.table)
    

    #type=T -> Terminal (checkMate,Draw)
    #type=E -> MaxHeight Reached
    #type=L -> Lowerbound
    #typer=U -> UpperBound
    def storeState(self,State,score,deep,type,colorTurn,flagColor,move=None):
        
        zooHash=self.zoobrist.compute_zoobristHash(State,flagColor)

        

        self.table[zooHash]={
            "score":score,
            "deep":deep,
            "Type":type,
            "turn":colorTurn,
            "move":move

        }

        

    def getNodeValues(self,State,colorFlag):

        zooHash=self.zoobrist.compute_zoobristHash(State,colorFlag)

        return self.table[zooHash]
