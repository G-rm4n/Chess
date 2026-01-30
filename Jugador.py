import re
import Tablero
from constants import *

class Player:

    def __init__(self,color,name):
        self.name=name
        self.color=color
    
    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color
    
    def get_type(self):
        return "Human"
    
    def make_choice(self):
        patron=r"^\((\d),(\d)\)$"

        while True:
            origin=input("ingresar coordenada de origen en la forma '(Y,X)':")
            match=re.match(patron,origin)
            if(match):
                origin=(int(match.group(1)),int(match.group(2)))
                break

        while True:
            destiny=input("ingresar coordenada de destino en la forma '(Y,X)':")
            match=re.match(patron,destiny)
            if(match):
                destiny=(int(match.group(1)),int(match.group(2)))
                break
        
        return origin,destiny
    
    def make_Choice_Promotion(self):
        pieceType=["TORRE","ALFIL","REINA","CABALLO"]

        while True:
            choice=input("Ingrese que pieza desea obtener por promocion:").upper()
            if choice in pieceType:
                break

        return choice
    
class BotPlayer(Player):

    def __init__(self, color,enemyColor,height):
        self.color=color
        self.enemyColor=enemyColor
        self.MaxTreeHeight=height
        self.BestMove=0
        self.BestScore=0

    def get_type(self):
        return "BOT"
        
    def make_Choice_Promotion(self):
        return "QUEEN"
    
    def generateBitBoards(self,Board:list):

        IDX_BLACK=13
        IDX_WHITE=6
        IDX_OCCUPIED=14
        

        BitBoards=[0 for i in range (15)]
        

        PieceDictionary={
            
            "KING":0,
            "PAWN":1,
            "TOWER":2,
            "BISHOP":3,
            "HORSE":4,
            "QUEEN":5

        }


        for i in range(8):
            for j in range(8):

                piece=Board[i][j]

                if piece is None:
                    continue

                mask=1<<(i*8)+j

                BitBoards[colorDictionary[piece.get_color()]+PieceDictionary[piece.getType()]]= BitBoards[colorDictionary[piece.get_color()]+PieceDictionary[piece.getType()]] | mask
                BitBoards[IDX_WHITE if piece.get_color()=="W" else IDX_BLACK]=BitBoards[IDX_WHITE if piece.get_color()=="W" else IDX_BLACK] | mask
            
        BitBoards[IDX_OCCUPIED]=BitBoards[IDX_WHITE]|BitBoards[IDX_BLACK]

        return BitBoards
    
    def GenerateIndividualBitboard(self,GlobalBitboard):

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

        

        pseudo_legal_Movements=self.GeneratePseudoLegalMovementsPawn(Bitboards[PieceDictionary["P"] + colorDictionary[color]],
                                                                Bitboards[IDX_WHITE_BITBOARD],
                                                                Bitboards[IDX_BLACK_BITBOARD],
                                                                color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.isKingSafe(Bitboards,color):

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

        

        pseudo_legal_Movements=self.GeneratePseudoLegalMovementsTower(Bitboards[PieceDictionary["T"] + colorDictionary[color]],
                                                                Bitboards[IDX_WHITE_BITBOARD],
                                                                Bitboards[IDX_BLACK_BITBOARD],
                                                                color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.isKingSafe(Bitboards,color):

                legalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return legalMovements

    def GeneratePseudoLegalMovementsTower(self,Bitboard:int,BitboardOccupied_White,BitboardOccupied_Black,color):
        LegalMovements=[]

        ROW_1 = 0b11111111
        ROW_8 = 0xFF00000000000000

        COL_1 = 0x0101010101010101  
        COL_8 = 0x8080808080808080 

        towers=self.GenerateIndividualBitboard(Bitboard)

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

        

        pseudo_legal_Movements=self.GeneratePseudoLegalMovementsBishop(Bitboards[PieceDictionary["B"] + colorDictionary[color]],
                                                                    Bitboards[IDX_WHITE_BITBOARD],
                                                                    Bitboards[IDX_BLACK_BITBOARD],
                                                                    color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.isKingSafe(Bitboards,color):

                legalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return legalMovements
    
    def GeneratePseudoLegalMovementsBishop(self,Bitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):
        LegalMovements=[]

        ROW_1 = 0b11111111
        ROW_8 = ROW_1<<56

        COL_1 = 0x0101010101010101  
        COL_8 = 0x8080808080808080

        Bishops=self.GenerateIndividualBitboard(Bitboard)

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

        

        LegalMovements=[]

        pseudo_Legal_movements=self.GeneratePseudoLegalMovementsHorse(Bitboards[PieceDictionary["H"]+colorDictionary[color]],
                                                                      Bitboards[IDX_WHITE_BITBOARD],
                                                                      Bitboards[IDX_BLACK_BITBOARD],
                                                                      color)

        for move in pseudo_Legal_movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.isKingSafe(Bitboards,color):
                LegalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return LegalMovements

    def GeneratePseudoLegalMovementsHorse(self,Bitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):
        LegalMovements=[]

        Horses=self.GenerateIndividualBitboard(Bitboard)

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

        

        pseudo_legal_Movements=self.GeneratePseudoLegalMovementsQueen(Bitboards[PieceDictionary["Q"] + colorDictionary[color]],
                                                                    Bitboards[IDX_WHITE_BITBOARD],
                                                                    Bitboards[IDX_BLACK_BITBOARD],
                                                                    color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.isKingSafe(Bitboards,color):

                legalMovements.append(move)
            
            self.unmake_move(Bitboards,move,capture,color)
        
        return legalMovements


    def GeneratePseudoLegalMovementsQueen(self,Bitboard:int,BitboardOccupied_White:int,BitboardOccupied_Black,color):

        LegalMovements=[]

        BishopMovements=self.GeneratePseudoLegalMovementsBishop(Bitboard,BitboardOccupied_White,BitboardOccupied_Black,color)
        TowerMovements=self.GeneratePseudoLegalMovementsTower(Bitboard,BitboardOccupied_White,BitboardOccupied_Black,color)

        LegalMovements=BishopMovements + TowerMovements

        for idx,mov in enumerate(LegalMovements):
            LegalMovements[idx]=(mov[0],mov[1],"Q")

        return LegalMovements
    
    def LegalKingMovements(self,Bitboards,color):

        legalMovements=[]

        IDX_WHITE_BITBOARD=6
        IDX_BLACK_BITBOARD=13

        pseudo_legal_Movements=self.generatePseudoLegalMovementsKing(Bitboards[PieceDictionary["K"] + colorDictionary[color]],
                                                                    Bitboards[IDX_WHITE_BITBOARD],
                                                                    Bitboards[IDX_BLACK_BITBOARD],
                                                                    color)
        
        for move in pseudo_legal_Movements:

            capture=self.make_move_on_Bitboard(Bitboards,move,color)

            if self.isKingSafe(Bitboards,color):

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

        startallie=7 if color=="B" else 0
        startenemie=0 if color=="B" else 7
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

        startallie=7 if color=="B" else 0

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



    def isKingSafe(self,Bitboards,color):

        ROW_1_2 = 0x000000000000FFFF
        ROW_8_7 = 0xFFFF000000000000

        COL_1_2 = 0x0303030303030303 
        COL_8_7 = 0xC0C0C0C0C0C0C0C0

        MaskA = 0xFEFEFEFEFEFEFEFE 
        MaskH = 0x7F7F7F7F7F7F7F7F

        
        kingBitboard=Bitboards[0 if color=="W" else 7]
        enemyHorses=Bitboards[11 if color=="W" else 4]
        enemyPawns=Bitboards[8 if color=="W" else 1]
        enemyTowers=Bitboards[9 if color=="W" else 2]
        enemyQueen=Bitboards[12 if color=="W" else 5]
        enemyBishops=Bitboards[10 if color=="W" else 3]
        enemyKing=Bitboards[7 if color=="W" else 0]


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
        
        Vray1=self.GenerateVerticalRay(Bitboards,kingBitboard,dy=1)
        Vray2=self.GenerateVerticalRay(Bitboards,kingBitboard,dy=(-1))
        
        if (Vray1 | Vray2) & (enemyQueen | enemyTowers | enemyKing):
            return False
        
        diagRay1=self.GenerateDiagonalRay(Bitboards,kingBitboard,dx=1,dy=1)

        if diagRay1 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False
        
        diagRay2=self.GenerateDiagonalRay(Bitboards,kingBitboard,dx=1,dy=(-1))

        if diagRay2 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False        
        
        diagRay3=self.GenerateDiagonalRay(Bitboards,kingBitboard,dx=(-1),dy=1)

        if diagRay3 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False
        
        diagRay4=self.GenerateDiagonalRay(Bitboards,kingBitboard,dx=(-1),dy=(-1))

        if diagRay4 &  (enemyPawns | enemyQueen | enemyBishops | enemyKing):
            return False


        return True
        

        



    def GenerateVerticalRay(self,Bitboards,position,dy):
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
    
    def GenerateHorizontalRay(self,Bitboards,position,dx):
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
    
    def GenerateDiagonalRay(self,Bitboards,position,dx,dy):
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
    
    def generatePseudoLegalMovments(self,Bitboards,Color):

        MovementsPawn=self.GeneratePseudoLegalMovementsPawn(Bitboards[PieceDictionary["P"]+colorDictionary[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsQueen=self.GeneratePseudoLegalMovementsQueen(Bitboards[PieceDictionary["Q"]+colorDictionary[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsKing=self.generatePseudoLegalMovementsKing(Bitboards[PieceDictionary["K"]+colorDictionary[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsTower=self.GeneratePseudoLegalMovementsTower(Bitboards[PieceDictionary["T"]+colorDictionary[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsHorse=self.GeneratePseudoLegalMovementsHorse(Bitboards[PieceDictionary["H"]+colorDictionary[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)
        MovementsBishop=self.GeneratePseudoLegalMovementsBishop(Bitboards[PieceDictionary["B"]+colorDictionary[Color]],Bitboards[IDX_WHITE_BITBOARD],Bitboards[IDX_BLACK_BITBOARD],Color)

        return MovementsQueen + MovementsTower + MovementsHorse + MovementsBishop + MovementsPawn + MovementsKing

    def scoreHorsePosition(self,HorseBitboard:int,Color):

        score=0

        score+=((HorseBitboard&MASK_CENTER).bit_count())*20
        
        score+=((HorseBitboard&BORDER_CENTER).bit_count())*15
        
        score+=((HorseBitboard&MASK_CENTER_CORNERS).bit_count())*10

        score-=((HorseBitboard&MASK_SIDE_CROSS).bit_count())*30

        score-=((HorseBitboard&MASK_NEAR_CORNERS).bit_count())*40
        
        score-=((HorseBitboard&MASK_INNER_CORNERS_ADJACENT).bit_count())*20

        score-=((HorseBitboard&MASK_CORNERS).bit_count())*50
        
        return score
    
    def scoreBishopPositions(self,BishopBitboard,color):

        score=0

        MaskAttack=0x8040201008440240 if color=="W" else 0x00420408102040C0

        score+=((BishopBitboard&MaskAttack).bit_count())*15

        score += (BishopBitboard & BORDER_CENTER).bit_count() * 20
        score += (BishopBitboard & MASK_CENTER).bit_count() * 15
        score += (BishopBitboard & MASK_CENTER_CORNERS).bit_count() * 10

        score += (BishopBitboard & MASK_BISHOP_LONG).bit_count() * 15
        score += (BishopBitboard & MASK_BISHOP_MID).bit_count() * 5

        score -= (BishopBitboard & MASK_SIDE_CROSS).bit_count() * 20
        score -= (BishopBitboard & MASK_CORNERS).bit_count() * 40
        score -= (BishopBitboard & MASK_NEAR_CORNERS).bit_count() * 25

        return score

        
    def scoreTowerPositions(self,TowerBitboard,color):

        score=0

        r2= ROW_2 if color=="W" else ROW_7
        r7= ROW_7 if color=="W" else ROW_2
        r8= ROW_8 if color=="W" else ROW_1

        score += ((TowerBitboard&r8).bit_count()) * 15
        score += ((TowerBitboard&r7).bit_count()) * 30
        score += ((TowerBitboard&r2).bit_count()) * 10
        score += ((TowerBitboard&MASK_CENTER).bit_count()) * 10

        score -= ((TowerBitboard&MASK_SIDE_STRIPS_VERTICAL).bit_count()) * 5

        return score
    
    def scoreQueenPositions(self,QueenBitboard,color):

        score=0

        score += ((QueenBitboard&MASK_CENTER).bit_count()) * 10
        score += ((QueenBitboard&BORDER_CENTER&MASK_CENTER_CORNERS).bit_count()) * 5

        score -= ((QueenBitboard&MASK_CORNERS).bit_count()) * 20
        score -= ((QueenBitboard&MASK_SIDE_CROSS).bit_count()) * 15
        score -= ((QueenBitboard&MASK_NEAR_CORNERS).bit_count()) * 10

        return score
    
    def scoreKingPositions(self,KingBitboard,color):

        score=0

        king_safe_zone = 0x00000000000000C6 if color=="W" else 0xC600000000000000
    
        score += (KingBitboard & king_safe_zone).bit_count() * 30
    
        score -= (KingBitboard & MASK_CENTER).bit_count() * 50
        score -= (KingBitboard & BORDER_CENTER).bit_count() * 30

        return score





    def scorePositions(self,BitBoards:list):
        staralie=colorDictionary[self.color]
        startEnemey=colorDictionary[self.enemyColor]

        myHorseScore=self.scoreHorsePosition(BitBoards[PieceDictionary["H"]+staralie],self.color)
        enemyHorseScore=self.scoreHorsePosition(BitBoards[PieceDictionary["H"]+startEnemey],self.enemyColor)

        myBishopScore=self.scoreBishopPositions(BitBoards[PieceDictionary["B"]+colorDictionary[self.color]],self.color)
        enemyBishopScore=self.scoreBishopPositions(BitBoards[PieceDictionary["B"]+colorDictionary[self.enemyColor]],self.enemyColor)

        myTowerScore=self.scoreTowerPositions(BitBoards[PieceDictionary["T"]+colorDictionary[self.color]],self.color)
        enemyToweScore=self.scoreTowerPositions(BitBoards[PieceDictionary["T"]+colorDictionary[self.enemyColor]],self.enemyColor)

        myQueenScore=self.scoreQueenPositions(BitBoards[PieceDictionary["Q"]+colorDictionary[self.color]],self.color)
        enemyQueenScore=self.scoreQueenPositions(BitBoards[PieceDictionary["Q"]+colorDictionary[self.enemyColor]],self.color)

        myKingScore=self.scoreKingPositions(BitBoards[PieceDictionary["K"]+colorDictionary[self.color]],self.color)
        enemyKingScore=self.scoreKingPositions(BitBoards[PieceDictionary["K"]+colorDictionary[self.enemyColor]],self.color)

        score=myHorseScore-enemyHorseScore+myBishopScore-enemyBishopScore+myTowerScore-enemyToweScore+myQueenScore-enemyQueenScore+myKingScore-enemyKingScore

        return score
    
    def filtherMovements(self,Movements,Bitboards,color):
        LegalMovements=[]

        for Move in Movements:

            capture=self.make_move_on_Bitboard(Bitboards,Move,color)

            if self.isKingSafe(Bitboards,color):
                LegalMovements.append(Move)
            
            self.unmake_move(Bitboards,Move,capture,color)
        
        return LegalMovements

    def alpha_Beta(self,height,Bitboards,alpha,beta):

        currentColor=self.color if ((height%2)==0) else self.enemyColor

        print(f"altura:{height}, turno:{currentColor}")

        if height==0:

            self.BestMove=0
            self.BestScore=-10**9

        if height==self.MaxTreeHeight:
            return (self.ScoreBoard(Bitboards)+self.scorePositions(Bitboards))

        allMoves = self.generatePseudoLegalMovments(Bitboards,currentColor)

        LegalMovements=self.filtherMovements(allMoves,Bitboards,currentColor)

        if height==0:
            print(f"los movimientos sin filtrar son:{allMoves}")
            print(f"los movimientos legales son:{LegalMovements}")

        if len(LegalMovements)==0:

            if not(self.isKingSafe(Bitboards,currentColor)):
                

                points=((10)**9 - height) if (height%2)==0 else ((-10)**9 + height)

            else:

                points=0

            return points


        if (height%2)==0:

            for Move in LegalMovements:

                print(f"bestMove is:{self.BestMove}")
                print(f"bestValue is:{self.BestScore}")

                capture=self.make_move_on_Bitboard(Bitboards,Move,currentColor)
                
                alpha=max(alpha,self.alpha_Beta(height+1,Bitboards,alpha,beta))

                self.unmake_move(Bitboards,Move,capture,currentColor)

                if height==0 and alpha>self.BestScore:

                    self.BestScore=alpha
                    self.BestMove=Move


                if alpha >= beta:
                    break

            return alpha

        else:      
            
            for Move in LegalMovements:

                capture=self.make_move_on_Bitboard(Bitboards,Move,currentColor)
                
                beta=min(beta,self.alpha_Beta(height+1,Bitboards,alpha,beta))
                
                self.unmake_move(Bitboards,Move,capture,currentColor)

                if beta <= alpha:
                    break
            
            return beta
    


    def ScoreBoard(self,Bitboards):

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

        checkKingSelf=(-200) if self.isKingSafe(Bitboards,self.color) else 0
        checkKingEnemy=(150) if self.isKingSafe(Bitboards,self.enemyColor) else 0

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

        print(self.alpha_Beta(0,bitBoards,-10**9,10**9))

        print((self.BestMove))
        input()
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