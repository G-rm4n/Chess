import re

class InputHandlder:

    def Get_color(self):
        raise NotImplementedError
    
    def Get_Choice(self):
        raise NotImplementedError

class ConsoleInputHandler:

    @staticmethod
    def Get_color():

        while True:
            PlayerColor=input("enter player color(W/B): ")

            if PlayerColor in ("W","B"):
                botColor=("W" if PlayerColor=="B" else "B")
                break

        return (PlayerColor,botColor)

    @staticmethod
    def Get_Choice():

        pattern=r"^\((\d),(\d)\)$"

        while True:
            origin=input("enter origin coord '(Y,X)':")
            match=re.match(pattern,origin)
            if(match):
                origin=(int(match.group(1)),int(match.group(2)))
                break

        while True:
            destiny=input("enter destiny coord '(Y,X)':")
            match=re.match(pattern,destiny)
            if(match):
                destiny=(int(match.group(1)),int(match.group(2)))
                break
        
        return origin,destiny
    
    @staticmethod
    def Get_Choice_promotion():
        pieceType=["TOWER","BISHOP","QUEEN","HORSE"]

        while True:
            choice=input("enter piece type: ").upper()

            if choice in pieceType:
                break

        return choice

