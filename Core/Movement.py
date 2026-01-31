import Core.Piece as Piece


class Movement:

    def __init__(self,origin,destiny,isCapture):
        self.origin=origin
        self.destiny=destiny
        self.isCaptura=isCapture
        self.capturedPiece=Piece.Piece
    
    def get_origin(self):
        return self.origin

    def get_destiny(self):
        return self.destiny
    
    def get_isCapture(self):
        return self.isCaptura
    
    
    def set_capture(self,p_captured=Piece):
        self.capturedPiece=p_captured
        return self.capturedPiece
    
    def get_player(self):
        return self.Player
    
     