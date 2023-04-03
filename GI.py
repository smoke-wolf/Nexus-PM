import os
import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QTextEdit, \
    QDialog, QInputDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setGeometry(200, 200, 400, 150)
        self.setWindowTitle('Package Installer')
        self.setStyleSheet("background-color: #2C3E50; color: white;")

        # Create layout
        layout = QVBoxLayout(self)

        # Add title label
        title_label = QLabel('Enter local directory or Git URL:', self)
        title_label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Add text box for input
        self.input_box = QLineEdit(self)
        self.input_box.setStyleSheet("background-color: white; color: black; border-radius: 5px;")
        layout.addWidget(self.input_box)

        # Add button to start installation
        install_button = QPushButton('Install', self)
        install_button.setStyleSheet(
            "background-color: #1abc9c; color: white; font-size: 16px; border-radius: 5px; padding: 5px 20px;")
        install_button.clicked.connect(self.start_installation)
        layout.addWidget(install_button)

        # Show the window
        self.show()

    def start_installation(self):
        input_text = self.input_box.text()

        if input_text.startswith('http'):
            print(f'Installing package from Git URL: {input_text}')

            # Prompt for common commands to run
            common_commands, ok = QInputDialog.getText(self, 'Common Commands', 'Enter any common commands to run:')
            if ok:
                print(f'Common commands to run: {common_commands}')

            import os

            def clone_repo(github_url):
                # Specify the destination directory for cloning the repository
                import os

                home_dir = os.path.expanduser("~")

                destination_dir = home_dir

                # Extract the repository name from the GitHub URL
                repo_name = github_url.split('/')[-1].split('.')[0]

                # Change to the destination directory
                os.chdir(destination_dir)

                # Clone the repository using git
                os.system(f'git clone {github_url}')

                # Return the path to the cloned repository
                return os.path.join(destination_dir)

            # Display a file tree of the downloaded repo
            repo_path = clone_repo(input_text)
            repo_files = []
            for root, dirs, files in os.walk(repo_path):
                level = root.replace(repo_path, '').count(os.sep)
                indent = ' ' * 4 * (level)
                files_list = [f'{indent}{f}' for f in files]
                repo_files.extend(files_list)
            if repo_files:
                files_str = '\n'.join(repo_files)
                files_list, ok = QInputDialog.getItem(self, 'Files in Downloaded Repo', 'Select a file to run:',
                                                      files_str.split('\n'), editable=False)
                if ok:
                    print(f'Selected file to run: {files_list}')

            # Add notes

            notes, ok = QInputDialog.getMultiLineText(self, 'Notes', 'Add any notes:')
            if ok:
                print(f'Notes: {notes}')

                data1 = f'''
=======================NOTES==========================
                    {notes}
======================================================
SIZE = 
    MEAN FILESIZE =
MAIN_LANGUAGE = 
    LANAUGE_DIVISION =
DATA = 
    DATE_DOWNLOADED =
    CURRENT_VERSION =
============================================================
'''

                with open('Data.late', 'a') as data:
                    data.write(data1)

        else:
            print(f'Installing package from local directory: {input_text}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
