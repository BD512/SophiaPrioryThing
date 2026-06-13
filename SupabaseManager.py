from supabase import create_client, Client
# documentation for supabase: https://supabase.com/docs/reference/python/
# documentation for postegresql: https://www.postgresql.org/docs/

class SupabaseManager:
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)

    def uploadImage(self, path: str, new_name: str):
        with open(path, "rb") as image_file:
            self.client.storage.from_("Images").upload(new_name, image_file)

    def getColumnNames(self, table) -> list[str]:
        result = (
            self.client.rpc(
                "get_columns",
                {"column_name": table}
            )
            .execute()
        )
        return [row["columns"] for row in result.data]


class PrioryDbManager(SupabaseManager):
    def __init__(self, item_table="tblHistoricalItem",image_table="tblItemImage",category_table="tblMatchingCategory"):
        super().__init__("https://ynrxfhpltaivjwbfsufa.supabase.co", "a secret key")
        self.item_table = item_table
        self.image_table = image_table
        self.category_table = category_table

    def getColumnFromCategoryTable(self, column_name: str) -> list[str]:
        result = (
            self.client.rpc(
                "get_categories",
                {"column_name": column_name}
            )
            .execute()
        )
        return result.data

    def getCategories(self):
        return self.getColumnFromCategoryTable("Category")

    def getSubCategories(self):
        return self.getColumnFromCategoryTable("Subcategory")

    def getCategoryDict(self):
        result = (
            self.client.rpc(
                "get_category_dict",
                {}
            )
            .execute()
        )
        print(result) # todo change to give dict

    def doesSubCategoryExist(self, category: str, subcategory: str) -> bool:
        result = (
            self.client.rpc(
                "is_subcategory",
                {"category": category, "subcategory": subcategory}
            )
            .execute()
        )
        return bool(result.data)

    def insertIntoImageTable(self, id_number: int, path: str):
        response = (
            self.client.table(self.image_table)
            .insert({"IDNumber": id_number, "ImagePath": path})
            .execute()
        )

    def insertIntoCategories(self, category: str, subcategory: str): # works
        response = (
            self.client.table(self.category_table)
            .insert({"Category": category, "Subcategory": subcategory})
            .execute()
        )

    def insertImagesForEntry(self, id_number: int, paths: list[str]):
        for image_path in paths:
            self.insertIntoImageTable(id_number, image_path)

    def insertIntoItem(self, name: str, category: str, subcategory: str, description: str|None = None,year: int|None=None,confidence: int=0, images: list=None) -> None:
        info_dict = {"Name": name,
                     "Subcategory": subcategory,
                     "Category": category,
                     "Confident": bool(confidence),
                     }
        if description is not None: info_dict["Description"] = description
        if year is not None: info_dict["Year"] = year
        response = (
            self.client.table(self.item_table)
            .insert(info_dict)
            .execute()
        )
        id_number = response.data[0]["IDNumber"]
        self.insertImagesForEntry(id_number, images)

    def editItemRecord(self, item_id, name: str|None=None, category: str=None, subcategory: str=None, description: str|None=None, year: int|None=None, confidence: int=None, images: list=None) -> None:
        info_dict = {}
        if name is not None: info_dict["Name"] = name
        if category is not None: info_dict["Category"] = category
        if subcategory is not None: info_dict["Subcategory"] = subcategory
        if confidence is not None: info_dict["Confident"] = bool(confidence)
        if description is not None: info_dict["Description"] = description
        if year is not None: info_dict["Year"] = year
        response = (
            self.client.table(self.item_table)
            .update(info_dict)
            .eq("IDNumber", item_id)
            .execute()
        )


a = PrioryDbManager()
# a.createDatabase()
a.insertIntoCategories("cross", "idk")
# print(a.insertIntoItem("cross", "crosses", "idk", "a cross"))

