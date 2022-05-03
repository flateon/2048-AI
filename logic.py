import numpy as np
from numba import jit


@jit(nopython=True, cache=True)
def new_game(n):
    matrix = np.zeros((n, n), dtype=np.int8)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix


@jit(nopython=True, cache=True, fastmath=True)
def add_two(mat):
    idx_avail = np.argwhere(mat == 0)
    if len(idx_avail) > 0:
        idx = idx_avail[np.random.randint(len(idx_avail))]
        mat[idx[0], idx[1]] = 1 if np.random.rand() < 0.9 else 2
    return mat


@jit(nopython=True, cache=True, fastmath=True)
def game_state(mat):
    # check for win cell
    if mat.max() >= 18:
        return 'win'
    # check for any zero entries
    if np.any(mat == 0):
        return None
    # check for same cells that touch each other
    for i in range(len(mat) - 1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0]) - 1):
            if mat[i, j] == mat[i + 1, j] or mat[i, j + 1] == mat[i, j]:
                return None
    for k in range(len(mat) - 1):  # to check the left/right entries on the last row
        if mat[len(mat) - 1, k] == mat[len(mat) - 1, k + 1]:
            return None
    for j in range(len(mat) - 1):  # check up/down entries on last column
        if mat[j, len(mat) - 1] == mat[j + 1, len(mat) - 1]:
            return None
    return 'lose'


@jit(nopython=True, cache=True)
def reverse(mat):
    return mat[:, ::-1]


@jit(nopython=True, cache=True, fastmath=True)
def cover_up(mat):
    new = np.zeros(mat.shape, dtype=np.int8)
    move = False
    for i in range(len(mat)):
        count = 0
        for j in range(len(mat)):
            if mat[i, j] != 0:
                new[i, count] = mat[i, j]
                if j != count:
                    move = True
                count += 1
    return new, move


@jit(nopython=True, cache=True, fastmath=True)
def merge(mat, move):
    score = 0
    for i in range(len(mat)):
        for j in range(len(mat) - 1):
            if mat[i, j] != 0 and mat[i, j] == mat[i, j + 1]:
                mat[i, j] += 1
                mat[i, j + 1] = 0
                score += 2 ** mat[i, j]
                move = True
    return mat, move, score


@jit(nopython=True, cache=True)
def cover_up_merge(mat):
    mat, move = cover_up(mat)
    mat, move, score = merge(mat, move)
    mat, _ = cover_up(mat)
    return mat, score, move


@jit(nopython=True, cache=True)
def up(mat):
    # return matrix after shifting up
    mat = mat.T
    mat, score, move = cover_up_merge(mat)
    mat = mat.T
    return mat, score, move


@jit(nopython=True, cache=True)
def down(mat):
    # return matrix after shifting down
    mat = mat.T
    mat = reverse(mat)
    mat, score, move = cover_up_merge(mat)
    mat = reverse(mat)
    mat = mat.T
    return mat, score, move


@jit(nopython=True, cache=True)
def left(mat):
    # return matrix after shifting left
    mat, score, move = cover_up_merge(mat)
    return mat, score, move


@jit(nopython=True, cache=True)
def right(mat):
    # return matrix after shifting right
    mat = reverse(mat)
    mat, score, move = cover_up_merge(mat)
    mat = reverse(mat)
    return mat, score, move
