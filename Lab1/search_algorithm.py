from maze import Maze, Point, Dict
from heapq import heappush, heappop


class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Stack:
    def __init__(self):
        self.items = []

    @property
    def is_empty(self):
        return self.items == []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()


class Queue:
    def __init__(self):
        self.items = []

    @property
    def is_empty(self):
        return self.items == []

    def enqueue(self, x):
        self.items.insert(0, x)

    def dequeue(self):
        return self.items.pop()


class PriorityQueue:
    def __init__(self):
        self.items = []

    @property
    def is_empty(self):
        return self.items == []

    def enqueue(self, x):
        heappush(self.items, x)

    def dequeue(self):
        return heappop(self.items)


def dfs(m: Maze, start):
    frontier: Stack[Node] = Stack()
    p = Node(start)
    frontier.push(p)
    state: set = {start}

    while not frontier.is_empty:
        current_node = frontier.pop()
        current_state = current_node.state

        if current_state == m.end:
            return current_node

        for neighbor in m.valid_path(current_state):
            if neighbor not in state:
                frontier.push(Node(neighbor, current_node))
                state.add(neighbor)

    return None


def bfs(m: Maze, start):
    frontier: Queue[Node] = Queue()
    p = Node(start)
    frontier.enqueue(p)
    state: set = {start}

    while not frontier.is_empty:
        current_node = frontier.dequeue()
        current_state = current_node.state

        if current_state == m.end:
            return current_node

        for neighbor in m.valid_path(current_state):
            if neighbor not in state:
                frontier.enqueue(Node(neighbor, current_node))
                state.add(neighbor)

    return None


def greedy(m: Maze, start, distance):
    frontier: PriorityQueue[Node] = PriorityQueue()
    p = Node(start, None, 0, distance(start))
    frontier.enqueue(p)
    explored = set()

    while not frontier.is_empty:
        current_node = frontier.dequeue()
        current_state = current_node.state
        explored.add(current_state)

        if current_state == m.end:
            return current_node

        for neighbor in m.valid_path(current_state):
            if neighbor not in explored:
                frontier.enqueue(Node(neighbor, current_node, 0, distance(neighbor)))

    return None


def AStar(m: Maze, start, distance):
    frontier: PriorityQueue[Node] = PriorityQueue()
    p = Node(start, None, 0, distance(start))
    frontier.enqueue(p)
    state: dict = {start: 0}

    while not frontier.is_empty:
        current_node = frontier.dequeue()
        current_state = current_node.state

        if current_state == m.end:
            return current_node

        for neighbor in m.valid_path(current_state):
            cost = current_node.cost + 1
            if neighbor not in state or (neighbor in state and cost < state[neighbor]):
                state[neighbor] = cost
                frontier.enqueue(Node(neighbor, current_node, cost, distance(neighbor)))

    return None


def Bonus_AStart(m: Maze, start, distance):
    frontier: PriorityQueue[Node] = PriorityQueue()
    p = Node(start, None, 0, distance(start))
    frontier.enqueue(p)
    bonus_points_dict = m.bonus_points_dict.copy()

    frontier_state: dict = {start: 0}

    while not frontier.is_empty:
        current_node = frontier.dequeue()
        current_state = current_node.state

        if current_state == m.end:
            return current_node

        for neighbor in m.valid_path(current_state):
            cost = current_node.cost + m.weight(neighbor, bonus_points_dict)
            if neighbor not in frontier_state or (neighbor in frontier_state and frontier_state[neighbor] > cost):
                frontier_state[neighbor] = cost
                frontier.enqueue(Node(neighbor, current_node, cost, distance(neighbor)))

    return None


def find_path(node, dict: Dict[Point, float] = None):
    path: List = []
    if dict != None:
        bonus_points_dict = dict.copy()
    path_cost = 0
    if node is not None:
        path.append(node.state)
        if dict != None and node.state in bonus_points_dict.keys():
            path_cost = path_cost + bonus_points_dict[node.state] - 1
            del bonus_points_dict[node.state]

    while node.parent is not None:
        node = node.parent
        path.append(node.state)
        if dict != None and node.state in bonus_points_dict.keys():
            path_cost = path_cost + bonus_points_dict[node.state] - 1
            del bonus_points_dict[node.state]
    path.reverse()

    path_cost = path_cost + len(path) - 1
    return path, path_cost
