from supabase import create_client, Client
# documentation for supabase: https://supabase.com/docs/reference/python/

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
        super().__init__("https://ynrxfhpltaivjwbfsufa.supabase.co", "sb_publishable_Z-TIgzIUXW7La2XHy5upVg_DvLV0sKG")
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

    def insertIntoImageTable(self, id_number: int, path: str):
        response = (
            self.client.table(self.image_table)
            .insert({"IDNumber": id_number, "ImagePath": path})
            .execute()
        )

    def insertImagesForEntry(self, id_number: int, paths: list[str]):
        for image_path in paths:
            self.insertIntoImageTable(id_number, image_path)

    def insertIntoItem(self, name: str, subcategory: str, category: str, description: str|None = None,year=None,confidence: int=0, images: list=None) -> None:
        info_dict = {"Name": name,
                     "Subcategory": subcategory,
                     "Category": category,
                     "Confidence": bool(confidence),
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

    def edit_item_record(self,item_id,name:str|None=None,subcategory="MISC",description:str|None = None,year=-1,confidence: int=0, images: list=None):
        # print("editing item record")
        # print(name)
        if year < 0: year = None # years in AD must be positive
        if description == "": description = None
        # print(f"{name},{subcategory},{description},{year},{confidence}")
        self.cursor.execute(f"UPDATE {self.item_table} SET Name=?, Subcategory=?, Description=?, Year=?, Confidence=? \
                            WHERE IDNumber=?;", (name,subcategory,description,year,confidence,item_id,),)
        self.conn.commit() # updates changes
        self.delete_images_for_item(item_id)
        if images is not None: self.add_images_for_item(item_id, images)
        info_dict = {
            "Name": name,
            "Subcategory": subcategory,
            "Confidence": bool(confidence)
        }
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
print(a.getColumnFromCategoryTable("Category"))

