from AI_Engine.constants import ROW_1,ROW_8,IDX_OCCUPIED,COL_1,COL_8
class RayGenerator:

    @staticmethod
    def GenerateVerticalRay(Bitboards,position,dy):

        GlobalOcupiedBitboard=Bitboards[IDX_OCCUPIED]

        ray=0
        
        while True:

            position= ((position & (~(ROW_8)))<<8) if dy>0 else ((position & (~(ROW_1)))>>8)
            
            if position==0:
                break

            ray |= position

            if (position & GlobalOcupiedBitboard):
                break
        
        return ray
    
    @staticmethod
    def GenerateHorizontalRay(Bitboards,position,dx):

        GlobalOcupiedBitboard=Bitboards[IDX_OCCUPIED]

        ray=0

        while True:
            
            position= ((position & (~(COL_8)) )<<1) if dx>0 else ((position & (~(COL_1)))>>1)

            if position==0:
                break

            ray |= position

            if position & GlobalOcupiedBitboard:
                break
        
        return ray
    
    @staticmethod
    def GenerateDiagonalRay(Bitboards,position,dx,dy):

        GlobalOcupiedBitboard=Bitboards[IDX_OCCUPIED]

        ray=0

        while True:

            position= ((position & (~(ROW_8)))<<8) if dy>0 else ((position & (~(ROW_1)))>>8)
            position= ((position & (~(COL_8)) )<<1) if dx>0 else ((position & (~(COL_1)))>>1)

            if position==0:
                break

            ray |= position

            if position & GlobalOcupiedBitboard:
                break
        
        return ray