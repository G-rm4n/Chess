import Tablero


class GameMaster:

    def __init__(self,hayT,hayE,temporizador):
        self.hayTablas=hayT
        self.hayEnroque=hayE
        self.temporizador=temporizador

    def getAttackersX(self,Board:Tablero.Board,square,color):

        attackers=[]

        resul=Board.generateHorizontalSquares(square)

        for squaree in resul:

            piece=Board.getPiece(squaree)

            if (piece is not None and
                piece.get_color()!=color and
                piece.validateMovement(squaree,square,True)):

                attackers.append(squaree)
        
        return attackers
    
    def isOccupied(self,square,board):
        return board.getPiece(square) is not None
    
    def isAttack(self,destiny,board,color):
        return board.isOccupied(destiny) and board.getPiece(destiny).get_color()!=color
    
    def verifyLegality(self,origin,destiny,Board:Tablero.Board,color):
        piece=Board.getPiece(origin)

        if piece is None or piece.get_color()!=color:
            return False

        isAttack=self.isAttack(destiny,Board,color)

        if not(piece.validateMovement(origin,destiny,isAttack)):
            return False
        
        occupiedsquare=Board.verifyOccupancyRay(origin,destiny)


        if occupiedsquare is not None and piece.get_type_movement()=="T":
            return False
        
        if Board.isOccupied(destiny) and not(isAttack):
            return False
        
        if not(self.simulateMovement(origin,destiny,color,Board)):
            return False
        
        return True
        

    def verifyPromotion(self,piece,square):
        y=0 if piece.get_color()=="B" else 7
        return piece.getType()=="PAWN" and square[0]==y
    
    def simulateMovement(self,origin,destiny,color,Board):
        
        estado=Board.saveStatus()

        Board.makeMove(origin,destiny)

        result=self.evaluateCheck(color,Board)

        Board.chargeStatus(estado)

        if len(result) !=0:
            return False
        
        return True

    
    def getAttackersY(self,Board:Tablero.Board,square,color):

        attackers=[]

        resul=Board.generateVerticalSquares(square)

        for squaree in resul:

            piece=Board.getPiece(squaree)

            if (piece is not None and
                piece.get_color()!=color and
                piece.validateMovement(squaree,square,True)):

                attackers.append(squaree)

        return attackers
    
    def getAttackersDiag(self,Board:Tablero.Board,square,color):

        attackers=[]

        resul=Board.generateDiagonalSquare(square)

        

        for squaree in resul:

            piece=Board.getPiece(squaree)

            if (piece is not None and
                piece.get_color()!=color and
                piece.validateMovement(squaree,square)):

                attackers.append(squaree)
            
        return attackers
    
    def getHorseAttackers(self,Board,square,color):

        horseDisplacements=[(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]

        horseSquares=[(square[0]+dy,square[1]+dx)
                            for dy, dx in horseDisplacements
                            if 0<=square[0]+dy<=7 and 0<=square[1]+dx<=7]
        
        attackers=[]

        for squareHorse in horseSquares:
                
            piece=Board.getPiece(squareHorse)
            if  (piece is not None and
                 not(piece.get_color()==color)
                 and piece.validateMovement(squareHorse,square,True)):
                
                attackers.append(squareHorse)

        return attackers
    
    #si es el color de la persona en turno, se obtendran todas las piezas del jugador fuera de turno que pueden atacarlo
    #si es el color del jugador fuera de turno, se obtendran todas las piezas del jugador en turno que pueden atacarlo
    def evaluateAttack(self,Board,square,color):

        list1=self.getAttackersX(Board,square,color)
        list2=self.getAttackersY(Board,square,color)
        list3=self.getAttackersDiag(Board,square,color)
        list4=self.getHorseAttackers(Board,square,color)
        
        return list1+list2+list3+list4
    
    def evaluateCheck(self,color,Board):
        posRey=Board.getKingSquare(color)


        attackers=self.evaluateAttack(Board,posRey,color)

        

        return attackers

    
    def evaluateCheckMate(self,Board:Tablero.Board,attackers,color):

        kingSquare=Board.getKingSquare(color)
        
        if len(attackers)==1:

            attacker=attackers[0]
            
            counterResponse=self.evaluateAttack(Board,attacker,Board.getPiece(attacker).get_color())

            
            if len(counterResponse)!=0 and any(self.verifyLegality(counter,attacker,Board,color) 
                                                for counter in counterResponse):
                
                
                return False
            
            if Board.getPiece(attacker).get_type_movement()!="NT":
                                          
                intermediateSquares=Board.getIntermediateSquare(kingSquare,attacker)

                

                #print(f"casillas intermedias entre el atacante y el rey:{intermediateSquares}")
                #input()

                for square in intermediateSquares:

                    myColorAttackers=self.evaluateAttack(Board,square,Board.getPiece(attacker).get_color())

                    if any(self.verifyLegality(myColorAttacker,attacker,Board,color)
                                                for myColorAttacker in myColorAttackers):
                        
                        return False
                    
                
        
        kingDisplacements=((0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1))

        possibleSquares=[(kingSquare[0]+dy,kingSquare[1]+dx)
                             for dy,dx in kingDisplacements
                             if 0<=kingSquare[0]+dy<=7 and 0<=kingSquare[1]+dx<=7]
        
        #print(f"las posibles casillas a donde puede moverse el rey son:{possibleSquares}")
        
        for squares in possibleSquares:

            piece=Board.getPiece(squares)

            if (piece is None or piece.get_color()!=color):

                if len(self.evaluateAttack(Board,squares,color))==0:

                    if self.verifyLegality(kingSquare,squares,Board,color):
                        input()

                        return False

            #print(f"la casilla: {squares} esta atacada o vacia o tiene a alguien del rey por lo cual el rey esta en jaque")
    
        return True


            
        