import sqlite3


class DBManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.init_db()

    def init_db(self):
        with self.connection:
            # Initialize the database schema here
            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS folders (
                                        id INTEGER PRIMARY KEY,
                                        name VARCHAR(255) NOT NULL,
                                        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
            )

            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS tags (
                                        id INTEGER PRIMARY KEY,
                                        name VARCHAR(255) NOT NULL,
                                        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
            )

            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS snippets (
                                        id INTEGER PRIMARY KEY,
                                        name VARCHAR(255) NOT NULL,
                                        folder_id INTEGER,
                                        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (folder_id) REFERENCES folders (id))"""
            )

            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS fragments (
                                        id INTEGER PRIMARY KEY,
                                        content VARCHAR(255) NOT NULL,
                                        snippet_id INTEGER,
                                        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (snippet_id) REFERENCES snippets (id))"""
            )

            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS snippet_tags (
                                        snippet_id INTEGER,
                                        tag_id INTEGER,
                                        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (snippet_id) REFERENCES snippets (id),
                                        FOREIGN KEY (tag_id) REFERENCES tags (id),
                                        PRIMARY KEY (snippet_id, tag_id))"""
            )

    def close(self):
        self.connection.close()
