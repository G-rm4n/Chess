from Bot_Engine.constants import ROW_1,ROW_2,ROW_7,ROW_8,COL_1_2,ROW_1_2,ROW_8_7,COL_8_7,COL_8,COL_1
from Bot_Engine.MoveGenerator.rayGenerator import RayGenerator
from Bot_Engine.MoveExecutor import MoveExecutor

class legalChecker:
    @staticmethod

    def filtherMovements(Movements,Bitboards,color):
            LegalMovements=[]

            for Move in Movements:

                undo_info=MoveExecutor.make_move(Bitboards,Move,color)


                if legalChecker.isKingSafe(Bitboards,color):
                    LegalMovements.append(Move)
                
                MoveExecutor.unMake_Move(Move,Bitboards,undo_info,color)
            
            return LegalMovements
    
    @staticmethod
    def isKingSafe(Bitboards,color):

        
        kingBitboard=Bitboards[0 if color=="W" else 7]
        enemyHorses=Bitboards[11 if color=="W" else 4]
        enemyPawns=Bitboards[8 if color=="W" else 1]
        enemyTowers=Bitboards[9 if color=="W" else 2]
        enemyQueen=Bitboards[12 if color=="W" else 5]
        enemyBishops=Bitboards[10 if color=="W" else 3]
        enemyKing=Bitboards[7 if color=="W" else 0]


        PossibleHorses=((((kingBitboard & (~(COL_8)) & (~(ROW_8_7)))<<17)) |
                         ((kingBitboard & (~(COL_1)) & (~(ROW_8_7)))<<15) | 
                         ((kingBitboard & (~(COL_1)) & (~(ROW_1_2)))>>17) | 
                         ((kingBitboard & (~(COL_8)) & (~(ROW_1_2)))>>15) | 
                         ((kingBitboard & (~(COL_8_7)) & (~(ROW_8)))<<10) | 
                         ((kingBitboard & (~(COL_1_2)) & (~(ROW_8)))<<6)  | 
                         ((kingBitboard & (~(COL_1_2)) & (~(ROW_1)))>>10) | 
                         ((kingBitboard & (~(COL_8_7)) & (~(ROW_1)))>>6))
        
        if PossibleHorses & enemyHorses:
            return False
        
        Vray1=RayGenerator.GenerateVerticalRay(Bitboards,kingBitboard,dy=1)
        Vray2=RayGenerator.GenerateVerticalRay(Bitboards,kingBitboard,dy=(-1))
        
        if (Vray1 | Vray2) & (enemyQueen | enemyTowers | enemyKing):
            return False
        
        Hray1=RayGenerator.GenerateHorizontalRay(Bitboards,kingBitboard,dx=1)
        Hray2=RayGenerator.GenerateHorizontalRay(Bitboards,kingBitboard,dx=(-1))

        if (Hray1 | Hray2) & (enemyQueen | enemyTowers | enemyKing):
            return False
        
        diagRay1=RayGenerator.GenerateDiagonalRay(Bitboards,kingBitboard,dx=1,dy=1)

        if diagRay1 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False
        
        diagRay2=RayGenerator.GenerateDiagonalRay(Bitboards,kingBitboard,dx=1,dy=(-1))

        if diagRay2 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False        
        
        diagRay3=RayGenerator.GenerateDiagonalRay(Bitboards,kingBitboard,dx=(-1),dy=1)

        if diagRay3 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False
        
        diagRay4=RayGenerator.GenerateDiagonalRay(Bitboards,kingBitboard,dx=(-1),dy=(-1))

        if diagRay4 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False


        return True