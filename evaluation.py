import numpy as np
from numba import jit


@jit(nopython=True, fastmath=True, cache=True)
def monotonicity(matrix):
    """
    计算单调性
    将矩阵蛇形化
    计算相邻元素递增数与递减数的插值
    [1,2,3  -->
     6,5,4  <--
     7,8,9] -->
     snake_like:[1,2,3,4,5,6,7,8,9]
    """
    # score = 0
    snake_like = matrix.copy()
    snake_like[1::2] = matrix[1::2, ::-1]
    snake_like = snake_like.ravel()
    # monotonicity
    difference = snake_like[:-1] - snake_like[1:]
    # score += (difference > 0).sum()
    # score -= (difference < 0).sum()
    return abs(difference.sum())


@jit(nopython=True, fastmath=True, cache=True)
def smoothness(matrix):
    """
    计算平滑性
    计算行,列相邻元素的差值
    """
    score = 0
    # row monotonicity
    difference = matrix[:, :-1] - matrix[:, 1:]
    score += np.abs(difference).sum()
    # col monotonicity
    difference = matrix[:-1, :] - matrix[1:, :]
    score += np.abs(difference).sum()
    return score


@jit(nopython=True, fastmath=True, cache=True)
def evaluation(matrix, weight):
    empty_score = np.log((matrix == 0).sum() + 0.1)
    monotonicity_score = monotonicity(matrix) + monotonicity(matrix.T) #+ \
                         #monotonicity(matrix[:, ::-1]) + monotonicity(matrix.T[:, ::-1])
    smoothness_score = smoothness(matrix)
    max_value_score = matrix.max()
    return np.array([empty_score, monotonicity_score, smoothness_score, max_value_score]).dot(weight)
