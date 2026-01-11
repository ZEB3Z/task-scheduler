# Task Scheduler

A modern, offline Windows desktop To-Do application built with Python and PySide6 (Qt for Python).

## Features

- **Fully Offline**: No internet connection required
- **Local Storage**: All data stored in JSON files
- **Dark Theme**: Modern, minimal dark interface
- **Task Management**: Create, complete, and delete tasks
- **Subject Categories**: Color-coded, reorderable categories
- **Multiple Views**: All Tasks, Today, Completed, By Subject
- **Search**: Quick search across all tasks
- **Drag & Drop**: Reorder subjects by dragging
- **Keyboard Friendly**: Minimal interaction required

## Technology Stack

- **Python 3.8+**
- **PySide6**: Qt for Python (native UI framework)
- **PyInstaller**: Packaging into single executable

## Installation & Setup

### Option 1: Run from Source (Development)

1. **Install Python 3.8 or higher** if not already installed

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python src/main.py
   ```

### Option 2: Build Executable (Distribution)

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```bash
   python build_exe.py
   ```

   Or manually:
   ```bash
   pyinstaller --name TaskScheduler --onefile --windowed --clean src/main.py
   ```

3. **Find the executable**:
   - The `TaskScheduler.exe` file will be in the `dist` folder
   - Double-click to run

## Data Storage

All data is stored locally in JSON format in the `data` directory:

- `data/tasks.json`: All tasks
- `data/subjects.json`: All subjects/categories

The data directory is created automatically on first run in the same directory as the executable.

## Usage

### Adding Tasks

1. Type a task title in the input field
2. Click "Add" or press Enter
3. Tasks are assigned to the currently selected subject/view

### Managing Subjects

1. Click "+ Add Subject" to create a new category
2. Choose a color for the subject
3. Right-click a subject for options:
   - **Edit**: Change the name
   - **Archive**: Hide the subject (tasks remain)
   - **Delete**: Remove the subject (tasks become unassigned)
   - **Change Color**: Update the color
4. Drag subjects to reorder them

### Views

- **All Tasks**: Shows all tasks (default)
- **Today**: Shows incomplete tasks
- **Completed**: Shows completed tasks
- **By Subject**: Click a subject to filter tasks

### Search

Type in the search box to filter tasks by title.

## Keyboard Shortcuts

- **Enter**: Add task (when input focused)
- **Click**: Select/view tasks
- **Right-click**: Context menu for tasks/subjects

## Building for Distribution

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build (using script)
python build_exe.py

# Or manually
pyinstaller --name TaskScheduler --onefile --windowed --clean src/main.py
```

The executable will be in the `dist` folder. You can distribute this single `.exe` file.

**Note**: On first run, the executable will extract files to a temporary directory. The `data` folder will be created next to the executable for portable use.

## Requirements

- Windows 7 or higher
- No additional runtime dependencies (all bundled in executable)

## License

This is a standalone application for personal use.
