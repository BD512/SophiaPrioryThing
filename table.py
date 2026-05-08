from tkinter import ttk, Button, Toplevel, Label, Menu, Frame, Entry, Tk
import pickle

class HistoricItem:
    def __init__(self, name:str, subcategory:str, approx_year:str, description:str, no_images:int):
        self.name = name
        self.subcategory = subcategory
        self.approx_year = approx_year
        self.description = description
        self.no_images = no_images

    def get_name(self):
        return self.name

    def get_no_images(self):
        return self.no_images

    def get_subcategory(self):
        return self.subcategory

    def get_approx_year(self):
        return self.approx_year

    def get_description(self):
        return self.description

    def set_name(self, name):
        self.name = name

    def set_images(self, images):
        self.images = images

    def set_subcategory(self, subcategory):
        self.subcategory = subcategory

    def set_description(self, description):
        self.description = description

    def set_approx_year(self, approx_year):
        self.approx_year = approx_year

class Table(list):
    def __init__(self, items, filename:str, db_manager):
        super().__init__()
        self.db = db_manager
        self.read_from_db()
        self.extend(items)

    def read_from_db(self):
        self.clear()
        data = self.db.get_historic_items()
        self.extend([HistoricItem(record[0], record[1], record[2], record[3], record[4]) for record in data])

    def deleteHistoricItem(self, HistoricItem):
        self.remove(HistoricItem)
        self.writeToFile()

    def addNew(self, name, subcategory, approx_year, description:float, images:bool):
        self.append(HistoricItem(name, subcategory, approx_year, description, images))
        self.writeToFile()

class itemsListWidget(ttk.Treeview):
    def __init__(self, master, items:Table):
        super().__init__(master, show="headings", columns=("c1", "c2", "c3", "c4", "c5"), height=4)
        self.items = items
        self.items_shown = items
        self.column("#1")
        self.heading("#1", text="Name")
        self.column("#2")
        self.heading("#2", text="Subcategory")
        self.column("#3")
        self.heading("#3", text="Approx Year")
        self.column("#4")
        self.heading("#4", text="Description")
        self.column("#5")
        self.heading("#5", text="Images")
        self.showitems()
        self.right_click_options = Menu(self, tearoff=0) ######## self might have to be a Tk instance??
        self.right_click_options.add_command(label="Edit", command=self.editSelection)
        self.right_click_options.add_command(label="Delete", command=self.deleteSelection)
        self.bind("<Button-3>", self.showRightClickOptions)

    def getSelection(self):
        return self.selection()

    def editSelection(self):
        pass
        # HistoricItem = self.items.findHistoricItemFromname(self.getSelection()[0])
        # EditHistoricItemWidget(self, HistoricItem, self.update_items)

        # print(self.getSelection()[0].get_subcategory())
    def deleteSelection(self):
        pass
        # HistoricItem = self.items.findHistoricItemFromname(self.getSelection()[0])
        # self.items.deleteHistoricItem(HistoricItem)
        # if HistoricItem in self.items_shown:
        #     self.items_shown.remove(HistoricItem)
        # self.update_items()

    def showRightClickOptions(self, event):
        row_id = self.identify_row(event.y)
        if row_id is not None:
            self.selection_set(row_id)
            self.right_click_options.post(event.x_root, event.y_root)

    def clear(self):
        for child in self.get_children():
            self.delete(child)

    def showitems(self):
        for HistoricItem in self.items_shown:
            print(HistoricItem.get_name())
            self.show_historic_item(HistoricItem)

    def show_historic_item(self, HistoricItem):
        self.insert('', "end", iid=HistoricItem.get_name(), values=(HistoricItem.get_name(), HistoricItem.get_subcategory(), HistoricItem.get_approx_year(), f"£{HistoricItem.get_description():.2f}", "yes" if HistoricItem.isimages() else "no"))

    def update_items(self):
        self.clear()
        self.showitems()
        self.items.writeToFile()

    def change_items_shown(self, items):
        self.items_shown = items
        self.update_items()

class SearchBox(Frame):
    def __init__(self, master, items, list_widget):
        super().__init__(master)
        self.items = items
        self.list_widget = list_widget
        Label(self, text="Search:").grid(row=0, column=0)
        self.search_entry = Entry(self)
        self.search_entry.grid(row=0, column=1)
        self.search_entry.bind("<KeyRelease>", self.searchAndUpdate)

    def searchAndUpdate(self, event=None):
        items = self.items.searchByPhrase(self.search_entry.get())
        self.list_widget.change_items_shown(items)

class OptionsBar(Frame):
    def __init__(self, master, items, list_widget):
        super().__init__(master)
        self.items = items
        self.list_widget = list_widget
        self.search_box = SearchBox(self, self.items, list_widget)
        self.search_box.grid(row=0, column=0)
        Button(self, text="Add", command=self.addHistoricItem).grid(row=0, column=1)

    def addHistoricItem(self):
        pass
        #AddNewHistoricItemWidget(self, self.items, self.search_box.searchAndUpdate)

class DropDownSelectWidget(Frame):
    def __init__(self, master, options, starting_option):
        super().__init__(master)
        self.option_menu = ttk.Combobox(self, values=options)
        self.option_menu.set(starting_option)
        self.option_menu.grid(row=0, column=0)

    def getSelection(self) -> str:
        return self.option_menu.get()

class HistoricItemInfoEntry(Frame):
    def __init__(self, master, approx_years, name="", subcategory="", approx_year=None, description=10, is_images=True):
        super().__init__(master)
        Label(self, text="name").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = Entry(self)
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        Label(self, text="subcategory").grid(row=1, column=0, padx=10, pady=5)
        self.subcategory_entry = Entry(self)
        self.subcategory_entry.insert(0, subcategory)
        self.subcategory_entry.grid(row=1, column=1, padx=10, pady=5)
        Label(self, text="approx_year").grid(row=2, column=0, padx=10, pady=5)
        self.approx_year_entry = DropDownSelectWidget(self, approx_years, approx_year if approx_year else approx_years[0])
        self.approx_year_entry.grid(row=2, column=1, padx=10, pady=5)
        Label(self, text="description £").grid(row=3, column=0, padx=10, pady=5)
        self.description_entry = Entry(self)
        self.description_entry.insert(0, str(description))
        self.description_entry.grid(row=3, column=1, padx=10, pady=5)
        Label(self, text="Is images").grid(row=4, column=0, padx=10, pady=5)
        self.is_images_entry = DropDownSelectWidget(self, ["Yes", "No"], "Yes" if is_images else "No")
        self.is_images_entry.grid(row=4, column=1, padx=10, pady=5)

    def get_name(self):
        return self.name_entry.get()

    def get_subcategory(self):
        return self.subcategory_entry.get()

    def get_approx_year(self):
        return self.approx_year_entry.getSelection()

    def get_description(self):
        return self.description_entry.get()

    def getIsimages(self):
        return self.is_images_entry.getSelection()