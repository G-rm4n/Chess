from Core.Board import Board
from Adapters.Bitboard import Bitboard

bd=Board()
bd.prepareBoard()
Bitboards=Bitboard.generateBitboards(bd.getPositions())

for idx,bb in enumerate(Bitboards):
    print(f"idx:{idx} bb:{bin(bb)}")