
# copied from Kaela's code but made a few changes
# making independent of the database instance to make the code more versatile
# if info needed from database to show options to add a record, this will be passed in as a parameter

from tkinter import Tk, Label, Entry, ttk, Text, IntVar, Button

class RecordEntryGUI(Tk):
    def __init__(self):
        super().__init__()
        self.confidence_level = IntVar()
        self.categories = ("S", "L", "CS", "P", "W", "E", "LC", "M")  # set categories
        # to be moved to the main program to decide this

        Label(self, text="Item name:").grid(row=0, column=0, padx=10, pady=(5, 0))
        self.name_entry = Entry(self)
        self.name_entry.grid(row=1, column=0, padx=10, pady=10)

        Label(self, text="Category:").grid(row=0, column=1, padx=10, pady=(5, 0))
        self.category_menu = ttk.Combobox(self, values=self.categories)
        self.category_menu.grid(row=1, column=1, padx=10, pady=0)
        self.category_menu.bind('<<ComboboxSelected>>', self.update_subcategory_menu)
        self.category_menu.set("M")

        Label(self, text="Subcategory:").grid(row=2, column=1, padx=10, pady=0)
        self.subcategory_menu = ttk.Combobox(self, values=self.category_dict["M"])  # default selection is miscellaneous
        self.subcategory_menu.grid(row=3, column=1, padx=10, pady=(0, 10))
        self.subcategory_menu.bind('<FocusIn>', self.update_subcategory_menu)
        self.subcategory_menu.bind('<Button-1>', self.update_subcategory_menu)

        Label(self, text="Description:").grid(row=0, column=2, padx=10, pady=(5, 0))
        self.description_entry = Text(self, height=5, width=25, wrap="word")
        self.description_entry.grid(row=1, column=2, rowspan=3, pady=10, sticky="n")

        Label(self, text="Year:").grid(row=0, column=3, padx=10, pady=(5, 0))
        self.year_entry = Entry(self)
        self.year_entry.grid(row=1, column=3, padx=10, pady=0)

        # Label(self, text="Year confidence:").grid(row=0, column=4, padx=(5,0), pady=10)
        self.confident_check = ttk.Checkbutton(self, text="I am confident", variable=self.confidence_level, onvalue=1,
                                               offvalue=0)
        self.confident_check.grid(row=2, column=3, padx=10, pady=10, sticky="n")

        addBtn = Button(self, text="Add item")
        addBtn.grid(row=4, column=3, padx=10, pady=10, sticky="n")

        testBtn = Button(self, text="test", command=self.test)
        testBtn.grid(row=2, column=0)

    def update_subcategory_menu(self, event):
        current_category = self.category_menu.get()
        self.subcategory_menu.config(values=self.category_dict[current_category])

    def get_name(self) -> str:
        return self.name_entry.get()

    def get_subcategory(self) -> str:
        return self.subcategory_menu.get()

    def get_description(self) -> str:
        return self.description_entry.get("1.0", "end-1c")

    def get_year(self) -> int:
        return self.year_entry.get()

    def get_confidence(self) -> bool:
        return self.confidence_level.get()

    def is_valid_record(self) -> bool:
        pass

    def test(self):
        print(self.get_name(), self.get_category(), self.get_description(), self.get_year(), self.get_confidence())
        # print(bool(self.get_name()))

    def add_record(self):
        try:
            pass

        except ValueError:
            pass

    def addCategory(self):
        pass


entry = RecordEntryGUI()
entry.mainloop()