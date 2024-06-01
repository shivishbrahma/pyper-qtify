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
)
from PyQt5.QtCore import Qt
import os

from db_manager import DBManager
from folders import FolderModel
from snippets import SnippetModel
from tags import TagModel


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
        self.__width = 960
        self.__height = 720

        self.__current_folder_id = -1

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.__name)
        self.setGeometry(self.__left, self.__top, self.__width, self.__height)

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
        self.splitter.addWidget(self.sidebar_widget)

        # Folders Tree
        self.folders_tree = QTreeWidget()
        self.folders_tree.setHeaderLabel("Folders")
        self.folders_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.folders_tree.customContextMenuRequested.connect(self.show_folder_menu)
        self.sidebar_layout.addWidget(self.folders_tree)

        # Tags List
        self.tags_label = QLabel("Tags")
        self.sidebar_layout.addWidget(self.tags_label)

        self.tags_list = QListWidget()
        self.tags_list.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tags_list.customContextMenuRequested.connect(self.show_tag_menu)
        self.sidebar_layout.addWidget(self.tags_list)

        # Snippets List
        self.snippets_widget = QWidget()
        self.snippets_layout = QVBoxLayout(self.snippets_widget)
        self.splitter.addWidget(self.snippets_widget)

        self.snippets_label = QLabel("Snippets")
        self.snippets_layout.addWidget(self.snippets_label)
        self.snippets_list = QListWidget()
        self.snippets_list.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.snippets_list.customContextMenuRequested.connect(self.show_snippet_menu)
        self.snippets_layout.addWidget(self.snippets_list)

        # Snippet Editor
        self.snippet_editor = QTextEdit()
        self.splitter.addWidget(self.snippet_editor)

        # Load initial data
        self.load_initial_data()

    def load_folders(self):
        self.folders_tree.clear()
        folders = self.folder_model.get_folders()
        for folder in folders:
            item = QTreeWidgetItem(self.folders_tree)
            item.setText(0, folder[1])
            item.setData(0, Qt.UserRole, folder[0])

    def load_tags(self):
        self.tags_list.clear()
        tags = self.tag_crud.get_tags()
        for tag in tags:
            self.tags_list.addItem(tag[1])

    def load_snippets(self, item):
        # folder_name = item.text()
        folder_id = item.data(0, Qt.UserRole)
        snippets = self.snippet_model.get_snippets(folder_id)
        self.snippets_list.clear()
        for snippet in snippets:
            self.snippets_list.addItem(snippet[1])

    def load_initial_data(self):
        self.load_folders()
        self.load_tags()
        # select current folder
        current_folder_item = self.folders_tree.currentItem()
        if current_folder_item:
            self.load_snippets(current_folder_item)
        # check if folder_list is empty
        elif self.folders_tree.topLevelItemCount() != 0:
            self.load_snippets(self.folders_tree.topLevelItem(0))

    # def show_folder_menu(self, position):
    #     folders.show_folder_menu(self.folders_tree, position)

    # def show_tag_menu(self, position):
    #     tags.show_tag_menu(self.tags_list, position)

    # def show_snippet_menu(self, position):
    #     snippets.show_snippet_menu(self.snippets_list, position)

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnippetTool()
    window.show()
    sys.exit(app.exec_())
