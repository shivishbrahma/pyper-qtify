import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QWidget,
    QTreeWidget,
    QListWidget,
    QTextEdit,
    QSplitter,
    QTreeWidgetItem,
    QToolBar,
    QAction,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import qtawesome as qta
import os
import json

from db_manager import DBManager
from folders import FolderModel, load_folders, load_folders_ui
from snippets import SnippetModel, load_snippets, load_snippets_ui, load_snippet_editor
from tags import TagModel, load_tags_tree, load_tags_ui


class SnippetTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__dir__ = os.path.dirname(os.path.abspath(__file__))
        self.db_manager = DBManager(os.path.join(self.__dir__, "codesnipper.db"))
        self.folder_model = FolderModel(self.db_manager)
        self.snippet_model = SnippetModel(self.db_manager)
        self.tag_crud = TagModel(self.db_manager)

        self.__name = "Code Snipper"
        self.__left = 100
        self.__top = 100
        self.__width = 1024
        self.__height = 720

        self.load_theme("light-github")

        self.init_ui()

    def load_theme(self, theme_name):
        self.theme_name = theme_name
        with open(os.path.join(self.__dir__, "themes", theme_name + ".json")) as f:
            self.theme = json.load(f)

    def init_ui(self):
        self.setWindowTitle(self.__name)
        self.setGeometry(self.__left, self.__top, self.__width, self.__height)
        icon = QIcon(os.path.join(self.__dir__, "assets/icons/icon-without-bg.png"))
        self.setWindowIcon(icon)

        # Main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        # Splitter for vertical grids
        self.splitter = QSplitter()
        self.main_layout.addWidget(self.splitter)

        # Sidebar with folders and tags
        self.sidebar_widget = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.sidebar_widget)

        # Folders Tree
        load_folders_ui(self)

        # Tags List
        load_tags_ui(self)

        # Snippets List
        load_snippets_ui(self)

        # Snippet Editor
        load_snippet_editor(self)

        # Set splitter sizes (1:1:2)
        self.splitter.setStretchFactor(0, 1)  # Sidebar (folders and tags)
        self.splitter.setStretchFactor(1, 1)  # Snippets list
        self.splitter.setStretchFactor(2, 2)  # Snippet editor

        # Load initial data
        self.load_initial_data()

        # Apply theme
        self.apply_theme()

    def create_menubar(self):
        pass

    def load_initial_data(self):
        load_folders(self)
        load_tags_tree(self)
        # select current folder
        current_folder_item = self.folders_tree.currentItem()
        if current_folder_item:
            load_snippets(self, current_folder_item)
            self.folders_tree.setCurrentItem(current_folder_item)
        # check if folder_list is not empty
        elif self.folders_tree.topLevelItemCount() != 0:
            load_snippets(self, self.folders_tree.topLevelItem(0))
            self.folders_tree.setCurrentItem(self.folders_tree.topLevelItem(0))

        self.folders_tree.currentItemChanged.connect(
            lambda: load_snippets(self, self.folders_tree.currentItem())
        )

    # def show_folder_menu(self, position):
    #     folders.show_folder_menu(self.folders_tree, position)

    # def show_tag_menu(self, position):
    #     tags.show_tag_menu(self.tags_tree, position)

    # def show_snippet_menu(self, position):
    #     snippets.show_snippet_menu(self.snippets_list, position)

    def apply_theme(self):
        # set background color
        self.setStyleSheet(
            f"background-color: {self.theme['colors']['background']}; color: {self.theme['colors']['text']}; font-size: {self.theme['styles']['defaultText']['fontSize']};"
        )

        # Apply header styles
        header_labels = [
            self.folders_label,
            self.tags_label,
            self.snippets_label,
        ]

        for label in header_labels:
            label.setStyleSheet(
                f"font-size: {self.theme['styles']['headerLabel']['fontSize']};color: {self.theme['colors']['header']['foreground']};"
            )
        # self.header_toolbar.setStyleSheet(f"background-color: {self.theme['colors']['header']['background']}; border: 1px solid {self.theme['colors']['header']['border']};")

        text_inputs = [
            self.snippet_editor_widget.header.title_edit,
            self.snippet_editor_widget.header.tags_edit,
            self.snippet_editor_widget.body.content_edit,
        ]

        input_style = "background-color: {}; color: {}; font-size: {};border: {};"
        for input in text_inputs:
            input.setStyleSheet(
                input_style.format(
                    self.theme["colors"]["editor"]["background"],
                    self.theme["colors"]["editor"]["foreground"],
                    "20px" if input == self.snippet_editor_widget.header.title_edit else "15px",
                    "1px solid transparent",
                )
            )

            # Style title input: show border on focus and remove on blur
            input.focusInEvent = lambda event, input=input: input.setStyleSheet(
                input_style.format(
                    self.theme["colors"]["editor"]["background"],
                    self.theme["colors"]["editor"]["foreground"],
                    "20px" if input == self.snippet_editor_widget.header.title_edit else "15px",
                    "1px solid #000000",
                )
            )
            input.focusOutEvent = lambda event, input=input: input.setStyleSheet(
                input_style.format(
                    self.theme["colors"]["editor"]["background"],
                    self.theme["colors"]["editor"]["foreground"],
                    "20px" if input == self.snippet_editor_widget.header.title_edit else "15px",
                    "1px solid transparent",
                )
            )

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnippetTool()
    window.show()
    sys.exit(app.exec_())
