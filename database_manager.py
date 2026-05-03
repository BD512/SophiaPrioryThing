import sqlite3

# class that manages the database (3 tables)
class DatabaseManager:
    def __init__(self,database = "Priory.db", item_table="tblHistoricalItem",image_table="tblItemImage",category_table="tblMatchingCategory"):
        # extracts names of tables for consistency
        self.item_table = tables[0]
        self.image_table = tables[1]
        self.category_table = tables[2]
        #connects to database
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    # method to get list of column names in a certain table
    def get_column_names(self,table:str):
        self.cursor.execute(f"PRAGMA table_info({table});")
        # retrieves all data about columns in that table as a list of tuples
        columns_info = self.cursor.fetchall()
        column_names = tuple([column[1] for column in columns_info])
        # the column name is the second piece of data (after the column number)
        return column_names

    # method to return any entire column from table
    def get_column(self,table:str,column:str):
        statement = f"SELECT {column} FROM {table};"
        self.cursor.execute(statement)
        return self.cursor.fetchall()
    
    # method to insert a new record into image table
    def insert_into_image(self,ID_number:int,path:str):
        column_names = self.get_column_names(self.image_table)
        self.cursor.execute(f"INSERT INTO {self.image_table} {column_names} \
                            VALUES ({ID_number},'{path}');")
        self.conn.commit() # updates changes

    # method to insert a new record into historic items table
    def insert_into_item(self,name="NULL",subcategory="MISC",description = "NULL",year=-1,confidence=0):
        if year < 0: year = "NULL" # years in AD must be positive
        temp = [name,subcategory,description]
        for i in range(len(temp)):
            if temp[i] != "NULL":
                temp[i] = f"'{temp[i]}'" # adds extra speech marks around strings
        name,subcategory,description = temp # unpacks after updating
        column_names = self.get_column_names(self.item_table)[1:] # first column is autoincrement
        self.cursor.execute(f"INSERT INTO {self.item_table} {column_names} \
                            VALUES ({name},{subcategory},{description},{year},{confidence});")
        self.conn.commit() # updates changes

    # method to insert a new record into matching category table
    def insert_into_category(self,subcategory="MISC",category="MISC"):
        column_names = self.get_column_names(self.category_table)
        self.cursor.execute(f"INSERT INTO {self.category_table} {column_names} \
                            VALUES ('{subcategory}','{category}');")
        self.conn.commit() # updates changes

    # method to get image path/s from image id
    def get_image_path(self,id:int):
        statement = f"SELECT ImagePath FROM {self.image_table} WHERE IDNumber=? ;"
        self.cursor.execute(statement,(id,)) # parameter must be passed in as tuple
        return self.cursor.fetchall()
    
    # method to get corresponding overarching category from the matching category table
    def get_category(self,subcategory:str) -> str:
        statement = f"SELECT Category FROM {self.category_table} WHERE Subcategory='{subcategory}' ;"
        self.cursor.execute(statement)
        temp = self.cursor.fetchall() # not yet in a usable format
        category = temp[0][0]
        return category
    
    # method to return the list of subcategories for a given category
    def get_subcategories(self, category:str) -> list[str]:
        statement = f"SELECT Subcategory FROM {self.category_table} WHERE Category='{category}' ;"
        self.cursor.execute(statement)
        temp = self.cursor.fetchall() # not yet in a usable format
        subcategory_list = list()
        for subcategory in temp:
            subcategory_list.append(subcategory[0])
        return subcategory_list
    
    # method to return a dictionary of categories and their associated list of categories
    def get_category_dict(self, categories:tuple[str]) -> dict:
        #categories = self.get_column(f"{self.item_table}","Category")
        dictionary = dict()
        for category in categories:
            subcategories = self.get_subcategories(category)
            dictionary.update({category:subcategories})
        return dictionary

    # method to display list of all items - can be sorted differently
    def display_historic_items(self, order_by = "Year"):
        self.cursor.execute(f"""
            SELECT Name, Category, Description,
            CASE 
                WHEN Confidence = 1 THEN Year 
                ELSE "c. " || Year 
            END AS [approx Year]
            FROM HistoricalItems
            ORDER BY {order_by} IS NULL, {order_by};
            """)
        return self.cursor.fetchall()
    
    # method that commits changes and closes connection before a table object is garbage-collected
    def __del__(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    d = DatabaseManager()
    # testing
    # d.insert_into_item(name="Cross",description="Very nice.",category="Crucifixes",year=2000)
    # d.insert_into_category("MISC","M")
    # print(d.get_category("Lecturns"))
    # print(d.get_subcategories("CS"))
    # print(d.get_category_dict(("S", "L", "CS", "P", "W", "E", "LC", "M")))
    # d.insert_into_image(ID_number=10,path="fake.png")
    # d.insert_into_image(ID_number=10,path="fake.png")
