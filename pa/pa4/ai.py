from __future__ import absolute_import, division, print_function
from math import sqrt, log
from game import Game, WHITE, BLACK, EMPTY
import copy
import time
import random

class Node:
    # NOTE: modifying this block is not recommended
    def __init__(self, state, actions, parent=None):
        self.state = (state[0], copy.deepcopy(state[1]))
        self.num_wins = 0 #number of wins at the node
        self.num_visits = 0 #number of visits of the node
        self.parent = parent #parent node of the current node
        self.children = [] #store actions and children nodes in the tree as (action, node) tuples
        self.untried_actions = copy.deepcopy(actions) #store actions that have not been tried

# NOTE: deterministic_test() requires BUDGET = 1000
#   You can try higher or lower values to see how the AI's strength changes
BUDGET = 1000

class AI:
    # NOTE: modifying this block is not recommended
    def __init__(self, state):
        self.simulator = Game()
        self.simulator.reset(*state) #using * to unpack the state tuple
        self.root = Node(state, self.simulator.get_actions())

    def mcts_search(self):
        #TODO: Main MCTS loop

        iters = 0
        action_win_rates = {} #store the table of actions and their ucb values

        while(iters < BUDGET):
            if ((iters + 1) % 100 == 0):
                # NOTE: if your terminal driver doesn't support carriage returns
                #   you can use: print("{}/{}".format(iters + 1, BUDGET))
                print("\riters/budget: {}/{}".format(iters + 1, BUDGET), end="")
            self.simulator.reset(*self.root.state)
            node = self.select(self.root)
            rollout = self.rollout(node)
            self.backpropagate(node, rollout)
            # self.simulator.reset(self.root.state[0], self.root.state[1])  # (player , grid)
            # TODO: select a node, rollout, and backpropagate

            iters += 1
        print()

        # Note: Return the best action, and the table of actions and their win values 
        #   For that we simply need to use best_child and set c=0 as return values
        _, action, action_win_rates = self.best_child(self.root, 0)
        return action, action_win_rates

    def select(self, node):
        # while node is not terminal
        while not self.simulator.game_over:
            if len(node.untried_actions) != 0:
                return self.expand(node)
            else:
                node, _, _ = self.best_child(node, 1)

        # while node is not None: #As explained in Slack, ignore this line and follow pseudocode
        # NOTE: deterministic_test() requires using c=1 for best_child()
        #
        return node

    def expand(self, node):
        # TODO: add a new child node from an untried action and return this new node

        child_node = None #choose a child node to grow the search tree

        # IMPORTANT: use the following method to fetch the next untried action
        #   so that the order of action expansion is consistent with the test cases
        # print ("previous", node.state[0])

        # reset the node state
        self.simulator.reset(*node.state)
        action = node.untried_actions.pop(0)
        # place the action on the grid 
        self.simulator.place(action[0], action[1])
        # get child node 
        child_node = Node(self.simulator.state(), self.simulator.get_actions())
        # self.simulator.state()
        # set current node as child node's parent
        child_node.parent = node
        # append child tuple to the children list
        child = (action, child_node)
        node.children.append(child)
        # NOTE: Make sure to add the new node to the node.children
        # NOTE: You may find the following methods useful:
        #   self.simulator.state()
        #   self.simulator.get_actions()
        return child_node

    def best_child(self, node, c): 
        # TODO: determine the best child and action by applying the UCB formula

        best_child_node = None #store the best child node with UCB
        best_action = None #store the action that leads to the best child
        action_ucb_table = {} #store the UCB values of each child node (for testing)

        max_value = 0
        # loop through the children list to get child's action and child node
        for child_action, child_node in node.children:
            # apply formula to calculate ucb value
            UCB = child_node.num_wins / child_node.num_visits + c*sqrt(2*log(node.num_visits) / child_node.num_visits)
            # add it to dict of ucb table 
            action_ucb_table[child_action] = UCB
            # check best child action and the node
            if max_value < UCB:
                max_value = UCB
                best_child_node = child_node
                best_action = child_action
        return best_child_node, best_action, action_ucb_table

    def backpropagate(self, node, result):
        while (node is not None):
            # TODO: backpropagate the information about winner
            # IMPORTANT: each node should store the number of wins for the player of its **parent** node
            node.num_visits += 1
            # check node is not root
            if node != self.root:
                # if parent color = winner's color then increament num_win
                if node.parent.state[0] == BLACK and result[BLACK] == 1: 
                   node.num_wins += 1
                elif node.parent.state[0] == WHITE and result[WHITE] == 1:
                    node.num_wins += 1
            node = node.parent

    def rollout(self, node):
        # TODO: rollout (called DefaultPolicy in the slides)

        # NOTE: you may find the following methods useful:
        #   self.simulator.reset(*node.state)
        #   self.simulator.game_over
        #   self.simulator.rand_move()
        #   self.simulator.place(r, c)
        # reset node state
        self.simulator.reset(*node.state)

        # loop untile it reach the terminal state
        while not self.simulator.game_over:
            r, c = self.simulator.rand_move()
            self.simulator.place(r, c)
        # Determine reward indicator from result of rollout
        reward = {}
        if self.simulator.winner == BLACK:
            reward[BLACK] = 1
            reward[WHITE] = 0
        elif self.simulator.winner == WHITE:
            reward[BLACK] = 0
            reward[WHITE] = 1
        return reward