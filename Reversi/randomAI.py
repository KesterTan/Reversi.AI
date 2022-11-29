from gui import *
import random

# RANDOM AI
def randomAI(app, playerNumber):
    # check if its the player's turn
    if app.turn.number == playerNumber:
        # save positions of all possible moves
        movesAndLines = app.turn.getAllPossibleMoves(app.board)
        moves = set()
        for moveAndLine in movesAndLines:
            # print(moveAndLine)
            for key in moveAndLine:
                moves.add(key)
        # play a random allowed move
        numberOfMoves = len(moves)
        i = random.randint(0, numberOfMoves - 1)
        moves = list(moves)
        row_num = moves[i][0]    
        col_num = moves[i][1]  
        app.player2.play(row_num, col_num, app.board)
        
        # change turn
        app.turn = app.player1
