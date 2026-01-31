from Adapters.Bitboard import Bitboard
from Bot_Engine.constants import INF,NEG_INF
from Bot_Engine.Evaluate import Evaluator
from Bot_Engine.MoveGenerator.MoveGenerator import MoveGenerator
from Bot_Engine.legalCheck import legalChecker
from Bot_Engine.MoveExecutor import MoveExecutor
from Adapters.Translator import Translator

class bot:

    def __init__(self,color,enemyColor,MaxHeight):
        
        self.BestScoreFound=0
        self.BestMovementFound=0
        self.MaxHeight=MaxHeight
        self.botcolor=color
        self.enemyColor=enemyColor

    def alphaBetaSearch(self,height:int,Bitboards:list,alpha,beta):

        currentColor=self.botcolor if ((height%2)==0) else self.enemyColor

        if height==0:

            self.BestMovementFound=0
            self.BestScoreFound=-10**9

        if height==self.MaxHeight:
            return (Evaluator.ScoreBoard(Bitboards,self.botcolor,self.enemyColor)+ Evaluator.scorePositions(Bitboards,self.botcolor,self.enemyColor))

        allMoves = MoveGenerator.generatePseudoLegalMovments(Bitboards,currentColor)

        LegalMovements=legalChecker.filtherMovements(allMoves,Bitboards,currentColor)

        if len(LegalMovements)==0:

            if not(legalChecker.isKingSafe(Bitboards,currentColor)):
                

                points=((-10000) + height) if (height%2)==0 else ((10000) - height)

            else:

                points=0

            return points

        LegalMovements.sort(key=lambda m: Evaluator.ScoreMove(m,Bitboards,currentColor),reverse=True)

        if (height%2)==0:

            for Move in LegalMovements:

                undo_info=MoveExecutor.make_move(Bitboards,Move,currentColor)
                
                alpha=max(alpha,self.alphaBetaSearch(height+1,Bitboards,alpha,beta))

                MoveExecutor.unMake_Move(Move,Bitboards,undo_info,currentColor)

                if height==0 and alpha>self.BestScoreFound:
                    print(f"mejor movimiento antiguo encontrado:{self.BestMovementFound}")
                    print(f"mejor value antiguo encontrado:{self.BestScoreFound}")

                    self.BestScoreFound=alpha
                    self.BestMovementFound=Move
                    print(f"mejor movimiento nuevo es:{self.BestMovementFound}")
                    print(f"mejor movimiento nuevo es:{self.BestScoreFound}")

                if alpha >= beta:
                    break

                if alpha >= beta:
                    break

            return alpha

        else:      
            
            for Move in LegalMovements:

                undo_info=MoveExecutor.make_move(Bitboards,Move,currentColor)
                
                beta=min(beta,self.alphaBetaSearch(height+1,Bitboards,alpha,beta))
                
                MoveExecutor.unMake_Move(Move,Bitboards,undo_info,currentColor)

                if beta <= alpha:
                    break
            
            return beta
        
    def chooseMovement(self,BoardPositions):

        BitboardList=Bitboard.generateBitboards(BoardPositions)

        self.alphaBetaSearch(0,BitboardList,NEG_INF,INF)

        choose=Translator.translateMove(self.BestMovementFound)

        return choose
    
    def choosePromotion(self):

        return "QUEEN"
        
