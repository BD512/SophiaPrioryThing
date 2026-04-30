from tkinter import *

class RecordDetailsEntry(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        Label(self, text="Record Details").grid(row=0, column=0, sticky=W)
        Label(self, text="Item name").grid(row)