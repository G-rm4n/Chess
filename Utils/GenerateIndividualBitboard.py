
def generateIndividualBitboard(GlobalBitboard):
    
        IndividualBitBoards=[]

        for i in range(64): 

            mask=1<<i

            if mask & GlobalBitboard:
                IndividualBitBoards.append(mask)
        
        return IndividualBitBoards