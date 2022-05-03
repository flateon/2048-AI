import pathlib
import random
import time

import numpy as np
from numba import jit
from tqdm import tqdm

import logic
from evaluation import evaluation
from puzzle import GameGrid


@jit(nopython=True, fastmath=True)
def compute_all_op(matrix):
    matrix_up, _, move_up = logic.up(matrix)
    matrix_down, _, move_down = logic.down(matrix)
    matrix_left, _, move_left = logic.left(matrix)
    matrix_right, _, move_right = logic.right(matrix)
    return np.stack((matrix_up, matrix_down, matrix_left, matrix_right)), \
           np.array((move_up, move_down, move_left, move_right))


@jit(nopython=True, fastmath=True)
def search_max(matrix, weight, depth):
    max_score = -100000.0
    matrixs, moved = compute_all_op(matrix)
    for matrix_moved, move in zip(matrixs, moved):
        if not move: continue
        score_curr = search_expected(matrix_moved, weight, depth - 1)
        if score_curr > max_score:
            max_score = score_curr
    return max_score


@jit(nopython=True, fastmath=True)
def search_expected(matrix, weight, depth):
    score = 0
    idx_avail = np.argwhere(matrix == 0)
    if depth > 0:
        if len(idx_avail) == 0: return search_max(matrix, weight, depth - 1)
        for idx in idx_avail:
            matrix[idx[0], idx[1]] = 1
            score += search_max(matrix, weight, depth - 1) * 0.9
            matrix[idx[0], idx[1]] = 2
            score += search_max(matrix, weight, depth - 1) * 0.1
            matrix[idx[0], idx[1]] = 0
    else:
        if len(idx_avail) == 0: return evaluation(matrix, weight)
        for idx in idx_avail:
            matrix[idx[0], idx[1]] = 1
            score += evaluation(matrix, weight) * 0.9
            matrix[idx[0], idx[1]] = 2
            score += evaluation(matrix, weight) * 0.1
            matrix[idx[0], idx[1]] = 0
    return score / len(idx_avail)


@jit(nopython=True)
def expectimax(matrix, weight, depth):
    max_score = 0
    best_op = random.randrange(4)
    matrixs, moved = compute_all_op(matrix)
    for i, (matrix_moved, move) in enumerate(zip(matrixs, moved)):
        if not move: continue
        score_curr = search_expected(matrix_moved, weight, depth - 1)
        if score_curr > max_score:
            max_score = score_curr
            best_op = i
    return best_op


def ai(game=None, weight=None, depth=3, gui=False, save_path=None, progress=True):
    """
        game: a GameGrid object
        weight: weight of (empty_score, monotonicity_score, smoothness_score, max_value_score)
        depth: search depth
        gui: whether to display gui
        save_path: path to save game screenshot
        progress: whether to show progress bar
    """
    if game is None:
        game = GameGrid(gui)
    if weight is None:
        weight = np.array((2.35, 0.21, -0.2, 3.53))
    if save_path is not None:
        frame_idx = 0
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

    history_matrix = []
    pbar = tqdm(leave=False, position=0, disable=not progress)
    try:
        while game.state is None:
            # start = time.time()
            history_matrix.append(game.matrix)
            best_op = expectimax(game.matrix, weight, depth)
            game.move(best_op)
            pbar.update()
            if game.GUI:
                game.update_idletasks()
                game.update()
                if save_path is not None:
                    game.savefig(f'{save_path}/{frame_idx:05d}.bmp')
                    frame_idx += 1
                # time.sleep(max(0.05 - (time.time() - start), 0))
        score = game.score
        if gui:
            time.sleep(5)
    finally:
        pbar.close()
        game.master.destroy()
        return np.stack(history_matrix), score


if __name__ == '__main__':
    for _ in range(10):
        mat, score = ai(gui=True)
        print(f'score:{score:6d}, largest:{2 ** mat[-1].max()}')
