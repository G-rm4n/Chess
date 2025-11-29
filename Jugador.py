import re

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
        




