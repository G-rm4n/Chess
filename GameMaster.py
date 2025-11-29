
class GameMaster:

    def __init__(self,hayT,hayE,temporizador):
        self.hayTablas=hayT
        self.hayEnroque=hayE
        self.temporizador=temporizador

    def getAtacantesX(self,tablero,casilla,color):

        dx1=casilla[1]
        dx2=7 - casilla[1]

        distanciaHorizontal=[dx1,dx2]

        direcciones=[-1,1]

        atacantes=[]

        for distancia, direccion in zip(distanciaHorizontal,direcciones):
        
            resul=tablero.verificarOcupacionTrayectoria(casilla,(casilla[0],casilla[1]+(direccion*distancia)))
                
            if (resul is not None and
                 not(tablero.get_pieza(resul).get_color()==color)
                 and tablero.get_pieza(resul).validarMov(casilla)):
                
                atacantes.append(resul)

        return atacantes
    
    #verifica si la utlima casilla devuelta por el tablero es la de destino y si hay una pieza verifica que sea del otro equipo 
    def verificarCasilla(self,destino,ultimaCasilla,color,tablero):
        return destino==ultimaCasilla and tablero.get_pieza(ultimaCasilla).get_color()!=color

    def isAttack(self,destino,color,tablero):
        return (tablero.get_pieza(destino) is not None) and tablero.get_pieza(destino).get_color()!=color
    
    def verificar_legalidad_turno(self,origen,destino,tablero,color):
        pieza=tablero.get_pieza(origen)

        if pieza is None or pieza.get_color()!=color:
            return False
        
        isAttack=self.isAttack(destino,color,tablero)


        if not(pieza.validarMov(origen,destino,isAttack)):
            return False
        
        casilla=tablero.verificarOcupacionTrayectoria(origen,destino)

        if casilla is not None and not(self.verificarCasilla(destino,casilla,color,tablero)) and pieza.get_type_movement()=="T":
            return False

        if not(self.simularMovimiento(origen,destino,color,tablero)):
            return False
        
        return True
        

    def verificarPromocion(self,pieza,poscicion):
        y=0 if pieza.get_color()=="B" else 7
        return pieza.getTipo()=="peon" and poscicion[0]==y
    
    def simularMovimiento(self,origen,destino,color,tablero):
        
        estado=tablero.guardarEstado()

        tablero.efectuarMovimiento(origen,destino)

        resultado=self.evaluarJaque(color,tablero)

        tablero.restaurarEstado(estado)

        if resultado is not None:
            return True
        
        return False

    
    def getAtacantesY(self,tablero,casilla,color):

        dy1=casilla[0]
        dy2=7-casilla[0]

        distanciaVertical=[dy1,dy2]

        direcciones=[-1,1]

        atacantes=[]


        for distancia, direccion in zip(distanciaVertical,direcciones):

            resul=tablero.verificarOcupacionTrayectoria(casilla,(casilla[0]+(direccion*distancia),casilla[1]))
            
            if (resul is not None and
                 not(tablero.get_pieza(resul).get_color()==color)
                 and tablero.get_pieza(resul).validarMov(resul,casilla)):
                
                atacantes.append(resul)
        
        return atacantes
    
    def getAtacantesDiag(self,tablero,casilla,color):

        dx1=casilla[1]
        dx2=7 - casilla[1]
        dy1=casilla[0]
        dy2=7-casilla[0]

        vectoresDiagonales=[(-1,-1),(1,-1),(-1,1),(1,1)]

        incrementos=[
            min(dx1,dy1),
            min(dx1,dy2),
            min(dx2,dy1),
            min(dx2,dy2),
        ]

        atacantes=[]

        for (dey,dex),incremento in zip(vectoresDiagonales,incrementos):
            resul=tablero.verificarOcupacionTrayectoria(casilla,(casilla[0]+(dey*incremento),casilla[1]+(dex*incremento)))

            if (resul is not None and
                 not(tablero.get_pieza(resul).get_color()==color)
                 and tablero.get_pieza(resul).validarMov(resul,casilla)):
                
                atacantes.append(resul)

        return atacantes
    
    def getAtacantesCab(self,tablero,casilla,color):

        desplazamientosCaballo=[(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]

        poscicionesCaballo=[(casilla[0]+dy,casilla[1]+dx)
                            for dy, dx in desplazamientosCaballo
                            if 0<=casilla[0]+dy<=7 and 0<=casilla[1]+dx<=7]
        
        atacantes=[]

        for pos in poscicionesCaballo:
                
            pieza=tablero.get_pieza(pos)
            if  (pieza is not None and
                 not(pieza.get_color()==color)
                 and pieza.validarMov(casilla,pos)):
                
                atacantes.append(pos)

        return atacantes
    
    
    def evaluarAtaque(self,tablero,poscicion,color):

        list1=self.getAtacantesX(tablero,poscicion,color)
        list2=self.getAtacantesY(tablero,poscicion,color)
        list3=self.getAtacantesDiag(tablero,poscicion,color)
        list4=self.getAtacantesCab(tablero,poscicion,color)
        
        return list1+list2+list3+list4
    
    def evaluarJaque(self,color,tablero):
        posRey=tablero.get_rey_poscicion(color)


        atacantes=self.evaluarAtaque(tablero,posRey,color)

        return atacantes

    
    def evaluarJaqueMate(self,tablero,atacantes,color):

        poscicion=tablero.get_rey_poscicion(color)
        
        if len(atacantes)==1:

            if len(self.evaluarAtaque(tablero,(atacantes[0][1],atacantes[0][0]),tablero.get_pieza(atacantes[0]).get_color()))!=0:
                return False
            
            if tablero.get_pieza(atacantes[0]).get_type_movement()!="NT":
                
                casillasIntermedias=tablero.get_casillas_intermedias(poscicion,atacantes[0])

                for casilla in casillasIntermedias:

                    if (self.evaluarAtaque(tablero,casilla,tablero.get_pieza(atacantes[0]).get_color())) > 0:
                        return False

        
        desplazamientosRey=((0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1))

        poscicionesPosibles=[(poscicion[0]+dy,poscicion[1]+dx)
                             for dy,dx in desplazamientosRey
                             if 0<=poscicion[0]+dy<=7 and 0<=poscicion[1]+dx<=7]
        
        for posciciones in poscicionesPosibles:

            if ((tablero.get_pieza(posciciones) is None or
                tablero.get_pieza(posciciones).get_color()!=color) and
                self.evaluarAtaque(tablero,posciciones,color))==0:

                return False
            
        return True


            
        