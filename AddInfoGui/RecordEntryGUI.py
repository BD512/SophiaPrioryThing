from tkinter import Tk, Label, Entry, ttk, Text, IntVar, Button

class RecordEntryGUI(Tk):
    def __init__(self):
        super().__init__()

        self.confidence_level = IntVar()

        Label(self, text="Item name:").grid(row=0, column=0, padx=10, pady=(5,0))
        self.name_entry = Entry(self)
        self.name_entry.grid(row=1, column=0, padx=10, pady=10)

        Label(self, text="Category:").grid(row=0, column=1, padx=10, pady=(5,0))
        categories = ["A", "B", "C", "D"]
        self.category_menu = ttk.Combobox(self, values=categories)
        self.category_menu.grid(row=1, column=1, padx=10, pady=10)
        #self.category_menu.set("")

        Label(self, text="Description:").grid(row=0, column=2, padx=10, pady=(5,0))
        self.description_entry = Text(self, height=4, width=25, wrap="word")
        self.description_entry.grid(row=1, column=2, rowspan=2)

        Label(self, text="Year:").grid(row=0, column=3, padx=10, pady=(5,0))
        self.year_entry = Entry(self)
        self.year_entry.grid(row=1, column=3, padx=10, pady=0)

        #Label(self, text="Year confidence:").grid(row=0, column=4, padx=(5,0), pady=10)
        self.confident_check = ttk.Checkbutton(self, text="I am confident", variable=self.confidence_level, onvalue=1, offvalue=0)
        self.confident_check.grid(row=2, column=3, padx=10, pady=10, sticky="n")

        testBtn = Button(self, text="test", command=self.test)
        testBtn.grid(row=2, column=0)

    def getName(self) -> str:
        return self.name_entry.get()
    
    def getCategory(self) -> str:
        return self.category_menu.get()
    
    def getDescription(self) -> str:
        return self.description_entry.get("1.0", "end-1c")
    
    def getYear(self) -> int:
        return self.year_entry.get()
    
    def getConfidence(self) -> bool:
        return self.confidence_level.get()

    def isValidRecord(self) ->bool:
        pass

    def test(self):
        print(self.getName(), self.getCategory(), self.getDescription(), self.getYear(), self.getConfidence())
        #print(bool(self.getName()))

    def addRecord(self):
        try:
            pass

        except ValueError:
            pass

    def addCategory(self):
        pass

entry = RecordEntryGUI()
entry.mainloop()