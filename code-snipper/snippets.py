import qtawesome as qta
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QAction,
    QToolBar,
    QListWidget,
    QTextEdit,
    QLineEdit,
    QComboBox,
)
from PyQt5.QtCore import Qt

from db_manager import DBManager, Snippet, Fragment


class SnippetModel:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create_snippet(self, folder_id, name, content, language):
        new_snippet = Snippet(name=name, folder_id=folder_id)
        self.db_manager.session.add(new_snippet)
        self.db_manager.commit()

        new_fragment = Fragment(
            content=content, snippet_id=new_snippet.id, language=language
        )
        self.db_manager.session.add(new_fragment)
        self.db_manager.commit()

    def get_snippets(self, folder_id=None):
        if folder_id is None:
            return self.db_manager.session.query(Snippet).all()
        return (
            self.db_manager.session.query(Snippet).filter_by(folder_id=folder_id).all()
        )

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
        app.snippets_list.addItem(snippet.name)


def load_snippets_ui(app):
    """
    Load Snippets List
    """
    app.snippets_widget = QWidget()
    app.snippets_layout = QVBoxLayout(app.snippets_widget)
    app.snippets_layout.setContentsMargins(0, 0, 0, 0)
    app.splitter.addWidget(app.snippets_widget)

    # Snippets Header
    app.snippets_header_widget = QWidget()
    app.snippets_header_widget.setFixedHeight(30)
    app.snippets_header_layout = QHBoxLayout(app.snippets_header_widget)
    app.snippets_header_layout.setContentsMargins(5, 0, 0, 0)
    app.snippets_layout.addWidget(app.snippets_header_widget)

    # Snippets Header Label
    app.snippets_label = QLabel("Snippets")
    app.snippets_label.setFixedHeight(30)
    app.snippets_header_layout.addWidget(app.snippets_label)

    # Snippet Actions
    add_snippet_action = QAction(
        qta.icon(
            "mdi.plus",
            color=app.theme["colors"]["button"]["foreground"],
            scale_factor=1,
        ),
        "Add Snippet",
        app,
    )
    edit_snippet_action = QAction(
        qta.icon(
            "mdi.pencil",
            color=app.theme["colors"]["button"]["foreground"],
            scale_factor=1,
        ),
        "Edit Snippet",
        app,
    )
    delete_snippet_action = QAction(
        qta.icon(
            "mdi.delete",
            color=app.theme["colors"]["button"]["foreground"],
            scale_factor=1,
        ),
        "Delete Snippet",
        app,
    )

    # Set Event for click
    add_snippet_action.triggered.connect(lambda: add_snippet(app))
    # edit_snippet_action.triggered.connect(lambda: edit_snippet(app))

    # Snippets Toolbar
    snippets_toolbar = QToolBar(app)
    snippets_toolbar.addAction(add_snippet_action)
    snippets_toolbar.addAction(edit_snippet_action)
    snippets_toolbar.addAction(delete_snippet_action)
    app.snippets_header_layout.addWidget(snippets_toolbar, 0, Qt.AlignRight)

    app.snippets_list = QListWidget()
    app.snippets_list.setContextMenuPolicy(Qt.CustomContextMenu)
    # app.snippets_list.customContextMenuRequested.connect(app.show_snippet_menu)
    app.snippets_layout.addWidget(app.snippets_list)


def load_snippet_editor(app):
    """
    Load Snippet Editor
    """
    app.snippet_editor_widget = QWidget()
    app.snippet_editor_layout = QVBoxLayout(app.snippet_editor_widget)
    app.snippet_editor_layout.setContentsMargins(0, 0, 0, 0)

    app.snippet_title_input = QLineEdit()
    app.snippet_title_input.setPlaceholderText("Snippet title")
    app.snippet_editor_layout.addWidget(app.snippet_title_input)
    # Toggle read only on double click
    # app.snippet_title_input.mouseDoubleClickEvent = lambda event: app.snippet_title_input.setReadOnly(
    #     app.snippet_title_input.isReadOnly() ^ True
    # )

    # Snippet Tags
    app.snippet_tags_input = QLineEdit()
    app.snippet_tags_input.setPlaceholderText("Add Tag")
    app.snippet_editor_layout.addWidget(app.snippet_tags_input)

    # Snippet Editor
    app.snippet_editor_input = QTextEdit()
    app.snippet_editor_input.setPlaceholderText("Snippet content")
    app.snippet_editor_layout.addWidget(app.snippet_editor_input)

    # Select copy or paste as plain text
    app.snippet_editor_input.setAcceptRichText(False)

    # Enable code language highlighting
    app.snippet_editor_input.setLineWrapMode(QTextEdit.NoWrap)
    app.snippet_editor_input.setTabStopWidth(
        4 * app.snippet_editor_input.fontMetrics().width(" ")
    )

    # Snippet Language
    app.snippet_language_input = QComboBox()
    languages = [
        "bash",
        "c",
        "cpp",
        "csharp",
        "dart",
        "elixir",
        "go",
        "haskell",
        "html",
        "java",
        "js",
        "json",
        "kotlin",
        "lua",
        "php",
        "py",
        "rb",
        "sql",
        "ts",
        "xml",
        "yaml",
    ]
    for language in languages:
        app.snippet_language_input.addItem(language)
    app.snippet_editor_layout.addWidget(app.snippet_language_input)

    app.splitter.addWidget(app.snippet_editor_widget)


def add_snippet(app):
    # Check if any folder is selected
    if len(app.folders_tree.selectedItems()) == 0:
        QMessageBox.warning(app, "Add Snippet", "Please select a folder.")
        return

    # Get folder id
    folder_id = app.folders_tree.selectedItems()[0].data(0, Qt.UserRole)

    snippet_title = app.snippet_title_input.text()
    snippet_content = app.snippet_editor_input.toPlainText()
    snippet_language = app.snippet_language_input.currentText()
    # snippet_tags = app.snippet_tags_input.text()

    app.snippet_model.create_snippet(
        folder_id, snippet_title, snippet_content, snippet_language
    )
    load_snippets(app, app.folders_tree.selectedItems()[0])
