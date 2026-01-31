from abc import ABC, abstractclassmethod

class Piece(ABC):

    def __init__(self,color,id):
        self.color=color
        self.cant_Mov=0
        self.estado=True
        self.id=id

    def get_color(self):
        return self.color
    
    def change_status(self):
        self.estado=not(self.estado)

    def get_status(self):
        return self.estado
    
    def incr_mov(self):
        self.cant_Mov+=1
    
    def get_cant_mov(self):
        return self.cant_Mov
    
    def get_id(self):
        return self.id
    
    def get_type_movement(self):
        return "T"
    
    @abstractclassmethod
    def validateMovement(self):
        raise NotImplementedError("not implemented")
    
    @abstractclassmethod
    def getType(self):
        raise NotImplementedError("Not implemented")
    
class Pawn(Piece):

    def validateMovement(self,origin,destiny,isAttack=bool):
        dy=destiny[0]-origin[0]
        dx=destiny[1]-origin[1]
        
        displacement= 1 if self.color=="W" else -1


        if(isAttack):

            return (abs(dx)==1 and dy==displacement) 
        else:

            if(dx)!=0:
                return False
            
            incremento=2 if self.cant_Mov==0 else 1

            return dy==displacement or dy==displacement*incremento
    
    def getType(self):
        return "PAWN"
                

class Tower(Piece):

    def validateMovement(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return dy==0 or dx==0
    
    def getType(self):
        return "TOWER"

class Bishop(Piece):

    def validateMovement(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return dy==dx
    
    def getType(self):
        return "BISHOP"

class King(Piece):

    def validateMovement(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return dx==1 or dy==1
    
    def getType(self):
        return "KING"
    
class Horse(Piece):

    def get_type_movement(self):
        return "NT"

    def validateMovement(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return ((dx==2 and dy==1) or (dx==1 and dy==2))
    
    def getType(self):
        return "HORSE"

class Queen(Piece):

    def validateMovement(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return dx==0 or dy==0 or dx==dy
    
    def getType(self):
        return "QUEEN"
