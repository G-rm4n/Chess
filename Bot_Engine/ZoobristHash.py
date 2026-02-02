import random
from Bot_Engine.constants import IDX_BLACK_BITBOARD,IDX_WHITE_BITBOARD,IDX_OCCUPIED
from Utils.GenerateIndividualBitboard import generateIndividualBitboard

class ZoobristHash:

    def __init__(self,seed=None):
        if seed:
            random.seed(seed)

        self.zoobristNumbers=[random.getrandbits(64) for _ in range(768)]
        self.sideToMove=random.getrandbits(64)

    def compute_zoobristHash(self,State,flagColor):

        zoobristHash=0

        for idx,bb in enumerate(State):

            if idx in (IDX_OCCUPIED,IDX_BLACK_BITBOARD,IDX_WHITE_BITBOARD):
                continue

            idvBBs=generateIndividualBitboard(bb)

            for idvBB in idvBBs:

                pieceSquare=idvBB.bit_length() - 1
                zoobristHash ^= self.zoobristNumbers[pieceSquare+idx]
        
        if flagColor:
            zoobristHash ^= self.sideToMove

        return zoobristHash
    

    
