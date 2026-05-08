from tkinter import Tk, Label, Entry, ttk, Text, IntVar, Button, Toplevel
from database_manager import DatabaseManager
from datetime import date

class RecordEntryWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.database = DatabaseManager()

        self.confidence_level = IntVar()
        self.categories = self.database.get_categories()

        Label(self, text="Item name:").grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.name_entry = Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        Label(self, text="Category:").grid(row=1, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.category_menu = ttk.Combobox(self, values=self.categories)
        self.category_menu.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
        self.category_menu.bind('<<ComboboxSelected>>', self.update_subcategory_menu)
        self.category_menu.set("Miscellaneous")

        self.category_dict = self.database.get_category_dict(self.categories)
        # print(self.category_dict)
        # print(self.category_dict["M"])

        Label(self, text="Subcategory:").grid(row=2, column=0, padx=10, pady=0, sticky="nsew")
        self.subcategory_menu = ttk.Combobox(self, values=self.category_dict["Miscellaneous"])  # default selection is miscellaneous
        self.subcategory_menu.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.subcategory_menu.bind('<FocusIn>', self.update_subcategory_menu)
        self.subcategory_menu.bind('<Button-1>',self.update_subcategory_menu)

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

        addBtn = Button(self, text="Add item", command=self.add_item_record) # the final submit button
        addBtn.grid(row=6, column=1, padx=10, pady=10, sticky="nsew")

        self.errorMsg = Label(self, text="", width=25, wraplength=120, fg="#da4646") # the error message to update depending on the input of 
        self.errorMsg.grid(row=6, column=0)

        # testBtn = Button(self, text="test", command=self.test)
        # testBtn.grid(row=6, column=1)

    def update_subcategory_menu(self, event): 
        current_category = self.category_menu.get()
        self.subcategory_menu.config(values=self.category_dict[current_category])

    def update_error_msg(self, text):
        self.errorMsg.config(text=text)

    def get_name(self) -> str:
        return self.name_entry.get().title()
    
    def get_category(self) -> str:
        return self.category_menu.get()

    def get_subcategory(self) -> str:
        return self.subcategory_menu.get()

    def get_description(self) -> str:
        return self.description_entry.get("1.0", "end-1c")

    def get_year(self) -> str:
        return self.year_entry.get()

    def get_confidence(self) -> bool:
        return bool(self.confidence_level.get()) # doesn't need to be validated so can be cast in the getter, unlike year

    def get_item_details_for_record(self) -> list[str, str, str, int, bool]: # returns all current item info but not the overall category, also, casts the year to be an integer as it's already been validated before now so won't cause a ValueError
        return [self.get_name(), self.get_subcategory(), self.get_description(), int(self.get_year()), self.get_confidence()]
    
    def get_all_item_details_for_validation(self) -> list[str, str, str, str, str, bool]: # returns all item details, including the larger category
        return [self.get_name(), self.get_subcategory(), self.get_category(), self.get_description(), self.get_year(), self.get_confidence()]

    def is_valid_record(self) -> bool: # returns if the current item's inputted data is valid, and updates the error message for whenever it isn't
        details = self.get_all_item_details_for_validation()
        not_null_details = self.get_all_item_details_for_validation()
        # print(f"b4 popping\nnot null details: {not_null_details}\ndetails: {details}")
        not_null_details.pop(3) # has the list of all items details without the descriotion for comparison:
        not_null_details.pop(3) # now removes the year based off of new index
        # print(f"after popping\nnot null details: {not_null_details}\ndetails: {details}")

        if "" in not_null_details: # because details[3] is the description, which is allowed to be an empty string
            self.update_error_msg("Make sure to enter all necesary item details (name and categories)")
            return False

        else:
            if details[4]: # if there is a year entered, check that it is valid
                try:
                    item_year = int(details[4])

                    if item_year > date.today().year:
                        self.update_error_msg("This year hasn't happened yet")
                        return False
                    
                    elif item_year < 0:
                        self.update_error_msg("Year must be positive AD")
                        return False
                    
                except ValueError:
                    self.update_error_msg("Make sure the year is an integer number")
                    return False
            
            self.update_error_msg("")
            return True

        # TODO:
        # add more validation? did i miss anything? it's 1:30am so i probably did
        # check what's happening with year validation - is this right?
        # is anything else allowed to be "", is anything ive allowed to be "" not actually allowed to be ""
        # AM i correct that all subcategories must be unique regardless of category?
        # is me casting confidence from an int to a bool unnecessary? just bc i noticed in database manager it's default value is an int
        # what's happening with images?

        # need option of adding a subcategory's description somewhere at some point yes yes
        # lol i haven't tested this at allllllllllllllllll
        # need to add method to database manager to get categories instead of having that hard-coded tuple in the initialisation of this toplevel

    def update_category(self): # if there is a new category or subcategory, it is added to the database's matching category table accordingly

        if self.is_new_category():
            if self.is_new_subcategory():
                self.database.insert_into_category(self.get_subcategory(),self.get_category(),"")

            else: # cannot have duplicate subcategories even with different categories - subcategories must be unique
                self.update_error_msg("If you are adding a new category, the subcategory must also be new")

        elif self.is_new_subcategory():
            self.database.insert_into_category(self.get_subcategory(),self.get_category(),"") # subcategory description is currently blank - maybe instead could have something appear for sophia to add description

    def is_new_category(self) -> bool: # method to return whether or not the current category is new
        if self.get_category() not in self.categories:
            return True
        return False

    def is_new_subcategory(self) -> bool: # method to check if the current subcategory already exists
        if self.get_subcategory() not in self.database.get_subcategories():
            return True
        return False

    def add_item_record(self): # inserts item record into the historical item table after updating the category table where necessary
        self.update_category()
        if self.is_valid_record():
            self.database.insert_into_item(self.get_item_details_for_record())
            print(self.get_item_details_for_record())
            # def insert_into_item(self,name="NULL",subcategory="MISC",description = "NULL",year=-1,confidence=0):
 

    def test(self): # testinggg!
        self.is_valid_record()
        print(self.get_name(), self.get_subcategory(), self.get_description(), self.get_year(), self.get_confidence())
        # print(bool(self.get_name()))


a = Tk()
entry = RecordEntryWindow(a)
a.mainloop()