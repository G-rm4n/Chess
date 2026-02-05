from Adapters.Bitboard import Bitboard
from Bot_Engine.constants import INF,NEG_INF
from Bot_Engine.Evaluate import Evaluator
from Bot_Engine.MoveGenerator.MoveGenerator import MoveGenerator
from Bot_Engine.legalCheck import legalChecker
from Bot_Engine.MoveExecutor import MoveExecutor
from Adapters.Translator import Translator
from Bot_Engine.TranspositionTable import TranspositionTable

class bot:

    def __init__(self,color,enemyColor,MaxHeight):
        self.BestScoreFound=0
        self.BestMovementFound=0
        self.MaxHeight=MaxHeight
        self.botcolor=color
        self.enemyColor=enemyColor
        self.TranspositionTable=TranspositionTable()

    def alphaBetaSearch(self,height:int,Bitboards:list,alpha,beta):

        if height==0:

            self.BestMovementFound=0
            self.BestScoreFound=-10**9

        currentColor=self.botcolor if ((height%2)==0) else self.enemyColor
        colorFlag=True if currentColor =="B" else False


        if self.TranspositionTable.isStateInTable(Bitboards,colorFlag):

            NodeValues=self.TranspositionTable.getNodeValues(Bitboards,colorFlag)

            score=NodeValues["score"]
            NodeType=NodeValues.get("Type")
            assert NodeValues["turn"] == currentColor, "SE RECUPERO UN HASH DE OTRO COLOR"            

            if NodeType == "E":

                if height == 0 and self.BestScoreFound<score:
                    self.BestScoreFound=score
                    move = NodeValues.get("move")

                    self.BestMovementFound=move

                if height!=0:
                    return score
            
            elif NodeType == "T":

                if height!=0:
                    return score
            
            elif NodeType=="L":
                assert NodeValues["turn"] == currentColor, "SE RECUPERO UN HASH DE OTRO COLOR"

                if height==0 and self.BestScoreFound<score:
                    self.BestScoreFound=score
                    move = NodeValues.get("move")

                    self.BestMovementFound=move
                
                alpha=max(score,alpha)
            
            
            elif NodeType=="U":

                beta=min(score,beta)
            
            if alpha>=beta:

                if self.BestMovementFound!=0:

                    return score
                
                # Si BestMovementFound == 0 y alpha >= beta, usar fallback
                if height!=0:
                    # En niveles profundos, retornamos el score (el padre actualizará)
                    return score
                # Si height == 0, continuar al fallback que está después del loop

           

        if height==self.MaxHeight:

                score=(Evaluator.ScoreBoard(Bitboards,self.botcolor,self.enemyColor)+ Evaluator.scorePositions(Bitboards,self.botcolor,self.enemyColor))
                self.TranspositionTable.storeState(Bitboards,score,height,"T",currentColor,colorFlag)
                return score
            
        allMoves = MoveGenerator.generatePseudoLegalMovments(Bitboards,currentColor)

        LegalMovements=legalChecker.filtherMovements(allMoves,Bitboards,currentColor)

        if len(LegalMovements)==0:

            if not(legalChecker.isKingSafe(Bitboards,currentColor)):
                

                points=((-10000) + height) if (height%2)==0 else ((10000) - height)

            else:

                points=0

            self.TranspositionTable.storeState(Bitboards,points,height,"T",currentColor,colorFlag)

            return points

        LegalMovements.sort(key=lambda m: Evaluator.ScoreMove(m,Bitboards,currentColor),reverse=True)

        bestLocalMove=0
        if (height%2)==0:
            best=-INF

            for Move in LegalMovements:

                undo_info=MoveExecutor.make_move(Bitboards,Move,currentColor)
                
                score=self.alphaBetaSearch(height+1,Bitboards,alpha,beta)

                if score>best:
                    best=score
                    bestLocalMove=Move

                alpha=max(score,alpha) 

                MoveExecutor.unMake_Move(Move,Bitboards,undo_info,currentColor)

                if height==0 and best>self.BestScoreFound:
                    
                    self.BestScoreFound=best
                    self.BestMovementFound=Move

                if alpha >= beta:

                    self.TranspositionTable.storeState(Bitboards,best,height,"L",currentColor,colorFlag,bestLocalMove)
                    break

            else:
                self.TranspositionTable.storeState(Bitboards,best,height,"E",currentColor,colorFlag,bestLocalMove)
            
            return best

        else:      
            best=INF

            for Move in LegalMovements:

                undo_info=MoveExecutor.make_move(Bitboards,Move,currentColor)
                
                score=self.alphaBetaSearch(height+1,Bitboards,alpha,beta)

                if best>score:
                    best=score
                    bestLocalMove=Move

                beta=min(beta,score)
                
                MoveExecutor.unMake_Move(Move,Bitboards,undo_info,currentColor)

                if beta <= alpha:
                    self.TranspositionTable.storeState(Bitboards,best,height,"U",currentColor,colorFlag,bestLocalMove)
                    break
            
            else:
                self.TranspositionTable.storeState(Bitboards,best,height,"E",currentColor,colorFlag,bestLocalMove)

            return best
        
    def chooseMovement(self, BoardPositions):

        BitboardList=Bitboard.generateBitboards(BoardPositions)

        self.alphaBetaSearch(0,BitboardList,NEG_INF,INF)
        
        choose=Translator.translateMove(self.BestMovementFound) if self.BestMovementFound!=0 else ((-1,-1),(-1,-1))

        return choose
    
    def choosePromotion(self):

        return "QUEEN"

