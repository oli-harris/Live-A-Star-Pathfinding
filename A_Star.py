from time import time
from itertools import product


def distance(xy1, xy2): return int(
    round(((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2)**0.5, 1)*10)


class Node():
    def __init__(self, xy, startNode, endNode):
        self.value = xy
        self.fCost = distance(self.value, startNode) + \
            distance(self.value, endNode)
        self.parents = [xy]

    def pos(self):
        return self.value

    def addParents(self, parents):
        self.parents += parents

    def getParents(self):
        return self.parents


class AStar():
    def __init__(self, maze, gridSizeX, gridSizeY):
        self.maze = maze
        self.start = [[index, row.index(2)]
                      for index, row in enumerate(maze) if 2 in row][0]
        self.end = [[index, row.index(3)]
                    for index, row in enumerate(maze) if 3 in row][0]
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY

    def neighbours(self, xy): return [[x2, y2] for x2 in range(xy[0]-1, xy[0]+2)
                                      for y2 in range(xy[1]-1, xy[1]+2)
                                      if (-1 < xy[0] < self.gridSizeX and
                                          -1 < xy[1] < self.gridSizeY and
                                          (xy[0] != x2 or xy[1] != y2) and
                                          (0 <= x2 < self.gridSizeX) and
                                          (0 <= y2 < self.gridSizeY) and
                                          self.maze[x2][y2] != 1 and
                                          [x2, y2] not in [x.pos() for x in self.closedList])]

    def calc(self):
        time0 = time()
        val = 0
        openList = []  # the set of nodes to be evaluated

        self.closedList = set()  # the set of nodes already evaluated
        openList.append(Node(self.start, self.start, self.end))

        while len(openList) > 0:
            openList.sort(key=lambda x: x.fCost)
            current = openList[0]
            del openList[0]
            self.closedList.add(current)

            if current.pos() == self.end:
                return current.getParents()

            neighbours = self.neighbours(current.pos())
            for neighbour in neighbours:
                neighbour = Node(neighbour, current.pos(), self.end)

                notInOpenList = neighbour.pos() not in [
                    x.pos() for x in openList]

                if neighbour.fCost < current.fCost or notInOpenList:
                    neighbour.addParents(current.getParents())
                    if notInOpenList:
                        openList.append(neighbour)

        raise ValueError('Unsolvable Maze')
