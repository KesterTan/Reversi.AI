from cmu_112_graphics import *
from main import *
from randomAI import *
from minimax import *
from monteCarlo import *
from network import Network
   
# APP CODE
# CITATION: Cmu graphics from CMU 112: https://www.cs.cmu.edu/~112/index.html
def appStarted(app):
    (app.rows, app.cols, app.cellSize, app.margin) = gameDimensions(app)
    app.board = []
    for i in range(app.rows):
        app.board.append([])
        for j in range(app.rows):
            app.board[i].append(0)
    # '1' is black
    # '2' is white
    app.board[3][3] = 1
    app.board[4][4] = 1
    app.board[3][4] = 2
    app.board[4][3] = 2
    app.emptyBoard = []
    for i in range(app.rows):
        app.emptyBoard.append([])
        for j in range(app.rows):
            app.emptyBoard[i].append(0)
    app.emptyBoard[3][3] = 1
    app.emptyBoard[4][4] = 1
    app.emptyBoard[3][4] = 2
    app.emptyBoard[4][3] = 2


    # initializes the two players as objects    
    app.player1 = player(1, app.board, app.rows, app.cols)
    app.player2 = player(2, app.board, app.rows, app.cols)
    
    app.player1.pieces = app.player1.getNumberOfPieces(app.board)
    app.player2.pieces = app.player2.getNumberOfPieces(app.board)

    # code that initializes a player's turn
    app.turn = app.player1

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
    app.MC = False
    app.network = False
    
    # home icon
    # image CITATION: https://icons8.com/icons/set/home
    app.imagehome = app.loadImage('home.png')
    app.homeImg = app.scaleImage(app.imagehome, 1.5)
    
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
    # background
    canvas.create_rectangle(0,0, app.width, app.height, fill='tan')
    # Title
    canvas.create_text(app.width // 2,
                       app.height // 10 + app.cellSize // 1.5,
                       text='Reversi.AI',
                       font='Helvetica 100 italic',
                       fill='mint cream')
    # black circle
    canvas.create_oval(app.margin + app.cellSize,
                       app.height//10 + 2.5 * app.cellSize,
                       app.margin + 2 * app.cellSize,
                       app.height//10 + 3.5 * app.cellSize,
                       fill='grey8',
                       width=0)
    
    # player1 name
    canvas.create_text(app.margin + 1.5 * app.cellSize,
                       app.height//10 + 4 * app.cellSize,
                       text="Player",
                       fill='grey8',
                       font='Helvetica 30')
    
    # white circle
    canvas.create_oval(app.margin + 6.5 * app.cellSize,
                        app.height//10 + 2.5 * app.cellSize,
                        app.margin + 7.5 * app.cellSize,
                        app.height//10 + 3.5 * app.cellSize,
                        fill='mint cream',
                        width=0)
    
    # computer name
    canvas.create_text(app.margin + 7 * app.cellSize,
                       app.height//10 + 4 * app.cellSize,
                       text="Computer",
                       fill='grey8',
                       font='Helvetica 30')

    # play button
    canvas.create_rectangle(app.margin + 1.25 * app.cellSize,
                            app.margin + 8.75 * app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.margin + 10.25 * app.cellSize,
                            fill="NavajoWhite1",
                            width=0)

    # monte carlo difficulty button
    canvas.create_rectangle(app.margin + 1.25 * app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.margin + 8.5 * app.cellSize,
                            fill="NavajoWhite1",
                            width=0)

    # monte carlo play words
    canvas.create_text(app.margin + 4.125 * app.cellSize,
                       app.margin + 7.75 * app.cellSize,
                       text="Versus MiniMax AI",
                       fill="grey8",
                       font="Helvetica 30")

    # play text
    canvas.create_text(app.margin +  4.125 * app.cellSize,
                       app.margin + 9.5 * app.cellSize,
                       text="Versus Monte Carlo AI",
                       fill='grey8',
                       font='Helvetica 30')

    # select difficulty words
    canvas.create_text(app.margin + 4.5*app.cellSize,
                       app.margin + 5.5*app.cellSize,
                       text='Slide to select difficulty',
                       font='Helvetica 20')

    canvas.create_text(app.margin + 0.5 * app.cellSize,
                       app.margin + 5.5 * app.cellSize,
                       text='Easy',
                       font='Helvetica 20')

    canvas.create_text(app.margin + 8 * app.cellSize,
                       app.margin + 5.5 * app.cellSize,
                       text='Hard',
                       font='Helvetica 20')
    # slider
    canvas.create_rectangle(app.margin + 0.5*app.cellSize,
                            app.margin + 6*app.cellSize,
                            app.margin + 8*app.cellSize,
                            app.margin + 6.5*app.cellSize,
                            width = 5)
    drawSlider(app, canvas)
    
def drawHomePage(app, canvas):
    # background
    canvas.create_rectangle(0,0, app.width, app.height, fill='tan')
    # Title
    canvas.create_text(app.width // 2,
                       app.height // 10 + app.cellSize // 1.5,
                       text='Reversi.AI',
                       font='Helvetica 100 italic',
                       fill='mint cream')

    # rectangle for two-player button
    canvas.create_rectangle(app.margin + 1.125*app.cellSize,
                            app.height // 5 + app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.height // 5 + 3 * app.cellSize,
                            fill='NavajoWhite1',
                            width=0)
    
    # text for two-player
    canvas.create_text(app.margin + 4.125 * app.cellSize,
                       app.height//5 + 2* app.cellSize,
                       text="Multiplayer",
                       font='Helvetica 30',
                       fill='grey8')
    
    # rectangle for offline button (against AI)
    canvas.create_rectangle(app.margin + 1.125*app.cellSize,
                            app.height // 5 + 4*app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.height // 5 + 6* app.cellSize,
                            fill='NavajoWhite1',
                            width=0)
    
    # text for playing against AI
    canvas.create_text(app.margin + 4.125 * app.cellSize,
                       app.height//5 + 5* app.cellSize,
                       text="Offline 1 Player",
                       font='Helvetica 30',
                       fill='grey8')

    # rectangle for server network button
    canvas.create_rectangle(app.margin + 1.125 * app.cellSize,
                            app.height // 5 + 7 * app.cellSize,
                            app.margin + 7 * app.cellSize,
                            app.height // 5 + 9 * app.cellSize,
                            fill='NavajoWhite1',
                            width=0)

    # text for playing against AI
    canvas.create_text(app.margin + 4.125 * app.cellSize,
                       app.height // 5 + 8 * app.cellSize,
                       text="Play Online",
                       font='Helvetica 30',
                       fill='grey8')
    
def drawGameplay(app, canvas):
    # background
    canvas.create_rectangle(0,0, app.width, app.height, fill='tan')
    # Title
    canvas.create_text(app.width//2,
                       app.cellSize//1.5,
                       text='Reversi.AI',
                       font='Helvetica 40 italic',
                       fill='mint cream')
    drawBoard(app, canvas)
    drawPieces(app, canvas)
    drawAllPotentialPieces(app, canvas)
    
    drawScore(app,canvas)
    
    if app.gameOver:
        drawGameOver(app, canvas)
        
    # draw home button
    # Image CITATION: https://icons8.com/icons/set/home
    canvas.create_image(app.width - app.cellSize, 
                        app.cellSize//1.5, 
                        image=ImageTk.PhotoImage(app.homeImg))
    
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
    # circle
    canvas.create_oval(app.margin + 1*app.cellSize,
                       app.margin + 8.5*app.cellSize, 
                       app.margin + 2*app.cellSize,
                       app.margin + 9.5*app.cellSize,
                       fill="gray8",
                       width=0)
    # text in circle
    canvas.create_text(app.margin + 1.5*app.cellSize, 
                       app.margin + 9*app.cellSize,
                       text="Player 1",
                       fill='mint cream')
    # display player1 score
    canvas.create_text(app.margin + 1.5*app.cellSize, 
                       app.margin + 10*app.cellSize,
                       text=app.player1.pieces,
                       font='Helvetica 26 bold', 
                       fill='black')

    if app.turn.number == 1:
        # create arrow for player1
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
        # create arrow for player2
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
    
    # circle player2
    canvas.create_oval(app.margin + 6*app.cellSize,
                       app.margin + 8.5*app.cellSize, 
                       app.margin + 7*app.cellSize, 
                       app.margin + 9.5*app.cellSize,
                       fill="mint cream",
                       width=0)
    # text in circle
    canvas.create_text(app.margin +6.5*app.cellSize, 
                       app.margin + 9*app.cellSize,
                       text="Player 2", fill='black')
    # display player2 score
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
    app.turn.getAllPossiblePositions(app.board)
    for position in app.turn.possibleMoves:
        drawPotentialPiece(app, canvas, position[0], position[1], 'grey70')

def drawPotentialPiece(app, canvas, row_num, col_num, color):
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
    
# create slider for AI difficulty
def drawSlider(app, canvas):
    x, y = app.drawSliderCircle
    canvas.create_oval(x - app.cellSize//2,
                       y - app.cellSize//2,
                       x + app.cellSize//2,
                       y + app.cellSize//2,
                       fill="black",
                       width=0)
    
    if not app.drawSliderCircleBool:
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
    
    # check if the mouse is within the box
    check = False
    if (x >= app.margin + 0.5*app.cellSize and
        x <= app.margin + 8*app.cellSize and
        y >= app.margin + 6*app.cellSize and
        y <= app.margin + 6.5*app.cellSize):
        app.drawSliderCircleBool = True
        check = True
        
    # determine the depth of minimax AI
    if app.drawSlider == True and check == True:
        app.drawSliderCircle = (x, app.margin + 6.25*app.cellSize)
        app.sliderX = int(((x - (app.margin + 0.5*app.cellSize))
                           // app.cellSize))
    
def mousePressed(app, event):
    x, y = event.x, event.y
    if app.home:
        if (app.margin + 1.125*app.cellSize <= x <= app.margin + 7 * app.cellSize and
                app.height // 5 + app.cellSize <= y <= app.height // 5 + 3 * app.cellSize):
            app.board = copy.deepcopy(app.emptyBoard)
            app.player2.board = copy.deepcopy(app.emptyBoard)
            app.player1.board = copy.deepcopy(app.emptyBoard)
            app.gamePlay = True
            app.home = False
        elif (app.margin + 1.125 * app.cellSize <= x <= app.margin + 7 * app.cellSize and
              app.height // 5 + 4 * app.cellSize <= y <= app.height // 5 + 6 * app.cellSize):
            app.board = copy.deepcopy(app.emptyBoard)
            app.player2.board = copy.deepcopy(app.emptyBoard)
            app.player1.board = copy.deepcopy(app.emptyBoard)
            app.home = False
            app.selectDifficulty = True
        elif (app.margin + 1.125 * app.cellSize <= x <= app.margin + 7 * app.cellSize and
              app.height // 5 + 7 * app.cellSize <= y <= app.height // 5 + 9 * app.cellSize):
            app.board = copy.deepcopy(app.emptyBoard)
            app.player2.board = copy.deepcopy(app.emptyBoard)
            app.player1.board = copy.deepcopy(app.emptyBoard)
            app.home = False
            # uncomment to play online version
            # app.network = True
            # app.player1.network = True
            # app.player2.network = True
            app.gamePlay = True
                
    if app.selectDifficulty:
        if (app.margin + 1.25 * app.cellSize <= x <= app.margin + 7 * app.cellSize and
                app.margin + 8.75 * app.cellSize <= y <= app.margin + 10.25 * app.cellSize):
            app.board = copy.deepcopy(app.emptyBoard)
            app.player2.board = copy.deepcopy(app.emptyBoard)
            app.player1.board = copy.deepcopy(app.emptyBoard)
            app.MC = True
            app.AI = False
            app.gamePlay = True
            app.selectDifficulty = False


        if (app.margin + 1.25 * app.cellSize <= x <= app.margin + 7 * app.cellSize <=
                y <= app.margin + 8.5 * app.cellSize):
            app.board = copy.deepcopy(app.emptyBoard)
            app.player2.board = copy.deepcopy(app.emptyBoard)
            app.player1.board = copy.deepcopy(app.emptyBoard)
            app.AI = True
            app.MC = False
            app.gamePlay = True
            app.selectDifficulty = False

    if app.gameOver == False and app.home == False:
        
        #user clicks the home button
        if (app.width - app.cellSize - 1.5*15 <= x <= app.width - app.cellSize + 1.5*15 and
                app.cellSize // 1.5 - 1.5 * 15 <= y <= app.cellSize // 1.5 + 1.5 * 15):
            print("clicked home")
            app.board = copy.deepcopy(app.emptyBoard)
            app.player2.board = copy.deepcopy(app.emptyBoard)
            app.player1.board = copy.deepcopy(app.emptyBoard)
            app.player1.pieces = 2
            app.player2.pieces = 2
            app.MC = False
            app.AI = False
            app.gamePlay = False
            app.home = True

        # get the x and y value of the mouse press
        row_num = (x - app.margin) // app.cellSize
        col_num = (y - app.margin) // app.cellSize
        
        # check if the move is legal
        if isValid(app, x, y):
            # if legal: change the board pieces to your colour
            app.board = app.turn.play(col_num, row_num, app.board)

            # if in an online game
            if app.network:
                moves, board, pieces = app.turn.parseData(app.turn.sendData())
                setMoves = set()
                listBoard = []
                for move in moves.split("-"):
                    number = move.split(",")
                    if number[0] != '':
                        setMoves.add((int(number[0]), int(number[1].strip(" "))))
                i = 0
                for line in board.split("-"):
                    listBoard.append([])
                    for value in line.split(","):
                        if value != " " and value != '':
                            print(value)
                            listBoard[i].append(int(value.strip(" ")))
                    i += 1
                app.board = listBoard
                app.pieces = int(pieces)
                app.moves = setMoves
            
            # updates score for both
            app.player1.pieces = app.player1.getNumberOfPieces(app.board)
            app.player2.pieces = app.player2.getNumberOfPieces(app.board)
            
            if app.player1.pieces == 0 or app.player2.pieces == 0:
                app.gameOver = True
            
            # get total number of pieces
            total = app.player1.pieces + app.player2.pieces
            if total >= app.rows * app.cols:
                app.gameOver = True
                app.turn = app.player1

            # get all of opponent's moves
            turn = app.turn.number
            opponent = app.player1
            if turn == 1:
                opponent = app.player2
            elif turn == 2:
                opponent = app.player1
            # if opponent has no moves: don't change player turn
            # if opponent has moves: change player turn
            if len(opponent.getAllPossibleMoves(app.board)) != 0:
                app.turn = opponent
        runAI(app)

    else:
        if (app.margin + app.cellSize * 3 <= x <= app.margin + app.cellSize * 5 <=
                y <= app.margin + app.cellSize * 5.5):
            print("Clicked play again")
            app.board = copy.deepcopy(app.emptyBoard)
            app.player1.board = copy.deepcopy(app.emptyBoard)
            app.player2.board = copy.deepcopy(app.emptyBoard)
            app.gamePlay = True
            app.gameOver = False

# this checks if the coordinates of the play is legitimate
# corresponds to one of the possible moves the player can make
def isValid(app, x, y):
     # get the row_num and col_num of the mouse press
    row_num = (x - app.margin) // app.cellSize
    col_num = (y - app.margin) // app.cellSize
    
    # check if it is out of the board
    if (x <= app.margin or y <= app.margin or x >= 8*app.cellSize + 
        app.margin or y >= 8*app.cellSize + app.margin):
        return False

    # if there already is a piece there
    if app.board[col_num][row_num] != 0:
        return False
    movesAndLines = app.turn.getAllPossibleMoves(app.board)
    moves = set()
    for moveAndLine in movesAndLines:
        for key in moveAndLine:
            moves.add(key)
    if (col_num, row_num) in moves:
        return True
    else:
        return False

# RUN AI
def runAI(app):
    if app.AI:
        print("minimax AI started")
        # uncomment this to start random AI
        # randomAI(app, 2)
        if app.turn.number == 2:
            minimaxAI(app, app.player2)
    if app.MC:
        print("starting MC")
        if app.turn.number == 2:
            # specify number simulations here
            mctsMain(app, app.player2, app.sliderX * 20)

def runReversi():
    runApp(width=800, height=900)
    
def main():
    runReversi()

if __name__ == '__main__':
    main()