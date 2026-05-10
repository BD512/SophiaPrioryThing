from tkinter import ttk, Menu, Frame, TclError
from functools import partial
from record_entry_GUI import EditItemWindow
from FinalSophiaCode.database_manager import DatabaseManager
from ImageWindow import ImagesWindow

class HistoricItems(list):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.read_from_db()

    def read_from_db(self, order_by = "Name", order = "ASC", subcategory=None, category=None):
        self.clear()
        data = self.db.get_historic_items(order_by,order,subcategory,category)
        print("DATA:")
        print(data)
        self.extend([(record[0], record[1], record[2], record[3], record[4], record[5]) for record in data])

    def delete_historic_item(self, record):
        identifier = self.db.get_id_number(record[0])
        if identifier:
            self.db.delete_record(identifier)
        self.read_from_db() # update list view 

class Table(ttk.Treeview):
    def __init__(self, master, database: DatabaseManager):
        super().__init__(master, show="headings", columns=("c1", "c2", "c3", "c4", "c5"), height=10)
        self.database = database
        self.items = HistoricItems(database)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10), foreground="black")
        self.columns={"#1":"Name", "#2":"Subcategory", "#3":"approx Year", "#4":"Description", "#5":"Images"}
        for key,value in self.columns.items():
            self.column(key)
            self.heading(key, text=value, command = partial(self.sort_column,key,False))
            #self.bind("<Button>",self.change_sort)
            #self.set_colour(key) # makes all text black explicitly 
            # system default looks black, but is stored as SystemButtonText
        # Alter the Treeview's heading styles after creation
        self.show_items()
        self.right_click_options = Menu(self, tearoff=0) # self might have to be a Tk instance?
        self.right_click_options.add_command(label="Edit", command=self.editSelection)
        self.right_click_options.add_command(label="Delete", command=self.deleteSelection)
        self.bind("<Button-3>", self.showRightClickOptions)
        self.bind("<Button-1>", self.potentially_show_images_window)

    def potentially_show_images_window(self, event):
        region = self.identify("region", event.x, event.y)
        if region == "cell":
            col = self.identify_column(event.x)
            row = self.identify_row(event.y) # the row iid
            print(row)
            if col == "#5" and row:
                ImagesWindow(self, self.database, int(row))
                # value = tree.set(row, col)
                # show_popup(value)

    # This is a basic example function to show the command is triggered
    def sort_column(self, index, reverse_flag):
        if reverse_flag: order="DESC"
        else: order= "ASC"
        order_by = self.columns.get(index)
        if order_by == "Images": order_by = "[Number of Images]"
        elif order_by == "approx Year": order_by = "Year"
        print(f"Sorting column '{index}', reverse: {reverse_flag}")
        self.items.read_from_db(order_by=order_by,order=order) # type: ignore
        self.update_items()
        # toggle the sorting direction for the next click
        self.heading(index, command=partial(self.sort_column,index,not reverse_flag))

    def getSelection(self):
        return self.selection()

    def editSelection(self):
        record = self.selection()[0]
        edit_item_window = EditItemWindow(self, self.database, record)
        self.wait_window(edit_item_window)
        self.update_items_from_database()
        # record = self.items.findrecordFromname(self.getSelection()[0])
        # EditrecordWidget(self, record, self.update_items)

        # print(self.getSelection()[0][1])
    def deleteSelection(self):
        record = self.getSelection()
        self.items.delete_historic_item(record)
        if record in self.items:
            self.items.remove(record)
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
        print(self.items)
        for record in self.items:
            self.show_historic_item(record)

    def show_historic_item(self, record):
        record = list(record) # cast to list so you can edit
        for i in range(len(record)):
            if record[i] == None:
                record[i] = "N/A" # more understandable for user
        # iid should be the primary key
        # print(record[0], record[1])
        try:
            self.insert('', "end", iid=record[0], values=(record[1], record[2], record[3], record[4],
                    "No images available" if record[5] == 0 else "Click to view images"))
        except TclError:
            pass

    def update_items(self):
        self.clear()
        self.show_items()

    def update_items_from_database(self):
        self.clear()
        self.items.read_from_db()
        self.show_items()

    def change_items_shown(self, items):
        self.items = items
        self.update_items()

class DropDownSelectWidget(Frame):
    def __init__(self, master, options, starting_option):
        super().__init__(master)
        self.option_menu = ttk.Combobox(self, values=options)
        self.option_menu.set(starting_option)
        self.option_menu.grid(row=0, column=0)

    def getSelection(self) -> str:
        return self.option_menu.get()