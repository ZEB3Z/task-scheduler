"""Task model for the To-Do application."""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Task:
    """Represents a single task in the application."""
    id: str
    title: str
    completed: bool
    subject_id: Optional[str]
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON storage."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create task from dictionary."""
        return cls(
            id=data['id'],
            title=data['title'],
            completed=data['completed'],
            subject_id=data.get('subject_id')
        )
