from db_manager import DBManager
import qtawesome as qta
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QActionGroup,
    QAction,
    QToolBar,
    QListWidget
)
from PyQt5.QtCore import Qt


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


def load_tags_tree(app):
    app.tags_tree.clear()
    tags = app.tag_crud.get_tags()
    for tag in tags:
        app.tags_tree.addItem(tag[1])


def load_tags_ui(app):
    app.tags_header_widget = QWidget()
    app.tags_header_layout = QHBoxLayout(app.tags_header_widget)
    app.tags_label = QLabel("Tags")
    app.tags_header_layout.addWidget(app.tags_label)
    app.tags_header_layout.setContentsMargins(0, 0, 0, 0)

    # add_folder_action = QAction(qta.icon("mdi.plus", color=app.theme["colors"]["button"]["foreground"]), "Add Folder", app)
    # edit_folder_action = QAction(qta.icon("mdi.pencil", color=app.theme["colors"]["button"]["foreground"]), "Edit Folder", app)

    # tags_header_action_group = QToolBar()
    # tags_header_action_group.addAction(add_folder_action)
    # tags_header_action_group.addAction(edit_folder_action)
    # app.tags_header_layout.addWidget(tags_header_action_group)

    app.sidebar_layout.addWidget(app.tags_header_widget)
    
    app.tags_tree = QListWidget()
    app.tags_tree.setContextMenuPolicy(Qt.CustomContextMenu)
    # app.tags_tree.customContextMenuRequested.connect(app.show_tag_menu)
    app.sidebar_layout.addWidget(app.tags_tree)
