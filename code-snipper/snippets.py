from db_manager import DBManager


class SnippetModel:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create_snippet(self, title, content, folder_id):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "INSERT INTO snippets (title, content, folder_id) VALUES (?, ?, ?)",
                (title, content, folder_id),
            )

    def get_snippets(self, folder_id=None):
        cursor = self.db_manager.connection.cursor()
        if folder_id:
            cursor.execute("SELECT * FROM snippets WHERE folder_id = ?", (folder_id,))
        else:
            cursor.execute("SELECT * FROM snippets")
        return cursor.fetchall()

    def update_snippet(self, snippet_id, title, content, folder_id):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "UPDATE snippets SET title = ?, content = ?, folder_id = ? WHERE id = ?",
                (title, content, folder_id, snippet_id),
            )

    def delete_snippet(self, snippet_id):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "DELETE FROM snippets WHERE id = ?", (snippet_id,)
            )
