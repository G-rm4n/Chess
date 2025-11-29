import Pieza
import Jugador

class Movimiento:

    def __init__(self,origin,destiny,isCapture):
        self.origen=origin
        self.destino=destiny
        self.isCaptura=isCapture
        self.piezaCapturada=Pieza.Pieza
        self.Jugador=Jugador
    
    def get_origin(self):
        return self.origen

    def get_destiny(self):
        return self.destino
    
    def get_isCapture(self):
        return self.isCaptura
    
    
    def set_capture(self,p_captured=Pieza):
        self.piezaCapturada=p_captured
        return self.piezaCapturada
    
    def get_player(self):
        return self.jugador
    
     