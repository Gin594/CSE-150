from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modifying this __init__ function
    def __init__(self, state, current_depth, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.depth = current_depth
        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        # if no children, it is terminal state
        if len(self.children) == 0:
            return True
        else:
            return False

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modifying this __init__ function
    def __init__(self, root_state, depth): 
        self.root = Node(root_state, 0, MAX_PLAYER)
        self.depth = depth
        self.simulator = Game()
        self.simulator.board_size = len(root_state[0])

    # recursive function to build a game tree
    def build_tree(self, node=None):
        if node == None:
            node = self.root

        if node.depth == self.depth: 
            return 

        if node.player_type == MAX_PLAYER:
            # 4 poosible direction move
            for dir in range(4):
                # reset node state
                self.simulator.reset(*(node.state))
                self.simulator.move(dir)
                # check for unique tile matrix
                if (self.simulator.get_state() != node.state):
                    newNode = Node(self.simulator.get_state(), node.depth+1, CHANCE_PLAYER)
                    # add node to children list of tuple
                    node.children.append((dir, newNode))

            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)
            

        elif node.player_type == CHANCE_PLAYER:
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():

            # reset node
            self.simulator.reset(*(node.state))
            # get all open tiles
            open_tiles = self.simulator.get_open_tiles()
            for i in open_tiles:
                # copy node state
                nextState = copy.deepcopy(node.state[0])
                # put 2 in the open tile
                nextState[i[0]][i[1]] = 2
                # set new node
                newNode = Node((nextState, node.state[1]), node.depth+1, MAX_PLAYER)
                # add to children list of tuple
                node.children.append((None, newNode))

        for child in node.children:
            self.build_tree(child[1])

    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):

        if node == None:
            node = self.root

        if node.is_terminal():
            # return payoff
            return node.state

        elif node.player_type == MAX_PLAYER:
            # set value to negative infinity
            value = float("-inf")
            for n in node.children:
                decision = self.expectimax(n[1])
                # get max value
                if decision[1] > value:
                    value = decision[1]
                    # store the max value direction
                    direction = n[0]
            return (direction, value)

        elif node.player_type == CHANCE_PLAYER:
            value = 0
            for n in node.children:
                decision = self.expectimax(n[1])
                value += decision[1] * self.chance(node)
            return (None, value)

    # get the probability
    def chance(self, node):
        return 1.0 / len(node.children)

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        return random.randint(0, 3)



