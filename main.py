from database_manager import DatabaseManager
from table import Table
from tkinter import Tk, Button
from record_entry_GUI import AddItemWindow

class Main(Tk):
    def __init__(self):
        super().__init__()
        self.title("Historic Items - Priory")
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.resizable(False, False)
        self.database_manager = DatabaseManager()
        # self.items = HistoricItems(self.database_manager)
        Button(self, text="Add", command=self.addItem).grid(row=0, column=0, sticky="nsew")
        self.list_widget = Table(self, self.database_manager)
        self.list_widget.update_items_from_database()
        self.list_widget.grid(row=1, column=0, sticky="nsew")


    def addItem(self):
        add_item = AddItemWindow(self, self.database_manager)
        self.wait_window(add_item)
        self.list_widget.update_items_from_database()
        # self.update()


if __name__ == "__main__":
    Main().mainloop()
    # d = DatabaseManager()
    # win = Tk()
    # win.title("Historic Items - Priory")
    # win.resizable(False, False)
    # items = HistoricItems(d)
    # list_widget = Table(win, items)
    # list_widget.update_items()
    #OptionsBar(win, table, list_widget).pack()
    # list_widget.pack()
    # win.mainloop()
    # d.drop_tables()
    # d.create_database()
    # d.create_subcategories()
    # d.insert_into_item(name="Silver Cross",subcategory="Coptic Crosses",description="It looks very shiny.",year=1999,confidence=1)
    # d.insert_into_item(name="Wooden Cross",subcategory="Coptic Crosses",description="Not shiny.",year=2010,confidence=1)
    # d.insert_into_item(name="Gold Cross",subcategory="Coptic Crosses",description="Very shiny.",year=1800)
    # d.insert_into_item(name="Silver Chalice",subcategory="Chalice",description="It looks very shiny.",year=1870)
    # d.insert_into_item(name="Gold Chalice",subcategory="Chalice",description="It looks very shiny.",year=1400)
    # d.insert_into_item(name="Small Thurible",subcategory="Thurible",description="It has bells on it.",year=1900)
    # d.insert_into_item(name="Big Thurible",subcategory="Thurible",description="Very heavy.",year=1850)
    # d.insert_into_item(name="Mystery Thurible",subcategory="Thurible")
    #print(d.display_historic_items())