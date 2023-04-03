import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QDesktopWidget, \
    QMessageBox, QTextEdit, QHBoxLayout, QVBoxLayout, QCheckBox, QDialog, QDialogButtonBox, QRadioButton, QButtonGroup


class GHPM_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the window title and geometry
        self.setWindowTitle('Nexus PM')
        self.setGeometry(100, 100, 600, 400)

        # Set the window background color to indigo/neon blue
        self.setStyleSheet("background-color: #4b0082;")

        # Set the window border style to a fancy one with black color
        self.setStyleSheet("QWidget#Nexus_PM_GUI {border: 2px solid black; border-radius: 10px;}")
        self.setObjectName("Nexus_PM_GUI")

        # Create the buttons on the left side of the screen
        self.install_button = QPushButton('Install', self)
        self.install_button.setGeometry(20, 50, 120, 30)
        self.install_button.clicked.connect(self.install_action)
        self.install_button.setStyleSheet("background-color: #191970; color: white; border-radius: 10px;")

        self.activate_button = QPushButton('Activate', self)
        self.activate_button.setGeometry(20, 100, 120, 30)
        self.activate_button.clicked.connect(self.activate_action)
        self.activate_button.setStyleSheet("background-color: #191970; color: white; border-radius: 10px;")

        self.uninstall_button = QPushButton('Information', self)
        self.uninstall_button.setGeometry(20, 150, 120, 30)
        self.uninstall_button.clicked.connect(self.uninstall_action)
        self.uninstall_button.setStyleSheet("background-color: #191970; color: white; border-radius: 10px;")

        self.settings_button = QPushButton('Settings', self)
        self.settings_button.setGeometry(20, 200, 120, 30)
        self.settings_button.clicked.connect(self.settings_action)
        self.settings_button.setStyleSheet("background-color: #191970; color: white; border-radius: 10px;")

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.setGeometry(20, 350, 120, 30)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: #191970; color: white; border-radius: 10px;")

        ## Create a banner with a friendly yellow theme to alert user of network not found
        self.banner = QMessageBox(self)
        self.banner.setIcon(QMessageBox.Warning)
        self.banner.setStyleSheet("background-color: #F5A623;")
        self.banner.setText("Local Directory Support Not Yet Available")
        self.banner.setStandardButtons(QMessageBox.Ok)
        self.banner.button(QMessageBox.Ok).setStyleSheet("background-color: #F5A623; color: white;")
        self.banner.exec_()

        self.default_text = QLabel(self)
        self.default_text.setGeometry(140, -220, 420, 800)
        self.default_text.setText('''
        Welcome to Nexus Package Manager 
                (Nexus-PM)

        Nexus-PM is the next-generation
        package manager, offering significant
        improvements over its predecessor.

        While still under development, our
        streamlined interface simplifies 
        package and dependency management, 
        making it easy for developers of all
        levels to use. 

        Happy coding!
        ''')
        self.default_text.setStyleSheet('''
        font-size: 18px;
        color: white;
        background-color: rgba(0, 0, 0, 0%);
        padding: 30px;
        border-radius: 15px;
        ''')

    def show_network_not_found_banner(self):
        self.network_not_found_banner.show()

    def hide_network_not_found_banner(self):
        self.network_not_found_banner.hide()

    def install_action(self):
        try:
            os.system('python3 {os.getcwd()}/GI.py')
        except:
            print('error')

    def activate_action(self):
        # Create the activation dialog
        activate_dialog = QDialog(self)
        activate_dialog.setWindowTitle('Activate Package')
        activate_dialog.setStyleSheet("background-color: #4b0082; color: white;")

        layout = QVBoxLayout(activate_dialog)
        layout.setSpacing(20)

        # Add a label to the dialog to get the package source
        label = QLabel('Please choose the package source:', activate_dialog)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        # Add radio buttons to the dialog for GitHub and Local Directory options
        github_radio_button = QRadioButton('GitHub', activate_dialog)
        local_radio_button = QRadioButton('Local Directory', activate_dialog)
        local_radio_button.setEnabled(False)

        # Create a button group to manage the radio buttons
        button_group = QButtonGroup(activate_dialog)
        button_group.addButton(github_radio_button)
        button_group.addButton(local_radio_button)

        layout.addWidget(github_radio_button)
        layout.addWidget(local_radio_button)

        # Add a line edit to the dialog to get the package name input
        package_name_input = QLineEdit(activate_dialog)
        package_name_input.setStyleSheet("background-color: white; color: black; border-radius: 5px;")
        layout.addWidget(package_name_input)

        # Add buttons to the dialog
        button_box = QDialogButtonBox(Qt.Horizontal, activate_dialog)
        button_box.setCenterButtons(True)
        button_box.setStyleSheet("padding: 10px;")

        activate_button = QPushButton('Activate', activate_dialog)

        def on_activate_button_clicked():
            if github_radio_button.isChecked():
                try:
                    os.system(f'python3 {os.getcwd()}/GCO.py')
                except:
                    print('error')
            elif local_radio_button.isChecked():
                self.activate_local_package(package_name_input.text())

        activate_button.clicked.connect(on_activate_button_clicked)
        button_box.addButton(activate_button, QDialogButtonBox.AcceptRole)

        cancel_button = QPushButton('Cancel', activate_dialog)
        cancel_button.clicked.connect(activate_dialog.reject)
        button_box.addButton(cancel_button, QDialogButtonBox.RejectRole)

        layout.addWidget(button_box)

        # Show the activation dialog
        if activate_dialog.exec_() == QDialog.Accepted:
            on_activate_button_clicked()

    def activate_package(self, package_name):
        # Activate the package and display a success message
        activate_success_dialog = QMessageBox(self)
        activate_success_dialog.setWindowTitle('Activation Successful')
        activate_success_dialog.setStyleSheet("background-color: #4b0082; color: white;")
        activate_success_dialog.setText(f'Package {package_name} has been activated.')
        activate_success_dialog.addButton('OK', QMessageBox.AcceptRole)
        activate_success_dialog.exec_()

    def uninstall_action(self):
        # Create a scrollable text box with the text "Hello World"
        scrollable_text_box_info = QTextEdit('''
        GitHub Package Manager (GHPM) is a package manager designed to effectively manage GitHub packages and local directories and file paths. Its main objective is to organize, compile, and recall packages with ease. GHPM uses strategic logic to install packages and handles all requirements and other prerequisites automatically through GitHub Installations to mitigate preventable exits and errors.

One of the main differentiating features of GHPM is its seamless, user-free installation of applications and projects. It allows for cross-instance reference of programs and contains all packages to allow for simple execution in future instances. Other package managers, such as Huber, have fundamental limitations such as using free installation on large ranges of applications.

GHPM's features include cross-version support post-v1.2.4, Windows versions, open-source, incredibly detailed 
documentation, systematic application scraping, password reset and account flexibility, structures and skeletons that 
allow compileable applications, install packages through GitHub (requires GitClone), link local directories to 
packages, embedded data logic that prevents cross UU?D (User/Device), beta data lock/encrypted storage, 
intuitive configurations to search for potential launch scripts, install complex applications and packages, 
automatic requirements installation for Git packages (requires pip), comprehensive event tracking (saved to 
system/cache/system/error log), fluid package launches using launch commands configured through installation, 
seamless uninstallation for GitHub installs and local imports (deletes directory), salt and hash-based encryption for 
passwords, direct cache editing and altering, and control system settings and personalization. All of these features 
are now doable through the GUI. 

GHPM's goals and to-do list include SHA256 for files related to updates, cross-platform compatibility that requires a 
Windows update, logging and monitoring to solve errors intuitively, API account connection and development, 
third-party integration, update installed repos, install APK and DMG applications, handle requirements within local 
installations, reconfigure file security/storage with pyminizip, patch null install/failed cleanup for installations, 
allow separate profiles (profile locking built-in), smoothen interfaces and tidy code (patches and corrections), 
automatic file additions with new versions (version updates facilitate new data), and add better listing features (
patched in GUI). 

In summary, GHPM is a comprehensive package manager designed to effectively manage GitHub packages and local 
directories and file paths. It has a wide range of features, including seamless, user-free installation of 
applications and projects, and handles all requirements and other prerequisites automatically through GitHub 
Installations. Its goals and to-do list show that GHPM is committed to improving its features and adding new ones to 
better serve its users.''', self)

        scrollable_text_box = QTextEdit('''Attention: This program is currently in beta development and is undergoing 
        active development and testing. Please note that you may encounter bugs, glitches, or other issues while 
        using this program. We appreciate your patience and feedback as we work to improve the software and provide a 
        better user experience. Thank you for your understanding! 

        -Nexus PM, 2023
        ''', self)

        scrollable_text_box.setStyleSheet(
            "background-color: #4b0082; color: white; border-radius: 5px; font-size: 12pt;")
        scrollable_text_box.setReadOnly(True)
        scrollable_text_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollable_text_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set the minimum size of the text box
        scrollable_text_box.setMinimumSize(200, 100)

        # Create the uninstallation dialog
        uninstall_dialog = QDialog(self)
        uninstall_dialog.setWindowTitle('GHPM Information')
        uninstall_dialog.setStyleSheet("background-color: #4b0082; color: white;")

        # Add the scrollable text box to the dialog
        layout = QVBoxLayout(uninstall_dialog)
        layout.addWidget(scrollable_text_box)

        # Show the uninstallation dialog
        uninstall_dialog.exec_()

    def show_uninstall_success_dialog(self, package_name):
        # Create and show the success dialog
        dialog = QMessageBox()
        dialog.setWindowTitle('Uninstallation Successful')
        dialog.setStyleSheet("background-color: #4b0082; color: white;")
        dialog.setText(f'Package "{package_name}" has been uninstalled.')
        dialog.addButton('OK', QMessageBox.AcceptRole)
        dialog.exec_()

    def uninstall_package(package_name):
        # Uninstall the package
        # ... code to uninstall the package goes here ...

        # Show the success dialog
        package_name.show_uninstall_success_dialog(package_name)

    def settings_action(self):
        # Create the settings dialog
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle('Settings')
        settings_dialog.setStyleSheet("background-color: #4b0082; color: white;")

        # Create a vertical layout for the dialog
        layout = QVBoxLayout(settings_dialog)

        # Add a label to the layout
        label = QLabel('Select the settings you want to change:', settings_dialog)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        # Add checkboxes for each setting to the layout
        proxy_checkbox = QCheckBox('Use proxy server', settings_dialog)
        proxy_checkbox.setStyleSheet("color: white;")
        layout.addWidget(proxy_checkbox)

        autoupdate_checkbox = QCheckBox('Check for updates automatically', settings_dialog)
        autoupdate_checkbox.setStyleSheet("color: white;")
        layout.addWidget(autoupdate_checkbox)

        # Add a horizontal layout for the buttons
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        # Add a button to save the changes to the buttons layout
        save_button = QPushButton('Save', settings_dialog)
        save_button.setStyleSheet("background-color: #191970; color: white; border-radius: 10px;")
        buttons_layout.addWidget(save_button)

        # Add a button to cancel the changes to the buttons layout
        cancel_button = QPushButton('Cancel', settings_dialog)
        cancel_button.setStyleSheet("background-color: #191970; color: white; border-radius: 10px;")
        buttons_layout.addWidget(cancel_button)

        # Connect the buttons to their actions
        save_button.clicked.connect(
            lambda: self.save_settings(proxy_checkbox.isChecked(), autoupdate_checkbox.isChecked()))
        save_button.clicked.connect(settings_dialog.close)

        cancel_button.clicked.connect(settings_dialog.close)

        # Add a grey overlap with disabled options notice
        overlap = QWidget(settings_dialog)
        overlap.setStyleSheet("background-color: rgba(128, 128, 128, 0.5);")
        overlap_layout = QVBoxLayout(overlap)
        overlap_label = QLabel('Options currently disabled', overlap)
        overlap_label.setStyleSheet("color: white; font-weight: bold;")
        overlap_layout.addWidget(overlap_label)
        overlap_checkbox1 = QCheckBox('Enable SHA256 checks', overlap)
        overlap_checkbox1.setStyleSheet("color: white;")
        overlap_checkbox1.setEnabled(False)
        overlap_layout.addWidget(overlap_checkbox1)
        overlap_checkbox2 = QCheckBox('Obfuscate (Nexus) or (Nexus-data)', overlap)
        overlap_checkbox2.setStyleSheet("color: white;")
        overlap_checkbox2.setEnabled(False)
        overlap_layout.addWidget(overlap_checkbox2)
        overlap_checkbox3 = QCheckBox('Automatically Update', overlap)
        overlap_checkbox3.setStyleSheet("color: white;")
        overlap_checkbox3.setEnabled(False)
        overlap_layout.addWidget(overlap_checkbox3)
        layout.addWidget(overlap)

        # Disable all buttons and checkboxes
        for button in [save_button, cancel_button]:
            button.setEnabled(False)
        for checkbox in [proxy_checkbox, autoupdate_checkbox, overlap_checkbox1, overlap_checkbox2]:
            checkbox.setEnabled(False)

        # Show the settings dialog
        settings_dialog.exec_()

    def save_settings(self, use_proxy, check_for_updates):
        # Save the settings
        # ...
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the application style to Fusion
    app.setStyle('Fusion')

    # Set the application palette to the neon blue and black color scheme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0, 0, 0))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(0, 43, 127))
    palette.setColor(QPalette.AlternateBase, QColor(0, 51, 153))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(0, 43, 127))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = GHPM_GUI()

    window.show()
    sys.exit(app.exec_())




