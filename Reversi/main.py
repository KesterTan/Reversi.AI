
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
            if lines:
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
