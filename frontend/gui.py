from cmu_112_graphics import *

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
    
    # gets number of pieces
    def getNumberOfPieces(self, board):
        self.board = board
        self.pieces = 0
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == self.number:
                    self.pieces += 1
        # print(f'Player {self.number} has {self.pieces} pieces')
        print(self.board)
        return self.pieces
    
    # get the position of the pieces
    def getPiecesPosition(self, board):
        self.board = board
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
        positions = self.getPiecesPosition(board)
        # print(positions)
        for x, y in positions:
            lines = self.getPossibleLines(x, y)
            # print(lines)
            if lines != []:
                self.moves += lines
        # print(f'User has these possible moves: {self.moves}')
        return self.moves
    
    def play(self, x, y, board):
        self.board = board
        self.board[x][y] = self.number
        
        # Flip over all the pieces from the line
        movesAndLines = self.getAllPossibleMoves(self.board)
        line = []
        for moveAndLine in movesAndLines:
            for key in moveAndLine:
                if key == (x, y):
                    line += moveAndLine[key]
                    
        print
        for (a, b) in line:
            # print(f'flipping {a}, {b}')
            self.board[a][b] = self.number
        
        # return the new board
        return self.board
            
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
    print(app.emptyBoard)
    
    # initializes the two players as objects    
    app.player1 = player(1, app.board, app.rows, app.cols)
    app.player2 = player(2, app.board, app.rows, app.cols)
    
     #turn    
    app.turn = app.player1
    # print(app.turn.getPiecesPosition(app.board))
    
    app.gameOver = False
    
def gameDimensions(app):
    rows = 8
    cols = 8
    margin = app.width//8
    cellSize = app.width//11
    return (rows, cols, cellSize, margin)
    
def redrawAll(app, canvas):
    drawGameplay(app, canvas)

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
    
    if app.gameOver == False:
        drawScore(app,canvas)
    else:
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
    
# def mouseMoved(app, event):
    
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
    
def mousePressed(app, event):
    x, y = event.x, event.y
    if app.gameOver == False:
        print(f"this is {app.turn.number}'s turn")
        # get the x and y value of the mouse press
        row_num = (x - app.margin) // app.cellSize
        col_num = (y - app.margin) // app.cellSize
        
        # check if the move is legal
        if isValid(app, x, y):
            # if legal: change the board pieces to your colour
            app.board = app.turn.play(col_num, row_num, app.board)
            print(f'playing move {col_num}, {row_num}')
            
            # updates score for both
            app.player1.pieces = app.player1.getNumberOfPieces(app.board)
            app.player2.pieces = app.player2.getNumberOfPieces(app.board)
            
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
        
def runReversi():
    runApp(width=800, height=900)
    
def main():
    runReversi()

if __name__ == '__main__':
    main()