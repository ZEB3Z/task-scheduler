"""Task list widget."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLineEdit, QPushButton, QCheckBox, QLabel, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QColor

from ..models.task import Task
from ..models.subject import Subject
from .theme import Theme


class TaskList(QWidget):
    """Widget for displaying and managing tasks."""
    
    task_changed = Signal()  # Emits when tasks are modified
    
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.filter_subject_id = None
        self.filter_type = None  # "today", "completed", etc.
        self.search_query = ""
        self.setup_ui()
        self.load_tasks()
    
    def setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search tasks...")
        self.search_edit.setStyleSheet(Theme.LINE_EDIT)
        self.search_edit.textChanged.connect(self.on_search_changed)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)
        
        # Add task input
        add_task_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Add a new task...")
        self.task_input.setStyleSheet(Theme.LINE_EDIT)
        self.task_input.returnPressed.connect(self.add_task)
        add_task_layout.addWidget(self.task_input)
        
        self.add_btn = QPushButton("Add")
        self.add_btn.setStyleSheet(Theme.BUTTON_PRIMARY)
        self.add_btn.clicked.connect(self.add_task)
        add_task_layout.addWidget(self.add_btn)
        layout.addLayout(add_task_layout)
        
        # Task list
        self.task_list = QListWidget()
        self.task_list.setStyleSheet(Theme.LIST_WIDGET + Theme.SCROLLBAR)
        self.task_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.task_list)
        
        # Status label
        self.status_label = QLabel("0 tasks")
        self.status_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY.name()}; font-size: 12px;")
        layout.addWidget(self.status_label)
    
    def load_tasks(self, filter_subject_id=None, filter_type=None):
        """Load and display tasks.
        
        Args:
            filter_subject_id: Subject ID to filter by (sets filter_subject_id, clears filter_type)
            filter_type: Filter type like "today" or "completed" (sets filter_type, clears filter_subject_id)
        """
        # Update current filters if explicitly provided
        if filter_subject_id is not None:
            self.filter_subject_id = filter_subject_id
            self.filter_type = None
        elif filter_type is not None:
            self.filter_type = filter_type
            self.filter_subject_id = None
        
        tasks = self.data_manager.load_tasks()
        subjects = {s.id: s for s in self.data_manager.load_subjects(include_archived=True)}
        
        # Filter tasks using current filters
        if self.filter_subject_id is not None:
            tasks = [t for t in tasks if t.subject_id == self.filter_subject_id]
        elif self.filter_type == "completed":
            tasks = [t for t in tasks if t.completed]
        elif self.filter_type == "today":
            # Simple "today" logic: tasks not completed
            tasks = [t for t in tasks if not t.completed]
        
        # Apply search
        if self.search_query:
            query_lower = self.search_query.lower()
            tasks = [t for t in tasks if query_lower in t.title.lower()]
        
        self.task_list.clear()
        
        for task in tasks:
            self.add_task_item(task, subjects.get(task.subject_id))
        
        self.update_status(len(tasks))
    
    def add_task_item(self, task: Task, subject: Subject = None):
        """Add a task item to the list."""
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(8, 4, 8, 4)
        item_layout.setSpacing(12)
        
        # Checkbox
        checkbox = QCheckBox()
        checkbox.setChecked(task.completed)
        checkbox.stateChanged.connect(
            lambda state, t=task: self.toggle_task(t.id, state == Qt.Checked)
        )
        item_layout.addWidget(checkbox)
        
        # Task title
        title_label = QLabel(task.title)
        title_label.setWordWrap(True)
        
        # Strike through if completed
        if task.completed:
            font = title_label.font()
            font.setStrikeOut(True)
            title_label.setFont(font)
            title_label.setStyleSheet(f"color: {Theme.TEXT_TERTIARY.name()};")
        else:
            title_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY.name()};")
        
        item_layout.addWidget(title_label, 1)
        
        # Subject color indicator
        if subject:
            color_label = QLabel("●")
            color_label.setStyleSheet(f"color: {subject.color}; font-size: 16px;")
            color_label.setToolTip(subject.name)
            item_layout.addWidget(color_label)
        
        list_item = QListWidgetItem()
        list_item.setData(Qt.UserRole, task.id)
        list_item.setSizeHint(item_widget.sizeHint())
        
        self.task_list.addItem(list_item)
        self.task_list.setItemWidget(list_item, item_widget)
    
    def add_task(self):
        """Add a new task."""
        title = self.task_input.text().strip()
        if not title:
            return
        
        task = Task(
            id=self.data_manager.generate_id(),
            title=title,
            completed=False,
            subject_id=self.filter_subject_id
        )
        
        self.data_manager.add_task(task)
        self.task_input.clear()
        self.load_tasks()
        self.task_changed.emit()
    
    def toggle_task(self, task_id: str, completed: bool):
        """Toggle task completion."""
        self.data_manager.update_task(task_id, completed=completed)
        self.load_tasks()
        self.task_changed.emit()
    
    def on_search_changed(self, text: str):
        """Handle search query change."""
        self.search_query = text
        self.load_tasks()
    
    def show_context_menu(self, position):
        """Show context menu for task item."""
        item = self.task_list.itemAt(position)
        if not item:
            return
        
        task_id = item.data(Qt.UserRole)
        tasks = self.data_manager.load_tasks()
        task = next((t for t in tasks if t.id == task_id), None)
        if not task:
            return
        
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(self.task_list.mapToGlobal(position))
        
        if action == delete_action:
            self.delete_task(task)
    
    def delete_task(self, task: Task):
        """Delete task with confirmation."""
        reply = QMessageBox.question(
            self, "Delete Task",
            f"Delete '{task.title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.data_manager.delete_task(task.id)
            self.load_tasks()
            self.task_changed.emit()
    
    def update_status(self, count: int):
        """Update status label."""
        self.status_label.setText(f"{count} task{'s' if count != 1 else ''}")
    
    def refresh(self):
        """Refresh the task list."""
        self.load_tasks()
