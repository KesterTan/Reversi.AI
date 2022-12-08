from gui import *
import copy
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
    return player1score, player2score
    
def minimax_max(app, board, p, depth, counter):
    # get all possible moves for the particular player number
    moves = p.getAllPossiblePositions(board)
    # base case
    if counter >= depth or moves == set():
        # compute scores for both black and white
        # return the final score (either black - white or white - black)
        scores = computeMinimax(board)
        if p.number == 1:
            return scores[0] - scores[1]
        else:
            return scores[1] - scores[0]
    else:
        # find out what color is the next player
        if p.number == 1:
            nextPlayer = app.player2
        else:
            nextPlayer = app.player1
        maxScore = -99999
        # recursive calls
        for move in moves:
            # play the move and pass the new board and moves into the min function
            newBoard = p.play(move[0], move[1], board)
            score = minimax_min(app, newBoard, nextPlayer, app.sliderX, counter+1)
            if score > maxScore:
                maxScore = score
        return maxScore

def minimax_min(app, board, p, depth, counter):
    # get all possible moves for the particular player number (can look to optimize this)
    moves = p.getAllPossiblePositions(board)
    # base case
    if counter >= depth or moves == set():
        # compute scores for both black and white
        # return the final score (either black - white or white - black)
        scores = computeMinimax(board)
        if p.number == 1:
            return scores[1] - scores[0]
        else:
            return scores[0] - scores[1]
    else:
        # find out what color is the next player
        if p.number == 1:
            nextPlayer = app.player2
        else:
            nextPlayer = app.player1
        minScore = 9999999
        # recursive calls
        for move in moves:
            #play the move and pass the new board and moves into the min function
            newBoard = p.play(move[0], move[1], board)
            score = minimax_max(app, newBoard, nextPlayer, depth, counter+1)
            if score < minScore:
                minScore = score
        return minScore

def minimaxAI(app, playerObj):
    print("Minimax AI playing")
    # declare new board
    board = copy.deepcopy(app.board)
    # get all moves of player (which is basically which player is the AI)
    moves = playerObj.getAllPossiblePositions(app.board)

    # find out who is the next player
    if playerObj.number == 1:
        nextPlayer = app.player2
    else:
        nextPlayer = app.player1
    maxScore = -999999
    bestMove = (1, 1)
    
    for move in moves:
        newBoard = playerObj.play(move[0], move[1], board)
        #specify depth here
        score = minimax_min(app, newBoard, nextPlayer, app.sliderX + 20, 0)

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

    # play best move
    playerObj.play(bestMove[0], bestMove[1], app.board)
    
    # check for end game after placing a piece
    check = True
    # check if the whole board has been filled up, if yes end game
    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            if app.board[i][j] == 0:
                check = False
    app.gameOver = check
    
    # check for the number of moves the opponent has
    # if zero moves, don't switch turns
    # change turn
    if playerObj.number == 1:
        # check for number of moves
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
        