"""Data persistence manager using JSON files."""
import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict
import uuid

from ..models.task import Task
from ..models.subject import Subject


def get_app_dir() -> Path:
    """Get the application directory (works for both dev and PyInstaller bundle)."""
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent.parent.parent


class DataManager:
    """Manages local file-based data storage."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize data manager.
        
        Args:
            data_dir: Directory to store data files. If None, uses directory next to executable.
        """
        if data_dir is None:
            # Use local data directory (portable, next to executable)
            self.data_dir = get_app_dir() / "data"
        else:
            self.data_dir = Path(data_dir)
        
        self.data_dir.mkdir(exist_ok=True)
        self.tasks_file = self.data_dir / "tasks.json"
        self.subjects_file = self.data_dir / "subjects.json"
        
        # Initialize files if they don't exist
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create JSON files if they don't exist."""
        if not self.tasks_file.exists():
            self._write_json(self.tasks_file, [])
        if not self.subjects_file.exists():
            self._write_json(self.subjects_file, [])
    
    def _read_json(self, file_path: Path) -> list:
        """Read JSON file and return list."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_json(self, file_path: Path, data: list):
        """Write list to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Task operations
    def load_tasks(self) -> List[Task]:
        """Load all tasks from storage."""
        data = self._read_json(self.tasks_file)
        return [Task.from_dict(item) for item in data]
    
    def save_tasks(self, tasks: List[Task]):
        """Save all tasks to storage."""
        data = [task.to_dict() for task in tasks]
        self._write_json(self.tasks_file, data)
    
    def add_task(self, task: Task) -> Task:
        """Add a new task."""
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)
        return task
    
    def update_task(self, task_id: str, **updates) -> Optional[Task]:
        """Update a task by ID."""
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                self.save_tasks(tasks)
                return task
        return None
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID."""
        tasks = self.load_tasks()
        tasks = [t for t in tasks if t.id != task_id]
        self.save_tasks(tasks)
        return len(tasks) < len(self.load_tasks())
    
    # Subject operations
    def load_subjects(self, include_archived: bool = False) -> List[Subject]:
        """Load subjects from storage.
        
        Args:
            include_archived: If True, include archived subjects.
        """
        data = self._read_json(self.subjects_file)
        subjects = [Subject.from_dict(item) for item in data]
        if not include_archived:
            subjects = [s for s in subjects if not s.archived]
        return sorted(subjects, key=lambda s: s.order)
    
    def save_subjects(self, subjects: List[Subject]):
        """Save all subjects to storage."""
        data = [subject.to_dict() for subject in subjects]
        self._write_json(self.subjects_file, data)
    
    def add_subject(self, subject: Subject) -> Subject:
        """Add a new subject."""
        subjects = self.load_subjects(include_archived=True)
        subjects.append(subject)
        self.save_subjects(subjects)
        return subject
    
    def update_subject(self, subject_id: str, **updates) -> Optional[Subject]:
        """Update a subject by ID."""
        subjects = self.load_subjects(include_archived=True)
        for i, subject in enumerate(subjects):
            if subject.id == subject_id:
                for key, value in updates.items():
                    if hasattr(subject, key):
                        setattr(subject, key, value)
                self.save_subjects(subjects)
                return subject
        return None
    
    def delete_subject(self, subject_id: str):
        """Delete a subject by ID and reassign its tasks."""
        subjects = self.load_subjects(include_archived=True)
        subjects = [s for s in subjects if s.id != subject_id]
        self.save_subjects(subjects)
        
        # Reassign tasks from deleted subject to None
        tasks = self.load_tasks()
        for task in tasks:
            if task.subject_id == subject_id:
                task.subject_id = None
        self.save_tasks(tasks)
    
    def archive_subject(self, subject_id: str, archived: bool = True):
        """Archive or unarchive a subject."""
        self.update_subject(subject_id, archived=archived)
    
    def reorder_subjects(self, subject_ids: List[str]):
        """Reorder subjects based on provided ID list."""
        subjects = self.load_subjects(include_archived=True)
        subject_dict = {s.id: s for s in subjects}
        
        # Update order based on new order
        for order, subject_id in enumerate(subject_ids):
            if subject_id in subject_dict:
                subject_dict[subject_id].order = order
        
        self.save_subjects(list(subject_dict.values()))
    
    @staticmethod
    def generate_id() -> str:
        """Generate a unique ID."""
        return str(uuid.uuid4())
