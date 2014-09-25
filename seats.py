# -*- coding: utf-8 -*-
import random
import os
from sys import platform
import codecs
import functools
import json
import csv
from Tkinter import *

if platform != 'darwin':
    from ttk import *
import tkMessageBox
import tkFileDialog

from lineinputdialog import LineInputDialog
from student import Student


class Seats:
    chosen_button = None
    seat_button_org_size = [0, 0]
    random_iteration = 50
    current_iteration = 0
    random_iteration_step = (500, 250, 100, 50)
    random_iteration_bound = (47, 40, 25, 0)
    names = []
    num_to_name = {}

    def __init__(self, master, row_count, total):
        self.parent = master
        self.row_count = row_count
        self.col_count = total / row_count
        self.total = total
        random.seed()

        self.init_gui()
        self.init_seat_buttons_with_json()
        self.load_name_num_list()

    def init_gui(self):
        Grid.rowconfigure(self.parent, 0, weight=1)
        Grid.columnconfigure(self.parent, 0, weight=1)
        self.frame = Frame(self.parent)
        self.frame.grid(row=0, column=0, columnspan=5)
        self.go_button = Button(self.parent, 
                                   text=u'Go',
                                   cursor=u'hand2',
                                   command=self.on_go_button_clicked
                                   )

        self.shuffle_button = Button(self.parent,
                                         text=u'Shuffle',
                                         cursor=u'hand2',
                                         command=self.on_shuffle_button_clicked
                                         )

        self.go_button.grid(row=1, 
                            column=0,
                            sticky=W+E,
                            )

        self.shuffle_button.grid(row=1,
                                 column=1,
                                 sticky=W
                                 ) 

        self.save_as_json_button = Button(self.parent,
                                             text=u'Save json',
                                             command=self.on_save_as_json_button_clicked
                                             )

        self.save_as_json_button.grid(row = 1, 
                                      column=2,
                                      pady=5)


        self.load_json_button = Button(self.parent,
                                             text=u'Load json',
                                             command=self.on_load_json_button_clicked
                                             )

        self.load_json_button.grid(row = 1, 
                                   column=3,
                                   pady=5)

        self.load_name_num_list_button = Button(self.parent,
                                                text='Load names',
                                                command=self.on_load_name_num_list_clicked
                                                )
        self.load_name_num_list_button.grid(row=1,
                                            column=4,
                                            pady=5)

    def init_seat_buttons(self):                
        if self.total % self.row_count:
            self.col_count += 1

        self.buttons = []
        name_idx = 0

        for r in xrange(self.row_count):
            for c in xrange(self.col_count):
                if self.enable_button(r, c):
                    b = Button(self.frame, 
                                  text=self.names[name_idx][0],
                                  command=functools.partial(self.on_seat_button_clicked, idx=name_idx)
                                  )

                    b.grid(row=r, column=c,
                           padx=5, pady=5
                           )
                    self.buttons.append([b, name_idx, r, c])
                    name_idx += 1

    def init_seat_buttons_with_json(self, 
                                    file_name=os.path.dirname(os.path.realpath(__file__))+'/seats.json'):
        with codecs.open(file_name, 'r', encoding='utf-8') as f:
            in_str = f.read()
            in_json = json.loads(in_str)

            del self.names[:]
            name_idx=0

            self.buttons = []

            for widget in self.frame.grid_slaves():
                widget.grid_remove()

            for js in in_json:
                r = js[u'row']
                c = js[u'col']
                text = js[u'name'].encode('utf-8')
                num = int(js[u'num'])

                self.names.append([text, num])

                b = Button(self.frame, 
                              text=text,
                              command=functools.partial(self.on_seat_button_clicked, idx=name_idx)
                              )

                b.grid(row=r, column=c,
                       padx=5, pady=5
                       )
                self.buttons.append([b, name_idx, r, c, num])
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
                style = Style()
                style.configure('normal.TButton')
                self.chosen_button[0].config(style='normal.TButton')

            self.chosen_button = self.buttons[idx]

            style = Style()
            style.configure('highlight.TButton', background='red')
            self.chosen_button[0].config(style='highlight.TButton')

        self.current_iteration += 1

        if self.current_iteration > self.random_iteration:
            self.go_button.config(state=NORMAL)
            self.parent.config(cursor='')
        else:
            t = 100
            for i, count in enumerate(self.random_iteration_bound):
                if self.current_iteration >= count:
                    t = self.random_iteration_step[i]
                    break
            self.parent.after(t, self.random_choose)

    def load_names(self, file_name=os.path.dirname(os.path.realpath(__file__))+'/names.txt'):
        with codecs.open(file_name, 'r', encoding='utf-8') as f:
            del self.names[:]
            for lines in f:
                self.names.append(lines.rstrip())

    def on_go_button_clicked(self):
        self.go_button.config(state=DISABLED)
        self.parent.config(cursor=u'wait')
        self.current_iteration = 0 
        self.random_choose()


    def on_shuffle_button_clicked(self):
        if self.chosen_button:
            style = Style()
            style.configure('normal.TButton')
            self.chosen_button[0].config(style='normal.TButton')

        random.shuffle(self.names)
        for i, btn in enumerate(self.buttons):
            btn[0].config(text=self.names[i][0])            
            btn[1] = self.names[i][1]

    def on_seat_button_clicked(self, idx):
        self.input_dialog = LineInputDialog(self.parent, 
                                            self.names[idx][0],
                                            self.names[idx][1]
                                            )
        if self.input_dialog.message:
            text = self.input_dialog.message[0]
            num = int(self.input_dialog.message[1])
            if len(text) == 0:
                text = self.num_to_name[num]

            self.buttons[idx][0].config(text=text)
            self.names[idx][0] = text
            self.names[idx][1] = num
            self.buttons[idx][4] = num

    def on_save_as_json_button_clicked(self):
        fName = tkFileDialog.asksaveasfilename(defaultextension='.json',
                                               initialfile='seats.json'
                                               )

        if len(fName) == 0:
            return False

        with codecs.open(fName, 'w', encoding='utf-8') as f:
            dst = []

            for btn in self.buttons:
                s = Student(name=btn[0].cget('text'), row=btn[2], column=btn[3], count=0, num=btn[4])
                dst.append(s)

            json.dump(dst, f, ensure_ascii=False, default=lambda obj: obj.__dict__)    

            return True      

    def on_load_json_button_clicked(self):
        fName = tkFileDialog.askopenfilename(defaultextension='.json',
                                             initialfile='seats.json'
                                             )

        if len(fName) == 0:
            return False

        self.init_seat_buttons_with_json(fName)
        return True

    def on_load_name_num_list_clicked(self):
        file_name = tkFileDialog.askopenfilename(defaultextension='.csv',
                                                 initialfile='names.csv'
                                                 )

        self.load_name_num_list(file_name=file_name)

    def load_name_num_list(self, file_name=os.path.dirname(os.path.realpath(__file__))+'/names.csv'):
        self.num_to_name = {}

        if len(file_name) == 0:
            return False

        with open(file_name, 'rb') as f:
            decode='utf-8'

            if platform == 'win32':
                decode='utf-8-sig'

            names_reader = csv.reader(f)
            for row in names_reader:
                self.num_to_name[int(row[0].decode(decode))] = row[1]
            
if __name__ == '__main__':
    root = Tk()
    seats = Seats(root, 6, 37)
    root.mainloop()
