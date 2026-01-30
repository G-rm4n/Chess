import GameMaster
import Jugador
import Movimiento
import Promocion
import Tablero
import time
import os


class Chess:
    
    def __init__(self):
        self.gameMaster=GameMaster.GameMaster(False,False,50)
        self.tablero=Tablero.Board()
        self.historialAcciones=[]
        self.jugadores=[None,None]

    def preparePlayers(self):
        
        for i in range(2):

            name=input("Ingrese el name de que utilizara las fichas "+ ("BLANCAS" if i%2==0 else "NEGRAS")+": ")
            self.jugadores[i]=Jugador.Player("W" if i%2==0 else "B",name)

        return self.jugadores
    
    def createMovement(self,origin,destiny,isAttack):
        Mov=Movimiento.Movement(origin,destiny,isAttack)
        return Mov

    def registerMovement(self,movement):
        self.historialAcciones.append(movement)
    
    def incrementMovements(self,piece):
        piece.incr_mov()
    
    def playRound(self,index):
        attackers=[]
        

        if self.historialAcciones:
            attackers=self.gameMaster.evaluateCheck(self.jugadores[index].get_color(),self.tablero)
            if len(attackers)>0 and self.gameMaster.evaluateCheckMate(self.tablero,attackers,self.jugadores[index].get_color()):
                return False
        
        while True:
            
            self.mostrarTablero(self.tablero)
            print(f"es turno de {self.jugadores[index].get_name()}")

            if len(attackers)>0:
                print(self.jugadores[index].get_name()+" tu rey esta en Jaque!!!")

            origin,destiny=self.jugadores[index].make_choice()

            if not(self.tablero.validateCoords(origin,destiny)) :
                print("coordenadas invalidas...")
                time.sleep(3)

                continue
            
            if not(self.gameMaster.verifyLegality(origin,destiny,self.tablero,self.jugadores[index].get_color())):
                print("movement ilegal...")
                time.sleep(3)

                continue

            isAttack=self.gameMaster.isAttack(destiny,self.tablero,self.jugadores[index].get_color())

            mov=self.createMovement(origin,destiny,isAttack)
            
            if isAttack:
                capturePiece=self.tablero.getPiece(destiny)
                mov.set_capture(capturePiece)
            
            self.registerMovement(mov)
            self.incrementMovements(self.tablero.getPiece(origin))

            self.tablero.makeMove(origin,destiny)
            
            if self.gameMaster.verifyPromotion(self.tablero.getPiece(destiny),destiny):
                self.makePromotion(destiny,index)

            input()

            break

        return True
        
    def mostrarTablero(self,tablero):
        symbolDictionary={
            "W":{
                "KING":"♔",
                "QUEEN":"♕",
                "TOWER":"♖",
                "BISHOP":"♗",
                "HORSE":"♘",
                "PAWN":"♙"
            },
            "B":{
                "KING":"♚",
                "QUEEN":"♛",
                "TOWER":"♜",
                "BISHOP":"♝",
                "HORSE":"♞",
                "PAWN":"♟"
            },
        }


        os.system("cls")

        for i in range(8):
            for j in range(8):
                squareContent=tablero.getPiece((i,j))
                if(squareContent!=None):
                    print(symbolDictionary[squareContent.get_color()][squareContent.getType()],sep=None,end="\t")
                else:
                    print("□",sep=None,end="\t") if (i%2!=0 and j%2==0) or (i%2==0 and j%2!=0) else print("■",sep=None,end="\t")
                
            print("\n")

    
    def IniciarJuego(self):
        self.preparePlayers()
        self.tablero.prepareBoard()
        
        i=0
        while True:
            
            if not(self.playRound(i%2)):
                break

            i=i+1
        
        print("fin del juego")


    def makePromotion(self,square,index):

        print("las piezas que puede obtener por Promocion son: 'QUEEN','BISHOP','Caballo','TOWER' \n")

        tipo=(self.jugadores[index].make_Choice_Promotion()).lower()

        pieza=self.tablero.createNewPiece(tipo,self.jugadores[index].get_color())

        self.tablero.assingPiece(square,pieza)

        self.registerPromotion(square,pieza)

    def registerPromotion(self,square,pieza):
        self.historialAcciones.append(Promocion.Promocion(square,pieza))
        return self.historialAcciones