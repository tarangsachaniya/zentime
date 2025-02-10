import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QWidget, QHBoxLayout, QStackedWidget, QMessageBox,
    QListWidgetItem, QInputDialog, QMenu
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTimer, Qt
from plyer import notification
import webbrowser
import os
from pymongo import MongoClient


class LoginRegisterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Productivity App")
        self.setGeometry(200, 200, 500, 400)

        # Initialize MongoDB
        self.init_db()

        # Main layout
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Login UI
        self.login_ui = QWidget()
        self.login_layout = QVBoxLayout()
        self.login_ui.setLayout(self.login_layout)

        self.login_label = QLabel("Login", self)
        self.login_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.login_label.setAlignment(Qt.AlignCenter)
        self.login_layout.addWidget(self.login_label)

        self.login_username = QLineEdit(self)
        self.login_username.setPlaceholderText("Username")
        self.login_layout.addWidget(self.login_username)

        self.login_password = QLineEdit(self)
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_layout.addWidget(self.login_password)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.login_layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.show_register_ui)
        self.login_layout.addWidget(self.register_button)

        # Register UI
        self.register_ui = QWidget()
        self.register_layout = QVBoxLayout()
        self.register_ui.setLayout(self.register_layout)

        self.register_label = QLabel("Register", self)
        self.register_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.register_label.setAlignment(Qt.AlignCenter)
        self.register_layout.addWidget(self.register_label)

        self.register_username = QLineEdit(self)
        self.register_username.setPlaceholderText("Username")
        self.register_layout.addWidget(self.register_username)

        self.register_password = QLineEdit(self)
        self.register_password.setPlaceholderText("Password")
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_layout.addWidget(self.register_password)

        self.register_button_confirm = QPushButton("Register", self)
        self.register_button_confirm.clicked.connect(self.register)
        self.register_layout.addWidget(self.register_button_confirm)

        self.back_to_login_button = QPushButton("Back to Login", self)
        self.back_to_login_button.clicked.connect(self.show_login_ui)
        self.register_layout.addWidget(self.back_to_login_button)

        # Add UIs to stacked widget
        self.stacked_widget.addWidget(self.login_ui)
        self.stacked_widget.addWidget(self.register_ui)

        # Show login UI by default
        self.show_login_ui()

    def init_db(self):
        self.client = MongoClient('mongodb+srv://lfa:lfaDB@cluster0.zdjyw.mongodb.net/')
        self.db = self.client['productivity_app']
        self.users = self.db['users']
        self.tasks = self.db['tasks']

    def show_login_ui(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_register_ui(self):
        self.stacked_widget.setCurrentIndex(1)

    def login(self):
        username = self.login_username.text()
        password = self.login_password.text()

        user = self.users.find_one({'username': username, 'password': password})

        if user:
            self.user_id = user['_id']
            self.show_productivity_app()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def register(self):
        username = self.register_username.text()
        password = self.register_password.text()

        if self.users.find_one({'username': username}):
            QMessageBox.warning(self, "Registration Failed", "Username already exists")
        else:
            user_id = self.users.insert_one({'username': username, 'password': password}).inserted_id
            QMessageBox.information(self, "Registration Successful", "You can now login with your credentials")
            self.show_login_ui()

    def show_productivity_app(self):
        self.productivity_app = ProductivityApp(self.user_id, self.db)
        self.setCentralWidget(self.productivity_app)


class ProductivityApp(QWidget):
    def __init__(self, user_id, db):
        super().__init__()
        self.user_id = user_id
        self.db = db
        self.tasks = self.db['tasks']
        self.start_time = time.time()

        self.init_ui()
        self.load_tasks()

        # Timer to update screen time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_screen_time)
        self.timer.start(1000)

    def init_ui(self):
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
                background: #F9CB43;
                color: #FFFFFF;
            }
        """)
        self.todo_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.todo_list.customContextMenuRequested.connect(self.show_context_menu)
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

        # Logout button
        logout_button = QPushButton("Logout", self)
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #F44336;
            }
        """)
        logout_button.clicked.connect(self.logout)
        main_layout.addWidget(logout_button)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #212121;")

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
            self.tasks.insert_one({'user_id': self.user_id, 'task': task, 'completed': False, 'is_available': True})
            self.load_tasks()
            self.todo_input.clear()

    def load_tasks(self):
        self.todo_list.clear()
        tasks = self.tasks.find({'user_id': self.user_id, 'is_available': True})
        for task in tasks:
            item = QListWidgetItem(task['task'])
            item.setData(Qt.UserRole, task['_id'])
            if task['completed']:
                item.setBackground(QColor("#4CAF50"))
                item.setForeground(QColor("#FFFFFF"))
            elif task['is_available']:
                item.setBackground(QColor("#E52020"))
                item.setForeground(QColor("#FFFFFF"))
            self.todo_list.addItem(item)

    def update_screen_time(self):
        elapsed_time = int(time.time() - self.start_time)
        self.screen_time_label.setText(f"Screen Time: {elapsed_time // 60}m {elapsed_time % 60}s")

        if elapsed_time % 3600 == 0:
            notification.notify(
                title="Screen Time Alert",
                message="You've been working for an hour. Take a short break!",
                timeout=5
            )

    def open_browser(self):
        webbrowser.open("https://www.google.com")

    def open_notepad(self):
        os.system("notepad.exe")

    def show_context_menu(self, position):
        item = self.todo_list.itemAt(position)
        if item:
            task_id = item.data(Qt.UserRole)
            task = self.tasks.find_one({'_id': task_id})

            menu = QMenu()
            edit_action = menu.addAction("Edit Task")
            delete_action = menu.addAction("Delete Task")

            if task['completed']:
                mark_pending_action = menu.addAction("Mark as Pending")
                mark_pending_action.triggered.connect(lambda: self.mark_task_pending(task_id))

            action = menu.exec_(self.todo_list.mapToGlobal(position))

            if action == edit_action:
                self.edit_task(task_id)
            elif action == delete_action:
                self.delete_task(task_id)

    def mark_task_pending(self, task_id):
        self.tasks.update_one({'_id': task_id}, {'$set': {'completed': False}})
        self.load_tasks()

    def edit_task(self, task_id):
        task, ok = QInputDialog.getText(self, "Edit Task", "Edit the task:")
        if ok and task:
            self.tasks.update_one({'_id': task_id}, {'$set': {'task': task}})
            self.load_tasks()

    def delete_task(self, task_id):
        self.tasks.update_one({'_id': task_id}, {'$set': {'is_available': False}})
        self.load_tasks()

    def logout(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginRegisterApp()
    window.show()
    sys.exit(app.exec_())