from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QGroupBox, QPushButton, QListWidget, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import os


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # initialize window properties
        self.setWindowTitle("Nexus Git")
        self.setFixedSize(600, 500)
        self.setStyleSheet(
            "background-color: #f5a623; color: #333; font-size: 16px;"
        )

        # initialize GUI elements
        self.central_widget = QWidget()
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)
        self.groupBox = QGroupBox('''Choose Git Repo -> Nexus GI''')
        self.groupBox.setStyleSheet(
            "QGroupBox { font-size: 24px; color: #333; background-color: #f5a623; border: 1px solid #333; }"
            "QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; color: #333; }"
        )

        self.folder_list = QListWidget()
        self.folder_list.setStyleSheet(
            "background-color: #fff; color: #333; font-size: 18px;"
        )
        self.folder_list.setFixedSize(500, 300)
        self.search_bar = QLineEdit()
        self.search_bar.setStyleSheet(
            "background-color: #fff; color: #333; font-size: 18px;"
        )
        self.search_bar.setPlaceholderText("Search folders...")
        self.search_bar.setFixedSize(500, 30)
        self.select_button = QPushButton("Select")
        self.select_button.setStyleSheet(
            "background-color: #fff; color: #333; font-size: 18px; border: 1px solid #333;"
        )
        self.select_button.setFixedSize(100, 50)

        # add GUI elements to layout
        self.layout.addWidget(self.groupBox, 0, 0, 1, 2)
        self.layout.addWidget(self.search_bar, 1, 0, 1, 2)
        self.layout.addWidget(self.folder_list, 2, 0, 1, 2)
        self.layout.addWidget(self.select_button, 3, 1)

        # set central widget
        self.setCentralWidget(self.central_widget)

        # connect signals and slots
        self.select_button.clicked.connect(self.select_folder)
        self.search_bar.textChanged.connect(self.filter_folders)

        # populate folder list
        self.populate_folder_list()

    def populate_folder_list(self):
        folder_path = os.path.expanduser("~")
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        self.folder_list.addItems(folders)

    def select_folder(self):
        selected_folder = self.folder_list.currentItem().text()
        import os

        home_dir = os.path.expanduser("~")
        print(home_dir)
        folder_path = f"{home_dir}/{selected_folder}"
        # do something with the selected folder here
        print(f"Selected folder: {selected_folder}")
        os.system(f'python3 {os.getcwd()}/GCO2.py {folder_path}')

    def filter_folders(self, text):
        folder_path = os.path.expanduser("~")
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        filtered_folders = [f for f in folders if text.lower() in f.lower()]
        self.folder_list.clear()
        self.folder_list.addItems(filtered_folders)

app = QApplication([])
window = MyWindow()
window.show()
app.exec_()

