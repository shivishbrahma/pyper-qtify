import qtawesome as qta
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QActionGroup,
    QAction,
    QToolBar,
    QListWidget,
)
from PyQt5.QtCore import Qt

from db_manager import DBManager, Snippet


class SnippetModel:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create_snippet(self, title, content, folder_id):
        new_snippet = Snippet(title=title, folder_id=folder_id)
        self.db_manager.session.add(new_snippet)
        self.db_manager.commit()

    def get_snippets(self, folder_id=None):
        if folder_id is None:
            return self.db_manager.session.query(Snippet).all()
        return self.db_manager.session.query(Snippet).filter_by(folder_id=folder_id).all()

    def update_snippet(self, snippet_id, title, content, folder_id):
        old_snippet = self.db_manager.session.query(Snippet).get(snippet_id)
        old_snippet.title = title
        # old_snippet.content = content
        old_snippet.folder_id = folder_id
        self.db_manager.commit()

    def delete_snippet(self, snippet_id):
        old_snippet = self.db_manager.session.query(Snippet).get(snippet_id)
        self.db_manager.session.delete(old_snippet)
        self.db_manager.commit()


def load_snippets(app, item):
    folder_id = item.data(0, Qt.UserRole)
    snippets = app.snippet_model.get_snippets(folder_id)
    app.snippets_list.clear()
    for snippet in snippets:
        app.snippets_list.addItem(snippet[1])


def load_snippets_ui(app):
    """
    Load Snippets List
    """
    app.snippets_widget = QWidget()
    app.snippets_layout = QVBoxLayout(app.snippets_widget)
    app.snippets_layout.setContentsMargins(0, 0, 0, 0)
    app.splitter.addWidget(app.snippets_widget)

    app.snippets_header_widget = QWidget()
    app.snippets_header_widget.setFixedHeight(30)
    app.snippets_header_layout = QHBoxLayout(app.snippets_header_widget)
    app.snippets_header_layout.setContentsMargins(5, 0, 0, 0)
    app.snippets_layout.addWidget(app.snippets_header_widget)

    app.snippets_label = QLabel("Snippets")
    app.snippets_label.setFixedHeight(30)
    app.snippets_header_layout.addWidget(app.snippets_label)

    app.snippets_list = QListWidget()
    app.snippets_list.setContextMenuPolicy(Qt.CustomContextMenu)
    # app.snippets_list.customContextMenuRequested.connect(app.show_snippet_menu)
    app.snippets_layout.addWidget(app.snippets_list)
