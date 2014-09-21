# -*- coding: utf-8 -*-
import random
import os
from sys import platform
import codecs
import functools
import json
import Tkinter as tk
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

    def __init__(self, master, row_count, total):
        self.load_names()

        self.parent = master
        self.row_count = row_count
        self.col_count = total / row_count
        self.total = total
        random.seed()

        self.init_gui()
        #self.init_seat_buttons()
        self.init_seat_buttons_with_json()

    def init_gui(self):
        tk.Grid.rowconfigure(self.parent, 0, weight=1)
        tk.Grid.columnconfigure(self.parent, 0, weight=1)
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=0, column=0, columnspan=4)
        self.go_button = tk.Button(self.parent, 
                                   text=u'Go',
                                   cursor=u'hand2',
                                   command=self.on_go_button_clicked
                                   )

        self.shuffle_button = tk.Button(self.parent,
                                         text=u'Shuffle',
                                         cursor=u'hand2',
                                         command=self.on_shuffle_button_clicked
                                         )

        self.go_button.grid(row=1, 
                            column=0,
                            sticky=tk.W+tk.E,
                            )

        self.shuffle_button.grid(row=1,
                                 column=1,
                                 sticky=tk.W
                                 ) 

        self.save_button = tk.Button(self.parent,
                                     text=u'Save',
                                     cursor="",
                                     command=self.on_save_button_clicked,
                                     )

        self.save_button.grid(row=1, 
                              column=2,
                              sticky=tk.E,
                              pady=5
                              )

        self.save_as_json_button = tk.Button(self.parent,
                                             text=u'Save json',
                                             command=self.on_save_as_json_button_clicked
                                             )

        self.save_as_json_button.grid(row = 1, 
                                      column=3,
                                      pady=5)



    def init_seat_buttons(self):                
        if self.total % self.row_count:
            self.col_count += 1

        self.buttons = []
        name_idx = 0

        for r in xrange(self.row_count):
            for c in xrange(self.col_count):
                if self.enable_button(r, c):
                    b = tk.Button(self.frame, 
                                  text=self.names[name_idx],
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

            for js in in_json:
                r = js[u'row']
                c = js[u'col']
                text = js[u'name'].encode('utf-8')

                self.names += text

                b = tk.Button(self.frame, 
                              text=text,
                              command=functools.partial(self.on_seat_button_clicked, idx=name_idx)
                              )

                b.grid(row=r, column=c,
                       padx=5, pady=5
                       )
                self.buttons.append([b, name_idx, r, c])
                name_idx += 1
        return

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
                if platform != 'darwin':
                    self.chosen_button[0].config(background=self.parent.cget("bg"))
                else:
                    self.chosen_button[0].config(foreground="black")

            self.chosen_button = self.buttons[idx]

            if platform != 'darwin':
                self.chosen_button[0].config(bg='green')
            else:
                self.chosen_button[0].config(fg='green')


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

    def load_names(self, file_name=os.path.dirname(os.path.realpath(__file__))+'/names.txt'):
        with codecs.open(file_name, 'r', encoding='utf-8') as f:
            del self.names[:]
            for lines in f:
                self.names.append(lines.rstrip())

    def on_go_button_clicked(self):
        self.go_button.config(state=tk.DISABLED)
        self.parent.config(cursor=u'wait')
        self.current_iteration = 0 
        self.random_choose()


    def on_shuffle_button_clicked(self):
        if self.chosen_button:
            self.chosen_button[0].config(background=self.parent.cget("bg"))

        random.shuffle(self.names)
        for i, btn in enumerate(self.buttons):
            btn[0].config(text=self.names[i])            
            btn[1] = i

    def on_save_button_clicked(self):
        if tkMessageBox.askyesno(u'Warning', u'This will overrite existing setting, OK?'):
            file_name=os.path.dirname(os.path.realpath(__file__))+'/names.txt'

            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                for name in self.names:
                    f.write(name + '\n')

            self.load_names()        

    def on_seat_button_clicked(self, idx):
        self.input_dialog = LineInputDialog(self.parent, self.names[idx])
        if self.input_dialog.message:
            self.buttons[idx][0].config(text=self.input_dialog.message)
            self.names[idx] = self.input_dialog.message

    def on_save_as_json_button_clicked(self):
        fName = tkFileDialog.asksaveasfilename(defaultextension='.json',
                                               initialfile='seats.json'
                                               )

        if fName is None:
            return False

        f = codecs.open(fName, 'w', encoding='utf-8')    


        dst = []

        for btn in self.buttons:
            dst.append(Student(name=btn[0].cget('text'), row=btn[2], column=btn[3], count=0))

        json.dump(dst, f, ensure_ascii=False, default=lambda obj: obj.__dict__)    

        f.close()
        return True      
            
if __name__ == '__main__':
    root = tk.Tk()
    seats = Seats(root, 6, 37)
    root.mainloop()
