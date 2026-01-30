import Pieza
import Jugador

class Movement:

    def __init__(self,origin,destiny,isCapture):
        self.origin=origin
        self.destiny=destiny
        self.isCaptura=isCapture
        self.capturedPiece=Pieza.Piece
        self.Jugador=Jugador.Player
    
    def get_origin(self):
        return self.origin

    def get_destiny(self):
        return self.destiny
    
    def get_isCapture(self):
        return self.isCaptura
    
    
    def set_capture(self,p_captured=Pieza):
        self.capturedPiece=p_captured
        return self.capturedPiece
    
    def get_player(self):
        return self.Player
    
     