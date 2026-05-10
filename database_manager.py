import sqlite3

# class that manages the database (3 tables)
class DatabaseManager:
    def __init__(self,database = "Priory.db", item_table="tblHistoricalItem",image_table="tblItemImage",category_table="tblMatchingCategory"):
        self.database = database
        self.item_table = item_table
        self.image_table = image_table
        self.category_table = category_table
        #connects to database
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.create_database() # created the tables in the database if they don't exist
        # it would be better programming if we got the below attributes from get_categories_dict
        self.categories = ("Stalls","Liturgical Items","Crosses and Staves","Pulpit and Lecturn","Stained Glass Windows",
                           "Embroidery","Lighting and Candles","Miscellaneous")
        self.subcategories = ("Ancient Stalls","Bishop Stalls","Sedilia","Chalice","Ciborium","Collection Plate","Flagon",
                              "Paten","Thurible","Coptic Crosses","Processional Crosses","Crucifixes","Churchwarden Staves",
                              "Verges","Pulpit","Lecturn","Regimental Chapel","Main Church","Altar Frontals - High Altar",
                              "Altar Frontals - Other","Hassocks","Copes","Chasubles","Chandeliers","Altar Candles",
                              "Baptismal Fonts","Icons","Statues","Wooden Chests","Aumbry")

    # method that creates database and tables needed from scratch
    def create_database(self):
        # create a table containing data about historical items
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.item_table} (
            IDNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(50) NOT NULL,
            Subcategory VARCHAR(20) NOT NULL DEFAULT('MISC'),
            Description VARCHAR(1000),
            Year INTEGER,
            Confidence INTEGER DEFAULT(0)
        );''')
        # create a linking table containing images
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.image_table} (
            IDNumber INTEGER NOT NULL,
            ImagePath VARCHAR(100) NOT NULL,
            FOREIGN KEY (IDNumber) REFERENCES HistoricalItem (IDNumber),
            PRIMARY KEY (IDNumber, ImagePath)
        );''')
        # create linking table for the subcategories and associated overarching categories
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.category_table} (
            Subcategory VARCHAR(20) NOT NULL DEFAULT('MISC'),
            Category VARCHAR(20) NOT NULL DEFAULT('MISC'),
            Description VARCHAR(500),
            FOREIGN KEY (Subcategory) REFERENCES HistoricalItem (Subcategory),
            PRIMARY KEY (Subcategory, Category)             
        );''')
        # commit the changes
        self.conn.commit()

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
    def insert_into_item(self,name:str|None=None,subcategory="MISC",description:str|None = None,year=-1,confidence=0, images: list=None):
        if year < 0: year = None # years in AD must be positive
        if description == "": description = None
        # temp = [name,subcategory,description]
        # for i in range(len(temp)):
            # if temp[i] != "NULL":
                # temp[i] = f"'{temp[i]}'" # adds extra speech marks around strings
        # name,subcategory,description = temp # unpacks after updating
        column_names = self.get_column_names(self.item_table)[1:] # first column is autoincrement
        print(f"INSERT INTO {self.item_table} {column_names} \
                            VALUES ({name},{subcategory},{description},{year},{confidence});")
        # print(f"{name},{subcategory},{description},{year},{confidence}")
        self.cursor.execute(f"INSERT INTO {self.item_table} {column_names} \
                            VALUES (?, ?, ?, ?, ?);", (name, subcategory, description, year, confidence))
        # print("should be adding it tp the table?")
        self.conn.commit() # updates changes
        if images is not None:
            self.add_images_for_item(self.cursor.lastrowid, images)

    def edit_item_record(self,item_id,name:str|None=None,subcategory="MISC",description:str|None = None,year=-1,confidence=0, images: list=None):
        if year < 0: year = None # years in AD must be positive
        if description == "": description = None
        
        print(f"{name},{subcategory},{description},{year},{confidence}")
        self.cursor.execute(f"UPDATE {self.item_table} SET Name=?, Subcategory=?, Description=?, Year=?, Confidence=? \
                            WHERE IDNumber=?;", (name,subcategory,description,year,confidence,item_id,),)
        self.conn.commit() # updates changes
        self.delete_images_for_item(item_id)
        if images is not None: self.add_images_for_item(item_id, images)


    def delete_images_for_item(self, id_number):
        self.cursor.execute(f"DELETE FROM {self.image_table} WHERE IDNumber=?;", (id_number,))
        self.conn.commit()

    def add_images_for_item(self, id_number: int, images: list):
        for image in images:
            self.insert_into_image(id_number, image)

    # method to insert a new record into matching category table
    def insert_into_category(self,subcategory="MISC",category="MISC",description:str|None = None):
        column_names = self.get_column_names(self.category_table)
        self.cursor.execute(f"INSERT INTO {self.category_table} {column_names} \
                            VALUES (? ,? , ?);",(subcategory,category,description))
        self.conn.commit() # updates changes

    # method to get image path/s from image id
    def get_image_path(self,identifier:int):
        statement = f"SELECT ImagePath FROM {self.image_table} WHERE IDNumber=? ;"
        self.cursor.execute(statement,(identifier,)) # parameter must be passed in as tuple
        return self.cursor.fetchall()[0]
    
    # method to get corresponding overarching category from the matching category table
    def get_category(self,subcategory:str) -> str:
        statement = f"SELECT Category FROM {self.category_table} WHERE Subcategory='{subcategory}' ;"
        self.cursor.execute(statement)
        temp = self.cursor.fetchall() # not yet in a usable format
        category = temp[0][0]
        return category
    
    # method to return the list of subcategories for a given category, and all subcategories if there isn't a given category
    def get_subcategories(self, category=None) -> list[str]:
        if category:
            statement = f"SELECT Subcategory FROM {self.category_table} WHERE Category='{category}' ;"

            self.cursor.execute(statement)
            temp = self.cursor.fetchall() # not yet in a usable format
            subcategory_list = list()
            for subcategory in temp:
                subcategory_list.append(subcategory[0])
            return subcategory_list
        
        else:
            subcategories = self.get_column(f"{self.category_table}","Subcategory")
            for i in range(len(subcategories)):
                subcategories[i] = subcategories[i][0]

            return subcategories

    # method to return id number of first item with that name
    def get_id_number(self,name):
        self.cursor.execute(f"SELECT IDNumber FROM {self.item_table} WHERE IDNumber=?",(name,))
        return self.cursor.fetchone()[0]
    
    # method to return tuple of details about an item from it's unique ID number
    def get_item_from_id(self, item_id) -> tuple:
        print(item_id)
        self.cursor.execute(f"SELECT * FROM {self.item_table} WHERE IDNumber=?",(item_id,))
        return self.cursor.fetchall()[0]
        
    def get_categories(self) -> tuple: # returns a tuple of all categories
        categories = self.get_column(f"{self.category_table}","Category")
        category_tuple = []
        for i in range(len(categories)):
            categories[i] = categories[i][0]
            if categories[i] not in category_tuple:
                category_tuple.append(categories[i])
        category_tuple.sort()
        return tuple(category_tuple)
    
    # method to return a dictionary of categories and their associated list of categories
    def get_category_dict(self, categories=None) -> dict: # returns all categories and subcategories if there is not a given category
        # returns a dictionary where the keys are the category and the values are lists of associated subcategories
        if not categories:
            categories = self.get_column(f"{self.item_table}","Category")
            for i in range(len(categories)):
                categories[i] = categories[i][0]
        dictionary = dict()
        for category in categories:
            subcategories = self.get_subcategories(category)
            dictionary.update({category:subcategories})
        return dictionary

    # method to return list of all items - can be sorted differently
    def get_historic_items(self, order_by = "Name", order = "ASC", subcategory=None, category=None):
        # validation
        if subcategory in self.subcategories:
            where_statement = f"WHERE Subcategory = '{subcategory}'"
        else:
            where_statement = ""
        if category in self.categories:
            where_statement = f"WHERE Subcategory = '{category}'"
        else:
            where_statement = ""
        if order not in ("ASC","DESC"):
            order="ASC" # reverts to default
        if order_by not in ("Name","Subcategory","Year","Description","[Number of Images]"):
            order_by = "Name"
        
        print(f"""
            SELECT Name, Subcategory,
            CASE 
                WHEN Confidence = 1 THEN Year 
                ELSE "c. " || Year 
            END AS [approx Year],
            Description,
            COUNT (ImagePath) OVER (PARTITION BY {self.item_table}.IDNumber) AS [Number of Images]
            FROM {self.item_table} LEFT JOIN {self.image_table} ON {self.item_table}.IDNumber = {self.image_table}.IDNumber
            {where_statement}
            ORDER BY {order_by} IS NULL, {order_by} {order}
            """)
        self.cursor.execute(f"""
            SELECT {self.item_table}.IDNumber, Name, Subcategory,
            CASE 
                WHEN Confidence = 1 THEN Year 
                ELSE "c. " || Year 
            END AS [approx Year],
            Description,
            COUNT (ImagePath) OVER (PARTITION BY {self.item_table}.IDNumber) AS [Number of Images]
            FROM {self.item_table} LEFT JOIN {self.image_table} ON {self.item_table}.IDNumber = {self.image_table}.IDNumber
            {where_statement}
            ORDER BY {order_by} IS NULL, {order_by} {order}
            """)
        return self.cursor.fetchall()
    
    def drop_tables(self):
        self.cursor.execute(f"DROP TABLE {self.item_table};")
        self.cursor.execute(f"DROP TABLE {self.image_table};")
        self.cursor.execute(f"DROP TABLE {self.category_table};")
        self.conn.commit()

    def create_subcategory(self, subcategory, category):
        self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",
                            (subcategory, category))
        self.conn.commit()

    def create_subcategories(self):
        # category S
        self.create_subcategory("Ancient Stalls","Stalls")
        self.create_subcategory("Bishop Stalls","Stalls")
        self.create_subcategory("Sedilia","Stalls")
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Ancient Stalls","Stalls"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Bishop Stalls","Stalls"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Sedilia","Stalls"))
        # category L
        self.create_subcategory("Chalice","Liturgical Items")
        self.create_subcategory("Ciborium","Liturgical Items")
        self.create_subcategory("Collection Plate","Liturgical Items")
        self.create_subcategory("Flagon","Liturgical Items")
        self.create_subcategory("Paten","Liturgical Items")
        self.create_subcategory("Thurible", "Liturgical Items")
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Chalice","Liturgical Items"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Ciborium","Liturgical Items"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Collection Plate","Liturgical Items"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Flagon","Liturgical Items"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Paten","Liturgical Items"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Thurible","Liturgical Items"))
        # category CS
        self.create_subcategory("Coptic Crosses","Crosses And Staves")
        self.create_subcategory("Processional Crosses","Crosses And Staves")
        self.create_subcategory("Crucifixes","Crosses And Staves")
        self.create_subcategory("Churchwarden Staves","Crosses And Staves")
        self.create_subcategory("Verges","Crosses And Staves")
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Coptic Crosses","Crosses and Staves"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Processional Crosses","Crosses and Staves"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Crucifixes","Crosses and Staves"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Churchwarden Staves","Crosses and Staves"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Verges","Crosses and Staves"))
        # category P
        self.create_subcategory("Pulpit","Pulpit And Lecturn")
        self.create_subcategory("Lecturn","Pulpit And Lecturn")
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Pulpit","Pulpit and Lecturn"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Lecturn","Pulpit and Lecturn"))
        # category W
        self.create_subcategory("Regimental Chapel","Stained Glass Windows")
        self.create_subcategory("Main Church","Stained Glass Windows")
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Regimental Chapel","Stained Glass Windows"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Main Church","Stained Glass Windows"))
        # category E
        self.create_subcategory("Altar Frontals - High Altar","Embroidery")
        self.create_subcategory("Altar Frontals - Other","Embroidery")
        self.create_subcategory("Hassocks","Embroidery")
        self.create_subcategory("Copes","Embroidery")
        self.create_subcategory("Chasubles","Embroidery")
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Altar Frontals - High Altar","Embroidery"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Altar Frontals - Other","Embroidery"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Hassocks","Embroidery"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Copes","Embroidery"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Chasubles","Embroidery"))
        # category LC
        self.create_subcategory("Chandeliers","Lighting And Candles")
        self.create_subcategory("Altar Candles","Lighting And Candles")
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Chandeliers","Lighting and Candles"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Altar Candles","Lighting and Candles"))
        # category M
        self.create_subcategory("Baptismal Fonts","Miscellaneous")
        self.create_subcategory("Icons","Miscellaneous")
        self.create_subcategory("Statues","Miscellaneous")
        self.create_subcategory("Wooden Chests","Miscellaneous")
        self.create_subcategory("Aumbry","Miscellaneous")
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Baptismal Fonts","Miscellaneous"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Icons","Miscellaneous"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Statues","Miscellaneous"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Wooden Chests","Miscellaneous"))
        # self.cursor.execute(f"INSERT INTO {self.category_table} (Subcategory,Category) VALUES (?,?);",("Aumbry","Miscellaneous"))

    def delete_record(self,identifier):
        self.cursor.execute(f"DELETE FROM {self.item_table} WHERE IDNumber =?", (identifier,))
        self.conn.commit()

    # method that commits changes and closes connection before a table object is garbage-collected
    def __del__(self):
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    d = DatabaseManager()
    # testing
    # database.insert_into_item(name="Cross",description="Very nice.",category="Crucifixes",year=2000)
    # d.insert_into_category("MISC","M")
    # print(d.get_category_dict(d.get_categories()))
    # print(d.get_categories())
    # d.insert_into_item("Book","Miscellaneous","boring",35,1)
 
    # print(database.get_category("Lecturns"))
    # print(database.get_subcategories("CS"))
    # print(database.get_category_dict(("S", "L", "CS", "P", "W", "E", "LC", "M")))
    # database.insert_into_image(ID_number=10,path="fake.png")
    # database.insert_into_image(ID_number=10,path="fake.png")
