from cmu_112_graphics import *
from main import *
from randomAI import *
from minimax import *
from monteCarlo import *
   
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
    app.MC = False
    
    #home icon
    app.imagehome = app.loadImage('home.png')
    app.homeImg = app.scaleImage(app.imagehome, 1.5)
    
    #confirm message if the user really wants to return to home
    app.confirmReturn = False
    app.confirmedReturn = False
    
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
        
    #play button
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
                       text="Play",
                       fill="grey8",
                       font="Helvetica 30")

    #play text
    canvas.create_text(app.margin +  4.125 * app.cellSize,
                       app.margin + 9.5 * app.cellSize,
                       text="Extra Hard Mode",
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
    #draw confirm message if home button pressed
    if app.confirmReturn:
        drawConfirmMessage(app, canvas)
    
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
    
    if app.gameOver:
        drawGameOver(app, canvas)
        
    #draw home button
    canvas.create_image(app.width - app.cellSize, 
                        app.cellSize//1.5, 
                        image=ImageTk.PhotoImage(app.homeImg))
        
def drawConfirmMessage(app, canvas):
    print('entered')
    canvas.create_rectangle(app.margin + app.cellSize*1.5, 
                        app.margin + app.cellSize*1.5,
                        app.margin + app.cellSize*6.5,
                        app.margin + app.cellSize*6.5,
                        fill="tan",
                        width=0)
    
    canvas.create_text(app.margin + app.cellSize*4,
                    app.margin + app.cellSize*2,
                    text=f"Are you sure you would like to return?",
                    font='Helvetica 30 italic bold',
                    fill='gray8')
    
    canvas.create_text(app.margin + app.cellSize*4,
                    app.margin + app.cellSize*3,
                    text=f"All of your progress will be lost",
                    font='Helvetica 20 italic bold',
                    fill='gray8')
    
    canvas.create_rectangle(app.margin + app.cellSize*3,
                        app.margin + app.cellSize*5,
                        app.margin + app.cellSize*5,
                        app.margin + app.cellSize*5.5,
                        fill='mint cream')
    
    canvas.create_text(app.margin + app.cellSize*4,
                            app.margin+ app.cellSize*5.25,
                            text="Return Home",
                            fill='gray8',
                            font='Helvetica 18 italic bold')
    
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
    # print(f 'possible Moves: {app.turn.possibleMoves}')
    for position in app.turn.possibleMoves:
        drawPotentialPiece(app, canvas, position[0], position[1], 'grey70')

def drawPotentialPiece(app, canvas, row_num, col_num, color):
    # print(f 'row and col: {row_num}, {col_num}')
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
            y >= app.margin + 8.75 * app.cellSize and
            y <= app.margin + 10.25 * app.cellSize):
            app.MC = True
            app.gamePlay = True
            app.selectDifficulty = False


        if (x >= app.margin + 1.25 * app.cellSize and
            x <= app.margin + 7 * app.cellSize and
            y >= app.margin + 7 * app.cellSize and
            y <= app.margin + 8.5 * app.cellSize):
            app.AI = True
            app.gamePlay = True
            app.selectDifficulty = False
    
    
    if app.gameOver == False and app.home == False:
        
        #user clicks the home button
        if (x >= app.width - app.cellSize - 1.5*15 and 
            x <= app.width - app.cellSize + 1.5*15 and
            y >= app.cellSize//1.5 - 1.5*15 and
            y <= app.cellSize//1.5 + 1.5*15):
                # app.confirmReturn = True
                app.board = app.emptyBoard
                app.gamePlay = False
                app.home = True
                # app.confirmedReturn = False
                # app.confirmReturn = False
            
        # if app.confirmReturn == True:
        #     #user clicks on confirm return
        #     if (x >= app.margin + app.cellSize*3 and 
        #         y >= app.margin + app.cellSize*5 and
        #         x <= app.margin + app.cellSize*5 and
        #         y <= app.margin + app.cellSize*5.5):
        #             app.confirmedReturn = True
        #     else:
        #         app.confirmReturn = False
                    
        # if app.confirmedReturn == True:
        #     app.board = app.emptyBoard
        #     app.gamePlay = False
        #     app.confirmedReturn = False
        #     app.confirmReturn = False
        #     app.gamePlay = False
        #     app.home = True
        # else:
        #     app.confirmReturn = False
            
        # get the x and y value of the mouse press
        row_num = (x - app.margin) // app.cellSize
        col_num = (y - app.margin) // app.cellSize
        
        # check if the move is legal
        if isValid(app, x, y):
            # if legal: change the board pieces to your colour
            app.board = app.turn.play(col_num, row_num, app.board)
            # print(f 'playing move {col_num}, {row_num}')
            
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
            # if opponent has no moves: dont change player turn
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

# RUN AI
def runAI(app):
    if app.AI:
        print("minimax AI started")
        # randomAI(app, 2)
        if app.turn.number == 2:
            minimaxAI(app, app.player2)
    if app.MC:
        print("starting MC")
        if app.turn.number == 2:
            # specify number simulations here
            mctsMain(app, app.player2, 100)
        
def runReversi():
    runApp(width=800, height=900)
    
def main():
    runReversi()

if __name__ == '__main__':
    main()