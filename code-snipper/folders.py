from db_manager import DBManager


class FolderModel:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create_folder(self, name):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "INSERT INTO folders (name) VALUES (?)", (name,)
            )

    def get_folders(self):
        cursor = self.db_manager.connection.cursor()
        cursor.execute("SELECT * FROM folders")
        return cursor.fetchall()

    def update_folder(self, folder_id, name):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "UPDATE folders SET name = ? WHERE id = ?", (name, folder_id)
            )

    def delete_folder(self, folder_id):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "DELETE FROM folders WHERE id = ?", (folder_id,)
            )
