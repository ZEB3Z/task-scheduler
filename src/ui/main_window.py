"""Main application window."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QPushButton, QFrame, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ..storage.data_manager import DataManager
from .subject_panel import SubjectPanel
from .task_list import TaskList
from .theme import Theme


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Set up the UI layout."""
        self.setWindowTitle("Task Scheduler")
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(800, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel: Subjects
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_panel.setFixedWidth(250)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # View buttons
        view_frame = QFrame()
        view_frame.setStyleSheet(f"background-color: {Theme.BACKGROUND_TERTIARY.name()};")
        view_layout = QVBoxLayout(view_frame)
        view_layout.setContentsMargins(8, 8, 8, 8)
        view_layout.setSpacing(4)
        
        self.all_tasks_btn = QPushButton("All Tasks")
        self.all_tasks_btn.setCheckable(True)
        self.all_tasks_btn.setChecked(True)
        self.all_tasks_btn.clicked.connect(lambda: self.switch_view(None))
        
        self.today_btn = QPushButton("Today")
        self.today_btn.setCheckable(True)
        self.today_btn.clicked.connect(lambda: self.switch_view("today"))
        
        self.completed_btn = QPushButton("Completed")
        self.completed_btn.setCheckable(True)
        self.completed_btn.clicked.connect(lambda: self.switch_view("completed"))
        
        for btn in [self.all_tasks_btn, self.today_btn, self.completed_btn]:
            btn.setStyleSheet(Theme.BUTTON_SECONDARY)
            view_layout.addWidget(btn)
        
        left_layout.addWidget(view_frame)
        
        # Subject panel
        self.subject_panel = SubjectPanel(self.data_manager)
        self.subject_panel.subject_selected.connect(self.on_subject_selected)
        self.subject_panel.subject_changed.connect(self.on_subject_changed)
        left_layout.addWidget(self.subject_panel)
        
        splitter.addWidget(left_panel)
        
        # Right panel: Tasks
        self.task_list = TaskList(self.data_manager)
        self.task_list.task_changed.connect(self.on_task_changed)
        splitter.addWidget(self.task_list)
        
        # Set splitter proportions
        splitter.setSizes([250, 950])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
    
    def apply_styles(self):
        """Apply dark theme styles."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Theme.BACKGROUND_PRIMARY.name()};
            }}
            QFrame {{
                background-color: {Theme.BACKGROUND_SECONDARY.name()};
                border: none;
            }}
            QPushButton:checked {{
                background-color: {Theme.ACCENT.name()};
                color: {Theme.TEXT_PRIMARY.name()};
            }}
        """)
    
    def switch_view(self, view_type):
        """Switch between different views."""
        # Uncheck all buttons
        self.all_tasks_btn.setChecked(view_type is None)
        self.today_btn.setChecked(view_type == "today")
        self.completed_btn.setChecked(view_type == "completed")
        
        # Load tasks with filter
        self.task_list.load_tasks(filter_type=view_type)
    
    def on_subject_selected(self, subject_id):
        """Handle subject selection."""
        # Uncheck view buttons
        self.all_tasks_btn.setChecked(False)
        self.today_btn.setChecked(False)
        self.completed_btn.setChecked(False)
        
        # Load tasks for selected subject
        self.task_list.load_tasks(filter_subject_id=subject_id)
    
    def on_subject_changed(self):
        """Handle subject changes."""
        self.task_list.refresh()
    
    def on_task_changed(self):
        """Handle task changes."""
        pass  # Can be used for notifications or updates
