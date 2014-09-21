# -*- coding: utf-8 -*-

import functools

import Tkinter as tk

class SeatsLayout:
    layout_types = [('Grid', 'GRID'),
                    ('Edge', 'EDGE'),
                    ('Group', 'GROUP'),
                    ]

    def __init__(self, parent):
        self.parent = parent
        tk.Grid.rowconfigure(self.parent, 0, weight=1)
        tk.Grid.columnconfigure(self.parent, 0, weight=1)
        self.init_layout_buttons()
        self.init_size_buttons()

    def init_layout_buttons(self):
        self.layout_group = tk.StringVar()
        self.layout_group.set('GRID')

        col = 0

        for layout_type, mode in self.layout_types:
            tk.Grid.rowconfigure(self.parent, 0, weight=1)
            tk.Grid.columnconfigure(self.parent, col, weight=1)

            b = tk.Radiobutton(self.parent,
                               text=layout_type,
                               variable=self.layout_group,
                               value=mode,
                               command=self.on_layout_button_clicked
                               )

            b.grid(row=0, column=col)
            col += 1

    def init_size_buttons(self):
        tk.Grid.rowconfigure(self.parent, 1, weight=1)
        self.row_label = tk.Label(text='Row')
        self.col_label = tk.Label(text='Col')

        self.row_spinbox = tk.Spinbox(self.parent, from_=1, to=10, width=3)
        self.col_spinbox = tk.Spinbox(self.parent, from_=1, to=10, width=3)

        self.row_label.grid(row=1, column=0)
        self.row_spinbox.grid(row=1, column=1, padx=4, pady=4)
        self.col_label.grid(row=1, column=2)
        self.col_spinbox.grid(row=1, column=3, padx=4, pady=4)

    def on_layout_button_clicked(self):
        layout_type = self.layout_group.get()
        print layout_type


if __name__ == '__main__':
    root = tk.Tk()
    widget = SeatsLayout(root)
    root.mainloop()
