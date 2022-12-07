from gui import *
# MINIMAX AI CITATION: I got the rough idea of minimax from this Youtube video: https://youtu.be/l-hh51ncgDI
# CITATION: I also took reference from this minimax algorithm written for Tic Tac Toe:
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/

def computeMinimax(board):
    # created weighted heuristic board based off my own experience playing reversi
    weightedBoard = [
        [30,  -20, 10, 10, 10, 10,   -20, 30],
        [-20, -15,-10, -5, -5, -5, -10, -20],
        [10, -10, -5,  0,  0,  0,  -5, 10],
        [10,  -5,  0,  3,  3,  0,  -5, 10],
        [10,  -5,  0,  3,  3,  0,  -5, 10],
        [10,  -5, -5,  0,  0,  0, -10, 10],
        [-20,  -10, -5, -5, -5,-10, -15, -20],
        [80,   -20, 10, 10, 10, 10,  -20, 80],
    ]
    player1score = 0
    player2score = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 1:
                player1score += weightedBoard[i][j]
            elif board[i][j] == 2:
                player2score += weightedBoard[i][j]
    return (player1score, player2score)
    
def minimax_max(app, board, player, depth, counter):
    # print("starting max")
    # get all possible moves for the particular playernumber (can look to optimize this)
    moves = player.getAllPossiblePositions(board)
    # print(moves)
    # base case
    if counter >= depth or moves == set():
        # compute scores for both black and white
        # return the final score (either black - white or white - black)
        scores = computeMinimax(board)
        # print(scores)
        if player.number == 1:
            # print(scores[0] - scores[1])
            return scores[0] - scores[1]
        else:
            # print(scores[1] - scores[0])
            return scores[1] - scores[0]
    else:
        #find out what color is the next player
        if player.number == 1:
            nextPlayer = app.player2
        else:
            nextPlayer = app.player1
        maxScore = -99999
        # recursive calls
        for move in moves:
            #play the move and pass the new board and moves into the min function
            newBoard = player.play(move[0], move[1], board)
            # print(f'newBoard: {newBoard}')
            score = minimax_min(app, newBoard, nextPlayer, app.sliderX, counter+1)
            print(f'maxScore: {score} for position ({move[0]}, {move[1]}) player {player.number}')
            if score > maxScore:
                maxScore = score
        return maxScore

def minimax_min(app, board, player, depth, counter):
    # print("starting min")
    # get all possible moves for the particular playernumber (can look to optimize this)
    moves = player.getAllPossiblePositions(board)
    # print(moves)
    # base case
    if counter >= depth or moves == set():
        # compute scores for both black and white
        # return the final score (either black - white or white - black)
        scores = computeMinimax(board)
        if player.number == 1:
            # print(scores[1] - scores[0])
            return scores[1] - scores[0]
        else:
            # print(scores[0] - scores[1])
            return scores[0] - scores[1]
    else:
        #find out what color is the next player
        if player.number == 1:
            nextPlayer = app.player2
        else:
            nextPlayer = app.player1
        minScore = 9999999
        # recursive calls
        for move in moves:
            #play the move and pass the new board and moves into the min function
            newBoard = player.play(move[0], move[1], board)
            # print(f'newBoard: {newBoard}')
            score = minimax_max(app, newBoard, nextPlayer, depth, counter+1)
            # print(score)
            print(f'minScore: {score} for position ({move[0]}, {move[1]}) player {player.number}')
            if score < minScore:
                minScore = score
        return minScore

def minimaxAI(app, player):
    print("AI's turn")
    # declare newboard
    board = copy.deepcopy(app.board)
    # get all moves of player (which is basically which player is the AI)
    moves = player.getAllPossiblePositions(app.board)

    # find out who is the next player
    if player.number == 1:
        nextPlayer = app.player2
    else:
        nextPlayer = app.player1
    maxScore = -999999
    bestMove = (1, 1)
    
    for move in moves:
        newBoard = player.play(move[0], move[1], board)
        #specify depth here
        score = minimax_min(app, newBoard, nextPlayer, 10, 0)
        print(f'score: {score} for player {player.number}')

        if score > maxScore:
            maxScore = score
            bestMove = move
            
    check = True
    #check if the whole board has been filled up, if yes end game
    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            if app.board[i][j] == 0:
                check = False
    app.gameOver = check
    
    print(f'bestScore" {maxScore}')
    print(f'bestMove: {bestMove}')
    #play best move
    player.play(bestMove[0], bestMove[1], app.board)
    
    #check for end game after placing a piece
    check = True
    #check if the whole board has been filled up, if yes end game
    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            if app.board[i][j] == 0:
                check = False
    app.gameOver = check
    
    #check for the number of moves the opponent has
    #if zero moves, don't switch turns
    #change turn
    if player.number == 1:
        #check for number of moves
        moves = app.player2.getAllPossiblePositions(app.board)
        if len(moves) == 0:
            app.turn = app.player1
        else:
            app.turn = app.player2
    else:
        moves = app.player1.getAllPossiblePositions(app.board)
        if len(moves) == 0:
            app.turn = app.player2
        else:
            app.turn = app.player1
        