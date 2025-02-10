import sys
import time
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QWidget, QHBoxLayout, QStackedWidget, QMessageBox,
    QListWidgetItem, QInputDialog, QMenu
)
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import QTimer, Qt
from plyer import notification
import psutil
import webbrowser
import os


class LoginRegisterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Productivity App")
        self.setGeometry(200, 200, 500, 400)

        # Initialize database
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
        self.conn = sqlite3.connect('productivity_app.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    def show_login_ui(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_register_ui(self):
        self.stacked_widget.setCurrentIndex(1)

    def login(self):
        username = self.login_username.text()
        password = self.login_password.text()

        self.cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()

        if user:
            self.user_id = user[0]
            self.show_productivity_app()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def register(self):
        username = self.register_username.text()
        password = self.register_password.text()

        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            QMessageBox.information(self, "Registration Successful", "You can now login with your credentials")
            self.show_login_ui()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Registration Failed", "Username already exists")

    def show_productivity_app(self):
        # Always show the productivity app, regardless of whether tasks exist or not
        self.productivity_app = ProductivityApp(self.user_id, self.conn)
        self.setCentralWidget(self.productivity_app)


class ProductivityApp(QWidget):
    def __init__(self, user_id, conn):
        super().__init__()
        self.user_id = user_id
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.start_time = time.time()

        self.init_ui()
        self.load_tasks()

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
            self.cursor.execute('INSERT INTO tasks (user_id, task) VALUES (?, ?)', (self.user_id, task))
            self.conn.commit()
            self.load_tasks()
            self.todo_input.clear()

    def load_tasks(self):
        self.todo_list.clear()
        self.cursor.execute('SELECT id, task, completed FROM tasks WHERE user_id = ?', (self.user_id,))
        tasks = self.cursor.fetchall()
        for task in tasks:
            item = QListWidgetItem(task[1])
            item.setData(Qt.UserRole, task[0])  # Store task ID in the item
            if task[2]:  # If task is completed
                item.setBackground(QColor("#4CAF50"))
                item.setForeground(QColor("#FFFFFF"))
            self.todo_list.addItem(item)

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
        webbrowser.open("https://www.google.com")

    def open_notepad(self):
        os.system("notepad.exe")

    def show_context_menu(self, position):
        item = self.todo_list.itemAt(position)
        if item:
            menu = QMenu()
            edit_action = menu.addAction("Edit Task")
            delete_action = menu.addAction("Delete Task")
            complete_action = menu.addAction("Mark as Complete")
            action = menu.exec_(self.todo_list.mapToGlobal(position))
            if action == edit_action:
                self.edit_task(item)
            elif action == delete_action:
                self.delete_task(item)
            elif action == complete_action:
                self.mark_task_complete(item)

    def edit_task(self, item):
        task_id = item.data(Qt.UserRole)
        new_task, ok = QInputDialog.getText(self, "Edit Task", "Edit your task:", text=item.text())
        if ok and new_task:
            self.cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
            self.conn.commit()
            self.load_tasks()

    def delete_task(self, item):
        task_id = item.data(Qt.UserRole)
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        self.load_tasks()

    def mark_task_complete(self, item):
        task_id = item.data(Qt.UserRole)
        self.cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
        self.conn.commit()
        self.load_tasks()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegisterApp()
    window.show()
    sys.exit(app.exec_())