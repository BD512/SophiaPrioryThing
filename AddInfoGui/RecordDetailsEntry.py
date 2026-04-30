from tkinter import *

class RecordDetailsEntry(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Record Details")
        self.geometry("600x600")
        Label(self, text="Item name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        Label(self, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        # dropdown with add category button (use thing from something else I made recently which had dropdown with other option)

        Label(self, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.description_entry = Text(self)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)
        Label(self, text="Image path:").grid(row=3, column=0, padx=5, pady=5)
        # do a path entry thing here - find the one I did in 2024