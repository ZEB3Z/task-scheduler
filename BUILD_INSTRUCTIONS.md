# Build Instructions for Task Scheduler

This document provides exact, step-by-step instructions to build the Windows executable.

## Prerequisites

1. **Python 3.8 or higher** installed on your Windows machine
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Command Prompt or PowerShell** (Windows built-in)

## Step-by-Step Build Process

### Step 1: Open Command Prompt

- Press `Win + R`, type `cmd`, and press Enter
- Or search for "Command Prompt" in the Start menu

### Step 2: Navigate to Project Directory

```cmd
cd path\to\task_scheduler
```

Replace `path\to\task_scheduler` with the actual path to your project directory.

For example:
- `cd C:\Projects\task_scheduler`
- `cd D:\MyApps\task_scheduler`
- Or wherever you've placed the project folder

### Step 3: Install Dependencies

```cmd
pip install -r requirements.txt
pip install pyinstaller
```

This installs:
- PySide6 (Qt for Python)
- PyInstaller (for building the executable)

### Step 4: Build the Executable

**Option A: Using the build script (Recommended)**

```cmd
python build_exe.py
```

**Option B: Manual build command**

```cmd
pyinstaller --name TaskScheduler --onefile --windowed --clean src/main.py
```

### Step 5: Locate the Executable

After the build completes:

1. Open Windows File Explorer
2. Navigate to the `dist` folder in your project directory
3. You will find `TaskScheduler.exe` in that folder

### Step 6: Test the Executable

1. Double-click `TaskScheduler.exe` to run it
2. The application should launch
3. A `data` folder will be created next to the executable on first run

### Step 7: Distribution (Optional)

To distribute the application:

1. Copy `TaskScheduler.exe` from the `dist` folder
2. You can place it anywhere on the target Windows machine
3. Double-click to run - no installation required
4. The `data` folder will be created automatically next to the executable

## Troubleshooting

### Issue: "python is not recognized"

**Solution**: Python is not in your PATH. Reinstall Python and make sure to check "Add Python to PATH".

### Issue: "pip is not recognized"

**Solution**: Python was installed without pip. Install Python again and ensure pip is included.

### Issue: Build fails with import errors

**Solution**: Make sure all dependencies are installed:
```cmd
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

### Issue: Executable is large (>100MB)

**Solution**: This is normal. PyInstaller bundles Python, Qt, and all dependencies into a single executable. The first run may be slightly slower as files are extracted.

### Issue: Antivirus flags the executable

**Solution**: This is a false positive common with PyInstaller executables. You may need to:
- Add an exception in your antivirus
- Sign the executable (requires code signing certificate)
- Distribute the source code instead

## Build Configuration Details

The build uses these PyInstaller options:

- `--onefile`: Creates a single executable file
- `--windowed`: No console window (GUI only)
- `--clean`: Cleans cache before building
- `--name TaskScheduler`: Sets the executable name

## Alternative: Development Mode

If you prefer to run from source instead of building:

```cmd
python src/main.py
```

This requires Python and PySide6 to be installed, but doesn't create an executable.

## Verification Checklist

After building, verify:

- [ ] `TaskScheduler.exe` exists in the `dist` folder
- [ ] Executable runs when double-clicked
- [ ] Application window opens
- [ ] Tasks can be added and saved
- [ ] Data persists after closing and reopening
- [ ] `data` folder is created next to the executable

## Next Steps

Once built, you can:
- Test the executable on your machine
- Copy it to other Windows machines
- Create a shortcut on your desktop
- Share it with others (single file distribution)
