from database_manager import DatabaseManager
from table import Table, itemsListWidget,OptionsBar
from tkinter import Tk

if __name__ == "__main__":
    d = DatabaseManager()
    win = Tk()
    win.title("Historic Items - Priory")
    win.resizable(False, False)
    table = Table([], "text.bin",d)
    list_widget = itemsListWidget(win, table)
    items = d.get_historic_items()
    list_widget.changeitemsShown(items)

    OptionsBar(win, table, list_widget).pack()
    list_widget.pack()
    win.mainloop()
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