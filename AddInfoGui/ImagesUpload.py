from tkinter import filedialog, Tk, Button, Frame, StringVar, Entry, Menu
from tkinter.ttk import Treeview
import os

class FileUpload(Frame):
    def __init__(self, master, uploaded_file_func, file_types: list = [("all", "*.*")]):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.file_types = file_types
        self.path = "\\"
        self.uploaded_file_func = uploaded_file_func
        # self.frame = Frame(root)
        # self.box_contents = StringVar()
        # self.path_entry = Entry(self, state="readonly", textvariable=self.box_contents)
        # self.path_entry.grid(column=0, row=0)
        self.upload_button = Button(self, text='Find', bd='5', command=self.findAndSavePath)
        self.upload_button.grid(column=0, row=0, sticky="nsew")

    def selectFilePath(self) -> str:
        f = filedialog.askopenfile() # filetypes=self.file_types
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
            # self.box_contents.set(self.path)
            self.uploaded_file_func()

    def setPath(self, path: str):
        self.path = path

    def getPath(self) -> str:
        return self.path

# todo add validation so can't upload the same image twice
class FilesPathsList(Treeview):
    def __init__(self, master, image_paths: list):
        super().__init__(master, show="headings", columns="c1", height=4)
        self.image_paths: list = image_paths
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

    def isPathRecorded(self, path: str): # todo add pop-up later in code if path already uploaded
        return path in self.image_paths

    def getImagePaths(self) -> list:
        return self.image_paths

class FilesUpload(Frame):
    def __init__(self, master, file_paths: list=None):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        if file_paths is None: file_paths = []
        self.files_upload_list = FilesPathsList(self, file_paths)
        self.files_upload_list.grid(row=0, column=0, sticky="nsew")
        self.file_upload = FileUpload(self, self.uploadedFile, file_paths)
        self.file_upload.grid(row=1, column=0, sticky="nsew")

    def uploadedFile(self):
        path = self.file_upload.getPath()
        self.files_upload_list.addImageFilePath(path)

    def getPaths(self) -> list:
        return self.files_upload_list.getImagePaths()





# todo - once the file paths have been selected, move to single folder
a = Tk()
a.rowconfigure(0, weight=1)
a.columnconfigure(0, weight=1)
FilesUpload(a).grid(row=0, column=0, sticky="nsew")
a.mainloop()