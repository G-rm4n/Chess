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
        self.tablero=Tablero.Tablero()
        self.historialAcciones=[]
        self.jugadores=[None,None]

    def Preparar_Jugadores(self):
        
        for i in range(2):

            nombre=input("Ingrese el nombre de que utilizara las fichas "+ ("Negras" if i%2==0 else "Blancas")+": ")
            self.jugadores[i]=Jugador.Jugador("B" if i%2==0 else "W",nombre)

        return self.jugadores
    
    def crearMovimiento(self,origen,destino,isAttack):
        Mov=Movimiento.Movimiento(origen,destino,isAttack)
        return Mov

    def registrarMovimiento(self,Movimiento):
        self.historialAcciones.append(Movimiento)
    
    def incrementarMovimientos(self,Pieza):
        Pieza.incr_mov()
    
    def jugarTurno(self,indice):
        

        if self.historialAcciones:
            Atacantes=self.gameMaster.evaluarJaque(self.jugadores[indice].get_color(),self.tablero)
            if len(Atacantes) >0 and self.gameMaster.evaluarJaqueMate(self.tablero,Atacantes,self.jugadores[indice].get_color()):
                return False
        
        while True:
            print(f"es turno de {self.jugadores[indice].get_nombre()}")
            self.mostrarTablero(self.tablero)
            origen,destino=self.jugadores[indice].make_choice()

            if not(self.tablero.validar_coordenadas(origen,destino)) :
                print("coordenadas inavlidas...")
                time.sleep(3)

                continue
            
            if not(self.gameMaster.verificar_legalidad_turno(origen,destino,self.tablero,self.jugadores[indice].get_color())):
                print("Movimiento ilegal...")
                time.sleep(3)

                continue

            isAttack=self.gameMaster.isAttack(destino,self.jugadores[indice].get_color(),self.tablero)

            mov=self.crearMovimiento(origen,destino,isAttack)
            
            if isAttack:
                piezaCaptura=self.tablero.get_pieza(destino)
                mov.set_capture(piezaCaptura)
            
            self.registrarMovimiento(mov)
            self.incrementarMovimientos(self.tablero.get_pieza(origen))

            self.tablero.efectuarMovimiento(origen,destino)
            
            if self.gameMaster.verificarPromocion(self.tablero.get_pieza(destino),destino):
                self.realizarPromocion(destino,indice)

            input()

            break

        return True
        
    def mostrarTablero(self,tablero):
        diccionarioSimbolos={
            "W":{
                "rey":"♔",
                "reina":"♕",
                "torre":"♖",
                "alfil":"♗",
                "caballo":"♘",
                "peon":"♙"
            },
            "B":{
                "rey":"♚",
                "reina":"♛",
                "torre":"♜",
                "alfil":"♝",
                "caballo":"♞",
                "peon":"♟"
            },
        }


        os.system("cls")

        for i in range(8):
            for j in range(8):
                contenidoCasilla=tablero.get_pieza((i,j))
                if(contenidoCasilla!=None):
                    print(diccionarioSimbolos[contenidoCasilla.get_color()][contenidoCasilla.getTipo()],sep=None,end="\t")
                else:
                    print("□",sep=None,end="\t") if (i%2!=0 and j%2==0) or (i%2==0 and j%2!=0) else print("■",sep=None,end="\t")
                
            print("\n")

    
    def IniciarJuego(self):
        self.Preparar_Jugadores()
        self.tablero.prepararTablero()
        
        i=0
        while True:
            
            if not(self.jugarTurno(i%2)):
                break

            i=i+1
        
        print("fin del juego")


    def realizarPromocion(self,poscicion,indice):

        print("las piezas que puede obtener por Promocion son: 'Reina','Alfil','Caballo','Torre' \n")

        tipo=(self.jugadores[indice].make_Choice_Promocion()).lower()

        pieza=self.tablero.crear_nueva_pieza(tipo,self.jugadores[indice].get_color())

        self.tablero.asignar_pieza(poscicion,pieza)

        self.registrarPromocion(poscicion,pieza)

    def registrarPromocion(self,poscicion,pieza):
        self.historialAcciones.append(Promocion.Promocion(poscicion,pieza))
        return self.historialAcciones