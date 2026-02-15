from AI_Engine.constants import MASK_CENTER,BORDER_CENTER,MASK_CENTER_CORNERS,MASK_SIDE_CROSS,MASK_NEAR_CORNERS,MASK_INNER_CORNERS_ADJACENT,MASK_CORNERS,MASK_BISHOP_LONG,MASK_BISHOP_MID,VALUEDICTIONARY,PIECETYPEDICTIONARY,MASK_SIDE_STRIPS_VERTICAL,ROW_1,ROW_2,ROW_7,ROW_8,COLORDICTIONARY,REVERSEPIECEDICTIONARY
from AI_Engine.legalCheck import legalChecker
from AI_Engine.MoveExecutor import MoveExecutor

class Evaluator:

    @staticmethod
    def ScoreMove(Move,Bitboards,color):

        score=0
        
        origen, destino, pieza = Move

        opp_offset = 7 if color == "W" else 0
        captured_piece_type = None


        for i in range(opp_offset, opp_offset + 6):
            if (Bitboards[i] >> destino) & 1:
                captured_piece_type = REVERSEPIECEDICTIONARY[i] 
                break
        

        if captured_piece_type is not None:

            score += (VALUEDICTIONARY[captured_piece_type]*10) - (VALUEDICTIONARY[pieza])

        if Move[2]=="P" and Evaluator.evaluatePosiblePromotion(Move[0],Bitboards[14],color):

            score +=900

        return score
        


    @staticmethod
    def ScoreBoard(Bitboards,color,enemyColor):

        materialPointsSelf=0

        materialPointsSelf += Bitboards[PIECETYPEDICTIONARY["KING"] + COLORDICTIONARY[color]].bit_count() * VALUEDICTIONARY["K"]
        materialPointsSelf += Bitboards[PIECETYPEDICTIONARY["PAWN"] + COLORDICTIONARY[color]].bit_count() * VALUEDICTIONARY["P"]
        materialPointsSelf += Bitboards[PIECETYPEDICTIONARY["TOWER"] + COLORDICTIONARY[color]].bit_count() * VALUEDICTIONARY["T"]
        materialPointsSelf += Bitboards[PIECETYPEDICTIONARY["BISHOP"] + COLORDICTIONARY[color]].bit_count() * VALUEDICTIONARY["B"]
        materialPointsSelf += Bitboards[PIECETYPEDICTIONARY["HORSE"] + COLORDICTIONARY[color]].bit_count() * VALUEDICTIONARY["H"]
        materialPointsSelf += Bitboards[PIECETYPEDICTIONARY["QUEEN"] + COLORDICTIONARY[color]].bit_count() * VALUEDICTIONARY["Q"]

        materialPointsEnemy=0
        materialPointsEnemy += Bitboards[PIECETYPEDICTIONARY["KING"] + COLORDICTIONARY[enemyColor]].bit_count() * VALUEDICTIONARY["K"]
        materialPointsEnemy += Bitboards[PIECETYPEDICTIONARY["PAWN"] + COLORDICTIONARY[enemyColor]].bit_count() * VALUEDICTIONARY["P"]
        materialPointsEnemy += Bitboards[PIECETYPEDICTIONARY["TOWER"] + COLORDICTIONARY[enemyColor]].bit_count() * VALUEDICTIONARY["T"]
        materialPointsEnemy += Bitboards[PIECETYPEDICTIONARY["BISHOP"] + COLORDICTIONARY[enemyColor]].bit_count() * VALUEDICTIONARY["B"]
        materialPointsEnemy += Bitboards[PIECETYPEDICTIONARY["HORSE"] + COLORDICTIONARY[enemyColor]].bit_count() * VALUEDICTIONARY["H"]
        materialPointsEnemy += Bitboards[PIECETYPEDICTIONARY["QUEEN"] + COLORDICTIONARY[enemyColor]].bit_count() * VALUEDICTIONARY["Q"]

        materialPoints= materialPointsSelf - materialPointsEnemy

        checkKingSelf=(-600) if not(legalChecker.isKingSafe(Bitboards,color)) else 0
        checkKingEnemy=(500) if not(legalChecker.isKingSafe(Bitboards,enemyColor)) else 0

        selfPawns=Bitboards[PIECETYPEDICTIONARY["PAWN"] + COLORDICTIONARY[color]]

        promotionPoints=0
        limitPromotionBonus= 1400

        while selfPawns and promotionPoints<limitPromotionBonus:
            
            pawn= selfPawns & -selfPawns
            selfPawns &=(selfPawns-1)

            promotionPoints+=Evaluator.evaluatePosiblePromotion(pawn,Bitboards[COLORDICTIONARY[enemyColor] + 6],color)

        totalPoints=materialPoints + checkKingEnemy + checkKingSelf + promotionPoints

        return totalPoints
    
    @staticmethod
    def evaluatePosiblePromotion(Pawn,occupiedBitboard,color):

        distance=7
        blocked=False

        while True:

            Pawn = (Pawn<<8) if color=="B" else (Pawn>>8)

            if Pawn & ((ROW_8) if color=="B" else (ROW_1)):
                distance=1
                break

            if Pawn & (~(occupiedBitboard)):
                distance-=1
            else:
                blocked
                break
                
        if blocked:
            penaltyDistance=8-distance
            return max(10,40/penaltyDistance)
        
        promotionValues ={
            1: 650,   
            2: 350,   
            3: 150,   
            4: 80,    
            5: 40,    
            6: 20,    
            7: 10 
        }

        return promotionValues.get(distance,10)
    
    @staticmethod
    def scoreHorsePosition(HorseBitboard:int,Color):

        score=0

        score+=((HorseBitboard&MASK_CENTER).bit_count())*80
        
        score+=((HorseBitboard&BORDER_CENTER).bit_count())*60
        
        score+=((HorseBitboard&MASK_CENTER_CORNERS).bit_count())*40

        score-=((HorseBitboard&MASK_SIDE_CROSS).bit_count())*100

        score-=((HorseBitboard&MASK_NEAR_CORNERS).bit_count())*130
        
        score-=((HorseBitboard&MASK_INNER_CORNERS_ADJACENT).bit_count())*80

        score-=((HorseBitboard&MASK_CORNERS).bit_count())*150
        
        return score
    
    @staticmethod
    def scoreBishopPositions(BishopBitboard,color):

        score=0

        MaskAttack=0x8040201008440240 if color=="W" else 0x00420408102040C0

        score+=((BishopBitboard&MaskAttack).bit_count())*60

        score += (BishopBitboard & BORDER_CENTER).bit_count() * 80
        score += (BishopBitboard & MASK_CENTER).bit_count() * 70
        score += (BishopBitboard & MASK_CENTER_CORNERS).bit_count() * 50

        score += (BishopBitboard & MASK_BISHOP_LONG).bit_count() * 60
        score += (BishopBitboard & MASK_BISHOP_MID).bit_count() * 25

        score -= (BishopBitboard & MASK_SIDE_CROSS).bit_count() * 80
        score -= (BishopBitboard & MASK_CORNERS).bit_count() * 140
        score -= (BishopBitboard & MASK_NEAR_CORNERS).bit_count() * 100

        return score

    @staticmethod
    def scoreTowerPositions(TowerBitboard,color):

        score=0

        r2= ROW_2 if color=="W" else ROW_7
        r7= ROW_7 if color=="W" else ROW_2
        r8= ROW_8 if color=="W" else ROW_1

        score += ((TowerBitboard&r8).bit_count()) * 60
        score += ((TowerBitboard&r7).bit_count()) * 120
        score += ((TowerBitboard&r2).bit_count()) * 40
        score += ((TowerBitboard&MASK_CENTER).bit_count()) * 45

        score -= ((TowerBitboard&MASK_SIDE_STRIPS_VERTICAL).bit_count()) * 20

        return score
    
    @staticmethod
    def scoreQueenPositions(QueenBitboard,color):

        score=0

        score += ((QueenBitboard&MASK_CENTER).bit_count()) * 40
        score += ((QueenBitboard&BORDER_CENTER&MASK_CENTER_CORNERS).bit_count()) * 5

        score -= ((QueenBitboard&MASK_CORNERS).bit_count()) * 80
        score -= ((QueenBitboard&MASK_SIDE_CROSS).bit_count()) * 60
        score -= ((QueenBitboard&MASK_NEAR_CORNERS).bit_count()) * 40

        return score
    
    @staticmethod
    def scoreKingPositions(KingBitboard,color):

        score=0

        king_safe_zone = 0x00000000000000C6 if color=="W" else 0xC600000000000000
    
        score += (KingBitboard & king_safe_zone).bit_count() * 150
    
        score -= (KingBitboard & MASK_CENTER).bit_count() * 200
        score -= (KingBitboard & BORDER_CENTER).bit_count() * 120

        return score
    
    @staticmethod
    def scorePositions(BitBoards:list,color,enemyColor):

        starallie=COLORDICTIONARY[color]
        startEnemy=COLORDICTIONARY[enemyColor]

        myHorseScore=Evaluator.scoreHorsePosition(BitBoards[PIECETYPEDICTIONARY["HORSE"]+starallie],color)
        enemyHorseScore=Evaluator.scoreHorsePosition(BitBoards[PIECETYPEDICTIONARY["HORSE"]+startEnemy],enemyColor)

        myBishopScore=Evaluator.scoreBishopPositions(BitBoards[PIECETYPEDICTIONARY["BISHOP"]+starallie],color)
        enemyBishopScore=Evaluator.scoreBishopPositions(BitBoards[PIECETYPEDICTIONARY["BISHOP"]+startEnemy],enemyColor)

        myTowerScore=Evaluator.scoreTowerPositions(BitBoards[PIECETYPEDICTIONARY["TOWER"]+starallie],color)
        enemyToweScore=Evaluator.scoreTowerPositions(BitBoards[PIECETYPEDICTIONARY["TOWER"]+startEnemy],enemyColor)

        myQueenScore=Evaluator.scoreQueenPositions(BitBoards[PIECETYPEDICTIONARY["QUEEN"]+starallie],color)
        enemyQueenScore=Evaluator.scoreQueenPositions(BitBoards[PIECETYPEDICTIONARY["QUEEN"]+startEnemy],enemyColor)

        myKingScore=Evaluator.scoreKingPositions(BitBoards[PIECETYPEDICTIONARY["KING"]+starallie],color)
        enemyKingScore=Evaluator.scoreKingPositions(BitBoards[PIECETYPEDICTIONARY["KING"]+startEnemy],enemyColor)

        score=myHorseScore-enemyHorseScore+myBishopScore-enemyBishopScore+myTowerScore-enemyToweScore+myQueenScore-enemyQueenScore+myKingScore-enemyKingScore

        return score