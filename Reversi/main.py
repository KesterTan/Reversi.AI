from network import Network
from gui import *

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
        self.network = False
        self.possibleMoves = set()

        # uncomment to play online version
        # self.net = Network()
    
    # gets number of pieces
    def getNumberOfPieces(self, board):
        self.pieces = 0
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == self.number:
                    self.pieces += 1
        return self.pieces
    
    # get the position of the pieces
    def getPiecesPosition(self, board):
        self.board = board
        self.positions = set()
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == self.number:
                    self.positions.add((y,x))
        return self.positions
                    
    # get lists of pieces that are captured: lists are used here cause they need to be ordered
    def getPossibleLines(self, x, y):
        # find uninterrupted lines from every direction from a selected piece that the player has (set of array of tuples of captured pieces)
        lines = []
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
                if (posX < 0 or posY < 0 or posX >= self.cols
                        or posY >= self.rows):
                    break
                # if it is itself
                elif self.board[posX][posY] == self.number:
                    break
                # if it is empty, then it is also possible
                # this is also the 'moves' you want to save
                elif self.board[posX][posY] == 0:
                    endPoint = (posX, posY)
                    possible = True
                    if line:
                        res[endPoint] = line
                    break
                # if it is an enemy piece, continue adding 1, and save the line
                else:
                    line.append((posX, posY))
                    posX += xMove
                    posY += yMove
            # only if it is possible to place a piece (there isn't a line of long enemy pieces till the end) and there is a line
            if len(res) != 0 and possible == True:
                lines.append(res)
        return lines
                                    
    def getAllPossibleMoves(self, board):
        self.board = board
        self.moves = []
        positions = self.getPiecesPosition(board)
        for x, y in positions:
            lines = self.getPossibleLines(x, y)
            if lines:
                self.moves += lines
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
        for moveAndLine in movesAndLines:
            for key in moveAndLine:
                if key == (x, y):
                    line += moveAndLine[key]
        
        for (a, b) in line:
            self.board[a][b] = self.number
        
        # return the new board
        return self.board

    # CITATION: adapted from https://github.com/techwithtim/Network-Game-Tutorial/blob/master/game.py
    def sendData(self):
        # send data about all possible moves, all positions, score to the server
        moves = self.getAllPossiblePositions(self.board)
        sendBoard = self.board
        score = self.pieces
        str_move = ""
        str_board = ""
        for move in moves:
            move = str(move).strip(")")
            str_move = str_move + move.strip("(") + "-"
        for line in sendBoard:
            line = str(line).strip("]")
            str_board = str_board + line.strip("[") + "-"
        data = str_move + ":" + str_board + ":" + str(score)
        reply = self.net.send(data)
        return reply

    # CITATION: adapted from https://github.com/techwithtim/Network-Game-Tutorial/blob/master/game.py
    @staticmethod
    def parseData(data):
        moves = set()
        newBoard = []
        score = 0
        try:
            d = data.split(":")
            moves = d[0]
            newBoard = d[1]
            score = int(d[2])
            return moves, newBoard, score
        except:
            return moves, newBoard, score