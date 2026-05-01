import sqlite3

# class that manages the database (2 tables)
class DatabaseManager():
    def __init__(self,database:str,tables:tuple):
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
 
    # method to insert a new record into table
    def insert(self,table:str,data:tuple):
        column_names = self.get_column_names(table)[1:] # primary key is auto-increment
        # a tuple of question marks needs to be passed into VALUES
        question = ""
        for i in range(len(data)): question+=("?,")
        question = question[:-1] # remove last comma
        self.cursor.execute(f"INSERT INTO {table} {column_names} VALUES ({question});",data)
        self.conn.commit() # updates changes

    # method to return any entire column from table
    def get_column(self,table:str,column:str):
        statement = f"SELECT {column} FROM {table};"
        self.cursor.execute(statement)
        return self.cursor.fetchall()
    
    # method to get image_path from image_id
    # this is used to get both the username and the user_id at different times
    def get_image_path(self,id:int):
        statement = f"SELECT ImagePath FROM {self.image_table} WHERE username=? ;"
        self.cursor.execute(statement,(id,)) # parameter must be passed in as tuple
        return self.cursor.fetchone()[0]

    # method that commits changes and closes connection before a table object is garbage-collected
    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def display_historic_items(self):
        self.cursor.execute("""
            SELECT Name, Category, Description,
            CASE 
                WHEN Confidence = 1 THEN Year 
                ELSE "c. " || Year 
            END AS [approx Year]
            FROM HistoricalItems
            ORDER BY Year IS NULL, Year
            """)
        return self.cursor.fetchall()
    