from AI_Engine.MoveExecutor import MoveExecutor
from AI_Engine.constants import COL_8, COL_1, ROW_1,ROW_2,ROW_7,ROW_8,COL_1_2,COL_8_7,ROW_1_2,ROW_8_7,PIECETYPEDICTIONARY,IDX_BLACK_BITBOARD,IDX_WHITE_BITBOARD,COLORDICTIONARY
from Utils.GenerateIndividualBitboard import generateIndividualBitboard


class MoveGenerator:
    @staticmethod
    def generatePseudoLegalMovments(Bitboards,Color):
        
        MovementsPawn=MoveGenerator.GeneratePseudoLegalMovementsPawn(Bitboards[PIECETYPEDICTIONARY["PAWN"]+COLORDICTIONARY[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsQueen=MoveGenerator.GeneratePseudoLegalMovementsQueen(Bitboards[PIECETYPEDICTIONARY["QUEEN"]+COLORDICTIONARY[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsKing=MoveGenerator.generatePseudoLegalMovementsKing(Bitboards[PIECETYPEDICTIONARY["KING"]+COLORDICTIONARY[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsTower=MoveGenerator.GeneratePseudoLegalMovementsTower(Bitboards[PIECETYPEDICTIONARY["TOWER"]+COLORDICTIONARY[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsHorse=MoveGenerator.GeneratePseudoLegalMovementsHorse(Bitboards[PIECETYPEDICTIONARY["HORSE"]+COLORDICTIONARY[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsBishop=MoveGenerator.GeneratePseudoLegalMovementsBishop(Bitboards[PIECETYPEDICTIONARY["BISHOP"]+COLORDICTIONARY[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)

        return MovementsQueen + MovementsTower + MovementsHorse + MovementsBishop + MovementsPawn + MovementsKing
    
    @staticmethod
    def GeneratePseudoLegalMovementsPawn(BitBoard,BitBoardOccupied_White,BitBoardOcuppied_Black,color):

        LegalMovements=[]

        

        if color=="W":

            Movement1=((BitBoard&(~ROW_8))<<8) & (~(BitBoardOccupied_White | BitBoardOcuppied_Black))
            Movement2=((BitBoard&ROW_2&(~ROW_8_7))<<16) & (~(BitBoardOccupied_White | BitBoardOcuppied_Black))
            Movement2=(Movement2 & (Movement1<<8))
            attack1=((BitBoard&(~ROW_8)&(~COL_8))<<9)&BitBoardOcuppied_Black
            attack2=((BitBoard&(~COL_1)&(~ROW_8))<<7)&BitBoardOcuppied_Black

            allDestinies= Movement1 | Movement2 | attack1 | attack2

            while allDestinies:

                to_pos= allDestinies & -allDestinies
                allDestinies &= (allDestinies-1)


                from_pos_mov1=to_pos>>8
                from_pos_mov2=to_pos>>16
                from_pos_at1=to_pos>>9
                from_pos_at2=to_pos>>7

                if (to_pos & Movement1) and (from_pos_mov1 & BitBoard):
                    LegalMovements.append((from_pos_mov1,to_pos,"P"))

                if (to_pos & Movement2) and (from_pos_mov2 & BitBoard):
                    LegalMovements.append((from_pos_mov2,to_pos,"P"))

                if (to_pos & attack1) and (from_pos_at1 &BitBoard):
                    LegalMovements.append((from_pos_at1,to_pos,"P"))
                
                if (to_pos & attack2) and (from_pos_at2 &BitBoard):
                    LegalMovements.append((from_pos_at2,to_pos,"P"))
        
            return LegalMovements


        else:
            Movement1=((BitBoard&(~(ROW_1)))>>8) & (~(BitBoardOccupied_White | BitBoardOcuppied_Black))
            Movement2=((BitBoard&ROW_7&(~ROW_1_2))>>16) & (~(BitBoardOccupied_White | BitBoardOcuppied_Black))
            Movement2=(Movement2 & (Movement1>>8))
            attack1=((BitBoard&(~COL_1)&(~ROW_1))>>9)&BitBoardOccupied_White
            attack2=((BitBoard&(~COL_8))&(~(ROW_1))>>7)&BitBoardOccupied_White

            allDestinies= Movement1 | Movement2 | attack1 | attack2

            

            while allDestinies:
                
                to_pos=allDestinies & -allDestinies
                allDestinies &=(allDestinies-1)

            
                from_pos_mov1=to_pos<<8
                from_pos_mov2=to_pos<<16
                from_pos_at1=to_pos<<9
                from_pos_at2=to_pos<<7

                if (to_pos & Movement1) and (from_pos_mov1 & BitBoard):
                    LegalMovements.append((from_pos_mov1,to_pos,"P"))

                if (to_pos & Movement2) and (from_pos_mov2 & BitBoard):
                    LegalMovements.append((from_pos_mov2,to_pos,"P"))

                if (to_pos & attack1) and (from_pos_at1 &BitBoard):
                    LegalMovements.append((from_pos_at1,to_pos,"P"))
                
                if (to_pos & attack2) and (from_pos_at2 &BitBoard):
                    LegalMovements.append((from_pos_at2,to_pos,"P"))

            return LegalMovements
    
    def GeneratePseudoLegalMovementsTower(TowerBitboard:int,BitboardOccupied_White,BitboardOccupied_Black,color):
        PseudoLegalMovements=[]

        towers=generateIndividualBitboard(TowerBitboard)

        for tower in towers:
            

            verticalMovements=0b0
            horizontalMovements=0b0

            auxBitboard=tower
            while True:
                

                auxBitboard=(auxBitboard & (~(ROW_8)))<<8

                

                if auxBitboard == 0:
                    break

                colition_Allies=auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies=auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break
                
                verticalMovements=verticalMovements | auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=tower
            while True:

                auxBitboard=(auxBitboard & (~(ROW_1)))>>8

                if auxBitboard == 0:
                    break

                colition_Allies=auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies=auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                verticalMovements= verticalMovements | auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=tower
            while True:

                auxBitboard=(auxBitboard & (~(COL_8)))<<1

                if auxBitboard== 0:
                    break

                colition_Allies=auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies=auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                horizontalMovements= horizontalMovements | auxBitboard

                if colition_Enemies:
                    break

            auxBitboard=tower
            while True:
                
                auxBitboard=(auxBitboard & (~(COL_1)))>>1

                if auxBitboard == 0:
                    break

                colition_Allies=auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies=auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                horizontalMovements= horizontalMovements | auxBitboard

                if colition_Enemies:
                    break

            PosibleMovements= horizontalMovements | verticalMovements

            while PosibleMovements:

                to_pos= PosibleMovements & -PosibleMovements
                PosibleMovements &= (PosibleMovements-1)
                
                PseudoLegalMovements.append((tower,to_pos,"T"))
        
        return PseudoLegalMovements
    

    def GeneratePseudoLegalMovementsBishop(BishopBitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):
        PseudoLegalMovements=[]

        Bishops=generateIndividualBitboard(BishopBitboard)

        for bishop in Bishops:

            Diag1=0b0
            Diag2=0b0

            auxBitboard=bishop
            while True:
                
                
                auxBitboard = (auxBitboard & (~(COL_8)) & (~(ROW_8)))<<9 

                if auxBitboard == 0:
                    break

                colition_Allies= auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies= auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                Diag1 |= auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=bishop
            while True:
                

                auxBitboard = (auxBitboard & (~(COL_1)) & (~(ROW_1)))>>9 

                if auxBitboard == 0:
                    break

                colition_Allies= auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies= auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break
                
                Diag1 |= auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=bishop
            while True:
                

                auxBitboard = (auxBitboard & (~(COL_1)) & (~(ROW_8)))<<7

                

                if auxBitboard == 0:
                    break
            
                colition_Allies= auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies= auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                Diag2 |= auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=bishop
            while True:

                

                auxBitboard = (auxBitboard & (~(COL_8)) & (~(ROW_1)))>>7

                

                if auxBitboard == 0:
                    break

                colition_Allies= auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies= auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                Diag2 |= auxBitboard

                if colition_Enemies:
                    break
            
            PosibleMovements= Diag1 | Diag2
            
            while PosibleMovements:

                to_pos=PosibleMovements & (-PosibleMovements)
                PosibleMovements &= (PosibleMovements - 1)

                PseudoLegalMovements.append((bishop,to_pos,"B"))
        
        return PseudoLegalMovements
    

    def GeneratePseudoLegalMovementsHorse(HorseBitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):
        PseudoLegalMovements=[]

        Horses=generateIndividualBitboard(HorseBitboard)
        
        for horse in Horses:

            Movement1=((horse & (~(COL_8)) & (~(ROW_8_7)))<<17) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement2=((horse & (~(COL_1)) & (~(ROW_8_7)))<<15) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement3=((horse & (~(COL_1)) & (~(ROW_1_2)))>>17) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement4=((horse & (~(COL_8)) & (~(ROW_1_2)))>>15) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement5=((horse & (~(COL_8_7)) & (~(ROW_8)))<<10) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White)) 
            Movement6=((horse & (~(COL_1_2)) & (~(ROW_8)))<<6)  & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement7=((horse & (~(COL_1_2)) & (~(ROW_1)))>>10) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement8=((horse & (~(COL_8_7)) & (~(ROW_1)))>>6)  & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            
            allMovements= Movement1 | Movement2 | Movement3 | Movement4 | Movement5 | Movement6 | Movement7 | Movement8

            while allMovements:
                    
                to_pos= allMovements & -allMovements
                allMovements &= (allMovements - 1)
                PseudoLegalMovements.append((horse,to_pos,"H"))

                
            
        return PseudoLegalMovements
    
    def GeneratePseudoLegalMovementsQueen(QueenBitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black:int,color):

        PseudoLegalMovements=[]

        BishopMovements=MoveGenerator.GeneratePseudoLegalMovementsBishop(QueenBitboard,BitboardOccupied_White,BitboardOccupied_Black,color)
        TowerMovements=MoveGenerator.GeneratePseudoLegalMovementsTower(QueenBitboard,BitboardOccupied_White,BitboardOccupied_Black,color)

        PseudoLegalMovements=BishopMovements + TowerMovements

        for idx,mov in enumerate(PseudoLegalMovements):
            PseudoLegalMovements[idx]=(mov[0],mov[1],"Q")

        return PseudoLegalMovements
    
    def generatePseudoLegalMovementsKing(KingBitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black:int,color):

        PseudoLegalMovements=[]

        Movement1=((KingBitboard & (~(ROW_8)))<<8) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement2=((KingBitboard & (~(ROW_1)))>>8) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement3=((KingBitboard & (~(COL_8)))<<1) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement4=((KingBitboard & (~(COL_1)))>>1) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement5=((KingBitboard & (~(ROW_8)) & (~(COL_8)))<<9) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement6=((KingBitboard & (~(ROW_8)) & (~(COL_1)))<<7) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement7=((KingBitboard & (~(ROW_1)) & (~(COL_1)))>>9) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement8=((KingBitboard & (~(ROW_1)) & (~(COL_8)))>>7) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))

        allMovements= Movement1 | Movement2 | Movement3 | Movement4 | Movement5 | Movement6 | Movement7 | Movement8

        while allMovements:

            to_pos=allMovements & -allMovements
            allMovements &= (allMovements-1)

            PseudoLegalMovements.append((KingBitboard,to_pos,"K"))

        return PseudoLegalMovements
