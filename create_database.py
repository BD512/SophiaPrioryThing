import sqlite3
 
# method that creates database and tables needed from scratch
def create_database(database = "Priory.db",tables = ("tblHistoricalItem","tblItemImage", "tblMatchingCategory")):
    # connect to the database (create if not exists)
    conn = sqlite3.connect(database)
    # create a cursor object
    cursor = conn.cursor()
    # create a table containing data about historical items
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {tables[0]} (
        IDNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(50) NOT NULL,
        Subcategory VARCHAR(20) NOT NULL DEFAULT('MISC'),
        Description VARCHAR(1000),
        Year INTEGER,
        Confidence INTEGER DEFAULT(0)
    );''')
    # create a linking table containing images
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {tables[1]} (
        IDNumber INTEGER NOT NULL,
        ImagePath VARCHAR(100) NOT NULL,
        FOREIGN KEY (IDNumber) REFERENCES HistoricalItems(IDNumber),
        PRIMARY KEY (IDNumber, ImagePath)
    );''')
    # create linking table for the subcategories and associated overarching categories
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {tables[2]} (
        Subcategory VARCHAR(20) NOT NULL DEFAULT('MISC'),
        Category VARCHAR(20) NOT NULL DEFAULT('MISC'),
        FOREIGN KEY (Subcategory) REFERENCES HistoricalItems(Subcategory),
        PRIMARY KEY (Subcategory, Category)             
    );''')
    # commit the changes
    conn.commit()
    # close the connection
    conn.close()

# for testing purposes
if __name__ == "__main__":
    create_database()