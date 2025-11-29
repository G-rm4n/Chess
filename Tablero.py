from Pieza import *
import copy
import Movimiento

class Tablero:

    def __init__(self):
        
        self.posciciones=[[None for _ in range(8)] for s in range(8)]
        self.cant_piezas_creadas=0


    def prepararTablero(self):
        piezasLista=[Torre,Caballo,Alfil,reina,Rey,Alfil,Caballo,Torre]
        
        for i in range(2):

            for j in range(8):
                if i%2!=0:
                    self.asignar_pieza((i,j),Peon("W",self.cant_piezas_creadas))
                    self.cant_piezas_creadas+=1

                    self.asignar_pieza((7-i,j),Peon("B",self.cant_piezas_creadas))
                    self.cant_piezas_creadas+=1
                else:
                    self.asignar_pieza((i,j),piezasLista[j]("W",self.cant_piezas_creadas))
                    self.cant_piezas_creadas+=1

                    self.asignar_pieza((7-i,j),piezasLista[j]("B",self.cant_piezas_creadas))
                    self.cant_piezas_creadas+=1

        return self.posciciones
    
    def validar_coordenadas(self,origen,destino):
        return 0<=destino[0]<=7 and 0<=destino[1]<=7 and 0<=origen[0]<=7 and 0<=origen[1]<=7 and destino!=origen

    def guardarEstado(self):
        return copy.deepcopy(self.posciciones)
    
    def restaurarEstado(self,estado):
        self.posciciones=estado
        return self.posciciones
    
    def efectuarMovimiento(self,origen,destino):

        self.posciciones[destino[0]][destino[1]]=self.posciciones[origen[0]][origen[1]]
        self.posciciones[origen[0]][origen[1]]=None
    
    def deshacerMovimiento(self,Mov=Movimiento.Movimiento):
        origin=Mov.get_origin()
        destiny=Mov.get_destiny()
        isCapture=Mov.get_isCapture()

        self.posciciones[origin[0]][origin[1]]=self.posciciones[destiny[0]][destiny[1]]
        self.posciciones[destiny[0]][destiny[1]]= Mov.getPiezaCapturada() if isCapture else None

        return self.posciciones
    
    
    #Retorna las casillas intermedias horizontales entre 2 casillas
    def get_casillas_intermediasY(self,origen,destino):
        casillas=[]

        dy=destino[0]-origen[0]

        step= 1 if dy>0 else -1

        for i in range(step,dy+step,step):
            poscicion=(origen[0]+i,origen[1])

            casillas.append(poscicion)
        
        return casillas
    
    #Retorna las casillas intermedias horizontales entre 2 casillas
    def get_casillas_intermediasX(self,origen,destino):
        casillas=[]
        dx=destino[1]-origen[1]
        
        step= 1 if dx>0 else -1

        for i in range(step,dx+step,step):
            poscicion=(origen[0],origen[1]+i)

            casillas.append(poscicion)
        
        return casillas
    
    #retorna las casillas intermedias diagonales entre 2 casillas
    def get_casillas_intermediasDiag(self,origen,destino):
        casillas=[]

        dx=destino[1]-origen[1]
        dy=destino[0]-origen[0]

        displacementX= 1 if dx>0 else -1
        displacementY= 1 if dy>0 else -1

        for i in range(1,abs(min(dx,dy))+1):

            poscicion=(origen[0]+(i*displacementY),origen[1]+(i*displacementX))
            
            casillas.append(poscicion)
        
        return casillas
    
    def get_casillas_intermedias(self,origen, destino):
        dx=destino[1]-origen[1]
        dy=destino[0]-origen[0]

        if (dy!=0 and dx!=0):
            return self.get_casillas_intermediasDiag(origen,destino)
        
        if dx==0:
            return self.get_casillas_intermediasY(origen,destino)
        
        return self.get_casillas_intermediasX(origen,destino)
    
    
    def verificarOcupacionTrayectoria(self,origen, destino):

        casillas=self.get_casillas_intermedias(origen,destino)

        for casilla in casillas:

            if self.get_pieza(casilla) is not None:
                return casilla
        
        return None

    
    def get_rey_poscicion(self,color):

        poscicion=next(((y,x)for y, fila in enumerate(self.posciciones)
                            for x, pieza in enumerate(fila)
                            if pieza!=None and pieza.get_color()==color and pieza.getTipo()=="rey"),
                            None)
        
        return poscicion
    
    def get_pieza(self,poscicion):
        return self.posciciones[poscicion[0]][poscicion[1]]
    
    def crear_nueva_pieza(self,tipo,color):

        diccionarioPiezas={
            "torre":Torre,
            "caballo":Caballo,
            "alfil":Alfil,
            "reina":reina,
        }
        
        pieza=diccionarioPiezas[tipo](color,self.cant_piezas_creadas)
        self.cant_piezas_creadas=+1

        return pieza
    
    def asignar_pieza(self,poscicion,pieza):
        self.posciciones[poscicion[0]][poscicion[1]]=pieza
        return self.posciciones
    