"""Subject panel widget with drag-and-drop reordering."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QMenu, QInputDialog, QMessageBox, QColorDialog
)
from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QColor, QDragEnterEvent, QDropEvent

from ..models.subject import Subject
from .theme import Theme


class SubjectPanel(QWidget):
    """Panel for managing subjects with drag-and-drop reordering."""
    
    subject_selected = Signal(str)  # Emits subject_id
    subject_changed = Signal()  # Emits when subjects are modified
    
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()
        self.load_subjects()
    
    def setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header
        header_layout = QHBoxLayout()
        self.add_subject_btn = QPushButton("+ Add Subject")
        self.add_subject_btn.setStyleSheet(Theme.BUTTON_PRIMARY)
        self.add_subject_btn.clicked.connect(self.add_subject)
        header_layout.addWidget(self.add_subject_btn)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Subject list
        self.subject_list = QListWidget()
        self.subject_list.setStyleSheet(Theme.LIST_WIDGET + Theme.SCROLLBAR)
        self.subject_list.setDragDropMode(QListWidget.InternalMove)
        self.subject_list.itemClicked.connect(self.on_item_clicked)
        self.subject_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.subject_list.customContextMenuRequested.connect(self.show_context_menu)
        self.subject_list.model().rowsMoved.connect(self.on_reordered)
        layout.addWidget(self.subject_list)
        
        # "All Tasks" item (always first)
        all_item = QListWidgetItem("All Tasks")
        all_item.setData(Qt.UserRole, None)
        all_item.setFlags(all_item.flags() & ~Qt.ItemIsDragEnabled & ~Qt.ItemIsDropEnabled)
        font = all_item.font()
        font.setBold(True)
        all_item.setFont(font)
        self.subject_list.addItem(all_item)
    
    def load_subjects(self):
        """Load subjects from storage."""
        subjects = self.data_manager.load_subjects(include_archived=False)
        
        # Clear existing subjects (keep "All Tasks")
        while self.subject_list.count() > 1:
            item = self.subject_list.item(1)
            self.subject_list.takeItem(1)
        
        # Add subjects
        for subject in subjects:
            self.add_subject_item(subject)
    
    def add_subject_item(self, subject: Subject):
        """Add a subject item to the list."""
        item = QListWidgetItem(subject.name)
        item.setData(Qt.UserRole, subject.id)
        
        # Color indicator
        color = QColor(subject.color)
        item.setForeground(color)
        
        self.subject_list.addItem(item)
    
    def add_subject(self):
        """Show dialog to add a new subject."""
        name, ok = QInputDialog.getText(
            self, "Add Subject", "Subject name:",
            text=""
        )
        if not ok or not name.strip():
            return
        
        # Choose color
        color = QColorDialog.getColor(QColor(Theme.ACCENT), self, "Choose Color")
        if not color.isValid():
            return
        
        # Create subject
        subjects = self.data_manager.load_subjects(include_archived=True)
        max_order = max([s.order for s in subjects], default=-1)
        
        subject = Subject(
            id=self.data_manager.generate_id(),
            name=name.strip(),
            color=color.name(),
            archived=False,
            order=max_order + 1
        )
        
        self.data_manager.add_subject(subject)
        self.add_subject_item(subject)
        self.subject_changed.emit()
    
    def on_item_clicked(self, item: QListWidgetItem):
        """Handle subject item click."""
        subject_id = item.data(Qt.UserRole)
        self.subject_selected.emit(subject_id)
    
    def on_reordered(self, parent, start, end, destination, row):
        """Handle subject reordering."""
        # Get current order of subject IDs
        subject_ids = []
        for i in range(1, self.subject_list.count()):  # Skip "All Tasks"
            item = self.subject_list.item(i)
            subject_id = item.data(Qt.UserRole)
            if subject_id:
                subject_ids.append(subject_id)
        
        self.data_manager.reorder_subjects(subject_ids)
        self.subject_changed.emit()
    
    def show_context_menu(self, position):
        """Show context menu for subject item."""
        item = self.subject_list.itemAt(position)
        if not item or item.data(Qt.UserRole) is None:  # Skip "All Tasks"
            return
        
        menu = QMenu(self)
        
        edit_action = menu.addAction("Edit")
        archive_action = menu.addAction("Archive")
        delete_action = menu.addAction("Delete")
        menu.addSeparator()
        color_action = menu.addAction("Change Color")
        
        action = menu.exec_(self.subject_list.mapToGlobal(position))
        
        if action == edit_action:
            self.edit_subject(item)
        elif action == archive_action:
            self.archive_subject(item)
        elif action == delete_action:
            self.delete_subject(item)
        elif action == color_action:
            self.change_color(item)
    
    def edit_subject(self, item: QListWidgetItem):
        """Edit subject name."""
        subject_id = item.data(Qt.UserRole)
        subjects = self.data_manager.load_subjects(include_archived=True)
        subject = next((s for s in subjects if s.id == subject_id), None)
        if not subject:
            return
        
        name, ok = QInputDialog.getText(
            self, "Edit Subject", "Subject name:",
            text=subject.name
        )
        if ok and name.strip():
            self.data_manager.update_subject(subject_id, name=name.strip())
            item.setText(name.strip())
            self.subject_changed.emit()
    
    def archive_subject(self, item: QListWidgetItem):
        """Archive subject."""
        subject_id = item.data(Qt.UserRole)
        self.data_manager.archive_subject(subject_id, archived=True)
        self.load_subjects()  # Reload to remove archived
        self.subject_changed.emit()
    
    def delete_subject(self, item: QListWidgetItem):
        """Delete subject with confirmation."""
        subject_id = item.data(Qt.UserRole)
        subjects = self.data_manager.load_subjects(include_archived=True)
        subject = next((s for s in subjects if s.id == subject_id), None)
        if not subject:
            return
        
        reply = QMessageBox.question(
            self, "Delete Subject",
            f"Delete '{subject.name}'? Tasks will be unassigned.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.data_manager.delete_subject(subject_id)
            self.load_subjects()
            self.subject_changed.emit()
    
    def change_color(self, item: QListWidgetItem):
        """Change subject color."""
        subject_id = item.data(Qt.UserRole)
        subjects = self.data_manager.load_subjects(include_archived=True)
        subject = next((s for s in subjects if s.id == subject_id), None)
        if not subject:
            return
        
        color = QColorDialog.getColor(
            QColor(subject.color), self, "Choose Color"
        )
        if color.isValid():
            self.data_manager.update_subject(subject_id, color=color.name())
            item.setForeground(color)
            self.subject_changed.emit()
    
    def refresh(self):
        """Refresh the subject list."""
        self.load_subjects()
