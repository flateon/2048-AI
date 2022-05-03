import time

from ai import *


def replay(history, save_path=None, score=0):
    if save_path is not None:
        frame_idx = 0
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

    game = GameGrid(GUI=True)
    game.score = score
    time.sleep(1)
    try:
        for matrix in tqdm(history):
            game.matrix = matrix
            game.update_grid_cells()
            game.update_idletasks()
            game.update()
            if save_path is not None:
                game.savefig(f'{save_path}/{frame_idx:05d}.bmp')
                frame_idx += 1
        while game.state is None:
            game.move(random.randrange(4))
            if save_path is not None:
                game.savefig(f'{save_path}/{frame_idx:05d}.bmp')
                frame_idx += 1
        time.sleep(5)
    finally:
        game.master.destroy()
