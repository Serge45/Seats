# -*- coding: utf-8 -*-

import functools
import collections

import Tkinter as tk

class SeatsLayout:
    seat_buttons = collections.defaultdict(list)
    student_label = u'Student'
    none_label = u'None'                


    def __init__(self, parent):
        self.parent = parent
        self.row_count = tk.IntVar(parent)
        self.col_count = tk.IntVar(parent) 
        self.row_count.set(7)
        self.col_count.set(6)
        tk.Grid.rowconfigure(self.parent, 0, weight=1)
        tk.Grid.columnconfigure(self.parent, 0, weight=1)

        #self.init_layout_buttons()
        self.init_size_buttons()
        self.init_seat_panel()
        self.update_seat_buttons()

    def init_layout_buttons(self):
        col = 0
        tk.Grid.rowconfigure(self.parent, 0, weight=1)

        for layout_type, mode in self.layout_types:
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
        for col in xrange(4):
            tk.Grid.columnconfigure(self.parent, col, weight=1)
            
        self.row_label = tk.Label(text='Row')
        self.col_label = tk.Label(text='Col')

        self.row_spinbox = tk.Spinbox(self.parent, from_=2, to=10, width=3, 
                                      textvariable=self.row_count,
                                      command=self.update_seat_buttons
                                      )
        self.col_spinbox = tk.Spinbox(self.parent, from_=2, to=10, width=3,
                                      textvariable=self.col_count,
                                      command=self.update_seat_buttons
                                      )

        self.row_label.grid(row=1, column=0)
        self.row_spinbox.grid(row=1, column=1, padx=4, pady=4)
        self.col_label.grid(row=1, column=2)
        self.col_spinbox.grid(row=1, column=3, padx=4, pady=4)

    def init_seat_panel(self):
        self.seat_panel = tk.Frame(self.parent)
        self.seat_panel.grid(row=2, column=0, columnspan=4)
        tk.Grid.rowconfigure(self.parent, 2, weight=10)

    def update_seat_buttons(self):
        for widget in self.seat_panel.grid_slaves():
            widget.grid_remove()

        self.seat_buttons.clear()   

        for j in xrange(self.row_count.get()):
            for i in xrange(self.col_count.get()):
                b = tk.Button(self.seat_panel, text=self.student_label,
                              command= functools.partial(self.on_seat_button_clicked, 
                                                         row=j, col=i
                                                         )
                              )
                b.grid(row=j, column=i, padx=4, pady=4)
                self.seat_buttons[j].append([b, True])

    def on_layout_button_clicked(self):
        layout_type = self.layout_group.get()
        self.update_seat_buttons()

    def on_seat_button_clicked(self, row, col):
        btn = self.seat_buttons[row][col]

        if btn[0].cget('text') == self.student_label:
            btn[0].config(text=self.none_label)
            btn[1] = False
        else:
            btn[0].config(text=self.student_label)
            btn[1] = True

if __name__ == '__main__':
    root = tk.Tk()
    widget = SeatsLayout(root)
    root.mainloop()
