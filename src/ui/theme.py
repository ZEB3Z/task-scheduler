"""Dark theme styling for the application."""
from PySide6.QtGui import QColor


class Theme:
    """Dark theme color palette and styles."""
    
    # Color palette
    BACKGROUND_PRIMARY = QColor(22, 22, 24)
    BACKGROUND_SECONDARY = QColor(30, 30, 32)
    BACKGROUND_TERTIARY = QColor(38, 38, 40)
    BACKGROUND_HOVER = QColor(45, 45, 47)
    
    TEXT_PRIMARY = QColor(255, 255, 255)
    TEXT_SECONDARY = QColor(180, 180, 180)
    TEXT_TERTIARY = QColor(120, 120, 120)
    
    ACCENT = QColor(96, 165, 250)
    ACCENT_HOVER = QColor(120, 180, 255)
    
    BORDER = QColor(50, 50, 52)
    
    SUCCESS = QColor(34, 197, 94)
    DANGER = QColor(239, 68, 68)
    
    # Stylesheets
    MAIN_WINDOW = f"""
        QMainWindow {{
            background-color: {BACKGROUND_PRIMARY.name()};
        }}
    """
    
    BUTTON_PRIMARY = f"""
        QPushButton {{
            background-color: {ACCENT.name()};
            color: {TEXT_PRIMARY.name()};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {ACCENT_HOVER.name()};
        }}
        QPushButton:pressed {{
            background-color: {ACCENT.name()};
            opacity: 0.9;
        }}
    """
    
    BUTTON_SECONDARY = f"""
        QPushButton {{
            background-color: {BACKGROUND_TERTIARY.name()};
            color: {TEXT_PRIMARY.name()};
            border: 1px solid {BORDER.name()};
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {BACKGROUND_HOVER.name()};
        }}
    """
    
    LINE_EDIT = f"""
        QLineEdit {{
            background-color: {BACKGROUND_SECONDARY.name()};
            color: {TEXT_PRIMARY.name()};
            border: 1px solid {BORDER.name()};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }}
        QLineEdit:focus {{
            border: 1px solid {ACCENT.name()};
        }}
    """
    
    LIST_WIDGET = f"""
        QListWidget {{
            background-color: {BACKGROUND_SECONDARY.name()};
            color: {TEXT_PRIMARY.name()};
            border: none;
            outline: none;
        }}
        QListWidget::item {{
            background-color: {BACKGROUND_SECONDARY.name()};
            padding: 8px;
            border-bottom: 1px solid {BORDER.name()};
        }}
        QListWidget::item:hover {{
            background-color: {BACKGROUND_HOVER.name()};
        }}
        QListWidget::item:selected {{
            background-color: {BACKGROUND_TERTIARY.name()};
        }}
    """
    
    SCROLLBAR = f"""
        QScrollBar:vertical {{
            background: {BACKGROUND_PRIMARY.name()};
            width: 10px;
            border: none;
        }}
        QScrollBar::handle:vertical {{
            background: {BACKGROUND_TERTIARY.name()};
            border-radius: 5px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {BACKGROUND_HOVER.name()};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar:horizontal {{
            background: {BACKGROUND_PRIMARY.name()};
            height: 10px;
            border: none;
        }}
        QScrollBar::handle:horizontal {{
            background: {BACKGROUND_TERTIARY.name()};
            border-radius: 5px;
            min-width: 20px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {BACKGROUND_HOVER.name()};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
    """
