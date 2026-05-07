from database_manager import DatabaseManager

if __name__ == "__main__":
    d = DatabaseManager()
    d.drop_tables()
    d.create_database()
    d.create_subcategories()