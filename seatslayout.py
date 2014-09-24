# -*- coding: utf-8 -*-

import functools
import collections
import codecs
import json
from sys import platform

from Tkinter import *
import tkFileDialog

from student import Student

if platform != 'darwin':
    from ttk import *

class SeatsLayout:
    seat_buttons = collections.defaultdict(list)
    student_label = u'Student'
    none_label = u'None'                


    def __init__(self, parent):
        self.parent = parent
        self.row_count = IntVar(parent)
        self.col_count = IntVar(parent) 
        self.row_count.set(7)
        self.col_count.set(6)
        Grid.rowconfigure(self.parent, 0, weight=1)
        Grid.columnconfigure(self.parent, 0, weight=1)

        #self.init_layout_buttons()
        self.init_size_buttons()
        self.init_save_json_button()
        self.init_seat_panel()
        self.update_seat_buttons()

    def init_layout_buttons(self):
        col = 0
        Grid.rowconfigure(self.parent, 0, weight=1)

        for layout_type, mode in self.layout_types:
            Grid.columnconfigure(self.parent, col, weight=1)

            b = Radiobutton(self.parent,
                            text=layout_type,
                            variable=self.layout_group,
                            value=mode,
                            command=self.on_layout_button_clicked
                            )

            b.grid(row=0, column=col)
            col += 1

    def init_size_buttons(self):
        self.size_panels = [Frame(self.parent), Frame(self.parent),]

        for i, panel in enumerate(self.size_panels):
            panel.grid(row=0, column=i, sticky=W)
        
        Grid.rowconfigure(self.parent, 1, weight=1)
        for col in xrange(2):
            Grid.columnconfigure(self.parent, col, weight=1)
            
        self.row_label = Label(self.size_panels[0], text=u'Row')
        self.col_label = Label(self.size_panels[1], text=u'Col')

        self.row_spinbox = Spinbox(self.size_panels[0], from_=2, to=10, width=3, 
                                   textvariable=self.row_count,
                                   command=self.update_seat_buttons
                                   )
        self.col_spinbox = Spinbox(self.size_panels[1], from_=2, to=10, width=3,
                                   textvariable=self.col_count,
                                   command=self.update_seat_buttons
                                   )

        self.row_label.grid(row=0, column=0)
        self.row_spinbox.grid(row=0, column=1, padx=4, pady=4)
        self.col_label.grid(row=0, column=0)
        self.col_spinbox.grid(row=0, column=1, padx=4, pady=4)

    def init_save_json_button(self):
        self.save_json_button = Button(self.parent, text=u'Save',
                                       command=self.on_save_json_button_clicked
                                       )    
        self.save_json_button.grid(row=0, column=3, sticky=W)

    def init_seat_panel(self):
        self.seat_panel = Frame(self.parent)
        self.seat_panel.grid(row=2, column=0, columnspan=4)
        Grid.rowconfigure(self.parent, 2, weight=10)

    def update_seat_buttons(self):
        for widget in self.seat_panel.grid_slaves():
            widget.grid_remove()

        self.seat_buttons.clear()   

        for j in xrange(self.row_count.get()):
            for i in xrange(self.col_count.get()):
                b = Button(self.seat_panel, text=self.student_label,
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

    def on_save_json_button_clicked(self):
        fName = tkFileDialog.asksaveasfilename(defaultextension='.json',
                                               initialfile='seats.json'
                                               )

        if len(fName) == 0:
            return False

        with codecs.open(fName, 'w', encoding='utf-8') as f:
            dst = []
            for row, item in self.seat_buttons.iteritems():
                for idx, col in enumerate(item):
                    if col[1] == True:
                        s = Student(name=u'Blank', row=row, column=idx)
                        dst.append(s)

            json.dump(dst, f, ensure_ascii=False, default=lambda obj: obj.__dict__)    
            return True



if __name__ == '__main__':
    root = Tk()
    widget = SeatsLayout(root)
    root.mainloop()
