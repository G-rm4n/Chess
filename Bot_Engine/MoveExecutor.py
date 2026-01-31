from Bot_Engine.constants import IDX_BLACK_BITBOARD,IDX_WHITE_BITBOARD

class MoveExecutor:

    def make_move(Bitboards,movement,color):

        undo_info=None

        startallie=7 if color=="B" else 0
        startenemie=0 if color=="B" else 7
        globalBitboardallie=IDX_WHITE_BITBOARD if color=="W" else IDX_BLACK_BITBOARD
        globalBitboardenemie=IDX_BLACK_BITBOARD if color=="W" else IDX_WHITE_BITBOARD

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        for i in range(startenemie,startenemie+6):

            if Bitboards[i] & movement[1]:

                undo_info=(movement[1],i)
                Bitboards[i] &= ~(movement[1])
                Bitboards[globalBitboardenemie] &= ~(movement[1])
                break

        Bitboards[PieceDictionary[movement[2]]+startallie] &= ~(movement[0])
        Bitboards[PieceDictionary[movement[2]]+startallie] |=  (movement[1])

        Bitboards[globalBitboardallie] &= ~(movement[0])
        Bitboards[globalBitboardallie] |= (movement[1])

        
        
        return undo_info
    
    def unMake_Move(move,Bitboards,undo_info,color):

        origin,destiny,pieceType=move[0],move[1],move[2]

        startallie=7 if color=="B" else 0

        globalBitboardallie=IDX_WHITE_BITBOARD if color=="W" else IDX_BLACK_BITBOARD
        globalBitboardenemie=IDX_BLACK_BITBOARD if color=="W" else IDX_WHITE_BITBOARD

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        if undo_info is not None:

            pieceCapturedIndex=undo_info[1]
            piecePosition=undo_info[0]

            Bitboards[pieceCapturedIndex] |= piecePosition
            Bitboards[globalBitboardenemie] |= piecePosition
        
        Bitboards[PieceDictionary[pieceType]+startallie] &= ~destiny
        Bitboards[PieceDictionary[pieceType]+startallie] |=  origin

        Bitboards[globalBitboardallie] &= ~destiny
        Bitboards[globalBitboardallie] |= origin