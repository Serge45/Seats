# -*- coding: utf-8 -*-
from Tkinter import *

from sys import platform

if platform != 'darwin':
    from ttk import *
import tkSimpleDialog

class LineInputDialog(tkSimpleDialog.Dialog):
    def __init__(self, parent, title=u'', num=0):
        self.name = title
        self.num = num
        tkSimpleDialog.Dialog.__init__(self, parent, title)

    def body(self, parent):
        Grid.rowconfigure(parent, 0, weight=1)
        Grid.columnconfigure(parent, 0, weight=1)

        Label(parent, text="請輸入姓名或座號").grid(row=0, column=0, columnspan=2, sticky=E+W)
        Label(parent, text="姓名").grid(row=1, column=0, sticky=E+W)
        Label(parent, text="座號").grid(row=2, column=0, sticky=E+W)

        self.name_var = StringVar()
        self.name_var.set(self.name)
        self.num_var = StringVar()
        self.num_var.set(self.num)
        self.name_input = Entry(parent, textvariable=self.name_var)
        self.name_input.grid(row=1, column=1, sticky=E+W)
        self.num_input = Entry(parent, textvariable=self.num_var)
        self.num_input.grid(row=2, column=1, sticky=E+W)

        return self.name_input

    def apply(self):
        self.message = [self.name_input.get(), self.num_input.get()]


if __name__ == '__main__':
    root = Tk()
    d = LineInputDialog(parent=root, title=u"QQ", num=10)
