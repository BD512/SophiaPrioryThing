import sqlite3

# class that manages the database (2 tables)
class DatabaseManager():
    def __init__(self,database = "Priory.db",tables = ("tblHistoricalItem","tblItemImage")):
        # extracts names of tables for consistency
        self.items_table = tables[0]
        self.image_table = tables[1]
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
    def insert_into_items(self,name="NULL",category="MISC",description = "NULL",year="NULL",confidence=0):
        for i in name,category,description,year:
            if i != "NULL":
                i = f"'{i}'" # adds extra speech marks around strings
        column_names = self.get_column_names(self.items_table)[1:] # first column is autoincrement
        self.cursor.execute(f"INSERT INTO {self.image_table} {column_names} \
                            VALUES ({name},{category},{description},{year},{confidence});")
        self.conn.commit() # updates changes

    # method to get image path/s from image id
    def get_image_path(self,id:int):
        statement = f"SELECT ImagePath FROM {self.image_table} WHERE ImageId=? ;"
        self.cursor.execute(statement,(id,)) # parameter must be passed in as tuple
        return self.cursor.fetchall()

    # method that commits changes and closes connection before a table object is garbage-collected
    def __del__(self):
        self.conn.commit()
        self.conn.close()

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
    