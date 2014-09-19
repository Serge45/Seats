# -*- coding: utf-8 -*-
from Tkinter import *
import tkSimpleDialog

class LineInputDialog(tkSimpleDialog.Dialog):
    def body(self, parent):
        Grid.rowconfigure(parent, 0, weight=1)
        Grid.columnconfigure(parent, 0, weight=1)

        Label(parent, text="請輸入姓名").grid(row=0, column=0, columnspan=2, sticky=E+W)

        self.line_input = Entry(parent)
        self.line_input.grid(row=1, column=0, columnspan=2, sticky=E+W)

        return self.line_input

    def apply(self):
        self.message = self.line_input.get()


if __name__ == '__main__':
    root = Tk()
    d = LineInputDialog(root)
