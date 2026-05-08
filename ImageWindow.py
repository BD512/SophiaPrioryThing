from tkinter import PhotoImage, Toplevel, Button, Label, Frame, Tk

from database_manager import DatabaseManager

class ImagesViewer(Frame):
    def __init__(self, master, photo_paths: tuple):
        super().__init__(master)
        self.photo_paths = photo_paths
        self.current_photo_index = 0
        Button(self, text="<", command=self.moveToNextImage).grid(row=0, column=0)
        self.current_photo_file = PhotoImage(file=self.photo_paths[self.current_photo_index])
        self.image = Label(self, image=self.current_photo_file)
        self.image.grid(row=0, column=1)
        Button(self, text=">", command=self.moveToNextImage).grid(row=0, column=2)

    def moveToNextImage(self):
        self.current_photo_index = (self.current_photo_index + 1) % len(self.photo_paths)
        self.current_photo_file = self.photo_paths[self.current_photo_index]
        self.image.configure(image=self.current_photo_file)

class ImagesWindow(Toplevel):
    def __init__(self, master, photo_paths: tuple):
        super().__init__(master)
        if len(photo_paths) == 0:
            Label(self, text="No photos for this item").grid(row=0, column=1)
        else:
            ImagesViewer(self, photo_paths)
        Button(self, text="Close", command=self.destroy).grid(row=1, column=1)

if __name__ == "__main__":
    master = Tk()
    master.title("Main Window")



