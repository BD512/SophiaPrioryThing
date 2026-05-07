from tkinter import filedialog, Tk, Button, Frame, StringVar, Entry, Canvas, Scrollbar, Menu
from tkinter.ttk import Treeview
import os

class FileUpload(Frame):
    def __init__(self, master=None, file_types: list = [("all", "*.*")]):
        super().__init__(master)
        self.file_types = file_types
        self.path = "\\"
        # self.frame = Frame(root)
        self.box_contents = StringVar()
        self.path_entry = Entry(self, state="readonly", textvariable=self.box_contents)
        self.path_entry.grid(column=0, row=0)
        self.upload_button = Button(self, text='Find', bd='5', command=self.findAndSavePath)
        self.upload_button.grid(column=2, row=0)

    def selectFilePath(self) -> str:
        filetypes = self.file_types
        f = filedialog.askopenfile(filetypes=filetypes, initialdir=self.path)
        print(self.path)
        if f:
            filepath = os.path.abspath(f.name)
            return filepath
        return ""

    def findAndSavePath(self) -> None:
        p = self.selectFilePath()
        if len(p) > 0:
            self.path = p
            # self.path_entry.delete(0, END)
            # self.path_entry.insert(0, str(self.path))
            self.box_contents.set(self.path)

    def setPath(self, path: str):
        self.box_contents.set(path)
        self.path = path

    def getPath(self) -> str:
        return self.path

# todo add validation so can't upload the same image twice
class FilesUploadList(Treeview):
    def __init__(self, master, image_paths: tuple):
        super().__init__(master)
        self.image_paths: list = list(image_paths)
        self.column("#1")
        self.heading("#1", text="Image path")
        self.right_click_options = Menu(self, tearoff=0)  ######## self might have to be a Tk instance??
        self.right_click_options.add_command(label="Delete", command=self.deleteSelection)
        self.bind("<Button-3>", self.showRightClickOptions)

    def getSelection(self):
        return self.selection()[0]

    def deleteSelection(self):
        path = self.getSelection()
        self.deletePath(path)

    def deletePath(self, path: str):
        if path in self.image_paths:
            self.image_paths.remove(path)
        self.updatePaths()

    def showPaths(self):
        for path in self.image_paths:
            self.showImageFilePath(path)

    def updatePaths(self):
        self.clear()
        self.showPaths()

    def clear(self):
        for child in self.get_children():
            self.delete(child)

    def showRightClickOptions(self, event):
        row_id = self.identify_row(event.y)
        if row_id is not None:
            self.selection_set(row_id)
            self.right_click_options.post(event.x_root, event.y_root)

    def addImageFilePath(self, path):
        self.image_paths.append(path)
        self.showImageFilePath(path)

    def showImageFilePath(self, path: str):
        self.insert('', "end", iid=path, values=(path, ))

class FilesUpload(Canvas):
    def __init__(self, master):
        super().__init__(master)
        # todo create a scrollable thing for the image paths
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.configure(yscrollcommand=self.scrollbar.set)


# todo - once the file paths have been selected, move to single folder
a = Tk()
FileUpload(a).pack()
a.mainloop()