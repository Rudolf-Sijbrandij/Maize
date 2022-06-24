from random import *


def unvisited_neighbour(rows, columns, cur, vis, maze_type, dif, maze):
    """
    Kijkt in alle 4 richtingen; omhoog, omlaag, links en rechts, of er een stap die richting in gemaakt kan worden
    zo niet, returned de functie [[-1, -1], [-1, -1]] en weet het programma dat hij terug moet totdat hij weer ergens
    anders wel verder kan. Als hij wel verder kan, dan returned hij de coördinaten van de nieuwe cell.

    Args:
        rows (int):     De hoeveelheid rows die de gebruiker heeft opgegeven voor de grootte van de maze.
        columns (int):  De hoeveelheid columns die de gebruiker heeft opgegeven voor de grootte van de maze.
        cur (list):     De coördinaten van de huidige cell waarvoor je naar neighbours kijkt.
        vis (list):     Een lijst van coördinaten van al eerder bezochte cellen.
        maze_type (int):De maze type, als het 0 is is het een normale maze, als het 1 is is het een disjointed maze.
                            Alleen relevant als het om het generaten van een maze gaat
        dif (int):      Een getal, 0 of 1, dat aangeeft of de functie wordt gebruikt door de dfs() functie of door
                            de Tremaux() functie, gaat erom of er stappen van 1 of van 2 gemaakt worden.
        maze (list):    Alleen relevant voor Tremaux, laat de functie kijken of de stap die hij maakt wel op het pad is
                            en niet door een muur heen gaat

    Returns:
        list:   Een lijst met coordinaten van een neighbour 1 stap verder en 2 stappen verder
                    of als er geen geldige neighbours zijn een lijst met 2x [-1, -1] die aangeeft dat het programma
                    weer terug moet omdat het doodloopt of niet verder kan
    """
    curx = cur[0]
    cury = cur[1]
    up = [[curx, cury - 2], [curx, cury - 1]]
    down = [[curx, cury + 2], [curx, cury + 1]]
    right = [[curx + 2, cury], [curx + 1, cury]]
    left = [[curx - 2, cury], [curx - 1, cury]]
    neighbors = [down, up, right, left]
    shuffle(neighbors)
    for neighbor in neighbors:
        check = True
        if neighbor[dif][0] < 0 or neighbor[dif][1] < 0:
            check = False
        elif neighbor[dif][0] > rows - 1 or neighbor[dif][1] > columns - 1:
            check = False
        if maze_type == 1:
            rand = randrange(0, int(((rows + columns / 2) / 1.5)))
            if (neighbor[dif] not in vis or rand == 1) and check:
                return neighbor
        elif dif == 1:
            if neighbor[dif] not in vis and check and maze[neighbor[dif][0]][neighbor[dif][1]] == 1:
                return neighbor
        else:
            if neighbor[dif] not in vis and check:
                return neighbor
    return [[-1, -1], [-1, -1]]


def dfs(rows, columns, maze_type):
    """
    Doormiddel van de dimensies van de gebruiker maakt het algoritme een doolhof doormiddel van het
    Depth First Search maze generation algoritme.

    Args:
        rows (int): De hoeveelheid rows die de gebruiker heeft opgegeven voor de grootte van de maze
        columns (int): De hoeveelheid columns die de gebruiker heeft opgegeven voor de grootte van de maze
        maze_type (int): De maze type, als het 0 is is het een normale maze, als het 1 is is het een disjointed maze

    Returns:
        list: een maze waar muren 0 zijn en paden 1
    """
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
            neighbor_list = unvisited_neighbour(rows, columns, current, visited,maze_type, 0, maze)
            nextcell = neighbor_list[0]
            wall = neighbor_list[1]
            stack.append(nextcell)
            visited.append(current)
            current = nextcell
            maze[current[0]][current[1]] = 1
            maze[wall[0]][wall[1]] = 1
    return maze


def solver(maze):
    """
    Zoekt een pad naar het einde van de maze vanaf het begin doormiddel van depth first search maze solving algorithm.
    Maakt gebruik van een eerder gemaakte maze van het maze generation algorithm.

    Args:
        maze (list): Een lijst met de opbouw [rows[columns]] waar 0 een muur is en 1 een pad.

    Returns:
        list: een lijst van coördinaten van het pad naar het einde van de maze.
    """
    current = [0, 0]
    solution = [current]
    visited = []
    rows = len(maze)
    columns = len(maze[0])
    while current != [rows - 1, columns - 1]:
        current = solution[len(solution) - 1]
        solution.pop()
        while current != [-1, -1]:
            if current == [rows - 1, columns - 1]:
                return solution
            visited.append(current)
            nextcell = unvisited_neighbour(rows, columns, current, visited, 0, 1, maze)[1]
            if current not in solution and nextcell != [-1, -1]:
                solution.append(current)
            current = nextcell
            solution.append(current)
    return solution
