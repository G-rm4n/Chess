from Core import Board, GameMaster, Movement,Promotion
from States import GameStates
from Handlers import InputHandler
from UI.Display import ConsoleDisplay
from Bot_Engine import Bot


state=GameStates.PREPARINGGAME
previousState=None

board=Board.Board()
GameMasterinst=GameMaster.GameMaster()


bot_king_attackers=[]
player_king_attackers=[]

origin=(int,int)
destiny=(int,int)

movementList=[]

PlayerColor=""
BotColor=""

while True:
    if len(player_king_attackers)>0 and GameMasterinst.evaluateCheckMate(board,player_king_attackers,PlayerColor):
        break
    
    if len(bot_king_attackers)>0 and GameMasterinst.evaluateCheckMate(board,bot_king_attackers,BotColor):
        break

    if state==GameStates.PREPARINGGAME:

        PlayerColor,BotColor=InputHandler.ConsoleInputHandler.Get_color()
        state=(GameStates.PLAYER_TURN if PlayerColor=="W" else GameStates.Bot_TURN)
        currentColor="W"
        board.prepareBoard()
        bot=Bot.bot(BotColor,PlayerColor,4)
    
    ConsoleDisplay.DisplayBoard(board)
    ConsoleDisplay.DisplayTurn(state)

    if state==GameStates.PLAYER_TURN:

        ConsoleDisplay.DisplayBoard(board)
        ConsoleDisplay.DisplayTurn(state)
        origin,destiny=InputHandler.ConsoleInputHandler.Get_Choice()
        previousState=state
        state=GameStates.Movement_Choiced
        

    if state==GameStates.Bot_TURN:
        ConsoleDisplay.DisplayBoard(board)
        ConsoleDisplay.DisplayTurn(state)
        choose=bot.chooseMovement(board.getPositions())
        origin,destiny=choose[0],choose[1]
        previousState=state
        state=GameStates.Movement_Choiced
        

    
    if state==GameStates.Movement_Choiced:

        if not(board.validateCoords(origin,destiny)):
            ConsoleDisplay.displayCoordError()
            state=previousState
            continue

        if not(GameMasterinst.verifyLegality(origin,destiny,board,currentColor)):
            ConsoleDisplay.displayMovementError()
            state=previousState
            continue
        
        isAttack=GameMasterinst.isAttack(destiny,board,currentColor)

        movement=Movement.Movement(origin,destiny,isAttack)

        if isAttack:
            capturedPiece=board.getPiece(destiny)
            movement.set_capture(capturedPiece)
        
        movementList.append(movement)

        board.increaseMovements(origin)

        board.makeMove(origin,destiny)

        if GameMasterinst.verifyPromotion(board.getPiece(destiny),destiny):

            choice=(InputHandler.ConsoleInputHandler.Get_Choice_promotion()) if previousState==GameStates.PLAYER_TURN else (bot.choosePromotion)
            newPiece=board.createNewPiece(choice,PlayerColor if previousState==GameStates.PLAYER_TURN else BotColor)
            board.assingPiece(destiny,newPiece)

        state=(GameStates.Bot_TURN) if previousState==GameStates.PLAYER_TURN else GameStates.PLAYER_TURN

    player_king_attackers=GameMasterinst.evaluateCheck(PlayerColor,board)
    bot_king_attackers=GameMasterinst.evaluateCheck(BotColor,board)

    currentColor=(BotColor if currentColor==PlayerColor else PlayerColor)

        

    
    



    