"""Subject/Category model for the To-Do application."""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Subject:
    """Represents a subject/category in the application."""
    id: str
    name: str
    color: str  # Hex color code
    archived: bool
    order: int  # For reordering
    
    def to_dict(self) -> dict:
        """Convert subject to dictionary for JSON storage."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Subject':
        """Create subject from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            color=data['color'],
            archived=data.get('archived', False),
            order=data.get('order', 0)
        )
