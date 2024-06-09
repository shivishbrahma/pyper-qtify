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
    QListWidgetItem,
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

    def get_snippet(self, snippet_id):
        return self.db_manager.session.query(Snippet).get(snippet_id)

    def update_snippet(self, snippet_id, folder_id, name, content, language):
        old_snippet = self.get_snippet(snippet_id)
        old_snippet.name = name
        old_snippet.folder_id = folder_id
        old_snippet.fragments[0].content = content
        old_snippet.fragments[0].language = language
        self.db_manager.commit()

    def delete_snippet(self, snippet_id):
        old_snippet = self.db_manager.session.query(Snippet).get(snippet_id)
        self.db_manager.session.delete(old_snippet.fragments[0])
        self.db_manager.session.delete(old_snippet)
        self.db_manager.commit()


class SnippetEditor(QWidget):
    def __init__(self, app, snippet_id=-1):
        super().__init__(parent=app)
        self.app = app
        self.snippet_id = snippet_id

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header = SnippetEditorHeader(self.app, self.snippet_id)
        self.body = SnippetEditorBody(self.app, self.snippet_id)
        self.footer = SnippetEditorFooter(self.app, self.snippet_id)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.body)
        self.layout.addWidget(self.footer)

    def set_snippet_id(self, snippet_id):
        self.snippet_id = snippet_id
        # propagate to other widgets
        self.header.set_snippet_id(snippet_id)
        self.body.set_snippet_id(snippet_id)
        self.footer.set_snippet_id(snippet_id)

    def set_title(self, title):
        self.header.set_title(title)

    def set_tags(self, tags):
        self.header.set_tags(tags)

    def set_content(self, content):
        self.body.set_content(content)

    def set_language(self, language):
        self.footer.set_language(language)

    def title(self):
        return self.header.title()

    def tags(self):
        return self.header.tags()

    def content(self):
        return self.body.content()

    def language(self):
        return self.footer.language()


class SnippetEditorHeader(QWidget):
    def __init__(self, app, snippet_id=-1):
        super().__init__(parent=app)
        self.app = app
        self.snippet_id = snippet_id

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Snippet name")
        # self.title.textChanged.connect(self.title_changed)
        self.layout.addWidget(self.title_edit)

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Add Tag")
        # self.tags.textChanged.connect(self.tags_changed)
        self.layout.addWidget(self.tags_edit)

    def title(self):
        return self.title_edit.text()

    def set_title(self, title):
        self.title_edit.setText(title)

    def tags(self):
        return self.tags_edit.text()

    def set_tags(self, tags):
        self.tags_edit.setText(tags)

    def set_snippet_id(self, snippet_id):
        self.snippet_id = snippet_id


class SnippetEditorBody(QWidget):
    def __init__(self, app, snippet_id=-1):
        super().__init__(parent=app)
        self.app = app
        self.snippet_id = snippet_id

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Snippet content")
        # self.content.textChanged.connect(self.content_changed)
        self.layout.addWidget(self.content_edit)

    def content(self):
        return self.content_edit.toPlainText()

    def set_content(self, content):
        self.content_edit.setPlainText(content)

    def set_snippet_id(self, snippet_id):
        self.snippet_id = snippet_id


class SnippetEditorFooter(QWidget):
    def __init__(self, app, snippet_id=-1):
        super().__init__(parent=app)
        self.app = app
        self.snippet_id = snippet_id

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.load_languages()
        self.load_toolbar()

    def load_languages(self):
        self.languages = [
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
        self.language_combo = QComboBox()
        for language in self.languages:
            self.language_combo.addItem(language)
        # self.language_combo.currentTextChanged.connect(self.language_changed)
        self.layout.addWidget(self.language_combo, stretch=2)

    def load_toolbar(self):
        self.toolbar = QToolBar()

        save_action = QAction(
            qta.icon("mdi.content-save", scale_factor=1), "Save", self
        )
        save_action.triggered.connect(self.save_snippet)
        self.toolbar.addAction(save_action)

        self.layout.addWidget(self.toolbar, 1, Qt.AlignRight)

    def language(self):
        return self.language_combo.currentText()

    def set_language(self, language):
        self.language_combo.setCurrentText(language)

    def set_snippet_id(self, snippet_id):
        self.snippet_id = snippet_id

    def save_snippet(self):
        if self.snippet_id == -1:
            add_snippet(self.app)
        else:
            update_snippet(self.app, self.snippet_id)


def load_snippets(app, item):
    folder_id = item.data(0, Qt.UserRole)
    snippets = app.snippet_model.get_snippets(folder_id)
    app.snippets_list.clear()
    for snippet in snippets:
        snippet_list_item = QListWidgetItem(app.snippets_list)
        snippet_list_item.setText(snippet.name)
        snippet_list_item.setData(Qt.UserRole, snippet.id)


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
    add_snippet_action.triggered.connect(lambda: clear_snippet_editor(app))
    # edit_snippet_action.triggered.connect(lambda: edit_snippet(app))

    # Snippets Toolbar
    snippets_toolbar = QToolBar(app)
    snippets_toolbar.addAction(add_snippet_action)
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
    app.snippet_editor_widget = SnippetEditor(app)

    app.splitter.addWidget(app.snippet_editor_widget)

    # App Snippet List on click
    app.snippets_list.itemSelectionChanged.connect(
        lambda: reload_snippet_editor_ui(app)
    )


def reload_snippet_editor_ui(app):
    if len(app.snippets_list.selectedItems()) == 0:
        return
    app.snippet_list_item = app.snippets_list.selectedItems()[0]

    snippet = app.snippet_model.get_snippet(app.snippet_list_item.data(Qt.UserRole))

    app.snippet_editor_widget.set_title(snippet.name)
    app.snippet_editor_widget.set_content(snippet.fragments[0].content)
    app.snippet_editor_widget.set_language(snippet.fragments[0].language)
    app.snippet_editor_widget.set_snippet_id(snippet.id)


def add_snippet(app):
    # Check if any folder is selected
    if len(app.folders_tree.selectedItems()) == 0:
        QMessageBox.warning(app, "Add Snippet", "Please select a folder.")
        return

    # Get folder id
    folder_id = app.folders_tree.selectedItems()[0].data(0, Qt.UserRole)

    snippet_title = app.snippet_editor_widget.title()
    snippet_content = app.snippet_editor_widget.content()
    snippet_language = app.snippet_editor_widget.language()
    # snippet_tags = app.snippet_tags_input.text()

    app.snippet_model.create_snippet(
        folder_id, snippet_title, snippet_content, snippet_language
    )

    # Info prompt add message
    QMessageBox.information(
        app, "Add Snippet", "Snippet has been added successfully."
    )

    clear_snippet_editor(app)
    load_snippets(app, app.folders_tree.selectedItems()[0])


def update_snippet(app, snippet_id):
    # Check if any folder is selected
    if len(app.folders_tree.selectedItems()) == 0:
        QMessageBox.warning(app, "Add Snippet", "Please select a folder.")
        return

    # Get folder id
    folder_id = app.folders_tree.selectedItems()[0].data(0, Qt.UserRole)

    snippet_title = app.snippet_editor_widget.title()
    snippet_content = app.snippet_editor_widget.content()
    snippet_language = app.snippet_editor_widget.language()
    # snippet_tags = app.snippet_tags_input.text()

    app.snippet_model.update_snippet(
        snippet_id, folder_id, snippet_title, snippet_content, snippet_language
    )

    # Info prompt update message
    QMessageBox.information(
        app, "Update Snippet", "Snippet has been updated successfully."
    )
    
    load_snippets(app, app.folders_tree.selectedItems()[0])


def clear_snippet_editor(app):
    app.snippet_editor_widget.set_title("")
    app.snippet_editor_widget.set_content("")
    app.snippet_editor_widget.set_language("")
    app.snippet_editor_widget.set_snippet_id(-1)
