# Project Structure

## Overview

```
task_scheduler/
├── src/                          # Source code
│   ├── main.py                   # Application entry point
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   ├── task.py               # Task model (id, title, completed, subject_id)
│   │   └── subject.py            # Subject model (id, name, color, archived, order)
│   ├── storage/                  # Data persistence
│   │   ├── __init__.py
│   │   └── data_manager.py       # JSON file-based storage manager
│   └── ui/                       # User interface
│       ├── __init__.py
│       ├── main_window.py        # Main application window
│       ├── task_list.py          # Task list widget
│       ├── subject_panel.py      # Subject panel with drag-and-drop
│       └── theme.py              # Dark theme styling
├── data/                         # Data directory (created at runtime)
│   ├── tasks.json               # Task storage (created automatically)
│   └── subjects.json            # Subject storage (created automatically)
├── build_exe.py                  # PyInstaller build script
├── requirements.txt              # Python dependencies
├── README.md                     # User documentation
├── BUILD_INSTRUCTIONS.md         # Build instructions
└── PROJECT_STRUCTURE.md          # This file
```

## Key Components

### Models (`src/models/`)

- **Task**: Represents a task with id, title, completed status, and subject_id
- **Subject**: Represents a category with id, name, color, archived status, and order

### Storage (`src/storage/`)

- **DataManager**: Handles all file I/O operations
  - Uses JSON format for human-readable storage
  - Stores data in `data/` directory next to executable
  - Works in both development and bundled executable modes

### UI (`src/ui/`)

- **MainWindow**: Main application window with splitter layout
- **TaskList**: Widget for displaying and managing tasks
  - Supports filtering, search, and task operations
- **SubjectPanel**: Widget for managing subjects
  - Drag-and-drop reordering
  - Context menu for edit/archive/delete/color
- **Theme**: Dark theme color palette and stylesheets

## Data Storage Format

### tasks.json

```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "completed": false,
    "subject_id": "subject-uuid-or-null"
  }
]
```

### subjects.json

```json
[
  {
    "id": "uuid-string",
    "name": "Subject Name",
    "color": "#RRGGBB",
    "archived": false,
    "order": 0
  }
]
```

## Architecture Notes

- **Offline-first**: All data stored locally in JSON files
- **Portable**: Data directory created next to executable
- **Modular**: Clear separation of models, storage, and UI
- **No database**: Simple file-based storage
- **No network**: Fully offline operation
