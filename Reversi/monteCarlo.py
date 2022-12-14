# MONTE CARLO SEARCH CITATION: Got the idea of MCTS from this video: https://www.youtube.com/watch?v=Fbs4lnGLS8M&ab_channel=FullstackAcademy
# MONTE CARLO CITATION: TOOK REFERENCE FROM THIS WEBSITE: https://ai-boson.github.io/mcts/
# UCT CITATION: TOOK UCT FROM THIS WEBSITE: https://royhung.com/reversi
# MONTE CARLO CITATION: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search

import copy
import random
import math
from gui import *

# Bad moves set (near corners that will allow for others to steal corners)
badMoves = {
    (0,1), (1,0), (1,1),
    (0,6), (1,6), (1,7),
    (6,7), (6,6), (7,6),
    (6,1), (7,1), (6,0)
}
# Good Moves set (all the corners and sides except those adjacent to corners)
goodMoves = {
    (0,0), (0,7), (7,7), (7,0),
    (2,0), (3,0), (4,0), (5,0),
    (0,2), (0,3), (0,4), (0,5),
    (2,7), (3,7), (4,7), (5,7),
    (7,2), (7,3), (7,4), (7,5)
}

# Creating class for every node of the trr
class Node:
    def __init__(self, move = None, parent = None, board = None, turn = None):
        self.turn = turn
        self.board = board
        self.move = move
        self.parent = parent
        self.untriedMoves = []
        self.untriedMoves = list(self.turn.getAllPossiblePositions(self.board))
        self.children = []
        self.wins = 0
        self.visits = 0

    # add child to any node
    def addChildNode(self, move, turn, board):
        # declare a new child object
        child = Node(move = move, parent = self, board = board, turn = turn)
        # move has already been tried
        self.untriedMoves.remove(move)
        self.children.append(child)
        print("adding child")
        return child

    # select the best child for a child using UCT
    def uct(self, originalTurn):
        val = 0
        largest = self.children[0]
        largestValue = -9999
        # if it is the same color as starting piece
        if originalTurn == self.turn:
            for child in self.children:
                val = child.wins/child.visits + math.sqrt(math.log1p(self.visits)/child.visits)
                if val > largestValue:
                    largestValue = val
                    largest = child
        else:
            for child in self.children:
                val = 1 - (child.wins/child.visits + math.sqrt(math.log1p(self.visits)/child.visits))
                if val > largestValue:
                    largestValue = val
                    largest = child
        return largest
def backPropagate(n, win):
    n.visits += 1
    if win:
        n.wins += 1
    # if the node has a parent, push the result all the way to the top
    if n.parent:
        backPropagate(n.parent, win)
def mcts(app, rootTurn, simulations):
    # declare root node
    turn = copy.deepcopy(rootTurn)
    board = copy.deepcopy(app.board)
    rootNode = Node(board=board, turn=rootTurn)
    node = rootNode

    # repeat for the number of simulations
    for i in range(simulations):
        # print(f"number of simulations: {i}")
        node = rootNode
        board = copy.deepcopy(app.board)

        # SELECT move to play
        # check if all moves has already been tried, if yes select one using uct and actually play it
        while node.untriedMoves == [] and node.children != []:
            node = node.uct(turn)
            if app.turn.number == 2:
                board = turn.play(node.move[0], node.move[1], board)
            # change turn
            if turn.number == 1:
                # check for number of moves
                moves = app.player2.getAllPossiblePositions(app.board)
                if len(moves) == 0:
                    turn = app.player1
                else:
                    turn = app.player2
            else:
                moves = app.player1.getAllPossiblePositions(app.board)
                if len(moves) == 0:
                    turn = app.player2
                else:
                    turn = app.player1

        # EXPAND
        # expansion of the tree nodes, add new node to the starting node
        # if there are still untried moves, try a random move in the untried moves
        while node.untriedMoves:
            randomMove = random.choice(node.untriedMoves)

            # play the move
            board = turn.play(randomMove[0], randomMove[1], board)

            # add the random move as one of the children and move to that node
            node = node.addChildNode(move=randomMove, board=board, turn=turn)

        # SIMULATION
        # rollout of the tree, make all moves from that node
        # while the node is not a terminal node
        # noticed that the AI selects randomly -> include some psuedo random selection to prevent this
        while True:
            possibleMovesSet = turn.getAllPossiblePositions(board)
            possibleMoves = list(possibleMovesSet)
            # if possible moves still exists, means game is not over, then continue
            if possibleMoves:
                # prioritise good moves
                for goodMove in goodMoves:
                    if goodMove in possibleMovesSet:
                        board = turn.play(goodMove[0], goodMove[1], board)
                        continue
                # if not choose a random move
                randomMove = random.choice(possibleMoves)
                # if random move is bad, choose again
                if randomMove in badMoves:
                    randomMove = random.choice(possibleMoves)
                board = turn.play(randomMove[0], randomMove[1], board)
                # after playing a move switch turns
                if turn.number == 1:
                    # check for number of moves
                    moves = app.player2.getAllPossiblePositions(board)
                    if len(moves) == 0:
                        turn = app.player1
                    else:
                        turn = app.player2
                else:
                    moves = app.player1.getAllPossiblePositions(board)
                    if len(moves) == 0:
                        turn = app.player2
                    else:
                        turn = app.player1
                # don't go to the else statement
                continue
            # if there are no more possible moves, means game has ended, then check what is the result
            else:
                if rootTurn.number == 1:
                    if app.player1.pieces > app.player2.pieces:
                        # player 1 won
                        backPropagate(node, True)
                    backPropagate(node, False)
                    board = copy.deepcopy(app.board)
                    break
                else:
                    if app.player2.pieces > app.player1.pieces:
                        backPropagate(node, True)
                    backPropagate(node, False)
                    board = copy.deepcopy(app.board)
                    break

    # return the child node with the highest wins because it means that it is the best
    highestWins = -999
    bestNode = rootNode
    for childNode in rootNode.children:
        if childNode.wins > highestWins:
            highestWins = childNode.wins
            bestNode = childNode
    return bestNode

def mctsMain(app, rootTurn, simulations):
    selectedNode = mcts(app, rootTurn, simulations)
    app.board = rootTurn.play(selectedNode.move[0], selectedNode.move[1], app.board)

    # check for end game after placing a piece
    check = True

    # check if the whole board has been filled up, if yes end game
    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            if app.board[i][j] == 0:
                check = False
    app.gameOver = check

    # switch turns
    if rootTurn.number == 1:
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