import re
import Tablero

class Jugador:

    def __init__(self,color,nombre):
        self.nombre=nombre
        self.color=color
    
    def get_nombre(self):
        return self.nombre
    
    def get_color(self):
        return self.color
    
    def get_type(self):
        return "Human"
    
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

    def __init__(self, color,enemyColor,height):
        self.color=color
        self.enemyColor=enemyColor
        self.MaxTreeHeight=height
        self.BestMove=0
        self.BestScore=0

    def get_type(self):
        return "BOT"
        
    def make_Choice_Promocion(self):
        return "REINA"
    
    def generateBitBoards(self,Board:list):
        IDX_BLACK=13
        IDX_WHITE=6
        IDX_OCCUPIED=14
        

        BitBoards=[0 for i in range (15)]
        ColorDictionary={
            "W":7,
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
    
    def generateIndividualBitboard(self,GlobalBitboard):

        IndividualBitBoards=[]

        for i in range(64):

            

            mask=1<<i

            if mask & GlobalBitboard:
                IndividualBitBoards.append(mask)
        
        return IndividualBitBoards
    
    def LegalPawnMovements(self,Bitboards,color):

        legalMovements=[]

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        colorDictionary={
            "B":0,
            "W":7
        }

        pseudo_legal_Movements=self.GeneratePseudoLegalMovementsPawn(Bitboards[PieceDictionary["P"] + colorDictionary[color]],
                                                                Bitboards[IDX_WHITE_BITBOARD],
                                                                Bitboards[IDX_BLACK_BITBOARD],
                                                                color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.evaluarJaque(Bitboards,color):

                legalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return legalMovements

    def GeneratePseudoLegalMovementsPawn(self,BitBoard,BitBoardOccupied_White,BitBoardOcuppied_Black,color):

        LegalMovements=[]

        MaskA = 0xFEFEFEFEFEFEFEFE 
        MaskH = 0x7F7F7F7F7F7F7F7F

        if color=="W":

            
            row2=0b11111111<<8

            Movement1=(BitBoard<<8) & (~(BitBoardOccupied_White | BitBoardOcuppied_Black))
            Movement2=((BitBoard&row2)<<16) & (~(BitBoardOccupied_White | BitBoardOcuppied_Black))
            attack1=((BitBoard&MaskH)<<9)&BitBoardOcuppied_Black
            attack2=((BitBoard&MaskA)<<7)&BitBoardOcuppied_Black

            allDestinies= Movement1 | Movement2 | attack1 | attack2


            while allDestinies:

                to_pos= allDestinies & -allDestinies
                allDestinies &= (allDestinies-1)


                from_pos_mov1=to_pos>>8
                from_pos_mov2=to_pos>>16
                from_pos_at1=to_pos>>9
                from_pos_at2=to_pos>>7

                if (to_pos & Movement1) and (from_pos_mov1 & BitBoard):
                    LegalMovements.append((from_pos_mov1,to_pos,"P"))

                if (to_pos & Movement2) and (from_pos_mov2 & BitBoard):
                    LegalMovements.append((from_pos_mov2,to_pos,"P"))

                if (to_pos & attack1) and (from_pos_at1 &BitBoard):
                    LegalMovements.append((from_pos_at1,to_pos,"P"))
                
                if (to_pos & attack2) and (from_pos_at2 &BitBoard):
                    LegalMovements.append((from_pos_at2,to_pos,"P"))
        
            return LegalMovements


        else:
            

            row7=0b11111111<<48

            Movement1=(BitBoard>>8) & (~(BitBoardOccupied_White | BitBoardOcuppied_Black))
            Movement2=((BitBoard&row7)>>16) & (~(BitBoardOccupied_White | BitBoardOcuppied_Black))
            attack1=((BitBoard&MaskH)>>9)&BitBoardOccupied_White
            attack2=((BitBoard&MaskA)>>7)&BitBoardOccupied_White

            allDestinies= Movement1 | Movement2 | attack1 | attack2

            

            while allDestinies:
                
                to_pos=allDestinies & -allDestinies
                allDestinies &=(allDestinies-1)

            
                from_pos_mov1=to_pos<<8
                from_pos_mov2=to_pos<<16
                from_pos_at1=to_pos<<9
                from_pos_at2=to_pos<<7

                if (to_pos & Movement1) and (from_pos_mov1 & BitBoard):
                    LegalMovements.append((from_pos_mov1,to_pos,"P"))

                if (to_pos & Movement2) and (from_pos_mov2 & BitBoard):
                    LegalMovements.append((from_pos_mov2,to_pos,"P"))

                if (to_pos & attack1) and (from_pos_at1 &BitBoard):
                    LegalMovements.append((from_pos_at1,to_pos,"P"))
                
                if (to_pos & attack2) and (from_pos_at2 &BitBoard):
                    LegalMovements.append((from_pos_at2,to_pos,"P"))

            return LegalMovements
    
    def LegalTowerMovements(self,Bitboards,color):

        legalMovements=[]

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        colorDictionary={
            "B":0,
            "W":7
        }

        pseudo_legal_Movements=self.GeneratePseudoLegalMovementsTower(Bitboards[PieceDictionary["T"] + colorDictionary[color]],
                                                                Bitboards[IDX_WHITE_BITBOARD],
                                                                Bitboards[IDX_BLACK_BITBOARD],
                                                                color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.evaluarJaque(Bitboards,color):

                legalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return legalMovements

    def GeneratePseudoLegalMovementsTower(self,Bitboard:int,BitboardOccupied_White,BitboardOccupied_Black,color):
        LegalMovements=[]

        ROW_1 = 0b11111111
        ROW_8 = 0xFF00000000000000

        COL_1 = 0x0101010101010101  
        COL_8 = 0x8080808080808080 

        towers=self.generateIndividualBitboard(Bitboard)

        for tower in towers:
            

            verticalMovements=0b0
            horizontalMovements=0b0

            auxBitboard=tower
            while True:
                

                auxBitboard=(auxBitboard & (~(ROW_8)))<<8

                

                if auxBitboard == 0:
                    break

                colition_Allies=auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies=auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break
                
                verticalMovements=verticalMovements | auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=tower
            while True:

                auxBitboard=(auxBitboard & (~(ROW_1)))>>8

                if auxBitboard == 0:
                    break

                colition_Allies=auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies=auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                verticalMovements= verticalMovements | auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=tower
            while True:

                auxBitboard=(auxBitboard & (~(COL_8)))<<1

                if auxBitboard== 0:
                    break

                colition_Allies=auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies=auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                horizontalMovements= horizontalMovements | auxBitboard

                if colition_Enemies:
                    break

            auxBitboard=tower
            while True:
                
                auxBitboard=(auxBitboard & (~(COL_1)))>>1

                if auxBitboard == 0:
                    break

                colition_Allies=auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies=auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                horizontalMovements= horizontalMovements | auxBitboard

                if colition_Enemies:
                    break

            PosibleMovements= horizontalMovements | verticalMovements

            while PosibleMovements:

                to_pos= PosibleMovements & -PosibleMovements
                PosibleMovements &= (PosibleMovements-1)
                
                LegalMovements.append((tower,to_pos,"T"))
        
        return LegalMovements
    
    def LegalBishopMovements(self,Bitboards,color):

        legalMovements=[]

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        colorDictionary={
            "B":0,
            "W":7
        }

        pseudo_legal_Movements=self.generatePseudoLegalMovementsBishop(Bitboards[PieceDictionary["B"] + colorDictionary[color]],
                                                                    Bitboards[IDX_WHITE_BITBOARD],
                                                                    Bitboards[IDX_BLACK_BITBOARD],
                                                                    color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.evaluarJaque(Bitboards,color):

                legalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return legalMovements
    
    def generatePseudoLegalMovementsBishop(self,Bitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):
        LegalMovements=[]

        ROW_1 = 0b11111111
        ROW_8 = ROW_1<<56

        COL_1 = 0x0101010101010101  
        COL_8 = 0x8080808080808080

        Bishops=self.generateIndividualBitboard(Bitboard)

        for bishop in Bishops:

            Diag1=0b0
            Diag2=0b0

            auxBitboard=bishop
            while True:
                
                
                auxBitboard = (auxBitboard & (~(COL_8)) & (~(ROW_8)))<<9 

                if auxBitboard == 0:
                    break

                colition_Allies= auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies= auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                Diag1 |= auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=bishop
            while True:
                

                auxBitboard = (auxBitboard & (~(COL_1)) & (~(ROW_1)))>>9 

                

                if auxBitboard == 0:
                    break

                colition_Allies= auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies= auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break
                
                Diag1 |= auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=bishop
            while True:
                

                auxBitboard = (auxBitboard & (~(COL_1)) & (~(ROW_8)))<<7

                

                if auxBitboard == 0:
                    break
            
                colition_Allies= auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies= auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                Diag2 |= auxBitboard

                if colition_Enemies:
                    break
            
            auxBitboard=bishop
            while True:

                

                auxBitboard = (auxBitboard & (~(COL_8)) & (~(ROW_1)))>>7

                

                if auxBitboard == 0:
                    break

                colition_Allies= auxBitboard & (BitboardOccupied_White if color=="W" else BitboardOccupied_Black)
                colition_Enemies= auxBitboard & (BitboardOccupied_Black if color=="W" else BitboardOccupied_White)

                if colition_Allies:
                    break

                Diag2 |= auxBitboard

                if colition_Enemies:
                    break
            
            PosibleMovements= Diag1 | Diag2
            
            while PosibleMovements:

                to_pos=PosibleMovements & (-PosibleMovements)
                PosibleMovements &= (PosibleMovements - 1)

                LegalMovements.append((bishop,to_pos,"B"))
        
        return LegalMovements
    
    def LegalHorseMovements(self,Bitboards,color):

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        colorDictionary={
            "B":0,
            "W":7
        }

        LegalMovements=[]

        pseudo_Legal_movements=self.generatePseudoLegalMovementsHorse(Bitboards[PieceDictionary["H"]+colorDictionary[color]],
                                                                      Bitboards[IDX_WHITE_BITBOARD],
                                                                      Bitboards[IDX_BLACK_BITBOARD],
                                                                      color)

        for move in pseudo_Legal_movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.evaluarJaque(Bitboards,color):
                LegalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return LegalMovements

    def generatePseudoLegalMovementsHorse(self,Bitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):
        LegalMovements=[]

        Horses=self.generateIndividualBitboard(Bitboard)

        ROW_1 = 0b11111111
        ROW_8 = ROW_1<<56

        COL_1 = 0x0101010101010101 
        COL_8 = 0x8080808080808080

        ROW_1_2 = 0x000000000000FFFF
        ROW_8_7 = 0xFFFF000000000000

        COL_1_2 = 0x0303030303030303 
        COL_8_7 = 0xC0C0C0C0C0C0C0C0
        
        for horse in Horses:

            Movement1=((horse & (~(COL_8)) & (~(ROW_8_7)))<<17) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement2=((horse & (~(COL_1)) & (~(ROW_8_7)))<<15) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement3=((horse & (~(COL_1)) & (~(ROW_1_2)))>>17) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement4=((horse & (~(COL_8)) & (~(ROW_1_2)))>>15) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement5=((horse & (~(COL_8_7)) & (~(ROW_8)))<<10) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White)) 
            Movement6=((horse & (~(COL_1_2)) & (~(ROW_8)))<<6)  & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement7=((horse & (~(COL_1_2)) & (~(ROW_1)))>>10) & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            Movement8=((horse & (~(COL_8_7)) & (~(ROW_1)))>>6)  & (~(BitboardOccupied_Black if color=="B" else BitboardOccupied_White))
            
            allMovements= Movement1 | Movement2 | Movement3 | Movement4 | Movement5 | Movement6 | Movement7 | Movement8

            while allMovements:
                    
                to_pos= allMovements & -allMovements
                allMovements &= (allMovements - 1)
                LegalMovements.append((horse,to_pos,"H"))

                
            
        return LegalMovements
    
    def LegalQueenMovements(self,Bitboards,color):

        legalMovements=[]

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        colorDictionary={
            "B":0,
            "W":7
        }

        pseudo_legal_Movements=self.generatePseudoLegalMovementsQueen(Bitboards[PieceDictionary["Q"] + colorDictionary[color]],
                                                                    Bitboards[IDX_WHITE_BITBOARD],
                                                                    Bitboards[IDX_BLACK_BITBOARD],
                                                                    color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.evaluarJaque(Bitboards,color):

                legalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return legalMovements


    def generatePseudoLegalMovementsQueen(self,Bitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):

        LegalMovements=[]

        BishopMovements=self.generatePseudoLegalMovementsBishop(Bitboard,BitboardOccupied_White,BitboardOccupied_Black,color)
        TowerMovements=self.GeneratePseudoLegalMovementsTower(Bitboard,BitboardOccupied_White,BitboardOccupied_Black,color)

        LegalMovements=BishopMovements + TowerMovements

        for idx,mov in enumerate(LegalMovements):
            LegalMovements[idx]=(mov[0],mov[1],"Q")

        return LegalMovements
    
    def LegalKingMovements(self,Bitboards,color):

        legalMovements=[]

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        colorDictionary={
            "B":0,
            "W":7
        }

        pseudo_legal_Movements=self.generatePseudoLegalMovementsKing(Bitboards[PieceDictionary["K"] + colorDictionary[color]],
                                                                    Bitboards[IDX_WHITE_BITBOARD],
                                                                    Bitboards[IDX_BLACK_BITBOARD],
                                                                    color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.evaluarJaque(Bitboards,color):

                legalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return legalMovements
    
    def generatePseudoLegalMovementsKing(self,Bitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):

        LegalMovements=[]

        ROW_1 = 0b11111111
        ROW_8 = ROW_1<<56

        COL_1 = 0x0101010101010101  
        COL_8 = 0x8080808080808080

        Movement1=((Bitboard & (~(ROW_8)))<<8) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement2=((Bitboard & (~(ROW_1)))>>8) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement3=((Bitboard & (~(COL_8)))<<1) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement4=((Bitboard & (~(COL_1)))>>1) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement5=((Bitboard & (~(ROW_8)) & (~(COL_8)))<<9) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement6=((Bitboard & (~(ROW_8)) & (~(COL_1)))<<7) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement7=((Bitboard & (~(ROW_1)) & (~(COL_1)))>>9) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))
        Movement8=((Bitboard & (~(ROW_1)) & (~(COL_8)))>>7) & (~(BitboardOccupied_White if color=="W" else BitboardOccupied_Black))

        allMovements= Movement1 | Movement2 | Movement3 | Movement4 | Movement5 | Movement6 | Movement7 | Movement8

        while allMovements:

            to_pos=allMovements & -allMovements
            allMovements &= (allMovements-1)

            LegalMovements.append((Bitboard,to_pos,"K"))

        return LegalMovements        

        
    def make_move_on_Bitboard(self,Bitboards,movement,color):

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        captured=None

        startallie=0 if color=="B" else 7
        startenemie=7 if color=="B" else 0
        globalBitboardallie=IDX_WHITE_BITBOARD if color=="W" else IDX_BLACK_BITBOARD
        globalBitboardenemie=IDX_BLACK_BITBOARD if color=="B" else IDX_WHITE_BITBOARD

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        for i in range(startenemie,startenemie+6):

            if Bitboards[i] & movement[1]:

                captured=(Bitboards[1],i)
                Bitboards[i] &= ~(movement[1])
                Bitboards[globalBitboardenemie] &= ~(movement[1])
                break

        Bitboards[PieceDictionary[movement[2]]+startallie] &= ~(movement[0])
        Bitboards[PieceDictionary[movement[2]]+startallie] |=  (movement[1])

        Bitboards[globalBitboardallie] &= ~(movement[0])
        Bitboards[globalBitboardallie] |= (movement[1])

        
        
        return captured
        
    def unmake_move(self,Bitboards,move,captured_bitboard,color):

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        startallie=0 if color=="B" else 7

        globalBitboardallie=IDX_WHITE_BITBOARD if color=="W" else IDX_BLACK_BITBOARD
        globalBitboardenemie=IDX_BLACK_BITBOARD if color=="B" else IDX_WHITE_BITBOARD

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        if captured_bitboard is not None:

            Bitboards[captured_bitboard[1]] |= captured_bitboard[0]
            Bitboards[globalBitboardenemie] |= captured_bitboard[0]
        
        Bitboards[PieceDictionary[move[2]]+startallie] &= ~(move[1])
        Bitboards[PieceDictionary[move[2]]+startallie] |=  (move[0])

        Bitboards[globalBitboardallie] &= ~(move[1])
        Bitboards[globalBitboardallie] |= (move[0])



    def evaluarJaque(self,Bitboards,color):

        ROW_1_2 = 0x000000000000FFFF
        ROW_8_7 = 0xFFFF000000000000

        COL_1_2 = 0x0303030303030303 
        COL_8_7 = 0xC0C0C0C0C0C0C0C0

        MaskA = 0xFEFEFEFEFEFEFEFE 
        MaskH = 0x7F7F7F7F7F7F7F7F

        
        kingBitboard=Bitboards[0 if color=="B" else 7]
        enemyHorses=Bitboards[11 if color=="B" else 4]
        enemyPawns=Bitboards[8 if color=="B" else 1]
        enemyTowers=Bitboards[9 if color=="B" else 2]
        enemyQueen=Bitboards[12 if color=="B" else 5]
        enemyBishops=Bitboards[10 if color=="B" else 3]
        enemyKing=Bitboards[7 if color=="B" else 0]


        PossibleHorses=(((kingBitboard & (~(COL_8_7)) & (~(ROW_8_7)))<<17) | 
                        ((kingBitboard & (~(COL_1_2)) & (~(ROW_8_7)))<<15) | 
                        ((kingBitboard & (~(COL_1_2)) & (~(ROW_1_2)))>>17) | 
                        ((kingBitboard & (~(COL_8_7)) & (~(ROW_1_2)))>>15) |
                        ((kingBitboard & (~(COL_1_2)) & (~(ROW_1_2)))<<10) |
                        ((kingBitboard & (~(COL_8_7)) & (~(ROW_1_2)))<<6)  |
                        ((kingBitboard & (~(COL_8_7)) & (~(ROW_8_7)))>>10) |
                        ((kingBitboard & (~(COL_1_2)) & (~(ROW_8_7)))>>6))
        
        if PossibleHorses & enemyHorses:
            return False
        
        Vray1=self.generateVerticalRay(Bitboards,kingBitboard,dy=1)
        Vray2=self.generateVerticalRay(Bitboards,kingBitboard,dy=(-1))
        
        if (Vray1 | Vray2) & (enemyQueen | enemyTowers | enemyKing):
            return False
        
        diagRay1=self.generateDiagonalRay(Bitboards,kingBitboard,dx=1,dy=1)

        if diagRay1 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False
        
        diagRay2=self.generateDiagonalRay(Bitboards,kingBitboard,dx=1,dy=(-1))

        if diagRay2 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False        
        
        diagRay3=self.generateDiagonalRay(Bitboards,kingBitboard,dx=(-1),dy=1)

        if diagRay3 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False
        
        diagRay4=self.generateDiagonalRay(Bitboards,kingBitboard,dx=(-1),dy=(-1))

        if diagRay4 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False


        return True
        

        



    def generateVerticalRay(self,Bitboards,position,dy):
        ROW_1 = 0b11111111
        ROW_8 = ROW_1<<56

        GlobalOcupiedBitboard=Bitboards[14]

        ray=0
        
        while True:

            position= ((position & (~(ROW_8)))<<8) if dy>0 else ((position & (~(ROW_1)))>>8)
            
            if position==0:
                break

            ray |= position

            if (position & GlobalOcupiedBitboard):
                break
        
        return ray
    
    def generateHorizontalRay(self,Bitboards,position,dx):
        COL_1 = 0x0101010101010101  
        COL_8 = 0x8080808080808080

        GlobalOcupiedBitboard=Bitboards[14]

        ray=0

        while True:
            
            position= ((position & (~(COL_8)) )<<1) if dx>0 else ((position & (~(COL_1)))>>1)

            if position==0:
                break

            ray |= position

            if position & GlobalOcupiedBitboard:
                break
        
        return ray
    
    def generateDiagonalRay(self,Bitboards,position,dx,dy):
        COL_1 = 0x0101010101010101  
        COL_8 = 0x8080808080808080

        ROW_1 = 0b11111111
        ROW_8 = ROW_1<<56

        GlobalOcupiedBitboard=Bitboards[14]

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


    def alpha_Beta(self,height,Bitboards,alpha,beta):

        if height==0:

            self.BestMove=0
            self.BestValue=-10**9

        if height==self.MaxTreeHeight:
            return self.puntuarTablero(Bitboards,height)

        LegalMovesPawn=self.LegalPawnMovements(Bitboards,self.color if (height%2)==0 else self.enemyColor)
        
        LegalMovesQueen=self.LegalQueenMovements(Bitboards,self.color if (height%2)==0 else self.enemyColor)
        
        LegalMovesBishop=self.LegalBishopMovements(Bitboards,self.color if (height%2)==0 else self.enemyColor)
        
        LegalMovesTower=self.LegalTowerMovements(Bitboards,self.color if (height%2)==0 else self.enemyColor)
        
        LegalMovesKing=self.LegalKingMovements(Bitboards,self.color if (height%2)==0 else self.enemyColor)
        
        LegalMovesHorse=self.LegalHorseMovements(Bitboards,self.color if (height%2)==0 else self.enemyColor)

        allLegalMoves=LegalMovesQueen+LegalMovesBishop+LegalMovesHorse+LegalMovesKing+LegalMovesPawn+LegalMovesTower

        currentColor=self.color if (height%2)==0 else self.enemyColor

        if len(allLegalMoves)==0:

            if not(self.evaluarJaque(Bitboards,currentColor)):

                points=(10**9 - height) if height%2==0 else ((-10)**9 + height)
            else:

                points=0

            return points 

        if (height%2)==0:

            for Move in allLegalMoves:

                capture=self.make_move_on_Bitboard(Bitboards,Move,currentColor)

                alpha=max(alpha,self.alpha_Beta(height+1,Bitboards,alpha,beta))

                self.unmake_move(Bitboards,Move,capture,currentColor)

                if height==0 and alpha>self.BestValue:
                    self.BestValue=alpha
                    self.BestMove=Move

                if beta<=alpha:
                    break
            
            return alpha

        else:      
            
            for Move in allLegalMoves:

                capture=self.make_move_on_Bitboard(Bitboards,Move,currentColor)
                
                beta=min(beta,self.alpha_Beta(height+1,Bitboards,alpha,beta))

                self.unmake_move(Bitboards,Move,capture,currentColor)
                if beta>=alpha:
                    break

            return beta
        

    def puntuarTablero(self,Bitboards,height):

        ValueDictionary={
            "K":0,
            "P":100,
            "T":500,
            "B":330,
            "H":320,
            "Q":900

        }

        PieceDictionary={
            "K":0,
            "P":1,
            "T":2,
            "B":3,
            "H":4,
            "Q":5
        }

        startDict={
            "B":0,
            "W":7,
        }


        materialPointsSelf=0
        materialPointsSelf += Bitboards[PieceDictionary["K"] + startDict[self.color]].bit_count() * ValueDictionary["K"]
        materialPointsSelf += Bitboards[PieceDictionary["P"] + startDict[self.color]].bit_count() * ValueDictionary["P"]
        materialPointsSelf += Bitboards[PieceDictionary["T"] + startDict[self.color]].bit_count() * ValueDictionary["T"]
        materialPointsSelf += Bitboards[PieceDictionary["B"] + startDict[self.color]].bit_count() * ValueDictionary["B"]
        materialPointsSelf += Bitboards[PieceDictionary["H"] + startDict[self.color]].bit_count() * ValueDictionary["H"]
        materialPointsSelf += Bitboards[PieceDictionary["Q"] + startDict[self.color]].bit_count() * ValueDictionary["Q"]

        materialPointsEnemy=0
        materialPointsEnemy += Bitboards[PieceDictionary["K"] + startDict[self.enemyColor]].bit_count() * ValueDictionary["K"]
        materialPointsEnemy += Bitboards[PieceDictionary["P"] + startDict[self.enemyColor]].bit_count() * ValueDictionary["P"]
        materialPointsEnemy += Bitboards[PieceDictionary["T"] + startDict[self.enemyColor]].bit_count() * ValueDictionary["T"]
        materialPointsEnemy += Bitboards[PieceDictionary["B"] + startDict[self.enemyColor]].bit_count() * ValueDictionary["B"]
        materialPointsEnemy += Bitboards[PieceDictionary["H"] + startDict[self.enemyColor]].bit_count() * ValueDictionary["H"]
        materialPointsEnemy += Bitboards[PieceDictionary["Q"] + startDict[self.enemyColor]].bit_count() * ValueDictionary["Q"]

        materialPoints= materialPointsSelf - materialPointsEnemy

        checkKingSelf=(-200) if self.evaluarJaque(Bitboards,self.color) else 0
        checkKingEnemy=(150) if self.evaluarJaque(Bitboards,self.enemyColor) else 0

        selfPawns=Bitboards[PieceDictionary["P"] + startDict[self.color]]

        promotionPoints=0

        while selfPawns and promotionPoints<1800:
            
            pawn= selfPawns & -selfPawns
            selfPawns &=(selfPawns-1)

            promotionPoints+=self.evaluarPromocionPosible(pawn,Bitboards[startDict[self.enemyColor] + 6])

        totalPoints=materialPoints + checkKingEnemy + checkKingSelf + promotionPoints

        return totalPoints



    def translateMove(self,Move:tuple):

        origin,destiny,type=Move

        colOrigin=origin%255
        rowOrigin=0

        colDestiny=destiny%255
        rowDestiny=0

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





    
    def make_choice(self,PoscicionesTablero):
        bitBoards=self.generateBitBoards(PoscicionesTablero)

        self.alpha_Beta(0,bitBoards,-10**9,10**9)

        return self.translateMove(self.BestMove)

    def evaluarPromocionPosible(self,Pawn,occupiedBitboard):

        ROW_8 = (0b11111111)<<56
        ROW_1 = 0b11111111

        distance=7

        while True:

            Pawn = (Pawn<<8) if self.color=="B" else (Pawn>>8)

            if Pawn & ((ROW_8) if self.color=="B" else (ROW_1)):
                distance=1
                break

            if Pawn & (~(occupiedBitboard)):
                distance-=1
            else:
                distance+=2
                break
                
        
        points=900/(distance)

        return points
        



        
        


        