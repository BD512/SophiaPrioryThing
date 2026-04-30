from tkinter import *

class RecordDetailsEntry(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        Label(self, text="Record Details").grid(row=0, column=0, sticky=W)
        Label(self, text="Item name").grid(row=1, column=0, sticky=W)
        name_entry = Entry(self)
        name_entry.grid(row=1, column=1)
        Label(self, text="Item price").grid(row=2, column=0, sticky=W)
        price_entry = Entry(self)
        price_entry.grid(row=2, column=1)