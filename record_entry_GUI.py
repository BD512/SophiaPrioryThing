from tkinter import Tk, Label, Entry, ttk, Text, IntVar, Button, Toplevel, Frame
from database_manager import DatabaseManager
from datetime import date
from ImagesUpload import FilesUpload

class RecordDetailsEntry(Frame):
    def __init__(self, master, categories: tuple, category_dict: dict, name: str="", description: str="", category: str=None, subcategory: str=None, year: int=None, confidence: int=0):
        super().__init__(master)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.confidence_level = IntVar(value=confidence)
        self.categories = categories

        Label(self, text="Item name:").grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.name_entry = Entry(self)
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        Label(self, text="Category:").grid(row=1, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.category_menu = ttk.Combobox(self, values=self.categories)
        self.category_menu.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
        self.category_menu.bind('<<ComboboxSelected>>', self.updateSubcategoryMenu)
        self.category_menu.set("Miscellaneous" if category is None else category)

        self.category_dict = category_dict # self.database.get_category_dict(self.categories)
        # print(self.category_dict)
        # print(self.category_dict["M"])

        Label(self, text="Subcategory:").grid(row=2, column=0, padx=10, pady=0, sticky="nsew")
        self.subcategory_menu = ttk.Combobox(self, values=self.category_dict[
            "Miscellaneous"] if subcategory is None else subcategory)  # default selection is miscellaneous
        self.subcategory_menu.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.subcategory_menu.bind('<FocusIn>', self.updateSubcategoryMenu)
        self.subcategory_menu.bind('<Button-1>', self.updateSubcategoryMenu)

        Label(self, text="Description:").grid(row=3, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.description_entry = Text(self, wrap="word", width=4, height=4)
        self.description_entry.insert("1.0", description)
        self.description_entry.grid(row=3, column=1, pady=10, sticky="nsew")

        Label(self, text="Year:").grid(row=4, column=0, padx=10, pady=(5, 0))
        self.year_entry = Entry(self)
        if year is not None: self.year_entry.insert(0, str(year))
        self.year_entry.grid(row=4, column=1, padx=10, pady=0)

        # Label(self, text="Year confidence:").grid(row=0, column=4, padx=(5,0), pady=10)
        self.confident_check = ttk.Checkbutton(self, text="I am confident in year", variable=self.confidence_level,
                                               onvalue=1,
                                               offvalue=0)
        self.confident_check.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

        self.files_upload = FilesUpload(self, "test")
        self.files_upload.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def getName(self) -> str:
        return self.name_entry.get().title()

    def getCategory(self) -> str:
        return self.category_menu.get().title()

    def getSubcategory(self) -> str:
        return self.subcategory_menu.get().title()

    def getDescription(self) -> str:
        return self.description_entry.get("1.0", "end-1c").capitalize()

    def getYear(self) -> str:
        return self.year_entry.get()

    def getConfidence(self) -> bool:
        return bool(
            self.confidence_level.get())  # doesn't need to be validated so can be cast in the getter, unlike year

    def updateSubcategoryMenu(self, event):
        current_category = self.category_menu.get()
        if current_category in self.category_dict.keys():
            self.subcategory_menu.config(values=self.category_dict[current_category])
        else:
            self.subcategory_menu.config(values=[])

class RecordDetailsWindow(Toplevel):
    def __init__(self, master, database_manager: DatabaseManager, name: str="", description: str="", category: str=None, subcategory: str=None, year: int=None, confidence: int=0):
        super().__init__(master)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # self.add_item = True
        self.database = database_manager

        categories = self.database.get_categories()
        self.record_entry = RecordDetailsEntry(self, self.database.get_categories(),
                                               self.database.get_category_dict(categories), name, description, category, subcategory, year, confidence)
        self.record_entry.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.action_btn = Button(self, text="Enter", command=self.enter_item)  # the final submit button

        # else:  # must be editing
        # action_btn = Button(self, text="Edit item", command=self.add_item_record)  # the final submit button

        self.action_btn.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.error_msg = Label(self, text="", width=25, wraplength=120,
                               fg="#da4646")  # the error message to update depending on the input of
        self.error_msg.grid(row=1, column=0)

    def change_button_text(self, text):
        self.action_btn.config(text=text)

    def enter_item(self):
        raise NotImplementedError

    def update_error_msg(self, text):
        self.error_msg.config(text=text)

    def get_item_details_for_record(self) -> tuple[
        str, str, str, int, bool]:  # returns all current item info but not the overall category, also, casts the year to be an integer as it's already been validated before now so won't cause a ValueError
        try:
            return self.record_entry.getName(), self.record_entry.getSubcategory(), self.record_entry.getDescription(), int(
                self.record_entry.getYear()), self.record_entry.getConfidence()
        except ValueError:
            return self.record_entry.getName(), self.record_entry.getSubcategory(), self.record_entry.getDescription(), -1, self.record_entry.getConfidence()

    def get_all_item_details_for_validation(self) -> list[
        str|bool]:  # returns all item details, including the larger category
        return [self.record_entry.getName(), self.record_entry.getSubcategory(), self.record_entry.getCategory(), self.record_entry.getDescription(), self.record_entry.getYear(),
                self.record_entry.getConfidence()]

    def get_database_categories(self):
        return self.database.get_categories()

    def get_database_subcategories(self):
        return self.database.get_subcategories()

    def is_valid_record(
            self) -> bool:  # returns if the current item's inputted data is valid, and updates the error message for whenever it isn't
        details = self.get_all_item_details_for_validation()
        not_null_details = self.get_all_item_details_for_validation()
        # print(f"b4 popping\nnot null details: {not_null_details}\ndetails: {details}")
        not_null_details.pop(3)  # has the list of all items details without the descriotion for comparison:
        not_null_details.pop(3)  # now removes the year based off of new index
        # print(f"after popping\nnot null details: {not_null_details}\ndetails: {details}")

        if "" in not_null_details:  # because details[3] is the description, which is allowed to be an empty string
            self.update_error_msg("Make sure to enter all necesary item details (name and categories)")
            return False

        if self.update_category():

            if details[4] != "":  # if there is a year entered, check that it is valid
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

        else:
            return False

        # TODO:
        # need option of adding a subcategory's description somewhere at some point yes yes

        # with beth's edits, i swear now the categories being used inside some of these classes aren't updated as categories are added because they're attributes instead of getters? idk check this

    def is_new_category(self) -> bool:  # method to return whether or not the current category is new
        if self.record_entry.getCategory() not in self.get_database_categories():
            print("new category")
            return True
        print("old category")
        return False

    def is_new_subcategory(self) -> bool:  # method to check if the current subcategory already exists
        # print(self.get_subcategory(), self.database.get_subcategories())
        # print(self.get_subcategory() not in self.database.get_subcategories())
        if self.record_entry.getSubcategory() not in self.get_database_subcategories():
            print("new subcategory")
            return True
        print("old subcategory")
        return False

    def update_category(
            self):  # if there is a new category or subcategory, it is added to the database's matching category table accordingly, returns whether this was successful
        print("updating category")
        if self.is_new_category():
            if self.is_new_subcategory():
                self.database.insert_into_category(self.record_entry.getSubcategory(), self.record_entry.getCategory(), None)
                return True

            else:  # cannot have duplicate subcategories even with different categories - subcategories must be unique
                self.update_error_msg("If you are adding a new category, the subcategory must also be new")
                return False

        elif self.is_new_subcategory():
            self.database.insert_into_category(self.record_entry.getSubcategory(), self.record_entry.getCategory(),
                                               None)  # subcategory description is currently None - maybe instead could have something appear for sophia to add description
            return True

        else:
            return True


class AddItemWindow(RecordDetailsWindow):
    def __init__(self, master, database_manager:DatabaseManager):
        super().__init__(master, database_manager)
        self.change_button_text("Add item")
        self.title("Add Item")

    def enter_item(
            self):  # inserts item record into the historical item table after updating the category table where necessary
        # self.update_category()
        if self.is_valid_record():
            details = self.get_item_details_for_record()
            # print(details[3])
            if details[3] != -1:
                self.database.insert_into_item(details[0], details[1], details[2], details[3], details[4])
            else:  # enforce not being confident about the year if no year has been entered
                self.database.insert_into_item(details[0], details[1], details[2], details[3], False)

            # def insert_into_item(self,name="NULL",subcategory="MISC",description = "NULL",year=-1,confidence=0):


class EditItemWindow(RecordDetailsWindow):
    def __init__(self, master, database_manager: DatabaseManager, item_id):
        self.database = database_manager
        self.item_details = self.database.get_item_from_id(item_id) # id, name, subcategory, description, year, confidence
        print(self.item_details)
        d = self.get_item_details_to_fill()
        super().__init__(master, database_manager, d[0], d[1], d[2], d[3], d[4], d[5]) # todo pass information got from database in as parameter here
        self.title("Edit Item")
        self.change_button_text("Edit item")
        # name: str="", description: str="", category: str=None, subcategory: str=None, year: int=None, confidence):

    def get_item_details_to_fill(self) -> tuple:
        d = self.item_details
        category = self.database.get_category(d[2])
        return d[1], d[3], category, d[2], d[4], d[5]
    
    def enter_item(self):
        if self.is_valid_record():
            details = self.get_item_details_for_record()
            if details[3] != -1:
                self.database.edit_item_record(details[0], details[1], details[2], details[3], details[4])
            else:
                self.database.edit_item_record(details[0], details[1], details[2], details[3], False)
        self.destroy()


a = Tk()
entry = AddItemWindow(a, DatabaseManager())
edit = EditItemWindow(a, DatabaseManager(),5)
a.mainloop()