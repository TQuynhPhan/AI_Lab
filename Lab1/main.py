import os
import matplotlib.pyplot as plt
from maze import Maze, Point
from search_algorithm import dfs, bfs, greedy, AStar, find_path, Bonus_AStart


def find_start_end(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 'S':
                start = Point(i, j)

            elif matrix[i][j] == ' ':
                if (i == 0) or (i == len(matrix) - 1) or (j == 0) or (j == len(matrix[0]) - 1):
                    end = Point(i, j)
            else:
                pass
    return start, end


def read_file(file_name: str = 'maze.txt'):
    f = open(file_name, 'r')
    n_bonus_points = int(next(f)[:-1])

    bonus_points_dict: Dict[Point, float] = {}
    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        point = Point(x, y)
        bonus_points_dict[point] = reward

    text = f.read()
    matrix = [list(i) for i in text.splitlines()]
    f.close()

    row = len(matrix)
    col = len(matrix[0])

    start, exit = find_start_end(matrix)

    return matrix, row, col, start, exit, bonus_points_dict


def visualize_maze(matrix, bonus, start, end, route=None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    # 1. Define walls and array of direction based on the route
    walls = [(i, j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] == 'x']
    path = [(i, j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] == '*']

    if route:
        direction = []
        for i in range(1, len(route)):
            if route[i][0] - route[i - 1][0] > 0:
                direction.append('v')  # ^
            elif route[i][0] - route[i - 1][0] < 0:
                direction.append('^')  # v
            elif route[i][1] - route[i - 1][1] > 0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    # 2. Drawing the map
    ax = plt.figure(dpi=100).add_subplot(111)

    for i in ['top', 'bottom', 'right', 'left']:
        ax.spines[i].set_visible(False)

    # tường
    plt.scatter([i[1] for i in walls], [-i[0] for i in walls],
                marker='X', s=100, color='black')

    # path
    plt.scatter([i[1] for i in path], [-i[0] for i in path],
                marker='.', s=100, color='blue')

    # Điểm thưởng
    plt.scatter([i[1] for i in bonus], [-i[0] for i in bonus],
                marker='P', s=100, color='green')
    # start
    plt.scatter(start[1], -start[0], marker='*',
                s=100, color='gold')

    if route:
        for i in range(len(route) - 2):
            plt.scatter(route[i + 1][1], -route[i + 1][0],
                        marker=direction[i], color='silver')

    plt.text(end[1], -end[0], 'EXIT', color='red',
             horizontalalignment='center',
             verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')

    for _, point in enumerate(bonus):
        print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')


def maze_without_bonus_point():
    file_map1 = '../test/maze_map1.txt'
    file_map2 = '../test/maze_map2.txt'
    file_map3 = '../test/maze_map3.txt'
    file_map4 = '../test/maze_map4.txt'
    file_map5 = '../test/maze_map5.txt'
    print('press 1 to select maze_map1.txt')
    print('press 2 to select maze_map2.txt')
    print('press 3 to select maze_map3.txt')
    print('press 4 to select maze_map4.txt')
    print('press 5 to select maze_map5.txt')
    print('Defaut: 1')
    print("Select Maze Map File: ")
    mazeSelection = input()

    if mazeSelection == '2':
        filename = file_map2
    elif mazeSelection == '3':
        filename = file_map3
    elif mazeSelection == '4':
        filename = file_map4
    elif mazeSelection == '5':
        filename = file_map5
    else:
        filename = file_map1

    matrix, row, col, start, end, bonus_points_dict = read_file(filename)
    m: Maze = Maze(row, col, matrix, start, end, bonus_points_dict)

    bonus_points = []
    for key in bonus_points_dict.keys():
        reward = bonus_points_dict[key]
        bonus_points.append((key.x, key.y, reward))

    solve_dfs = dfs(m, m.start)
    if solve_dfs is None:
        print("Can't solve this maze using depth first search\n")
    else:
        path_dfs, path_cost_dfs = find_path(solve_dfs)
        visualize_maze(matrix, bonus_points, start, end, path_dfs)
        print("Cost of DFS search's path:", path_cost_dfs, "\n")

    solve_bfs = bfs(m, m.start)
    if solve_bfs is None:
        print("Can't solve this maze using breadth first search\n")
    else:
        path_bfs, path_cost_bfs = find_path(solve_bfs)
        visualize_maze(matrix, bonus_points, start, end, path_bfs)
        print("Cost of BFS search's path:", path_cost_bfs, "\n")

    solve_greedy_m = greedy(m, m.start, m.manhattan_distance)
    if solve_greedy_m is None:
        print("Can't solve this maze using greedy search (manhattan_distance)\n")
    else:
        path_greedy_m, path_cost_greedy_m = find_path(solve_greedy_m)
        visualize_maze(matrix, bonus_points, start, end, path_greedy_m)
        print("Cost of greedy search's (manhattan_distance) path:", path_cost_greedy_m, "\n")

    solve_greedy_e = greedy(m, m.start, m.euclidean_distance)
    if solve_greedy_e is None:
        print("Can't solve this maze using greedy search (euclidean_distance)\n")
    else:
        path_greedy_e, path_cost_greedy_e = find_path(solve_greedy_e)
        visualize_maze(matrix, bonus_points, start, end, path_greedy_e)
        print("Cost of greedy search's (euclidean_distance) path:", path_cost_greedy_e, "\n")

    solve_AStar_m = AStar(m, m.start, m.manhattan_distance)
    if solve_AStar_m is None:
        print("Can't solve this maze using A* search (manhattan_distance)\n")
    else:
        path_AStar_m, path_cost_AStar_m = find_path(solve_AStar_m)
        visualize_maze(matrix, bonus_points, start, end, path_AStar_m)
        print("Cost of A* search's (manhattan_distance) path:", path_cost_AStar_m, "\n")

    solve_AStar_e = AStar(m, m.start, m.euclidean_distance)
    if solve_AStar_e is None:
        print("Can't solve this maze using A* search (euclidean_distance)\n")
    else:
        path_AStar_e, path_cost_AStar_e = find_path(solve_AStar_e)
        visualize_maze(matrix, bonus_points, start, end, path_AStar_e)
        print("Cost of A* search's (euclidean_distance) path:", path_cost_AStar_e, "\n")


def maze_with_bonus_point():
    file_map1 = '../test/bonus_map1.txt'
    file_map2 = '../test/bonus_map2.txt'
    file_map3 = '../test/bonus_map3.txt'
    print('press 1 to select bonus_map1.txt')
    print('press 2 to select bonus_map2.txt')
    print('press 3 to select bonus_map3.txt')

    print('Defaut: 1')
    print("Select Maze Map File: ")
    mazeSelection = input()

    if mazeSelection == '2':
        filename = file_map2
    elif mazeSelection == '3':
        filename = file_map3
    else:
        filename = file_map1

    matrix, row, col, start, end, bonus_points_dict = read_file(filename)
    m: Maze = Maze(row, col, matrix, start, end, bonus_points_dict)

    bonus_points = []
    for key in bonus_points_dict.keys():
        reward = bonus_points_dict[key]
        bonus_points.append((key.x, key.y, reward))
    solve_Bonus_Astart_m = Bonus_AStart(m, m.start, m.manhattan_distance)
    if solve_Bonus_Astart_m is None:
        print("Can't solve this maze using a* search")
    else:
        path_Bonus_Astart_m, path_cost_Bonus_Astart_m = find_path(solve_Bonus_Astart_m, bonus_points_dict)
        visualize_maze(matrix, bonus_points, start, end, path_Bonus_Astart_m)
        print("Cost of bonus a* search's (manhattan_distance) path:", path_cost_Bonus_Astart_m)

    solve_Bonus_Astart_e = Bonus_AStart(m, m.start, m.euclidean_distance)
    if solve_Bonus_Astart_e is None:
        print("Can't solve this maze using a* search")
    else:
        path_Bonus_Astart_e, path_cost_Bonus_Astart_e = find_path(solve_Bonus_Astart_e, bonus_points_dict)
        visualize_maze(matrix, bonus_points, start, end, path_Bonus_Astart_e)
        print("Cost of bonus a* search's (euclidean_distance) path:", path_cost_Bonus_Astart_e)


if __name__ == "__main__":

    print('press 1 to select Maze without bonus point')
    print('press 2 to select Maze with bonus points')
    print('Defaut: 1')
    print("Select Maze Type: ")
    mazeSelection = input()

    filename = ''
    if mazeSelection == '2':
        print('Maze with bonus points')
        maze_with_bonus_point()
    else:
        print('Maze without bonus point')
        maze_without_bonus_point()


