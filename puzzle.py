from tkinter import Frame, Label, CENTER

import numpy as np
import tkcap

import logic as logic
from constants import *


class GameGrid(Frame):
    def __init__(self, GUI=True):
        Frame.__init__(self)

        self.GUI = GUI
        self.key2op_id = {
            KEY_UP: 0,
            KEY_DOWN: 1,
            KEY_LEFT: 2,
            KEY_RIGHT: 3,
            KEY_UP_ALT1: 0,
            KEY_DOWN_ALT1: 1,
            KEY_LEFT_ALT1: 2,
            KEY_RIGHT_ALT1: 3,
            KEY_UP_ALT2: 0,
            KEY_DOWN_ALT2: 1,
            KEY_LEFT_ALT2: 2,
            KEY_RIGHT_ALT2: 3,
        }
        self.op = (logic.up, logic.down, logic.left, logic.right)
        self.matrix = logic.new_game(GRID_LEN)
        self.score = 0
        self.state = None
        if self.GUI:
            self.grid()
            self.master.title('2048')
            self.master.bind('<Key>', self.key_down)
            self.grid_cells = []
            self.init_grid()
            self.update_grid_cells()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()

        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(
                    background,
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    width=SIZE / GRID_LEN,
                    height=SIZE / GRID_LEN
                )
                cell.grid_propagate(0)
                cell.grid(
                    row=i,
                    column=j,
                    padx=GRID_PADDING,
                    pady=GRID_PADDING
                )
                cell.pack_propagate(0)
                t = Label(
                    master=cell,
                    text="",
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=FONT,
                )
                t.pack(expand=True, fill='both')
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        display_matrix = 2 ** self.matrix.astype(np.int32)
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = display_matrix[i][j]
                if new_number == 1:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=BACKGROUND_COLOR_DICT[new_number],
                        fg=CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def move(self, op_id):
        self.matrix, score, done = self.op[op_id](self.matrix)
        self.score += score
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.state = logic.game_state(self.matrix)
            if self.GUI:
                self.update_grid_cells()
                if self.state == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[2][1].configure(text="Score:", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[2][2].configure(text=f"{self.score}", bg=BACKGROUND_COLOR_CELL_EMPTY)
                elif self.state == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[2][1].configure(text="Score:", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[2][2].configure(text=f"{self.score}", bg=BACKGROUND_COLOR_CELL_EMPTY)

    def key_down(self, event):
        key = event.keysym
        if key == KEY_QUIT:
            exit()
        elif key in self.key2op_id.keys():
            self.move(self.key2op_id[key])

    def savefig(self, filename):
        cap = tkcap.CAP(self.master)
        cap.capture(filename)


if __name__ == '__main__':
    GameGrid().mainloop()
