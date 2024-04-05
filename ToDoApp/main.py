import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QListWidget,
    QMessageBox,
)
from PyQt5.QtGui import QFont


class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []

        self.setWindowTitle("To-Do List App")
        self.setGeometry(100, 100, 500, 700)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter a new task")
        self.task_input.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add Task", self)
        self.add_button.setFont(QFont("Arial", 14))
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)

        self.task_list = QListWidget(self)
        self.task_list.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.task_list)

        self.update_button = QPushButton("Update Task", self)
        self.update_button.setFont(QFont("Arial", 14))
        self.update_button.clicked.connect(self.update_task)
        self.layout.addWidget(self.update_button)

        self.remove_button = QPushButton("Remove Task", self)
        self.remove_button.setFont(QFont("Arial", 14))
        self.remove_button.clicked.connect(self.remove_task)
        self.layout.addWidget(self.remove_button)

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty.")

    def update_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            new_task = self.task_input.text().strip()
            if new_task:
                selected_item.setText(new_task)
                self.task_input.clear()
                self.task_list.clearSelection()
                QMessageBox.information(self, "Success", "Task updated successfully.")
            else:
                QMessageBox.warning(self, "Warning", "Task cannot be empty.")
        else:
            QMessageBox.warning(self, "Warning", "Select a task to update.")

    def remove_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task = selected_item.text()
            if task in self.tasks:  # Check if the task exists in the list
                self.tasks.remove(task)
                self.update_task_list()
                self.task_input.clear()
            else:
                QMessageBox.warning(self, "Warning", "Task not found.")
        else:
            QMessageBox.warning(self, "Warning", "Select a task to remove.")

    def update_task_list(self):
        self.task_list.clear()
        self.task_list.addItems(self.tasks)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
