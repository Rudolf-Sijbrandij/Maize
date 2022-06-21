from random import *


def dfs(rows, columns):
    def unvisited_neighbor(cur, vis):
        curx = cur[0]
        cury = cur[1]
        neighbors = [[curx - 2, cury], [curx, cury + 2], [curx + 2, cury], [curx, cury - 2]]
        shuffle(neighbors)
        for neighbor in neighbors:
            check = True
            if neighbor[0] < 0 or neighbor[1] < 0:
                check = False
            elif neighbor[0] > rows - 1 or neighbor[1] > columns - 1:
                check = False
            if neighbor not in vis and check:
                return neighbor
        return [-1, -1]

    maze = []
    stack = []
    visited = []
    for x in range(rows):
        maze.append([])
        for y in range(columns):
            maze[x].append(0)
    stack.append([0, 0])
    visited.append([0, 0])
    while len(stack) != 0:
        current = stack[len(stack)-1]
        maze[current[0]][current[1]] = 1
        stack.pop()
        while current != [-1, -1]:
            nextcell = unvisited_neighbor(current, visited)
            stack.append(nextcell)
            visited.append(current)
            if (current[0] - nextcell[0]) != 0 or (nextcell[0] - current[0]) != 0:
                wall = [int((nextcell[0] + current[0]) / 2), nextcell[1]]
            else:
                wall = [nextcell[0], int((nextcell[1] + current[1]) / 2)]
            current = nextcell
            maze[current[0]][current[1]] = 1
            maze[wall[0]][wall[1]] = 1
    return maze
