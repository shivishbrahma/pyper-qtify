from db_manager import DBManager
from PyQt5.QtWidgets import (
    QWidget,
    QTreeWidget,
    QHBoxLayout,
    QLabel,
    QToolBar,
    QAction,
    QTreeWidgetItem,
    QInputDialog,
    QMessageBox,
    QMenu
)
from PyQt5.QtCore import Qt
import qtawesome as qta


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


def load_folders(app):
    app.folders_tree.clear()
    folders = app.folder_model.get_folders()
    for folder in folders:
        item = QTreeWidgetItem(app.folders_tree)
        item.setIcon(0, qta.icon("mdi.folder"))
        item.setText(0, folder[1])
        item.setData(0, Qt.UserRole, folder[0])


def load_folders_ui(app):
    """
    Load Folder Tree
    """
    app.folders_header_widget = QWidget()
    app.folders_header_widget.setFixedHeight(30)
    app.folders_header_layout = QHBoxLayout(app.folders_header_widget)
    app.folders_label = QLabel("Folders")
    app.folders_label.setFixedHeight(30)
    app.folders_header_layout.addWidget(app.folders_label)
    app.folders_header_layout.setContentsMargins(0, 0, 0, 0)

    add_folder_action = QAction(
        qta.icon(
            "mdi.plus",
            color=app.theme["colors"]["button"]["foreground"],
            scale_factor=1,
        ),
        "Add Folder",
        app,
    )
    edit_folder_action = QAction(
        qta.icon(
            "mdi.pencil",
            color=app.theme["colors"]["button"]["foreground"],
            scale_factor=1,
        ),
        "Edit Folder",
        app,
    )
    delete_folder_action = QAction(
        qta.icon(
            "mdi.delete",
            color=app.theme["colors"]["button"]["foreground"],
            scale_factor=1,
        ),
        "Delete Folder",
        app,
    )

    # Set Actions for click
    add_folder_action.triggered.connect(lambda: add_folder_click(app))
    edit_folder_action.triggered.connect(lambda: edit_folder_click(app))
    delete_folder_action.triggered.connect(lambda: delete_folder_click(app))

    folders_header_toolbar = QToolBar(app)
    folders_header_toolbar.addAction(add_folder_action)
    folders_header_toolbar.addAction(edit_folder_action)
    folders_header_toolbar.addAction(delete_folder_action)
    folders_header_toolbar.setContentsMargins(0, 0, 0, 0)
    app.folders_header_layout.addWidget(folders_header_toolbar)

    app.sidebar_layout.addWidget(app.folders_header_widget)

    app.folders_tree = QTreeWidget()
    app.folders_tree.setContextMenuPolicy(Qt.CustomContextMenu)
    app.folders_tree.setHeaderHidden(True)
    app.folders_tree.customContextMenuRequested.connect(lambda: show_folder_menu(app))
    app.sidebar_layout.addWidget(app.folders_tree)


def show_folder_menu(app):
    # Create a context menu
    menu = QMenu(app)

    # Add actions to the menu
    add_folder_action = menu.addAction("Add Folder")
    edit_folder_action = menu.addAction("Edit Folder")
    delete_folder_action = menu.addAction("Delete Folder")

    # Show the menu
    action = menu.exec_(app.folders_tree.viewport().mapToGlobal(app.folders_tree.pos()))
    if action == add_folder_action:
        add_folder_click(app)
    if action == edit_folder_action:
        edit_folder_click(app)
    if action == delete_folder_action:
        delete_folder_click(app)

def add_folder_click(app):
    # Launch input dialog to take folder name
    folder_name, ok = QInputDialog.getText(app, "Add Folder", "Folder Name:")

    if ok and folder_name and folder_name.strip() != "":
        app.folder_model.create_folder(folder_name)
        load_folders(app)
    else:
        # Prompt to enter folder name
        QMessageBox.warning(app, "Add Folder", "Please enter a folder name.")


def edit_folder_click(app):
    # Get selected folder
    selected_item = app.folders_tree.currentItem()

    if not selected_item:
        QMessageBox.warning(app, "Edit Folder", "Please select a folder to edit.")
        return

    # Get folder id
    folder_id = selected_item.data(0, Qt.UserRole)

    # Launch input dialog to take folder name
    folder_name, ok = QInputDialog.getText(
        app, "Edit Folder", "Folder Name:", text=selected_item.text(0)
    )

    if not (ok and folder_name and folder_name.strip() != ""):
        # Prompt to enter folder name
        QMessageBox.warning(app, "Edit Folder", "Please enter a folder name.")
        return

    app.folder_model.update_folder(folder_id, folder_name)
    load_folders(app)


def delete_folder_click(app):
    # Get selected folder
    selected_item = app.folders_tree.currentItem()

    if not selected_item:
        # Prompt to select a folder
        QMessageBox.warning(app, "Delete Folder", "Please select a folder to delete.")
        return

    # Get folder id
    folder_id = selected_item.data(0, Qt.UserRole)

    # Prompt to confirm deletion
    if (
        QMessageBox.warning(
            app,
            "Delete Folder",
            f"Are you sure you want to delete the folder: {selected_item.text(0)}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        != QMessageBox.Yes
    ):
        return

    app.folder_model.delete_folder(folder_id)
    load_folders(app)
