import sys
import json
import os
from PyQt5.QtWidgets import (QApplication,QWidget,QLineEdit,QPushButton,QListWidget,
                             QListWidgetItem,QVBoxLayout,QHBoxLayout)
from PyQt5.QtCore import Qt

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = "tasks.json"
        self.initUI()

    def initUI(self):
        self.setWindowTitle("To-Do-List")
        self.setGeometry(500,100,500,500)

        self.input_task = QLineEdit(self)
        self.input_task.setPlaceholderText("Enter Task")

        self.add_button = QPushButton("Add Task",self)
        self.add_button.clicked.connect(self.add_task)

        self.delete_button = QPushButton("Delete Task",self)
        self.delete_button.clicked.connect(self.delete_task)

        self.complete_button = QPushButton("Complete Task",self)
        self.complete_button.clicked.connect(self.complete_task)

        self.clear_button = QPushButton("Clear Task",self)
        self.clear_button.clicked.connect(self.clear_task)

        self.edit_button = QPushButton("Edit Task",self)
        self.edit_button.clicked.connect(self.edit_task)


        self.save_button = QPushButton("Save Task",self)
        self.save_button.clicked.connect(self.save_task)

        self.task_list = QListWidget(self)
        self.load_tasks()
        self.task_list.itemChanged.connect(self.save_tasks)

        vbox = QVBoxLayout()

        vbox.addWidget(self.input_task)
        vbox.addWidget(self.task_list)

        hbox = QHBoxLayout()

        hbox.addWidget(self.add_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.complete_button)
        hbox.addWidget(self.clear_button)
        hbox.addWidget(self.edit_button)
        hbox.addWidget(self.save_button)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def add_task(self):
        task = self.input_task.text()

        if task:
            item = QListWidgetItem(task)
            item.setCheckState(Qt.Unchecked)
            self.task_list.addItem(item)
            self.input_task.clear()
            self.save_tasks()

    def delete_task(self):
        current_row = self.task_list.currentRow()

        if current_row >= 0:
            self.task_list.takeItem(current_row)
            self.save_tasks()

    def complete_task(self):
        current_row = self.task_list.currentRow()

        if current_row >= 0:
            item = self.task_list.item(current_row)
            if item.checkState() == Qt.Unchecked:
                item.setCheckState(Qt.Checked)
                self.save_tasks()

    def clear_task(self):
        self.task_list.clear()
        self.save_tasks()

    def edit_task(self):
        current_row = self.task_list.currentRow()

        if current_row >= 0:
            item = self.task_list.item(current_row)
            self.input_task.setText(item.text())

    def save_task(self):
        current_row = self.task_list.currentRow()

        if current_row >= 0:
            new_task = self.input_task.text()

            if new_task:
                self.task_list.item(current_row).setText(new_task)
                self.input_task.clear()
                self.save_tasks()


    def save_tasks(self):
        tasks = []
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            checked = item.checkState() == Qt.Checked
            tasks.append({"text":item.text(),"checked":checked})

        with open(self.filename, "w") as file:
            json.dump(tasks,file)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                tasks = json.load(file)

            for task in tasks:
                item = QListWidgetItem(task["text"])
                item.setCheckState(Qt.Checked if task ["checked"] else Qt.Unchecked)
                self.task_list.addItem(item)











if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoList()
    window.show()
    sys.exit(app.exec_())














