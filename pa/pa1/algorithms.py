from __future__ import print_function
from heapq import *  # Hint: Use heappop and heappush

ACTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]


class Agent:
    def __init__(self, grid, start, goal, type):
        self.grid = grid
        self.start = start
        self.grid.nodes[start].start = True
        self.goal = goal
        self.grid.nodes[goal].goal = True
        self.final_cost = 0  # Make sure to update this value at the end of UCS and Astar
        self.search(type)

    def search(self, type):
        self.finished = False
        self.failed = False
        self.type = type
        self.previous = {}
        if self.type == "dfs":
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "ucs":
            self.frontier = []
            # push start node to the priority queue
            heappush(self.frontier, (0, self.start))
            self.explored = []
        elif self.type == "astar":
            self.frontier = []
            hValue = self.heuristic(self.start, self.grid.goal)
            heappush(self.frontier, (hValue, self.start))
            self.explored = []

    def show_result(self):
        current = self.goal
        while not current == self.start:
            current = self.previous[current]
            # This turns the color of the node to red
            self.grid.nodes[current].in_path = True

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()
    # DFS

    def dfs_step(self):
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.pop()
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        for node in children:
            if node in self.explored or node in self.frontier:
                continue
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                if not self.grid.nodes[node].puddle:
                    self.previous[node] = current
                    if node == self.goal:
                        self.finished = True
                    else:
                        self.frontier.append(node)
                        self.grid.nodes[node].frontier = True
    # Implement BFS here

    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        # get the current node
        current = self.frontier.pop()
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        # check for the children
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        for node in children:
            # check node, don't update if already explored
            if node in self.explored or node in self.frontier:
                continue
            # check for range whether the node is reachable
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                # check puddle
                if not self.grid.nodes[node].puddle:
                    # set predecessor
                    self.previous[node] = current
                    # check if match the goal
                    if node == self.goal:
                        self.finished = True
                    else:
                        # insert node into frontier
                        self.frontier.insert(0, node)
                        # mark node is in the frontier
                        self.grid.nodes[node].frontier = True

    # Implement UCS here
    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        # get the pair of the current node
        curPair = heappop(self.frontier)
        # get current node
        current = curPair[1]
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)

        # check for the children
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        for node in children:
            if node in self.explored or node in self.frontier:
                continue
            # check node in range
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                if not self.grid.nodes[node].puddle:
                    self.previous[node] = current
                    if node == self.goal:
                        self.finished = True
                    else:
                        isFirstVisit = True
                        # update cost
                        cost = curPair[0] + self.grid.nodes[node].cost()
                        # check if children already in frontier
                        for child in self.frontier:
                            if child[1] == node:
                                isFirstVisit = False
                                if cost < child[0]:
                                    # remove the higher cost item
                                    heappop[child]
                                    heappush(self.frontier, (cost, node))
                                    self.grid.nodes[node].frontier = True
                                    # update final_cost
                                    self.final_cost = cost
                                   
                        if isFirstVisit:
                            heappush(self.frontier, (cost, node))
                            self.grid.nodes[node].frontier = True
                            # update final_cost
                            self.final_cost = cost


    # define a heuristic function
    def heuristic(self, node_a, node_b):
        return (node_a[0] - node_b[0])**2 + (node_a[1] - node_b[1])**2

    # Implement Astar here
    def astar_step(self):
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        curPair = heappop(self.frontier)
        # current node
        current = curPair[1]
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        for node in children:
            if node in self.explored or node in self.frontier:
                continue
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                # check if not hit the puddle
                if not self.grid.nodes[node].puddle:
                    self.previous[node] = current
                    # if match the goal
                    if node == self.goal:
                        self.finished = True
                    else:
                        # update cost by using heuristic function
                        cost = curPair[0] + self.grid.nodes[node].cost() \
                                     + self.heuristic(node, self.grid.goal) \
                                     - self.heuristic(current, self.grid.goal)
                        heappush(self.frontier, (cost, node))
                        self.grid.nodes[node].frontier = True
                        # update final_cost
                        self.final_cost = cost
