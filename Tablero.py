from Pieza import *
import copy
import Movimiento

class Board:

    def __init__(self):
        
        self.positions=[[None for _ in range(8)] for s in range(8)]
        self.createdPieces=0


    def prepareBoard(self):
        
        pieceList=[Tower,Horse,Bishop,Queen,King,Bishop,Horse,Tower]
        
        for i in range(2):

            for j in range(8):
                if i%2!=0:
                    self.assingPiece((i,j),Pawn("W",self.createdPieces))
                    self.createdPieces+=1

                    self.assingPiece((7-i,j),Pawn("B",self.createdPieces))
                    self.createdPieces+=1
                else:
                    self.assingPiece((i,j),pieceList[j]("W",self.createdPieces))
                    self.createdPieces+=1

                    self.assingPiece((7-i,j),pieceList[j]("B",self.createdPieces))
                    self.createdPieces+=1

        return self.positions
    
    def validateCoords(self,origin,destiny):
        return 0<=destiny[0]<=7 and 0<=destiny[1]<=7 and 0<=origin[0]<=7 and 0<=origin[1]<=7 and destiny!=origin

    def saveStatus(self):
        return copy.deepcopy(self.positions)
    
    def getPositions(self):
        return self.positions
    
    def chargeStatus(self,estado):
        self.positions=estado
        return self.positions
    
    def makeMove(self,origin,destiny):

        self.positions[destiny[0]][destiny[1]]=self.positions[origin[0]][origin[1]]
        self.positions[origin[0]][origin[1]]=None
    
    def unMakeMove(self,Mov=Movimiento.Movement):
        origin=Mov.get_origin()
        destiny=Mov.get_destiny()
        isCapture=Mov.get_isCapture()

        self.positions[origin[0]][origin[1]]=self.positions[destiny[0]][destiny[1]]
        self.positions[destiny[0]][destiny[1]]= Mov.getPiezaCapturada() if isCapture else None

        return self.positions
    
    
    #Retorna las Squares intermedias horizontales entre 2 Squares
    def getIntermediateSquareY(self,origin,destiny):
        Squares=[]

        dy=destiny[0]-origin[0]

        step= 1 if dy>0 else -1

        for i in range(step,dy,step):
            Square=(origin[0]+i,origin[1])

            Squares.append(Square)
        
        return Squares
    
    #Retorna las Squares intermedias horizontales entre 2 Squares
    def getIntermediateSquareX(self,origin,destiny):
        Squares=[]
        dx=destiny[1]-origin[1]
        
        step= 1 if dx>0 else -1

        for i in range(step,dx,step):
            Square=(origin[0],origin[1]+i)

            Squares.append(Square)
        
        return Squares
    
    #retorna las Squares intermedias diagonales entre 2 Squares
    def getIntermediateSquareDiag(self,origin,destiny):
        Squares=[]

        dx=destiny[1]-origin[1]
        dy=destiny[0]-origin[0]

        displacementX= 1 if dx>0 else -1
        displacementY= 1 if dy>0 else -1

        for i in range(1,abs(min(dx,dy))):

            Square=(origin[0]+(i*displacementY),origin[1]+(i*displacementX))
            
            Squares.append(Square)
        
        return Squares
    
    def getIntermediateSquare(self,origin, destiny):
        dx=destiny[1]-origin[1]
        dy=destiny[0]-origin[0]

        if (dy!=0 and dx!=0):
            return self.getIntermediateSquareDiag(origin,destiny)
        
        if dx==0:
            return self.getIntermediateSquareY(origin,destiny)
        
        return self.getIntermediateSquareX(origin,destiny)
    
    
    def verifyOccupancyRay(self,origin,destiny):

        Squares=self.getIntermediateSquare(origin,destiny)

        for square in Squares:


            if self.isOccupied(square):
                return square
        
        return None
    
    #retorna True si la casilla esta ocupada
    def isOccupied(self,square):
        return self.positions[square[0]][square[1]] is not None
    
    def generateHorizontalSquares(self,square):
        print(square)

        squares=[]

        i=1
        while True:

            if (square[1]+i)>7:
                break
            
            squares.append((square[0],square[1]+i))

            if self.isOccupied((square[0],square[1]+i)):
                break

            i+=1
        
        i=1
        while True:

            if (square[1]-i)<0:
                break

            squares.append((square[0],square[1]-i))

            if self.isOccupied((square[0],square[1]-i)):
                break

            i+=1

        return squares
    
    def generateVerticalSquares(self,square):

        squares=[]

        i=1
        while True:

            if (square[0]+i)>7:
                break
            

            squares.append((square[0]+i,square[1]))


            if self.isOccupied((square[0]+i,square[1])):
                break

            i+=1
        
        i=1
        while True:

            if (square[0]-i)<0:
                break

            squares.append((square[0]-i,square[1]))

            if self.isOccupied((square[0]-i,square[1])):
                break

            i+=1

        return squares
    

    def generateDiagonalSquare(self,square):

        squares=[]

        i=1
        while True:

            if (square[0]+i)>7 or (square[1]+i)>7:
                break
            

            squares.append((square[0]+i,square[1]+i))


            if self.isOccupied((square[0]+i,square[1]+i)):
                break

            i+=1
        
        i=1
        while True:

            if (square[0]-i)<0 or (square[1]-i)<0:
                break

            squares.append((square[0]-i,square[1]-i))

            if self.isOccupied((square[0]-i,square[1]-i)):
                break

            i+=1

        i=1
        while True:

            if (square[0]+i)>7 or (square[1]-i)<0:
                break
            

            squares.append((square[0]+i,square[1]-i))


            if self.isOccupied((square[0]+i,square[1]-i)):
                break

            i+=1
        
        i=1
        while True:

            if (square[0]-i)<0 or (square[1]+i)>7:
                break

            squares.append((square[0]-i,square[1]+i))

            if self.isOccupied((square[0]-i,square[1]+i)):
                break

            i+=1

        i=1
        
        return squares



    def getKingSquare(self,color):

        Square=next(((y,x)for y, fila in enumerate(self.positions)
                            for x, piece in enumerate(fila)
                            if piece!=None and piece.get_color()==color and piece.getType()=="KING"),
                            None)
        
        return Square
    
    def getPiece(self,Square):
        return self.positions[Square[0]][Square[1]]
    
    def createNewPiece(self,type,color):

        pieceDictionay={
            "TOWER":Tower,
            "HORSE":Horse,
            "BISHOP":Bishop,
            "QUEEN":Queen,
        }
        
        piece=pieceDictionay[type](color,self.createdPieces)
        self.createdPieces+=1

        return piece
    
    def assingPiece(self,Square,piece):
        self.positions[Square[0]][Square[1]]=piece
        return self.positions
    