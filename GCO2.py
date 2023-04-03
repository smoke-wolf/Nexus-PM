import os
import subprocess
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QTextEdit, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog, QGroupBox, QPushButton

class MainWindow(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 800, 600)

        # Create file system model and view
        self.model = QFileSystemModel()
        self.model.setRootPath(self.path)
        self.view = QTreeView(self)
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.index(self.path))
        self.view.setAnimated(False)
        self.view.setIndentation(20)
        self.view.setSortingEnabled(True)

        # Create notes widget
        self.notes = QTextEdit()
        self.notes.setReadOnly(False)

        # Create list widget
        self.list = QListWidget(self)
        self.list.addItems(['Option 1', 'Option 2', 'Option 3'])

        # Create settings group box
        self.settings_box = QGroupBox("Settings")
        self.delete_button = QPushButton("Delete")
        self.run_button = QPushButton("Run")
        self.settings_layout = QVBoxLayout()
        self.settings_layout.addWidget(self.delete_button)
        self.settings_layout.addWidget(self.run_button)
        self.settings_box.setLayout(self.settings_layout)

        # Create layouts
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.left_layout.addWidget(self.view)
        self.right_layout.addWidget(self.notes)
        self.right_layout.addWidget(self.list)
        self.right_layout.addWidget(self.settings_box)

        # Connect signals
        self.view.clicked.connect(self.file_selected)
        self.notes.textChanged.connect(self.notes_changed)
        self.list.itemClicked.connect(self.list_selected)
        self.delete_button.clicked.connect(self.delete_file)
        self.run_button.clicked.connect(self.run_file)

    def file_selected(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.notes.setPlainText(self.get_notes(path))

    def notes_changed(self):
        path = self.model.filePath(self.view.currentIndex())
        if os.path.isfile(path):
            self.save_notes(path, self.notes.toPlainText())

    def list_selected(self, item):
        print(item.text())

    def delete_file(self):
        path = self.model.filePath(self.view.currentIndex())
        import os
        fpath = f'{os.path.splitext(os.path.basename(path))[0]}'
        folder_path = os.path.dirname(fpath)

        import psutil

        psutil.os.remove(folder_path)
        print('dir removed')
    import subprocess

    # ...

    def run_file(self):
        path = self.model.filePath(self.view.currentIndex())
        print(path)
        if not os.path.isfile(path):
            return

        file_ext = os.path.splitext(path)[1].lower()
        if file_ext == '.py':
            fpath = f'{os.path.splitext(os.path.basename(path))[0]}'
            folder_path = os.path.dirname(fpath)

            command = f'cd {folder_path} && python3 {path}'

            print(command)
        elif file_ext in ['.c', '.cpp']:
            command = f'g++ "{path}" && ./a.out'
        elif file_ext == '.java':
            command = f'javac "{path}" && java "{os.path.splitext(os.path.basename(path))[0]}"'
        else:
            return

        # Open a new Terminal window and run the command
        os.system(f"osascript -e 'tell app \"Terminal\" to do script \"{command}\"'")



    def get_notes(self, path):
        # Read notes from file or return empty string if not exists
        notes_file = path + ".notes"
        if os.path.isfile(notes_file):
            with open(notes_file, 'r') as f:
                return f.read()
        else:
            return ""

    def save_notes(self, path, notes):
        # Save notes to file
        notes_file = path + ".notes"
        with open(notes_file, 'w') as f:
            f.write(notes)


style = """
QMainWindow {
    background-color: black;
}

QTreeView {
    background-color: black;
    border: none;
    color: white;
}

QTreeView::item:hover {
    background-color: #ff6ff2;
}

QTreeView::item:selected {
    background-color: #5f5fff;
}

QTextEdit {
    background-color: #f2f2f2;
    border: none;
    color: black;
}

QListWidget {
    background-color: #2b2b2b;
    color: white;
    border: none;
}

QListWidget::item:hover {
    background-color: #ff6ff2;
}

QListWidget::item:selected {
    background-color: #5f5fff;
}
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(sys.argv[1])
    window.setStyleSheet(style)

    window.show()
    sys.exit(app.exec_())
