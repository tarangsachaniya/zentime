<<<<<<< HEAD
import sys
import time
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QWidget, QHBoxLayout, QStackedWidget
)
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import QTimer, Qt
from plyer import notification
import psutil


class ProductivityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Productivity App")
        self.setGeometry(200, 200, 500, 400)

        # Initialize
        self.init_ui()
        self.start_time = time.time()

        # Timer to update screen time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_screen_time)
        self.timer.start(1000)  # Update every second

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Add header
        header = QLabel("Productivity Dashboard", self)
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #4CAF50; text-align: center;")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Screen time section
        self.screen_time_label = QLabel("Screen Time: 0s", self)
        self.screen_time_label.setFont(QFont("Arial", 12))
        self.screen_time_label.setStyleSheet("color: #FFFFFF; padding: 10px;")
        self.screen_time_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.screen_time_label)

        # To-Do list section
        todo_header = QLabel("To-Do List", self)
        todo_header.setFont(QFont("Arial", 14, QFont.Bold))
        todo_header.setStyleSheet("color: #FF9800; padding-top: 15px;")
        main_layout.addWidget(todo_header)

        self.todo_input = QLineEdit(self)
        self.todo_input.setPlaceholderText("Add a new task...")
        self.todo_input.setFont(QFont("Arial", 10))
        self.todo_input.setStyleSheet("padding: 10px; border-radius: 5px; background: #424242; color: #FFFFFF;")
        main_layout.addWidget(self.todo_input)

        self.todo_list = QListWidget(self)
        self.todo_list.setFont(QFont("Arial", 10))
        self.todo_list.setStyleSheet("""
            QListWidget {
                background: #303030;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #4CAF50;
                color: #FFFFFF;
            }
        """)
        main_layout.addWidget(self.todo_list)

        add_button = QPushButton("Add Task", self)
        add_button.setFont(QFont("Arial", 10))
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        add_button.clicked.connect(self.add_task)
        main_layout.addWidget(add_button)

        # Quick access tools section
        tools_header = QLabel("Quick Access Tools", self)
        tools_header.setFont(QFont("Arial", 14, QFont.Bold))
        tools_header.setStyleSheet("color: #FF9800; padding-top: 15px;")
        main_layout.addWidget(tools_header)

        tools_layout = QHBoxLayout()
        browser_button = QPushButton("Open Browser", self)
        browser_button.setStyleSheet(self.style_button("#03A9F4"))
        browser_button.clicked.connect(self.open_browser)

        notepad_button = QPushButton("Open Notepad", self)
        notepad_button.setStyleSheet(self.style_button("#03A9F4"))
        notepad_button.clicked.connect(self.open_notepad)

        tools_layout.addWidget(browser_button)
        tools_layout.addWidget(notepad_button)
        main_layout.addLayout(tools_layout)

        # Footer Section
        footer = QLabel("Stay productive and focused!", self)
        footer.setFont(QFont("Arial", 10, QFont.StyleItalic))
        footer.setStyleSheet("color: #BDBDBD; text-align: center; padding-top: 20px;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        # Main widget
        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet("background-color: #212121;")
        self.setCentralWidget(container)

    def style_button(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }}
            QPushButton:hover {{
                background-color: {color[:-1]}D9;
            }}
        """

    def add_task(self):
        task = self.todo_input.text()
        if task:
            self.todo_list.addItem(task)
            self.todo_input.clear()

    def update_screen_time(self):
        elapsed_time = int(time.time() - self.start_time)
        self.screen_time_label.setText(f"Screen Time: {elapsed_time // 60}m {elapsed_time % 60}s")

        if elapsed_time % 3600 == 0:  # Notify every hour
            notification.notify(
                title="Screen Time Alert",
                message="You've been working for an hour. Take a short break!",
                timeout=5
            )

    def open_browser(self):
        import webbrowser
        webbrowser.open("https://www.google.com")

    def open_notepad(self):
        import os
        os.system("notepad.exe")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductivityApp()
    window.show()
    sys.exit(app.exec_())
=======
import sys
import time
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QWidget, QHBoxLayout, QStackedWidget
)
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import QTimer, Qt
from plyer import notification
import psutil


class ProductivityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Productivity App")
        self.setGeometry(200, 200, 500, 400)

        # Initialize
        self.init_ui()
        self.start_time = time.time()

        # Timer to update screen time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_screen_time)
        self.timer.start(1000)  # Update every second

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Add header
        header = QLabel("Productivity Dashboard", self)
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #4CAF50; text-align: center;")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Screen time section
        self.screen_time_label = QLabel("Screen Time: 0s", self)
        self.screen_time_label.setFont(QFont("Arial", 12))
        self.screen_time_label.setStyleSheet("color: #FFFFFF; padding: 10px;")
        self.screen_time_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.screen_time_label)

        # To-Do list section
        todo_header = QLabel("To-Do List", self)
        todo_header.setFont(QFont("Arial", 14, QFont.Bold))
        todo_header.setStyleSheet("color: #FF9800; padding-top: 15px;")
        main_layout.addWidget(todo_header)

        self.todo_input = QLineEdit(self)
        self.todo_input.setPlaceholderText("Add a new task...")
        self.todo_input.setFont(QFont("Arial", 10))
        self.todo_input.setStyleSheet("padding: 10px; border-radius: 5px; background: #424242; color: #FFFFFF;")
        main_layout.addWidget(self.todo_input)

        self.todo_list = QListWidget(self)
        self.todo_list.setFont(QFont("Arial", 10))
        self.todo_list.setStyleSheet("""
            QListWidget {
                background: #303030;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #4CAF50;
                color: #FFFFFF;
            }
        """)
        main_layout.addWidget(self.todo_list)

        add_button = QPushButton("Add Task", self)
        add_button.setFont(QFont("Arial", 10))
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        add_button.clicked.connect(self.add_task)
        main_layout.addWidget(add_button)

        # Quick access tools section
        tools_header = QLabel("Quick Access Tools", self)
        tools_header.setFont(QFont("Arial", 14, QFont.Bold))
        tools_header.setStyleSheet("color: #FF9800; padding-top: 15px;")
        main_layout.addWidget(tools_header)

        tools_layout = QHBoxLayout()
        browser_button = QPushButton("Open Browser", self)
        browser_button.setStyleSheet(self.style_button("#03A9F4"))
        browser_button.clicked.connect(self.open_browser)

        notepad_button = QPushButton("Open Notepad", self)
        notepad_button.setStyleSheet(self.style_button("#03A9F4"))
        notepad_button.clicked.connect(self.open_notepad)

        tools_layout.addWidget(browser_button)
        tools_layout.addWidget(notepad_button)
        main_layout.addLayout(tools_layout)

        # Footer Section
        footer = QLabel("Stay productive and focused!", self)
        footer.setFont(QFont("Arial", 10, QFont.StyleItalic))
        footer.setStyleSheet("color: #BDBDBD; text-align: center; padding-top: 20px;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        # Main widget
        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet("background-color: #212121;")
        self.setCentralWidget(container)

    def style_button(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }}
            QPushButton:hover {{
                background-color: {color[:-1]}D9;
            }}
        """

    def add_task(self):
        task = self.todo_input.text()
        if task:
            self.todo_list.addItem(task)
            self.todo_input.clear()

    def update_screen_time(self):
        elapsed_time = int(time.time() - self.start_time)
        self.screen_time_label.setText(f"Screen Time: {elapsed_time // 60}m {elapsed_time % 60}s")

        if elapsed_time % 3600 == 0:  # Notify every hour
            notification.notify(
                title="Screen Time Alert",
                message="You've been working for an hour. Take a short break!",
                timeout=5
            )

    def open_browser(self):
        import webbrowser
        webbrowser.open("https://www.google.com")

    def open_notepad(self):
        import os
        os.system("notepad.exe")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductivityApp()
    window.show()
    sys.exit(app.exec_())
>>>>>>> 7a2ea50 (Basic Code)
