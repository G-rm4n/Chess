from Bot_Engine.constants import IDX_BLACK_BITBOARD,IDX_OCCUPIED,IDX_WHITE_BITBOARD,COLORDICTIONARY,PIECETYPEDICTIONARY

class Bitboard:

    def generateBitboards(Board:list):

        BitBoards=[0 for i in range (15)]


        for i in range(8):
            for j in range(8):

                piece=Board[i][j]

                if piece is None:
                    continue

                mask=1<<(i*8)+j

                BitBoards[COLORDICTIONARY[piece.get_color()]+PIECETYPEDICTIONARY[piece.getType()]]= BitBoards[COLORDICTIONARY[piece.get_color()]+PIECETYPEDICTIONARY[piece.getType()]] | mask
                BitBoards[IDX_WHITE_BITBOARD if piece.get_color()=="W" else IDX_BLACK_BITBOARD]=BitBoards[IDX_WHITE_BITBOARD if piece.get_color()=="W" else IDX_BLACK_BITBOARD] | mask
            
        BitBoards[IDX_OCCUPIED]=BitBoards[IDX_WHITE_BITBOARD]|BitBoards[IDX_BLACK_BITBOARD]

        return BitBoards