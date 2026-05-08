from tkinter import ttk, Button, Toplevel, Label, Menu, Frame, Entry, Tk
import pickle

class Book:
    def __init__(self, title:str, author:str, genre:str, rrp:float, loaned:bool):
        self.title = title
        self.author = author
        self.genre = genre
        self.rrp = rrp
        self.loaned = loaned

    def getTitle(self):
        return self.title

    def isLoaned(self):
        return self.loaned

    def getAuthor(self):
        return self.author

    def getGenre(self):
        return self.genre

    def getRRP(self):
        return self.rrp

    def setTitle(self, title):
        self.title = title

    def setLoaned(self, loaned):
        self.loaned = loaned

    def setAuthor(self, author):
        self.author = author

    def setRRP(self, rrp):
        self.rrp = rrp

    def setGenre(self, genre):
        self.genre = genre

class Library(list):
    def __init__(self, books, filename:str, read_from_file=True):
        super().__init__()
        self.filename = filename
        if read_from_file:
            try:
                self.readFromFile()
            except FileNotFoundError:
                pass
        self.extend(books)
        self.writeToFile()

    def searchByPhrase(self, phrase):
        books = []
        for book in self:
            if phrase.lower() in book.getTitle().lower() or phrase.lower() in book.getAuthor().lower():
                books.append(book)
        return books

    def readFromFile(self):
        self.clear()
        data = pickle.load(open(self.filename, "rb"))
        self.extend([Book(record[0], record[1], record[2], record[3], record[4]) for record in data])

    def writeToFile(self):
        pickle.dump([[book.getTitle(), book.getAuthor(), book.getGenre(), book.getRRP(), book.isLoaned()] for book in self], open(self.filename, "wb"))

    def deleteBook(self, book):
        self.remove(book)
        self.writeToFile()

    def findBookFromTitle(self, title):
        for book in self:
            if book.getTitle() == title:
                return book
        return None

    def findBooksFromAuthor(self, author):
        books = []
        for book in self:
            if book.getAuthor() == author:
                books.append(book)
        return books

    def findBooksFromGenre(self, genre):
        books = []
        for book in self:
            if book.getGenre() == genre:
                books.append(book)
        return books

    def findBooksFromRRPRange(self, min_rrp, max_rrp):
        books = []
        for book in self:
            if min_rrp <= book.getRRP() <= max_rrp:
                books.append(book)
        return books

    def findBooksFromLoanedStatus(self, is_loaned):
        books = []
        for book in self:
            if book.getLoanedStatus() == is_loaned:
                books.append(book)
        return books

    def addNew(self, title, author, genre, rrp:float, loaned:bool):
        self.append(Book(title, author, genre, rrp, loaned))
        self.writeToFile()

class AddNewBookWidget(Toplevel):
    def __init__(self, master, books, feedback_function, genres=["Mystery", "Thriller", "Romance", "Fiction", "Adventure", "Childrens", "Sci-fi"]):
        super().__init__(master)
        self.title("Add new")
        self.resizable(False, False)
        self.library = books
        self.feedback_function = feedback_function
        self.book_info_entry = BookInfoEntry(self, genres)
        self.book_info_entry.pack()
        Button(self, text="Submit", command=self.enter).pack()
        self.feedback_label = Label(self)
        self.feedback_label.pack()

    def enter(self):
        title = self.book_info_entry.getTitle()
        author = self.book_info_entry.getAuthor()
        genre = self.book_info_entry.getGenre()
        rrp = self.book_info_entry.getRRP()
        loaned = self.book_info_entry.getIsLoaned()
        try:
            self.library.addNew(title, author, genre, float(rrp), True if loaned == "Yes" else False)
            self.feedback_function()
            self.destroy()
        except ValueError:
            self.feedback_label.config(text="RRP must be a float", fg="red")

class EditBookWidget(Toplevel):
    def __init__(self, master, book, feedback_function, genres=["Mystery", "Thriller", "Romance", "Fiction", "Adventure", "Childrens", "Sci-fi"]):
        super().__init__(master)
        self.title("Edit new")
        self.resizable(False, False)
        self.book = book
        self.feedback_function = feedback_function
        self.book_info_entry = BookInfoEntry(self, genres, book.getTitle(), book.getAuthor(), book.getGenre(), book.getRRP(), book.isLoaned())
        self.book_info_entry.pack()
        Button(self, text="Submit", command=self.enter).pack()
        self.feedback_label = Label(self, fg="red")
        self.feedback_label.pack()

    def enter(self):
        title = self.book_info_entry.getTitle()
        author = self.book_info_entry.getAuthor()
        genre = self.book_info_entry.getGenre()
        rrp = self.book_info_entry.getRRP()
        loaned = self.book_info_entry.getIsLoaned()
        try:
            self.book.setTitle(title)
            self.book.setAuthor(author)
            self.book.setGenre(genre)
            self.book.setRRP(float(rrp))
            self.book.setLoaned(loaned == "Yes")
            self.feedback_function()
            self.destroy()
        except ValueError:
            self.feedback_label.config(text="RRP must be a float")



class BooksListWidget(ttk.Treeview):
    def __init__(self, master, books:Library):
        super().__init__(master, show="headings", columns=("c1", "c2", "c3", "c4", "c5"), height=4)
        self.books = books
        self.books_shown = books
        self.column("#1")
        self.heading("#1", text="Title")
        self.column("#2")
        self.heading("#2", text="Author")
        self.column("#3")
        self.heading("#3", text="Genre")
        self.column("#4")
        self.heading("#4", text="RRP")
        self.column("#5")
        self.heading("#5", text="Is loaned")
        self.showBooks()
        self.right_click_options = Menu(self, tearoff=0) ######## self might have to be a Tk instance??
        self.right_click_options.add_command(label="Edit", command=self.editSelection)
        self.right_click_options.add_command(label="Delete", command=self.deleteSelection)
        self.bind("<Button-3>", self.showRightClickOptions)

    def getSelection(self):
        return self.selection()

    def editSelection(self):
        book = self.books.findBookFromTitle(self.getSelection()[0])
        EditBookWidget(self, book, self.updateBooks)

        # print(self.getSelection()[0].getAuthor())
    def deleteSelection(self):
        book = self.books.findBookFromTitle(self.getSelection()[0])
        self.books.deleteBook(book)
        if book in self.books_shown:
            self.books_shown.remove(book)
        self.updateBooks()

    def showRightClickOptions(self, event):
        row_id = self.identify_row(event.y)
        if row_id is not None:
            self.selection_set(row_id)
            self.right_click_options.post(event.x_root, event.y_root)

    def clear(self):
        for child in self.get_children():
            self.delete(child)

    def showBooks(self):
        for book in self.books_shown:
            print(book.getTitle())
            self.showBook(book)

    def showBook(self, book):
        self.insert('', "end", iid=book.getTitle(), values=(book.getTitle(), book.getAuthor(), book.getGenre(), f"£{book.getRRP():.2f}", "yes" if book.isLoaned() else "no"))

    def updateBooks(self):
        self.clear()
        self.showBooks()
        self.books.writeToFile()

    def changeBooksShown(self, books):
        self.books_shown = books
        self.updateBooks()

class SearchBox(Frame):
    def __init__(self, master, books, list_widget):
        super().__init__(master)
        self.books = books
        self.list_widget = list_widget
        Label(self, text="Search:").grid(row=0, column=0)
        self.search_entry = Entry(self)
        self.search_entry.grid(row=0, column=1)
        self.search_entry.bind("<KeyRelease>", self.searchAndUpdate)

    def searchAndUpdate(self, event=None):
        books = self.books.searchByPhrase(self.search_entry.get())
        self.list_widget.changeBooksShown(books)

class OptionsBar(Frame):
    def __init__(self, master, books, list_widget):
        super().__init__(master)
        self.books = books
        self.list_widget = list_widget
        self.search_box = SearchBox(self, self.books, list_widget)
        self.search_box.grid(row=0, column=0)
        Button(self, text="Add", command=self.addBook).grid(row=0, column=1)

    def addBook(self):
        AddNewBookWidget(self, self.books, self.search_box.searchAndUpdate)

class DropDownSelectWidget(Frame):
    def __init__(self, master, options, starting_option):
        super().__init__(master)
        self.option_menu = ttk.Combobox(self, values=options)
        self.option_menu.set(starting_option)
        self.option_menu.grid(row=0, column=0)

    def getSelection(self) -> str:
        return self.option_menu.get()

class BookInfoEntry(Frame):
    def __init__(self, master, genres, title="", author="", genre=None, rrp=10, is_loaned=True):
        super().__init__(master)
        Label(self, text="Title").grid(row=0, column=0, padx=10, pady=10)
        self.title_entry = Entry(self)
        self.title_entry.insert(0, title)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        Label(self, text="Author").grid(row=1, column=0, padx=10, pady=5)
        self.author_entry = Entry(self)
        self.author_entry.insert(0, author)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)
        Label(self, text="Genre").grid(row=2, column=0, padx=10, pady=5)
        self.genre_entry = DropDownSelectWidget(self, genres, genre if genre else genres[0])
        self.genre_entry.grid(row=2, column=1, padx=10, pady=5)
        Label(self, text="RRP £").grid(row=3, column=0, padx=10, pady=5)
        self.rrp_entry = Entry(self)
        self.rrp_entry.insert(0, str(rrp))
        self.rrp_entry.grid(row=3, column=1, padx=10, pady=5)
        Label(self, text="Is loaned").grid(row=4, column=0, padx=10, pady=5)
        self.is_loaned_entry = DropDownSelectWidget(self, ["Yes", "No"], "Yes" if is_loaned else "No")
        self.is_loaned_entry.grid(row=4, column=1, padx=10, pady=5)

    def getTitle(self):
        return self.title_entry.get()

    def getAuthor(self):
        return self.author_entry.get()

    def getGenre(self):
        return self.genre_entry.getSelection()

    def getRRP(self):
        return self.rrp_entry.get()

    def getIsLoaned(self):
        return self.is_loaned_entry.getSelection()



win = Tk()
win.resizable(False, False)
win.title("Library")
library = Library([], "text.bin")
list_widget = BooksListWidget(win, library)

OptionsBar(win, library, list_widget).pack()
list_widget.pack()
win.mainloop()