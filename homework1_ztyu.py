############################################################
# ECS170: Uninformed Search
############################################################

student_name = "Zhongtian Yu  "

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
from collections import deque

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
        if n == 0:
            return 1
        total = n * n
        return math.factorial(total) / (math.factorial(n) * math.factorial(total - n))

def num_placements_one_per_row(n):
    if n == 0:
        return 0
    
    return n ** n


def n_queens_valid(board):
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                return False
    return True


def n_queens_helper(n, board):
    if len(board) == n:
        yield list(board)
    else:
        for col in range(n):
            new_board = board + [col]
            if n_queens_valid(new_board):
                yield from n_queens_helper(n, new_board)


def n_queens_solutions(n):
    yield from n_queens_helper(n, [])

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0

    def get_board(self):
        return [row[:] for row in self.board]

    def perform_move(self, row, col):
        for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.board[r][c] = not self.board[r][c]

    def scramble(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        for row in self.board:
            for cell in row:
                if cell:  # if any light is ture
                    return False
        return True

    def copy(self):
        return LightsOutPuzzle(self.get_board())

    def successors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                new_puzzle = self.copy()
                new_puzzle.perform_move(row, col)
                yield ((row, col), new_puzzle)

    def find_solution(self):
        visited = set()
        frontier = deque()
        frontier.append((self.copy(), []))
        visited.add(tuple(tuple(row) for row in self.board))

        while frontier:
            current, path = frontier.popleft()

            if current.is_solved():
                return path

            for move, new_puzzle in current.successors():
                state = tuple(tuple(row) for row in new_puzzle.get_board())
                if state not in visited:
                    visited.add(state)
                    frontier.append((new_puzzle, path + [move]))
        return None

def create_puzzle(rows, cols):
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(False)
        board.append(row)

    puzzle = LightsOutPuzzle(board)
    return puzzle  

############################################################
# Section 3: Linear Disk Movement
############################################################

def solve_identical_disks(length, n):
    start = tuple([1] * n + [0] * (length - n))
    goal = tuple([0] * (length - n) + [1] * n)

    visited = set()
    queue = deque()
    queue.append((start, []))
    visited.add(start)

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path

        for i in range(length):
            if state[i] == 1:
                # Move right by 1
                if i + 1 < length and state[i + 1] == 0:
                    new_state = list(state)
                    new_state[i], new_state[i + 1] = 0, 1
                    t = tuple(new_state)
                    if t not in visited:
                        visited.add(t)
                        queue.append((t, path + [(i, i + 1)]))
                # Jump right by 2
                if i + 2 < length and state[i + 1] == 1 and state[i + 2] == 0:
                    new_state = list(state)
                    new_state[i], new_state[i + 2] = 0, 1
                    t = tuple(new_state)
                    if t not in visited:
                        visited.add(t)
                        queue.append((t, path + [(i, i + 2)]))

    return None

def solve_distinct_disks(length, n):
    start = tuple(list(range(1, n + 1)) + [0] * (length - n))
    goal = tuple([0] * (length - n) + list(range(n, 0, -1)))

    visited = set()
    queue = deque()
    queue.append((start, []))
    visited.add(start)

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path

        for i in range(length):
            if state[i] != 0:
                # Move right by 1
                if i + 1 < length and state[i + 1] == 0:
                    new_state = list(state)
                    new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
                    t = tuple(new_state)
                    if t not in visited:
                        visited.add(t)
                        queue.append((t, path + [(i, i + 1)]))
                # Jump right by 2
                if i + 2 < length and state[i + 1] != 0 and state[i + 2] == 0:
                    new_state = list(state)
                    new_state[i], new_state[i + 2] = new_state[i + 2], new_state[i]
                    t = tuple(new_state)
                    if t not in visited:
                        visited.add(t)
                        queue.append((t, path + [(i, i + 2)]))

                # Jump left by 1
                if i - 1 >= 0 and state[i - 1] == 0:
                    new_state = list(state)
                    new_state[i], new_state[i - 1] = new_state[i - 1], new_state[i]
                    t = tuple(new_state)
                    if t not in visited:
                        visited.add(t)
                        queue.append((t, path + [(i, i - 1)]))

                # Jump left by 2
                if i - 2 >= 0 and state[i - 1] != 0 and state[i - 2] == 0:
                    new_state = list(state)
                    new_state[i], new_state[i - 2] = new_state[i - 2], new_state[i]
                    t = tuple(new_state)
                    if t not in visited:
                        visited.add(t)
                        queue.append((t, path + [(i, i - 2)]))

    return None