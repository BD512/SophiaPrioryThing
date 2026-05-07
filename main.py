from database_manager import DatabaseManager

if __name__ == "__main__":
    d = DatabaseManager()
    # d.drop_tables()
    # d.create_database()
    # d.create_subcategories()
    d.insert_into_item(name="Silver Cross",subcategory="Coptic Crosses",description="It looks very shiny.",year=1999,confidence=1)
    d.insert_into_item(name="Wooden Cross",subcategory="Coptic Crosses",description="Not shiny.",year=2010,confidence=1)
    d.insert_into_item(name="Gold Cross",subcategory="Coptic Crosses",description="Very shiny.",year=1800)
    d.insert_into_item(name="Silver Chalice",subcategory="Chalice",description="It looks very shiny.",year=1870)
    d.insert_into_item(name="Gold Chalice",subcategory="Chalice",description="It looks very shiny.",year=1400)
    d.insert_into_item(name="Small Thurible",subcategory="Thurible",description="It has bells on it.",year=1900)
    d.insert_into_item(name="Big Thurible",subcategory="Thurible",description="Very heavy.",year=1850)
    d.insert_into_item(name="Mystery Thurible",subcategory="Thurible")
    print(d.display_historic_items())