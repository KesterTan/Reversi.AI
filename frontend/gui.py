from cmu_112_graphics import *
import random

class player(object):
    def __init__(self, number, board, rows, cols):
        self.number = number
        self.board = board
        self.rows = rows
        self.cols = cols
        # saves the number of pieces
        self.pieces = 2
        # saves the position (x, y) of all the pieces
        self.positions = set()
        # saves all the possible positions that a user can place a piece and the corresponding line that will be swapped
        self.moves = []
        # saves all the possible lines (captured pieces in a line) a user can get
        self.lines = []
        self.possibleMoves = set()
    
    # gets number of pieces
    def getNumberOfPieces(self, board):
        self.pieces = 0
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == self.number:
                    self.pieces += 1
        # print(f'Player {self.number} has {self.pieces} pieces')
        return self.pieces
    
    # get the position of the pieces
    def getPiecesPosition(self, board):
        self.board = board
        self.positions = set()
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == self.number:
                    self.positions.add((y,x))
        # print(f'Player {self.number} has these pieces in these {self.positions} positions')
        return self.positions
                    
    # get lists of pieces that are captured: lists are used here cause they need to be ordered
    def getPossibleLines(self, x, y):
        # find uninterrupted lines from every direction from a selected piece that the player has (set of array of tuples of captured pieces)
        lines = []
        # print(f'testing possible lines for {x, y}')
        possibleDirections = {(0,1), (0, -1), (1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0)}
        for xMove, yMove in possibleDirections:
            # Values need to be redeclared each time or they will accumulate
            line = []
            endPoint = (0,0)
            res = {}
            posX = x
            posY = y
            
            posX += xMove
            posY += yMove
            possible = False
            number = 0
            if self.number == 1:
                number = 2
            elif self.number == 2:
                number = 1
            
            while True:
                # out of limits
                if posX < 0 or posY < 0 or posX >= self.cols or posY >= self.rows:
                    break
                # if it is itself
                elif self.board[posX][posY] == self.number:
                    break
                # if it is empty, then it is also possible
                # this is also the 'moves' you want to save
                elif self.board[posX][posY] == 0:
                    endPoint = (posX, posY)
                    possible = True
                    if line != []:
                        # print(f'endpoint: {endPoint}')
                        res[endPoint] = line
                    break
                # if it is an enemy piece, continue adding 1, and save the line
                else:
                    line.append((posX, posY))
                    posX += xMove
                    posY += yMove
            # only if it is possible to place a piece (there isn't a line of long enemy pieces till the end) and there is a line
            if len(res) != 0 and possible == True:
                # print(res)
                lines.append(res)
        # print(f'Position {x, y} has these lines: {lines}')
        return lines
                                    
    def getAllPossibleMoves(self, board):
        self.board = board
        self.moves = []
        positions = self.getPiecesPosition(board)
        # print(positions)
        for x, y in positions:
            lines = self.getPossibleLines(x, y)
            # print(lines)
            if lines != []:
                self.moves += lines
        # print(board)
        # print(f'User has these possible moves: {self.moves}')
        return self.moves
    
    def getAllPossiblePositions(self, board):
        self.board = board
        self.possibleMoves = set()
        self.getPiecesPosition(board)
        movesAndLines = self.getAllPossibleMoves(board)
        moves = set()
        for moveAndLine in movesAndLines:
            for key in moveAndLine:
                moves.add(key)
        
        for move in moves:
            if move not in self.positions:
                self.possibleMoves.add(move)
        return self.possibleMoves
     
    def play(self, x, y, board):
        self.getAllPossibleMoves(board)
        self.getPiecesPosition(board)
        self.board[x][y] = self.number
        # Flip over all the pieces from the line
        
        movesAndLines = self.moves
        line = []
        # print(f'movesandlines: {movesAndLines}')
        for moveAndLine in movesAndLines:
            # print(f'moveAndLine: {moveAndLine}')
            for key in moveAndLine:
                # print(f'key: {key}')
                if key == (x, y):
                    # print(f'move: {moveAndLine[key]}')
                    line += moveAndLine[key]
        
        for (a, b) in line:
            # print(f'flipping {a}, {b}')
            self.board[a][b] = self.number
        
        # return the new board
        return self.board
    
# APP CODE
def appStarted(app):
    (app.rows, app.cols, app.cellSize, app.margin) = gameDimensions(app)
    app.board = []
    for i in range(app.rows):
        app.board.append([])
        for j in range(app.rows):
            app.board[i].append(0)
    # print(app.board)
    # '1' is black
    # '2' is white
    app.board[3][3] = 1
    app.board[4][4] = 1
    app.board[3][4] = 2
    app.board[4][3] = 2
    app.emptyBoard = copy.deepcopy(app.board)
    
    # initializes the two players as objects    
    app.player1 = player(1, app.board, app.rows, app.cols)
    app.player2 = player(2, app.board, app.rows, app.cols)
    
    app.player1.pieces = app.player1.getNumberOfPieces(app.board)
    app.player2.pieces = app.player2.getNumberOfPieces(app.board)

     #turn    
    app.turn = app.player1
    # print(app.turn.getPiecesPosition(app.board))
    
    app.gamePlay = False
    app.home = True
    app.gameOver = False
    app.homePageButton1 = (1,2,3,4)
    app.homePageButton2 = (1,2,3,4)
    app.selectDifficulty = False
    app.AI = False
    app.drawSlider = False
    app.drawSliderCircle = (-99, -99)
    app.drawSliderCircleBool = False
    app.sliderX = 0
    
def gameDimensions(app):
    rows = 8
    cols = 8
    margin = app.width // 8
    cellSize = app.width // 11
    return (rows, cols, cellSize, margin)
    
def redrawAll(app, canvas):
    if app.home == True:
        drawHomePage(app, canvas)
    if app.selectDifficulty == True:
        drawSelectDifficulty(app, canvas)
    if app.gamePlay == True and app.home == False:
        drawGameplay(app, canvas)

def drawSelectDifficulty(app, canvas):
    #background
    canvas.create_rectangle(0,0, app.width, app.height, fill='tan')
    #Title
    canvas.create_text(app.width // 2,
                       app.height // 10 + app.cellSize // 1.5,
                       text='Reversi.AI',
                       font='Helvetica 100 italic',
                       fill='mint cream')
    #black circle
    canvas.create_oval(app.margin + app.cellSize,
                       app.height//10 + 2.5 * app.cellSize,
                       app.margin + 2 * app.cellSize,
                       app.height//10 + 3.5 * app.cellSize,
                       fill='grey8',
                       width=0)
    
    #player1 name
    canvas.create_text(app.margin + 1.5 * app.cellSize,
                       app.height//10 + 4 * app.cellSize,
                       text="Player",
                       fill='grey8',
                       font='Helvetica 30')
    
    #white circle
    canvas.create_oval(app.margin + 6.5 * app.cellSize,
                        app.height//10 + 2.5 * app.cellSize,
                        app.margin + 7.5 * app.cellSize,
                        app.height//10 + 3.5 * app.cellSize,
                        fill='mint cream',
                        width=0)
    
    #computer name
    canvas.create_text(app.margin + 7 * app.cellSize,
                       app.height//10 + 4 * app.cellSize,
                       text="Computer",
                       fill='grey8',
                       font='Helvetica 30')
    
    #arrows to swap
    
    #ai difficulty level
    
    #play button
    canvas.create_rectangle(app.margin + 1.25 * app.cellSize,
                            app.margin + 8 * app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.margin + 9.5 * app.cellSize,
                            fill="NavajoWhite1",
                            width=0)
    
    #play text
    canvas.create_text(app.margin +  4.125 * app.cellSize,
                       app.margin + 8.75 * app.cellSize,
                       text="Play",
                       fill='grey8',
                       font='Helvetica 30')
    #draw the slider
    canvas.create_rectangle(app.margin + 0.5*app.cellSize,
                            app.margin + 6*app.cellSize,
                            app.margin + 8*app.cellSize,
                            app.margin + 6.5*app.cellSize,
                            width = 5)
    drawSlider(app, canvas)
    
def drawHomePage(app, canvas):
    #background
    canvas.create_rectangle(0,0, app.width, app.height, fill='tan')
    #Title
    canvas.create_text(app.width // 2,
                       app.height // 10 + app.cellSize // 1.5,
                       text='Reversi.AI',
                       font='Helvetica 100 italic',
                       fill='mint cream')
    #rectangle for two-player button
    canvas.create_rectangle(app.margin + 1.125*app.cellSize,
                            app.height // 5 + app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.height // 5 + 3 * app.cellSize,
                            fill='NavajoWhite1',
                            width=0)
    
    #text for two-player
    canvas.create_text(app.margin + 4.125 * app.cellSize,
                       app.height//5 + 2* app.cellSize,
                       text="Two-Player",
                       font='Helvetica 30',
                       fill='grey8')
    
    #rectangle for offline button (against AI)
    canvas.create_rectangle(app.margin + 1.125*app.cellSize,
                            app.height // 5 + 4*app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.height // 5 + 6* app.cellSize,
                            fill='NavajoWhite1',
                            width=0)
    
    #text for playing against AI
    canvas.create_text(app.margin + 4.125 * app.cellSize,
                       app.height//5 + 5* app.cellSize,
                       text="Offline",
                       font='Helvetica 30',
                       fill='grey8')
    
def drawGameplay(app, canvas):
    #background
    canvas.create_rectangle(0,0, app.width, app.height, fill='tan')
    #Title
    canvas.create_text(app.width//2,
                       app.cellSize//1.5,
                       text='Reversi.AI',
                       font='Helvetica 40 italic',
                       fill='mint cream')
    drawBoard(app, canvas)
    drawPieces(app, canvas)
    drawAllPotentialPieces(app, canvas)
    
    drawScore(app,canvas)
    
    if app.gameOver == True:
        drawGameOver(app, canvas)
    
def drawGameOver(app, canvas):
    canvas.create_rectangle(app.margin + app.cellSize*1.5, 
                            app.margin + app.cellSize*1.5,
                            app.margin + app.cellSize*6.5,
                            app.margin + app.cellSize*6.5,
                            fill="tan",
                            width=0)
    if app.player1.pieces > app.player2.pieces:
        winner = app.player1.number
    else:
        winner = app.player2.number
    
    canvas.create_text(app.margin + app.cellSize*4,
                       app.margin + app.cellSize*2,
                       text=f"Player {winner} wins!",
                       font='Helvetica 30 italic bold',
                       fill='gray8')
    
    canvas.create_text(app.margin + app.cellSize*4,
                       app.margin + app.cellSize*3,
                       text=f'Player 1 score: {app.player1.pieces}',
                       font='Helvetica 25 italic',
                       fill='gray8')
    canvas.create_text(app.margin + app.cellSize*4,
                       app.margin + app.cellSize*4,
                       text=f'Player 2 score: {app.player2.pieces}',
                       font='Helvetica 25 italic',
                       fill='gray8')
        
    canvas.create_rectangle(app.margin + app.cellSize*3,
                            app.margin + app.cellSize*5,
                            app.margin + app.cellSize*5,
                            app.margin + app.cellSize*5.5,
                            fill='mint cream')
    canvas.create_text(app.margin + app.cellSize*4,
                            app.margin+ app.cellSize*5.25,
                            text="Play Again?",
                            fill='gray8',
                            font='Helvetica 18 italic bold')
    
def drawScore(app, canvas):
    #circle
    canvas.create_oval(app.margin + 1*app.cellSize,
                       app.margin + 8.5*app.cellSize, 
                       app.margin + 2*app.cellSize,
                       app.margin + 9.5*app.cellSize,
                       fill="gray8",
                       width=0)
    #text in circle
    canvas.create_text(app.margin + 1.5*app.cellSize, 
                       app.margin + 9*app.cellSize,
                       text="Player 1",
                       fill='mint cream')
    #display player1 score
    canvas.create_text(app.margin + 1.5*app.cellSize, 
                       app.margin + 10*app.cellSize,
                       text=app.player1.pieces,
                       font='Helvetica 26 bold', 
                       fill='black')

    if app.turn.number == 1:
        #create arrow for player1
        canvas.create_rectangle(app.margin + 2.75*app.cellSize,
                                app.margin + 8.875*app.cellSize,
                                app.margin + 3.25*app.cellSize,
                                app.margin + 9.125*app.cellSize,
                                fill="gray8",
                                width=0)
        canvas.create_polygon(app.margin + 2.5*app.cellSize,
                            app.margin + 9*app.cellSize,
                            app.margin + 2.75*app.cellSize,
                            app.margin + 8.75*app.cellSize,
                            app.margin +2.75*app.cellSize,
                            app.margin + 9.25*app.cellSize,
                            fill="gray8",
                            width=0)
        
    if app.turn.number == 2:
        #create arrow for player2
        canvas.create_rectangle(app.margin + 4.75*app.cellSize,
                                app.margin + 8.875*app.cellSize,
                                app.margin + 5.25*app.cellSize,
                                app.margin + 9.125*app.cellSize,
                                fill="mint cream",
                                width=0)
        canvas.create_polygon(app.margin + 5.5*app.cellSize,
                            app.margin + 9*app.cellSize,
                            app.margin + 5.25*app.cellSize,
                            app.margin + 8.75*app.cellSize,
                            app.margin +5.25*app.cellSize,
                            app.margin + 9.25*app.cellSize,
                            fill="mint cream",
                            width=0)
    
    #circle player2
    canvas.create_oval(app.margin + 6*app.cellSize,
                       app.margin + 8.5*app.cellSize, 
                       app.margin + 7*app.cellSize, 
                       app.margin + 9.5*app.cellSize,
                       fill="mint cream",
                       width=0)
    #text in circle
    canvas.create_text(app.margin +6.5*app.cellSize, 
                       app.margin + 9*app.cellSize,
                       text="Player 2", fill='black')
     #display player2 score
    canvas.create_text(app.margin +6.5*app.cellSize,
                       app.margin + 10*app.cellSize,
                       text=app.player2.pieces,
                       font='Helvetica 26 bold')

def drawBoard(app, canvas):
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app, canvas, i, j, 'sea green')
            
def drawCell(app, canvas, row_num, col_num, color):
    canvas.create_rectangle((app.margin + col_num*app.cellSize), 
                            (app.margin + row_num*app.cellSize),
                            (app.margin + (col_num + 1)*app.cellSize),
                            (app.margin + (row_num+1)*app.cellSize),
                            fill=color,
                            outline='gray11', width=app.width//200)
    
# draw helper positions to place pieces
def drawAllPotentialPieces(app, canvas):
    # print("drawing positions")
    app.turn.getAllPossiblePositions(app.board)
    # print(f'possible Moves: {app.turn.possibleMoves}')
    for position in app.turn.possibleMoves:
        drawPotentialPiece(app, canvas, position[0], position[1], 'grey70')

def drawPotentialPiece(app, canvas, row_num, col_num, color):
    # print(f'row and col: {row_num}, {col_num}')
    canvas.create_oval(app.margin + col_num*app.cellSize + app.cellSize //2.5,
                       app.margin + row_num*app.cellSize + app.cellSize//2.5,
                       app.margin + (col_num+1)*app.cellSize - app.cellSize//2.5,
                       app.margin + (row_num+1)*app.cellSize - app.cellSize//2.5,
                       fill=color,
                       width=0)

def drawPieces(app, canvas):
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j] == 2:
                drawCircle(app, canvas, i, j, 'mint cream')
            elif app.board[i][j] == 1:
                drawCircle(app, canvas, i, j, 'gray8')

def drawCircle(app, canvas, row_num, col_num, color):
    canvas.create_oval((app.margin + col_num*app.cellSize) + app.cellSize//12, 
                        (app.margin + row_num*app.cellSize) + app.cellSize//12,
                        (app.margin + (col_num+1)*app.cellSize) - app.cellSize//12,
                        (app.margin + (row_num+1)*app.cellSize) - app.cellSize//12,
                        fill=color,
                        width=0)
    
#create slider for AI difficulty
def drawSlider(app, canvas):
    x, y = app.drawSliderCircle
    canvas.create_oval(x - app.cellSize//2,
                       y - app.cellSize//2,
                       x + app.cellSize//2,
                       y + app.cellSize//2,
                       fill="black",
                       width=0)
    
    if app.drawSliderCircleBool == False:
        canvas.create_oval(app.margin,
                           app.margin + 6.25*app.cellSize - app.cellSize//2,
                           app.margin + 0.5*app.cellSize + app.cellSize//2,
                           app.margin + 6.25*app.cellSize + app.cellSize//2,
                           fill="black",
                           width=0)
    
def mouseDragged(app, event):
    if app.gamePlay == False or app.home == False or app.selectDifficulty == True:
        app.drawSlider = True
    x, y = event.x, event.y
    
    #check if the mouse is within the box
    check = False
    if (x >= app.margin + 0.5*app.cellSize and x <= app.margin + 8*app.cellSize and
    y >= app.margin + 6*app.cellSize and y <= app.margin + 6.5*app.cellSize):
        app.drawSliderCircleBool = True
        check = True
        
    #determine the depth of minimax AI
    if app.drawSlider == True and check == True:
        app.drawSliderCircle = (x, app.margin + 6.25*app.cellSize)
        app.sliderX = int(((x - (app.margin + 0.5*app.cellSize))
                           // app.cellSize) + 2)
    
def mousePressed(app, event):
    x, y = event.x, event.y
    if app.home == True:
        if (x >= app.margin + 1.125*app.cellSize and 
            x <= app.margin + 7 * app.cellSize and 
            y >= app.height // 5 + app.cellSize and 
            y <= app.height // 5 + 3 * app.cellSize):
                app.gamePlay = True
                app.home = False
        elif (x >= app.margin + 1.125*app.cellSize and 
              x <= app.margin + 7 * app.cellSize and 
              y >= app.height // 5 + 4*app.cellSize and 
              y <= app.height // 5 + 6*app.cellSize):
                app.home = False
                app.selectDifficulty = True
                
    if app.selectDifficulty == True:
        if (x >= app.margin + 1.25 * app.cellSize and
            x <= app.margin + 7 * app.cellSize and
            y >= app.margin + 8 * app.cellSize and
            y <= app.margin + 9.5 * app.cellSize):
                app.AI = True
                app.gamePlay = True
                app.selectDifficulty = False
        
    if app.gameOver == False and app.home == False:
        # get the x and y value of the mouse press
        row_num = (x - app.margin) // app.cellSize
        col_num = (y - app.margin) // app.cellSize
        
        # check if the move is legal
        if isValid(app, x, y):
            # if legal: change the board pieces to your colour
            app.board = app.turn.play(col_num, row_num, app.board)
            # print(f'playing move {col_num}, {row_num}')
            
            # updates score for both
            app.player1.pieces = app.player1.getNumberOfPieces(app.board)
            app.player2.pieces = app.player2.getNumberOfPieces(app.board)
            
            if app.player1.pieces == 0 or app.player2.pieces == 0:
                app.gameOver = True
            
            # get total number of pieces
            total = app.player1.pieces + app.player2.pieces
            if total >= app.rows * app.cols:
                app.gameOver = True

            # get all of opponent's moves
            turn = app.turn.number
            opponent = app.player1
            if turn == 1:
                opponent = app.player2
            elif turn == 2:
                opponent = app.player1
            # if opponnent has no moves: dont change player turn
            # if opponent has moves: change player turn
            if len(opponent.getAllPossibleMoves(app.board)) != 0:
                app.turn = opponent
                
        runAI(app)

    else:
        if (x >= app.margin + app.cellSize*3 and 
            y >= app.margin + app.cellSize*5 and
            x <= app.margin + app.cellSize*5 and
            y <= app.margin + app.cellSize*5.5):
            app.gameOver = False
            app.board = app.emptyBoard
            
# this checks if the coordinates of the play is legitimate (corrsponds to one of the possible moves the player can make)
def isValid(app, x, y):
     # get the row_num and col_num of the mouse press
    row_num = (x - app.margin) // app.cellSize
    col_num = (y - app.margin) // app.cellSize
    
    # check if it is out of the board
    if (x <= app.margin or y <= app.margin or x >= 8*app.cellSize + 
        app.margin or y >= 8*app.cellSize + app.margin):
        print("out")
        return False
    # if there already is a piece there
    if app.board[col_num][row_num] != 0:
        return False
    print(f'checking move {row_num}, {col_num} if valid')
    # print(app.turn.number)
    movesAndLines = app.turn.getAllPossibleMoves(app.board)
    moves = set()
    for moveAndLine in movesAndLines:
        # print(moveAndLine)
        for key in moveAndLine:
            moves.add(key)
    # print(moves)
    if (col_num, row_num) in moves:
        # print("true")
        return True
    else:
        return False
    
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

# MINIMAX AI
def computeMinimax(board):
    # created weighted heuristic board
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
        
# RUN AI
def runAI(app):
    if app.AI == True:
        print("AI started")
        # randomAI(app, 2)
        if app.turn.number == 2:
            minimaxAI(app, app.player2)
        
def runReversi():
    runApp(width=800, height=900)
    
def main():
    runReversi()

if __name__ == '__main__':
    main()