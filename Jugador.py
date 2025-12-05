import re
import Tablero
import Tree

class Jugador:

    def __init__(self,color,nombre):
        self.nombre=nombre
        self.color=color
    
    def get_nombre(self):
        return self.nombre
    
    def get_color(self):
        return self.color
    
    def make_choice(self):
        patron=r"^\((\d),(\d)\)$"

        while True:
            origen=input("ingresar coordenada de origen en la forma '(Y,X)':")
            match=re.match(patron,origen)
            if(match):
                origen=(int(match.group(1)),int(match.group(2)))
                break

        while True:
            destino=input("ingresar coordenada de destino en la forma '(Y,X)':")
            match=re.match(patron,destino)
            if(match):
                destino=(int(match.group(1)),int(match.group(2)))
                break
        
        return origen,destino
    
    def make_Choice_Promocion(self):
        tipoPieza=["TORRE","ALFIL","REINA","CABALLO"]

        while True:
            eleccion=input("Ingrese que pieza desea obtener por promocion:").upper()
            if eleccion in tipoPieza:
                break

        return eleccion
    
class JugadorPc(Jugador):

    def __init__(self, color):
        self.color=color
        
    
    def generateBitBoards(self,Board:list):
        IDX_BLACK=13
        IDX_WHITE=12
        IDX_OCCUPIED=14
        

        BitBoards=[0 for i in range (15)]
        ColorDictionary={
            "W":6,
            "B":0
        }

        PieceDictionary={
            "rey":0,
            "peon":1,
            "torre":2,
            "alfil":3,
            "caballo":4,
            "reina":5

        }


        for i in range(8):
            for j in range(8):

                piece=Board[i][j]

                if piece is None:
                    continue

                mascara=1<<(i*8)+j

                BitBoards[ColorDictionary[piece.get_color()]+PieceDictionary[piece.getTipo()]]= BitBoards[ColorDictionary[piece.get_color()]+PieceDictionary[piece.getTipo()]] | mascara
                BitBoards[IDX_WHITE if piece.get_color()=="W" else IDX_BLACK]=BitBoards[IDX_WHITE if piece.get_color()=="W" else IDX_BLACK] | mascara
            
        BitBoards[IDX_OCCUPIED]=BitBoards[IDX_WHITE]|BitBoards[IDX_BLACK]

        return BitBoards