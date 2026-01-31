
class Translator:

    @staticmethod
    def translateMove(Move:tuple):

        origin,destiny,type=Move

        for i in range(64):

            auxBitboard=1<<i

            if auxBitboard & origin:
                break

        colOrigin=i%8
        rowOrigin=i//8

        for i in range(64):

            auxBitboard=1<<i

            if auxBitboard & destiny:
                break

        colDestiny=i%8
        rowDestiny=i//8

        return ((rowOrigin,colOrigin),(rowDestiny,colDestiny))