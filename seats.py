# -*- coding: utf-8 -*-
import random
import os
import codecs
import Tkinter as tk


class Seats:
    chosen_button = None
    random_iteration = 50
    current_iteration = 0
    random_iteration_step = (500, 250, 100, 50)
    random_iteration_bound = (47, 40, 25, 0)
    names = []

    def __init__(self, master, row_count, total):
        self.load_names()

        self.parent = master
        random.seed()
        tk.Grid.rowconfigure(master, 0, weight=1)
        tk.Grid.columnconfigure(master, 0, weight=1)
        self.frame = tk.Frame(master)
        self.frame.grid(row=0, column=0)
        self.go_button = tk.Button(master, 
                                   text=u'Go',
                                   cursor='hand2',
                                   command=self.on_go_button_clicked
                                   )

        self.go_button.grid(row=1, 
                            column=0,
                            sticky=tk.W+tk.E
                            )

        self.row_count = row_count
        self.col_count = total / row_count

        if total % row_count:
            self.col_count += 1

        self.buttons = []
        name_idx = 0

        for r in xrange(self.row_count):
            for c in xrange(self.col_count):
                if self.enable_button(r, c):
                    b = tk.Button(self.frame, 
                                  text=self.names[name_idx]
                                  )

                    b.grid(row=r, column=c,
                           padx=5, pady=5
                           )
                    self.buttons.append(b)
                    name_idx += 1

    def enable_button(self, row, col):
        if row == 0 and col == 0:
            return False
        elif row == 0 and col == self.col_count - 1:
            return False
        elif row == self.row_count - 1 and col == 0:
            return False
        elif row == self.row_count - 1 and col == self.col_count - 1:
            return False
        return True

    def random_choose(self):
        idx = random.randint(0, len(self.buttons) - 1)

        if self.chosen_button != self.buttons[idx]:
            if self.chosen_button:
                self.chosen_button.config(background=self.parent.cget("bg"))

            self.chosen_button = self.buttons[idx]
            self.chosen_button.config(background='green')

        self.current_iteration += 1

        if self.current_iteration > self.random_iteration:
            self.go_button.config(state=tk.NORMAL)
            self.parent.config(cursor='')
        else:
            t = 100
            for i, count in enumerate(self.random_iteration_bound):
                if self.current_iteration >= count:
                    t = self.random_iteration_step[i]
                    break
            self.parent.after(t, self.random_choose)

    def on_go_button_clicked(self):
        self.go_button.config(state=tk.DISABLED)
        self.parent.config(cursor='wait')
        self.current_iteration = 0 
        self.random_choose()

    def load_names(self, file_name=os.path.dirname(os.path.realpath(__file__))+'/names.txt'):
        with codecs.open(file_name, 'r', encoding='utf8') as f:
            for lines in f:
                self.names.append(lines.rstrip())


if __name__ == '__main__':
    root = tk.Tk()
    seats = Seats(root, 6, 37)
    root.mainloop()
