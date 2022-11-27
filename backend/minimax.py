# black is mininimising (1)
# white is maximising (2)

from ..frontend.gui import *

# one for maxmimise and one for minimise

# function minimax(position, depth, maximizingPlayer):
    # if game over OR depth == end_depth
        # return evaluation of position (the score)
    
    # if it is the maximising player's turn:
        # set maxEval to -99999
        # for each child of position (for every possible move):
            # eval = minimax(child, depth+1, false)
            # maxEval = max(maxEval, eval)
        # return maxEval
    
    # else if it is the minimizing player's turn:
        # minEval = +9999999
        # for each child of position (for every possible move):
            # eval = minimax(child, depth-1, true)
            # minEval = min(minEval, eval)
        # return minEval