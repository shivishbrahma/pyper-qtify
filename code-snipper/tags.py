from db_manager import DBManager


class TagModel:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create_tag(self, name):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "INSERT INTO tags (name) VALUES (?)", (name,)
            )

    def get_tags(self):
        cursor = self.db_manager.connection.cursor()
        cursor.execute("SELECT * FROM tags")
        return cursor.fetchall()

    def update_tag(self, tag_id, name):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "UPDATE tags SET name = ? WHERE id = ?", (name, tag_id)
            )

    def delete_tag(self, tag_id):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "DELETE FROM tags WHERE id = ?", (tag_id,)
            )

    def add_tag_to_snippet(self, snippet_id, tag_id):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "INSERT INTO snippet_tags (snippet_id, tag_id) VALUES (?, ?)",
                (snippet_id, tag_id),
            )

    def remove_tag_from_snippet(self, snippet_id, tag_id):
        with self.db_manager.connection:
            self.db_manager.connection.execute(
                "DELETE FROM snippet_tags WHERE snippet_id = ? AND tag_id = ?",
                (snippet_id, tag_id),
            )
