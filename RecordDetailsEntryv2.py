
# copied from Kaela's code but made a few changes
# making independent of the database instance to make the code more versatile
# if info needed from database to show options to add a record, this will be passed in as a parameter

from tkinter import Tk, Label, Entry, ttk, Text, IntVar, Button, Toplevel
from FinalSophiaCode.database_manager import DatabaseManager

class RecordEntryWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.database = DatabaseManager()

        self.confidence_level = IntVar()
        self.categories = ("S", "L", "CS", "P", "W", "E", "LC", "M")  # set categories

        Label(self, text="Item name:").grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.name_entry = Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        Label(self, text="Category:").grid(row=1, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.category_menu = ttk.Combobox(self, values=self.categories)
        self.category_menu.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
        self.category_menu.bind('<<ComboboxSelected>>', self.updateSubcategoryMenu)
        self.category_menu.set("M")

        self.category_dict = self.database.get_category_dict(self.categories)
        # print(self.category_dict)
        # print(self.category_dict["M"])

        Label(self, text="Subcategory:").grid(row=2, column=0, padx=10, pady=0, sticky="nsew")
        self.subcategory_menu = ttk.Combobox(self, values=self.category_dict["M"])  # default selection is miscellaneous
        self.subcategory_menu.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.subcategory_menu.bind('<FocusIn>', self.updateSubcategoryMenu)
        self.subcategory_menu.bind('<Button-1>', self.updateSubcategoryMenu)

        Label(self, text="Description:").grid(row=3, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.description_entry = Text(self, wrap="word", width=4, height=4)
        self.description_entry.grid(row=3, column=1, pady=10, sticky="nsew")

        Label(self, text="Year:").grid(row=4, column=0, padx=10, pady=(5, 0))
        self.year_entry = Entry(self)
        self.year_entry.grid(row=4, column=1, padx=10, pady=0)

        # Label(self, text="Year confidence:").grid(row=0, column=4, padx=(5,0), pady=10)
        self.confident_check = ttk.Checkbutton(self, text="I am confident in year", variable=self.confidence_level, onvalue=1,
                                               offvalue=0)
        self.confident_check.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

        addBtn = Button(self, text="Add item") # the final submit button
        addBtn.grid(row=6, column=1, padx=10, pady=10, sticky="nsew")

        # testBtn = Button(self, text="test", command=self.test)
        # testBtn.grid(row=6, column=1)

    def updateSubcategoryMenu(self, event):
        current_category = self.category_menu.get()
        self.subcategory_menu.config(values=self.category_dict[current_category])

    def updateErrorMsg(self):
        pass

    def getName(self) -> str:
        return self.name_entry.get()

    def getSubcategory(self) -> str:
        return self.subcategory_menu.get()

    def getDescription(self) -> str:
        return self.description_entry.get("1.0", "end-1c")

    def getYear(self) -> int:
        return int(self.year_entry.get())

    def getConfidence(self) -> bool:
        return bool(self.confidence_level.get())

    def getItemDetails(self) -> tuple[str, str, str, int, bool]:
        return self.getName(), self.getSubcategory(), self.getDescription(), self.getYear(), self.getConfidence()

    def isValidRecord(self) -> bool:
        pass

    def isNewCategory(self):
        pass

    def isNewSubcategory(self):
        pass

    def test(self):
        print(self.getName(), self.getSubcategory(), self.getDescription(), self.getYear(), self.getConfidence())
        # print(bool(self.get_name()))

    def addItemRecord(self):

        current_item_details = self.getItemDetails()
        self.database.insert_into_item(current_item_details)

        try:
            pass

        except ValueError:
            pass

    def addCategory(self):
        pass

a = Tk()
entry = RecordEntryWindow(a)
a.mainloop()