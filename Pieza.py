from abc import ABC, abstractclassmethod

class Pieza(ABC):

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
    def validarMov(self):
        raise NotImplementedError("not implemented")
    
    @abstractclassmethod
    def getTipo(self):
        raise NotImplementedError("Not implemented")
    
class Peon(Pieza):

    def validarMov(self,origin,destiny,isAttack=bool):
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
    
    def getTipo(self):
        return "peon"
                

class Torre(Pieza):

    def validarMov(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return dy==0 or dx==0
    
    def getTipo(self):
        return "torre"

class Alfil(Pieza):

    def validarMov(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return dy==dx
    
    def getTipo(self):
        return "alfil"

class Rey(Pieza):

    def validarMov(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return dx==1 or dy==1
    
    def getTipo(self):
        return "rey"
    
class Caballo(Pieza):

    def get_type_movement(self):
        return "NT"

    def validarMov(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return ((dx==2 and dy==1) or (dx==1 and dy==2))
    
    def getTipo(self):
        return "caballo"

class reina(Pieza):

    def validarMov(self,origin,destiny,isAttack=bool):
        dy=abs(destiny[0]-origin[0])
        dx=abs(destiny[1]-origin[1])
        return dx==0 or dy==0 or dx==dy
    
    def getTipo(self):
        return "reina"
