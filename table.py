from tkinter import ttk, Button, Toplevel, Label, Menu, Frame, Entry, Tk
import pickle

class Table(list):
    def __init__(self, items, db_manager):
        super().__init__()
        self.db = db_manager
        self.read_from_db()
        self.extend(items)

    def read_from_db(self):
        self.clear()
        data = self.db.get_historic_items()
        self.extend([(record[0], record[1], record[2], record[3], record[4]) for record in data])

    def delete_historic_item(self, record):
        self.remove(record)
        #self.db.drop_record()

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
        self.show_items()
        self.right_click_options = Menu(self, tearoff=0) ######## self might have to be a Tk instance??
        self.right_click_options.add_command(label="Edit", command=self.editSelection)
        self.right_click_options.add_command(label="Delete", command=self.deleteSelection)
        self.bind("<Button-3>", self.showRightClickOptions)

    def getSelection(self):
        return self.selection()

    def editSelection(self):
        pass
        # record = self.items.findrecordFromname(self.getSelection()[0])
        # EditrecordWidget(self, record, self.update_items)

        # print(self.getSelection()[0][1])
    def deleteSelection(self):
        pass
        # record = self.items.findrecordFromname(self.getSelection()[0])
        # self.items.delete_historic_item(record)
        # if record in self.items_shown:
        #     self.items_shown.remove(record)
        # self.update_items()

    def showRightClickOptions(self, event):
        row_id = self.identify_row(event.y)
        if row_id is not None:
            self.selection_set(row_id)
            self.right_click_options.post(event.x_root, event.y_root)

    def clear(self):
        for child in self.get_children():
            self.delete(child)

    def show_items(self):
        for record in self.items_shown:
            print(record[0])
            self.show_historic_item(record)

    def show_historic_item(self, record):
        record = list(record) # cast to list so you can edit
        for i in range(len(record)):
            if record[i] == None:
                record[i] = "N/A" # more understandable for user
        self.insert('', "end", iid=record[0], values=(record[0], record[1], record[2], record[3], 
                    "No images available" if record[4] == 0 else "Click to view images"))

    def update_items(self):
        self.clear()
        self.show_items()

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
        Button(self, text="Add", command=self.addrecord).grid(row=0, column=1)

    def addrecord(self):
        pass
        #add_new_itemrecordWidget(self, self.items, self.search_box.searchAndUpdate)

class DropDownSelectWidget(Frame):
    def __init__(self, master, options, starting_option):
        super().__init__(master)
        self.option_menu = ttk.Combobox(self, values=options)
        self.option_menu.set(starting_option)
        self.option_menu.grid(row=0, column=0)

    def getSelection(self) -> str:
        return self.option_menu.get()