from tkinter import ttk, Menu, Frame

class HistoricItems(list):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.read_from_db()

    def read_from_db(self):
        self.clear()
        data = self.db.get_historic_items()
        self.extend([(record[0], record[1], record[2], record[3], record[4]) for record in data])

    def delete_historic_item(self, record):
        id = self.db.get_id_number(record[0])
        if id:
            self.db.delete_record(id)
        self.read_from_db() # update list view 

class Table(ttk.Treeview):
    def __init__(self, master, items:HistoricItems):
        super().__init__(master, show="headings", columns=("#1", "#2", "#3", "#4", "#5"), height=5)
        self.items = items
        self.items_shown = items
        columns={"#1":"Name", "#2":"Subcategory", "#3":"Approx Year", "#4":"Description", "#5":"Images"}
        for key,value in columns.items():
            self.column(key)
            self.heading(key, text=value)
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
        record = self.getSelection()
        self.items.delete_historic_item(record)
        if record in self.items_shown:
            self.items_shown.remove(record)
        self.update_items()

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

class DropDownSelectWidget(Frame):
    def __init__(self, master, options, starting_option):
        super().__init__(master)
        self.option_menu = ttk.Combobox(self, values=options)
        self.option_menu.set(starting_option)
        self.option_menu.grid(row=0, column=0)

    def getSelection(self) -> str:
        return self.option_menu.get()