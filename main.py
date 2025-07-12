import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSlider,
    QFileDialog, QMenu, QInputDialog, QLabel, QComboBox, QMessageBox,
    QGridLayout, QFrame, QHBoxLayout, QColorDialog, QTabWidget, QLineEdit
)
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent, QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QUrl, QSize, QTime # Import QTime for formatting

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices


# --- CONFIGURATION ---
APP_NAME = "Cyteboard"
# Determine the appropriate data directory based on the OS
if sys.platform.startswith('win'):
    DATA_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME)
elif sys.platform.startswith('darwin'):
    DATA_DIR = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', APP_NAME)
else:
    DATA_DIR = os.path.join(os.getenv('HOME'), '.local', 'share', APP_NAME)

DATA_FILE = os.path.join(DATA_DIR, "cyteboard_data.json")
MAX_SOUNDS = 100
BUTTONS_PER_ROW = 4
MAX_ROWS = MAX_SOUNDS // BUTTONS_PER_ROW
MIN_ROWS = 1
DEFAULT_ROWS = 4

# --- THEMES ---
THEMES = {
    "Cyber Green": {
        "bg_color": "#0d0d0d",
        "text_color": "#00ff7f",
        "button_bg_gradient_stop0": "#2a2a2a",
        "button_bg_gradient_stop1": "#1a1a1a",
        "button_border": "#00ff7f",
        "button_hover_bg": "#00ff7f",
        "button_hover_text": "#0d0d0d",
        "button_pressed_bg": "#00aa55",
        "broken_button_border": "#ff4747",
        "broken_button_text": "#ff4747",
        "broken_button_bg": "#4d1a1a",
        "broken_button_hover_bg": "#ff4747",
        "broken_button_hover_border": "#ff8a8a",
        "slider_groove_bg": "#2a2a2a",
        "slider_handle_bg": "#00ff7f",
        "slider_handle_border": "#0d0d0d",
        "combo_bg": "#1a1a1a",
        "combo_border": "#00ff7f",
        "menu_bg": "#1a1a1a",
        "menu_border": "#00ff7f",
        "separator_border": "#00ff7f",
        "input_bg": "#1a1a1a",
        "input_border": "#00ff7f",
    },
    "Blue Wave": {
        "bg_color": "#1a2a3a",
        "text_color": "#87ceeb",
        "button_bg_gradient_stop0": "#2c3e50",
        "button_bg_gradient_stop1": "#1a2a3a",
        "button_border": "#87ceeb",
        "button_hover_bg": "#87ceeb",
        "button_hover_text": "#1a2a3a",
        "button_pressed_bg": "#4682b4",
        "broken_button_border": "#ff6347",
        "broken_button_text": "#ff6347",
        "broken_button_bg": "#4a2c2c",
        "broken_button_hover_bg": "#ff6347",
        "broken_button_hover_border": "#ffa07a",
        "slider_groove_bg": "#2c3e50",
        "slider_handle_bg": "#87ceeb",
        "slider_handle_border": "#1a2a3a",
        "combo_bg": "#2c3e50",
        "combo_border": "#87ceeb",
        "menu_bg": "#2c3e50",
        "menu_border": "#87ceeb",
        "separator_border": "#87ceeb",
        "input_bg": "#2c3e50",
        "input_border": "#87ceeb",
    },
    "Crimson Night": {
        "bg_color": "#200a0a",
        "text_color": "#ff6347",
        "button_bg_gradient_stop0": "#3a1a1a",
        "button_bg_gradient_stop1": "#200a0a",
        "button_border": "#ff6347",
        "button_hover_bg": "#ff6347",
        "button_hover_text": "#200a0a",
        "button_pressed_bg": "#dc143c",
        "broken_button_border": "#ffd700",
        "broken_button_text": "#ffd700",
        "broken_button_bg": "#5a4d1a",
        "broken_button_hover_bg": "#ffd700",
        "broken_button_hover_border": "#fffacd",
        "slider_groove_bg": "#3a1a1a",
        "slider_handle_bg": "#ff6347",
        "slider_handle_border": "#200a0a",
        "combo_bg": "#3a1a1a",
        "combo_border": "#ff6347",
        "menu_bg": "#3a1a1a",
        "menu_border": "#ff6347",
        "separator_border": "#ff6347",
        "input_bg": "#3a1a1a",
        "input_border": "#ff6347",
    },
    "Forest Whisper": {
        "bg_color": "#1a2b20",
        "text_color": "#a2cd5a",
        "button_bg_gradient_stop0": "#2c4033",
        "button_bg_gradient_stop1": "#1a2b20",
        "button_border": "#a2cd5a",
        "button_hover_bg": "#a2cd5a",
        "button_hover_text": "#1a2b20",
        "button_pressed_bg": "#6b8e23",
        "broken_button_border": "#e3b330",
        "broken_button_text": "#e3b330",
        "broken_button_bg": "#4d401a",
        "broken_button_hover_bg": "#e3b330",
        "broken_button_hover_border": "#fbe798",
        "slider_groove_bg": "#2c4033",
        "slider_handle_bg": "#a2cd5a",
        "slider_handle_border": "#1a2b20",
        "combo_bg": "#2c4033",
        "combo_border": "#a2cd5a",
        "menu_bg": "#2c4033",
        "menu_border": "#a2cd5a",
        "separator_border": "#a2cd5a",
        "input_bg": "#2c4033",
        "input_border": "#a2cd5a",
    },
    "Purple Haze": {
        "bg_color": "#2a1a2b",
        "text_color": "#bf40bf",
        "button_bg_gradient_stop0": "#402c40",
        "button_bg_gradient_stop1": "#2a1a2b",
        "button_border": "#bf40bf",
        "button_hover_bg": "#bf40bf",
        "button_hover_text": "#2a1a2b",
        "button_pressed_bg": "#800080",
        "broken_button_border": "#ff8080",
        "broken_button_text": "#ff8080",
        "broken_button_bg": "#4a2c2c",
        "broken_button_hover_bg": "#ff8080",
        "broken_button_hover_border": "#ffc0c0",
        "slider_groove_bg": "#402c40",
        "slider_handle_bg": "#bf40bf",
        "slider_handle_border": "#2a1a2b",
        "combo_bg": "#402c40",
        "combo_border": "#bf40bf",
        "menu_bg": "#402c40",
        "menu_border": "#bf40bf",
        "separator_border": "#bf40bf",
        "input_bg": "#402c40",
        "input_border": "#bf40bf",
    },
    "Solar Flare": {
        "bg_color": "#3a2a1a",
        "text_color": "#ffaa00",
        "button_bg_gradient_stop0": "#50402c",
        "button_bg_gradient_stop1": "#3a2a1a",
        "button_border": "#ffaa00",
        "button_hover_bg": "#ffaa00",
        "button_hover_text": "#3a2a1a",
        "button_pressed_bg": "#cc8800",
        "broken_button_border": "#47b4ff",
        "broken_button_text": "#47b4ff",
        "broken_button_bg": "#1a3a4d",
        "broken_button_hover_bg": "#47b4ff",
        "broken_button_hover_border": "#87d6ff",
        "slider_groove_bg": "#50402c",
        "slider_handle_bg": "#ffaa00",
        "slider_handle_border": "#3a2a1a",
        "combo_bg": "#50402c",
        "combo_border": "#ffaa00",
        "menu_bg": "#50402c",
        "menu_border": "#ffaa00",
        "separator_border": "#ffaa00",
        "input_bg": "#50402c",
        "input_border": "#ffaa00",
    },
    "Ocean Depths": {
        "bg_color": "#0a1a20",
        "text_color": "#00bfff",
        "button_bg_gradient_stop0": "#1a2a30",
        "button_bg_gradient_stop1": "#0a1a20",
        "button_border": "#00bfff",
        "button_hover_bg": "#00bfff",
        "button_hover_text": "#0a1a20",
        "button_pressed_bg": "#0088cc",
        "broken_button_border": "#ff0000",
        "broken_button_text": "#ff0000",
        "broken_button_bg": "#4a1a1a",
        "broken_button_hover_bg": "#ff0000",
        "broken_button_hover_border": "#ff4d4d",
        "slider_groove_bg": "#1a2a30",
        "slider_handle_bg": "#00bfff",
        "slider_handle_border": "#0a1a20",
        "combo_bg": "#1a2a30",
        "combo_border": "#00bfff",
        "menu_bg": "#1a2a30",
        "menu_border": "#00bfff",
        "separator_border": "#00bfff",
        "input_bg": "#1a2a30",
        "input_border": "#00bfff",
    },
    "Rose Gold": {
        "bg_color": "#2a151a",
        "text_color": "#e0b0ff",
        "button_bg_gradient_stop0": "#3a202a",
        "button_bg_gradient_stop1": "#2a151a",
        "button_border": "#e0b0ff",
        "button_hover_bg": "#e0b0ff",
        "button_hover_text": "#2a151a",
        "button_pressed_bg": "#a050c0",
        "broken_button_border": "#ffd700",
        "broken_button_text": "#ffd700",
        "broken_button_bg": "#4d401a",
        "broken_button_hover_bg": "#ffd700",
        "broken_button_hover_border": "#fffacd",
        "slider_groove_bg": "#3a202a",
        "slider_handle_bg": "#e0b0ff",
        "slider_handle_border": "#2a151a",
        "combo_bg": "#3a202a",
        "combo_border": "#e0b0ff",
        "menu_bg": "#3a202a",
        "menu_border": "#e0b0ff",
        "separator_border": "#e0b0ff",
        "input_bg": "#3a202a",
        "input_border": "#e0b0ff",
    },
    "Emerald Glow": {
        "bg_color": "#152a1a",
        "text_color": "#00e080",
        "button_bg_gradient_stop0": "#253a2a",
        "button_bg_gradient_stop1": "#152a1a",
        "button_border": "#00e080",
        "button_hover_bg": "#00e080",
        "button_hover_text": "#152a1a",
        "button_pressed_bg": "#00a060",
        "broken_button_border": "#ff0000",
        "broken_button_text": "#ff0000",
        "broken_button_bg": "#4a1a1a",
        "broken_button_hover_bg": "#ff0000",
        "broken_button_hover_border": "#ff4d4d",
        "slider_groove_bg": "#253a2a",
        "slider_handle_bg": "#00e080",
        "slider_handle_border": "#152a1a",
        "combo_bg": "#253a2a",
        "combo_border": "#00e080",
        "menu_bg": "#253a2a",
        "menu_border": "#00e080",
        "separator_border": "#00e080",
        "input_bg": "#253a2a",
        "input_border": "#00e080",
    },
    "Golden Harvest": {
        "bg_color": "#2a2215",
        "text_color": "#ffa500",
        "button_bg_gradient_stop0": "#3a3020",
        "button_bg_gradient_stop1": "#2a2215",
        "button_border": "#ffa500",
        "button_hover_bg": "#ffa500",
        "button_hover_text": "#2a2215",
        "button_pressed_bg": "#cc8800",
        "broken_button_border": "#47b4ff",
        "broken_button_text": "#47b4ff",
        "broken_button_bg": "#1a3a4d",
        "broken_button_hover_bg": "#47b4ff",
        "broken_button_hover_border": "#87d6ff",
        "slider_groove_bg": "#3a3020",
        "slider_handle_bg": "#ffa500",
        "slider_handle_border": "#2a2215",
        "combo_bg": "#3a3020",
        "combo_border": "#ffa500",
        "menu_bg": "#3a3020",
        "menu_border": "#ffa500",
        "separator_border": "#ffa500",
        "input_bg": "#3a3020",
        "input_border": "#ffa500",
    },
    "Charcoal Grey": {
        "bg_color": "#202020",
        "text_color": "#cccccc",
        "button_bg_gradient_stop0": "#303030",
        "button_bg_gradient_stop1": "#202020",
        "button_border": "#999999",
        "button_hover_bg": "#666666",
        "button_hover_text": "#ffffff",
        "button_pressed_bg": "#404040",
        "broken_button_border": "#ff4747",
        "broken_button_text": "#ff4747",
        "broken_button_bg": "#4d1a1a",
        "broken_button_hover_bg": "#ff4747",
        "broken_button_hover_border": "#ff8a8a",
        "slider_groove_bg": "#303030",
        "slider_handle_bg": "#999999",
        "slider_handle_border": "#202020",
        "combo_bg": "#303030",
        "combo_border": "#999999",
        "menu_bg": "#303030",
        "menu_border": "#999999",
        "separator_border": "#999999",
        "input_bg": "#303030",
        "input_border": "#999999",
    },
    "Soft Peach": {
        "bg_color": "#ffe0b2",
        "text_color": "#8d6e63",
        "button_bg_gradient_stop0": "#ffcc80",
        "button_bg_gradient_stop1": "#ffe0b2",
        "button_border": "#bcaaa4",
        "button_hover_bg": "#bcaaa4",
        "button_hover_text": "#ffe0b2",
        "button_pressed_bg": "#a1887f",
        "broken_button_border": "#e57373",
        "broken_button_text": "#e57373",
        "broken_button_bg": "#f8bbd0",
        "broken_button_hover_bg": "#e57373",
        "broken_button_hover_border": "#ef9a9a",
        "slider_groove_bg": "#ffcc80",
        "slider_handle_bg": "#bcaaa4",
        "slider_handle_border": "#ffe0b2",
        "combo_bg": "#ffcc80",
        "combo_border": "#bcaaa4",
        "menu_bg": "#ffcc80",
        "menu_border": "#bcaaa4",
        "separator_border": "#bcaaa4",
        "input_bg": "#ffcc80",
        "input_border": "#bcaaa4",
    },
    "Deep Violet": {
        "bg_color": "#3f003f",
        "text_color": "#ffbfff",
        "button_bg_gradient_stop0": "#5a005a",
        "button_bg_gradient_stop1": "#3f003f",
        "button_border": "#ffbfff",
        "button_hover_bg": "#ffbfff",
        "button_hover_text": "#3f003f",
        "button_pressed_bg": "#800080",
        "broken_button_border": "#ffd700",
        "broken_button_text": "#ffd700",
        "broken_button_bg": "#4d401a",
        "broken_button_hover_bg": "#ffd700",
        "broken_button_hover_border": "#fffacd",
        "slider_groove_bg": "#5a005a",
        "slider_handle_bg": "#ffbfff",
        "slider_handle_border": "#3f003f",
        "combo_bg": "#5a005a",
        "combo_border": "#ffbfff",
        "menu_bg": "#5a005a",
        "menu_border": "#ffbfff",
        "separator_border": "#ffbfff",
        "input_bg": "#5a005a",
        "input_border": "#ffbfff",
    },
    "Muted Earth": {
        "bg_color": "#3d3b30",
        "text_color": "#c4a77d",
        "button_bg_gradient_stop0": "#524f42",
        "button_bg_gradient_stop1": "#3d3b30",
        "button_border": "#c4a77d",
        "button_hover_bg": "#c4a77d",
        "button_hover_text": "#3d3b30",
        "button_pressed_bg": "#967f5b",
        "broken_button_border": "#d32f2f",
        "broken_button_text": "#d32f2f",
        "broken_button_bg": "#5c2a2a",
        "broken_button_hover_bg": "#d32f2f",
        "broken_button_hover_border": "#ef5350",
        "slider_groove_bg": "#524f42",
        "slider_handle_bg": "#c4a77d",
        "slider_handle_border": "#3d3b30",
        "combo_bg": "#524f42",
        "combo_border": "#c4a77d",
        "menu_bg": "#524f42",
        "menu_border": "#c4a77d",
        "separator_border": "#c4a77d",
        "input_bg": "#524f42",
        "input_border": "#c4a77d",
    },
    "Skyline Blue": {
        "bg_color": "#1c2e4a",
        "text_color": "#82b1ff",
        "button_bg_gradient_stop0": "#2a426a",
        "button_bg_gradient_stop1": "#1c2e4a",
        "button_border": "#82b1ff",
        "button_hover_bg": "#82b1ff",
        "button_hover_text": "#1c2e4a",
        "button_pressed_bg": "#42a5f5",
        "broken_button_border": "#ffcc00",
        "broken_button_text": "#ffcc00",
        "broken_button_bg": "#4d401a",
        "broken_button_hover_bg": "#ffcc00",
        "broken_button_hover_border": "#fff176",
        "slider_groove_bg": "#2a426a",
        "slider_handle_bg": "#82b1ff",
        "slider_handle_border": "#1c2e4a",
        "combo_bg": "#2a426a",
        "combo_border": "#82b1ff",
        "menu_bg": "#2a426a",
        "menu_border": "#82b1ff",
        "separator_border": "#82b1ff",
        "input_bg": "#2a426a",
        "input_border": "#82b1ff",
    },
    "Sunset Orange": {
        "bg_color": "#4a2a1c",
        "text_color": "#ff8a65",
        "button_bg_gradient_stop0": "#6a402a",
        "button_bg_gradient_stop1": "#4a2a1c",
        "button_border": "#ff8a65",
        "button_hover_bg": "#ff8a65",
        "button_hover_text": "#4a2a1c",
        "button_pressed_bg": "#f4511e",
        "broken_button_border": "#00bcd4",
        "broken_button_text": "#00bcd4",
        "broken_button_bg": "#1c4a52",
        "broken_button_hover_bg": "#00bcd4",
        "broken_button_hover_border": "#26c6da",
        "slider_groove_bg": "#6a402a",
        "slider_handle_bg": "#ff8a65",
        "slider_handle_border": "#4a2a1c",
        "combo_bg": "#6a402a",
        "combo_border": "#ff8a65",
        "menu_bg": "#6a402a",
        "menu_border": "#ff8a65",
        "separator_border": "#ff8a65",
        "input_bg": "#6a402a",
        "input_border": "#ff8a65",
    },
    "Mint Fresh": {
        "bg_color": "#1a3a30",
        "text_color": "#a7ffeb",
        "button_bg_gradient_stop0": "#2a4a40",
        "button_bg_gradient_stop1": "#1a3a30",
        "button_border": "#a7ffeb",
        "button_hover_bg": "#a7ffeb",
        "button_hover_text": "#1a3a30",
        "button_pressed_bg": "#00bfa5",
        "broken_button_border": "#ff0000",
        "broken_button_text": "#ff0000",
        "broken_button_bg": "#4a1a1a",
        "broken_button_hover_bg": "#ff0000",
        "broken_button_hover_border": "#ff4d4d",
        "slider_groove_bg": "#2a4a40",
        "slider_handle_bg": "#a7ffeb",
        "slider_handle_border": "#1a3a30",
        "combo_bg": "#2a4a40",
        "combo_border": "#a7ffeb",
        "menu_bg": "#2a4a40",
        "menu_border": "#a7ffeb",
        "separator_border": "#a7ffeb",
        "input_bg": "#2a4a40",
        "input_border": "#a7ffeb",
    },
    "Coffee Blend": {
        "bg_color": "#3e2e2a",
        "text_color": "#d7ccc8",
        "button_bg_gradient_stop0": "#5a4a40",
        "button_bg_gradient_stop1": "#3e2e2a",
        "button_border": "#a1887f",
        "button_hover_bg": "#a1887f",
        "button_hover_text": "#3e2e2a",
        "button_pressed_bg": "#795548",
        "broken_button_border": "#ffeb3b",
        "broken_button_text": "#ffeb3b",
        "broken_button_bg": "#4d4a1a",
        "broken_button_hover_bg": "#ffeb3b",
        "broken_button_hover_border": "#fff9c4",
        "slider_groove_bg": "#5a4a40",
        "slider_handle_bg": "#a1887f",
        "slider_handle_border": "#3e2e2a",
        "combo_bg": "#5a4a40",
        "combo_border": "#a1887f",
        "menu_bg": "#5a4a40",
        "menu_border": "#a1887f",
        "separator_border": "#a1887f",
        "input_bg": "#5a4a40",
        "input_border": "#a1887f",
    }
}


class SoundButton(QPushButton):
    """ A custom button that can play a sound, with drag/drop and context menu. """
    def __init__(self, label, index, parent):
        super().__init__(label)
        self.index = index
        self.parent = parent
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.clicked.connect(self.handle_click)
        self.setProperty("broken", False)
        self.icon_path = ""
        self.update_icon() # Initialize with a potential icon

        # Ensure text is visible even with an icon
        self.setText(label)
        self.setIconSize(QSize(32, 32)) # Smaller default icon size

    def update_style(self):
        """ Forces a re-evaluation of the stylesheet for this widget. """
        self.style().unpolish(self)
        self.style().polish(self)
        self.update_icon() # Also update icon when style updates

    def update_icon(self):
        """ Sets or clears the button's icon based on self.icon_path. """
        if self.icon_path and os.path.exists(self.icon_path):
            pixmap = QPixmap(self.icon_path)
            # Scale pixmap to fit a reasonable size for the button
            scaled_pixmap = pixmap.scaled(self.iconSize(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.setIcon(QIcon(scaled_pixmap))
            self.setText(self.text()) # Ensure text is still set
        else:
            self.setIcon(QIcon()) # Clear the icon

    def handle_click(self):
        """ Plays the sound, opens a file dialog, or prompts to relocate a missing file. """
        is_broken = self.property("broken")
        
        if self.text().startswith("Empty") or is_broken:
            self.load_new_sound()
        else:
            data = self.parent.audio_files.get(str(self.index))
            if data and os.path.exists(data["path"]):
                url = QUrl.fromLocalFile(data["path"])
                self.parent.play_on_all_outputs(url)
            elif data:
                self.setProperty("broken", True)
                self.setToolTip(f"FILE NOT FOUND. Click to relocate.\nOriginal path: {data['path']}")
                self.update_style()

    def load_new_sound(self):
        """ Opens a file dialog to select a new audio file. """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_path:
            self.assign_file(file_path)

    def assign_file(self, file_path, icon_path=""):
        """ Assigns a new audio file to this button and updates its state. """
        filename = os.path.basename(file_path)
        nickname = os.path.splitext(filename)[0]
        self.setText(nickname)
        self.icon_path = icon_path # Store icon path
        self.parent.audio_files[str(self.index)] = {
            "path": file_path,
            "nickname": nickname,
            "icon": icon_path # Save icon path in data
        }
        self.setProperty("broken", False)
        self.setToolTip(f"Path: {file_path}")
        self.update_style()

    def show_context_menu(self, pos):
        """ Shows a right-click context menu for the button. """
        if self.text().startswith("Empty") and not self.property("broken"):
            return # No menu for truly empty slots

        menu = QMenu(self)
        
        load_sound_action = QAction("Load Sound", self)
        load_sound_action.triggered.connect(self.load_new_sound)
        menu.addAction(load_sound_action)

        if not self.text().startswith("Empty") and not self.property("broken"):
            change_nickname_action = QAction("Change Nickname", self)
            change_nickname_action.triggered.connect(self.change_nickname)
            menu.addAction(change_nickname_action)
            
            set_image_action = QAction("Set Image", self)
            set_image_action.triggered.connect(self.set_image)
            menu.addAction(set_image_action)

            if self.icon_path:
                clear_image_action = QAction("Clear Image", self)
                clear_image_action.triggered.connect(self.clear_image)
                menu.addAction(clear_image_action)

        if not self.text().startswith("Empty") or self.property("broken"):
            menu.addSeparator()
            remove_action = QAction("Remove Sound", self)
            remove_action.triggered.connect(self.remove_file)
            menu.addAction(remove_action)
            
        menu.exec(self.mapToGlobal(pos))

    def remove_file(self):
        """ Removes the sound and image from the button and data. """
        self.setText(f"Empty {self.index + 1}")
        self.icon_path = "" # Clear icon path
        self.parent.audio_files.pop(str(self.index), None)
        self.setProperty("broken", False)
        self.setToolTip("")
        self.update_style()

    def change_nickname(self):
        """ Opens a dialog to change the button's display text (nickname). """
        current_nickname = self.parent.audio_files.get(str(self.index), {}).get("nickname", "")
        text, ok = QInputDialog.getText(self, "Set Nickname", "Enter nickname:", text=current_nickname)
        if ok and text:
            self.setText(text)
            if str(self.index) in self.parent.audio_files:
                self.parent.audio_files[str(self.index)]["nickname"] = text

    def set_image(self):
        """ Opens a file dialog to select an image for the button. """
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)")
        if image_path:
            self.icon_path = image_path
            if str(self.index) in self.parent.audio_files:
                self.parent.audio_files[str(self.index)]["icon"] = image_path
            self.update_icon()

    def clear_image(self):
        """ Clears the image associated with the button. """
        self.icon_path = ""
        if str(self.index) in self.parent.audio_files:
            self.parent.audio_files[str(self.index)]["icon"] = ""
        self.update_icon()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
                self.assign_file(file_path)
                break
            elif file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.icon_path = file_path
                if str(self.index) in self.parent.audio_files:
                    self.parent.audio_files[str(self.index)]["icon"] = file_path
                self.update_icon()
                break

class ThemeFactory(QWidget):
    """ A widget for creating and customizing themes. """
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.current_custom_theme = parent_app.custom_theme.copy() if parent_app.custom_theme else self._get_default_custom_theme()
        self.init_ui()
        self.update_color_buttons()

    def _get_default_custom_theme(self):
        # A default set of colors for the custom theme
        return {
            "bg_color": "#202020",
            "text_color": "#00ff7f",
            "button_bg_gradient_stop0": "#303030",
            "button_bg_gradient_stop1": "#202020",
            "button_border": "#00ff7f",
            "button_hover_bg": "#00ff7f",
            "button_hover_text": "#202020",
            "button_pressed_bg": "#00aa55",
            "broken_button_border": "#ff4747",
            "broken_button_text": "#ff4747",
            "broken_button_bg": "#4d1a1a",
            "broken_button_hover_bg": "#ff4747",
            "broken_button_hover_border": "#ff8a8a",
            "slider_groove_bg": "#303030",
            "slider_handle_bg": "#00ff7f",
            "slider_handle_border": "#202020",
            "combo_bg": "#303030",
            "combo_border": "#00ff7f",
            "menu_bg": "#303030",
            "menu_border": "#00ff7f",
            "separator_border": "#00ff7f",
            "input_bg": "#303030",
            "input_border": "#00ff7f",
        }

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        color_options = [
            ("Background Color", "bg_color"),
            ("Text Color", "text_color"),
            ("Button Gradient Start", "button_bg_gradient_stop0"),
            ("Button Gradient End", "button_bg_gradient_stop1"),
            ("Button Border", "button_border"),
            ("Button Hover BG", "button_hover_bg"),
            ("Button Hover Text", "button_hover_text"),
            ("Button Pressed BG", "button_pressed_bg"),
            ("Broken Button Border", "broken_button_border"),
            ("Broken Button Text", "broken_button_text"),
            ("Broken Button BG", "broken_button_bg"),
            ("Broken Button Hover BG", "broken_button_hover_bg"),
            ("Broken Button Hover Border", "broken_button_hover_border"),
            ("Slider Groove BG", "slider_groove_bg"),
            ("Slider Handle BG", "slider_handle_bg"),
            ("Slider Handle Border", "slider_handle_border"),
            ("Combo Box BG", "combo_bg"),
            ("Combo Box Border", "combo_border"),
            ("Menu BG", "menu_bg"),
            ("Menu Border", "menu_border"),
            ("Separator Border", "separator_border"),
            ("Input BG", "input_bg"),
            ("Input Border", "input_border"),
        ]

        self.color_buttons = {}
        for i, (label_text, key) in enumerate(color_options):
            # Corrected logic for row and column
            row = i // 2
            col = (i % 2) * 2 # For label
            
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(label, row, col)

            color_button = QPushButton("")
            color_button.setFixedSize(QSize(30, 25))
            color_button.clicked.connect(lambda checked, k=key: self.pick_color(k))
            layout.addWidget(color_button, row, col + 1) # For button
            self.color_buttons[key] = color_button
        
        # Adjust row calculation for the buttons below
        num_color_options_rows = (len(color_options) + 1) // 2 
        
        apply_button = QPushButton("Apply Custom Theme")
        apply_button.clicked.connect(self.apply_custom_theme)
        layout.addWidget(apply_button, num_color_options_rows, 0, 1, 2) # Span across two columns

        save_button = QPushButton("Save Custom Theme")
        save_button.clicked.connect(self.save_custom_theme)
        layout.addWidget(save_button, num_color_options_rows + 1, 0, 1, 2)

        reset_button = QPushButton("Reset to Default Custom")
        reset_button.clicked.connect(self.reset_custom_theme)
        layout.addWidget(reset_button, num_color_options_rows + 2, 0, 1, 2)

    def pick_color(self, key):
        initial_color = QColor(self.current_custom_theme.get(key, "#000000"))
        color = QColorDialog.getColor(initial_color, self, f"Select {key.replace('_', ' ').title()} Color")
        if color.isValid():
            self.current_custom_theme[key] = color.name()
            self.update_color_buttons()
            self.apply_custom_theme() # Apply immediately for preview

    def update_color_buttons(self):
        for key, button in self.color_buttons.items():
            color_hex = self.current_custom_theme.get(key, "#000000")
            button.setStyleSheet(f"background-color: {color_hex}; border: 1px solid #555; border-radius: 5px;")
            button.setToolTip(color_hex)

    def apply_custom_theme(self):
        self.parent_app.custom_theme = self.current_custom_theme.copy()
        self.parent_app.apply_theme("Custom")

    def save_custom_theme(self):
        self.parent_app.custom_theme = self.current_custom_theme.copy()
        QMessageBox.information(self, "Theme Saved", "Custom theme settings saved!")
        # The theme will be saved automatically when the app closes via closeEvent

    def reset_custom_theme(self):
        self.current_custom_theme = self._get_default_custom_theme()
        self.update_color_buttons()
        self.apply_custom_theme()
        QMessageBox.information(self, "Theme Reset", "Custom theme reset to default settings.")


class Cyteboard(QMainWindow):
    """ The main application window with dynamic button grid. """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 800, 600)

        # Ensure the data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)

        self.audio_files = {}
        self.buttons = []
        self.num_rows = DEFAULT_ROWS
        self.current_theme_name = "Cyber Green" # Default theme
        self.custom_theme = None # To store the user's custom theme
        self.is_streaming_active = False # New state for the stream button

        self.player_output = QMediaPlayer(self)
        self.audio_output_device = QAudioOutput()
        self.player_output.setAudioOutput(self.audio_output_device)
        self.player_virtual = QMediaPlayer(self)
        self.audio_virtual_device = QAudioOutput()
        self.player_virtual.setAudioOutput(self.audio_virtual_device)

        # Initialize timeline slider and labels
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel("00:00")

        # Connect player signals to timeline
        self.player_output.durationChanged.connect(self.duration_changed)
        self.player_output.positionChanged.connect(self.position_changed)
        # Use sliderReleased to prevent constant updates while dragging
        self.position_slider.sliderReleased.connect(self.set_position_from_slider)


        self.load_data()
        self.init_ui()
        self.apply_theme(self.current_theme_name) # Apply initial theme
        self.rebuild_button_grid()
        
        self.audio_output_device.setVolume(self.volume_slider.value() / 100.0)
        self.audio_virtual_device.setVolume(self.volume_slider.value() / 100.0)

    def init_ui(self):
        """ Initializes the main window layout and control panel. """
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Main Soundboard Tab
        self.main_soundboard_widget = QWidget()
        main_layout = QVBoxLayout(self.main_soundboard_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.grid_container = QWidget()
        self.grid_container.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.grid_container.customContextMenuRequested.connect(self.show_background_context_menu)
        self.button_layout = QGridLayout(self.grid_container)
        self.button_layout.setSpacing(10)
        main_layout.addWidget(self.grid_container)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setObjectName("SeparatorFrame")
        main_layout.addWidget(separator)
        
        # --- Controls Section ---
        controls_widget = QWidget()
        controls_layout = QGridLayout(controls_widget)
        controls_layout.setSpacing(10)
        controls_layout.setColumnStretch(1, 1)

        # Volume control
        self.volume_label = QLabel("MASTER VOLUME")
        controls_layout.addWidget(self.volume_label, 0, 0, Qt.AlignmentFlag.AlignRight)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(75)
        self.volume_slider.valueChanged.connect(self.set_volume)
        controls_layout.addWidget(self.volume_slider, 0, 1)

        # Output device selection
        self.output_label = QLabel("OUTPUT DEVICE")
        controls_layout.addWidget(self.output_label, 1, 0, Qt.AlignmentFlag.AlignRight)
        self.output_combo = QComboBox()
        controls_layout.addWidget(self.output_combo, 1, 1)

        # Virtual input device selection
        self.virtual_label = QLabel("VIRTUAL INPUT")
        controls_layout.addWidget(self.virtual_label, 2, 0, Qt.AlignmentFlag.AlignRight)
        self.virtual_combo = QComboBox()
        controls_layout.addWidget(self.virtual_combo, 2, 1)

        # Timeline Slider and Labels
        controls_layout.addWidget(QLabel("TIMELINE"), 3, 0, Qt.AlignmentFlag.AlignRight)
        timeline_layout = QHBoxLayout()
        timeline_layout.addWidget(self.current_time_label)
        timeline_layout.addWidget(self.position_slider)
        timeline_layout.addWidget(self.total_time_label)
        controls_layout.addLayout(timeline_layout, 3, 1)

        # Theme selection
        self.theme_label = QLabel("THEME")
        controls_layout.addWidget(self.theme_label, 4, 0, Qt.AlignmentFlag.AlignRight) # Adjusted row index
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()) + ["Custom"]) # Add "Custom" to the list
        self.theme_combo.setCurrentText(self.current_theme_name) # Set initial selection
        self.theme_combo.currentIndexChanged.connect(self.handle_theme_selection)
        controls_layout.addWidget(self.theme_combo, 4, 1) # Adjusted row index

        # Add the Stream button
        self.stream_button = QPushButton("Stream")
        self.stream_button.setObjectName("StreamButton") # Set object name for specific styling
        self.stream_button.clicked.connect(self.toggle_stream_state) # Connect to the new toggle function
        controls_layout.addWidget(self.stream_button, 5, 0, 1, 2) # Adjusted row index, span across two columns
        
        main_layout.addWidget(controls_widget)
        self.tab_widget.addTab(self.main_soundboard_widget, "Soundboard")

        # Theme Factory Tab
        self.theme_factory_widget = ThemeFactory(self)
        self.tab_widget.addTab(self.theme_factory_widget, "Theme Factory")

        self.populate_device_lists()
        self.setAcceptDrops(True)
        self.update_stream_button_style() # Initialize stream button style

    def toggle_stream_state(self):
        """ Toggles the streaming active state and updates the button's appearance. """
        if not self.is_streaming_active:
            # If not active, show the warning and ask to proceed
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText("PC Audio to Mic Functionality")
            msg_box.setInformativeText(
                "This feature allows you to route your PC's audio directly to your microphone input, "
                "making it audible to others in calls or streams.\n\n"
                "**How it works (requires external software):**\n"
                "1.  **Install a Virtual Audio Cable:** (e.g., VB-Cable for Windows, BlackHole for macOS, JACK for Linux).\n"
                "2.  **Set Cyteboard's 'Virtual Input'**: Select the virtual cable's input as the 'Virtual Input' device in Cyteboard's controls.\n"
                "3.  **Set Your Communication App's Mic**: In your communication software (Discord, Zoom, OBS), select the virtual cable's *output* as your microphone.\n\n"
                "**Proceeding will not directly activate this feature within Cyteboard, but confirms you understand the setup.**"
            )
            msg_box.setWindowTitle("Stream Functionality Information")
            
            proceed_button = msg_box.addButton("Proceed (I Understand)", QMessageBox.ButtonRole.AcceptRole)
            cancel_button = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
            
            msg_box.exec()

            if msg_box.clickedButton() == proceed_button:
                self.is_streaming_active = True
                self.update_stream_button_style()
                print("User acknowledges streaming setup. Cyteboard's 'streaming mode' is now active.")
            else:
                print("Streaming information dialog cancelled. Cyteboard's 'streaming mode' remains inactive.")
        else:
            # If already active, turn it off
            self.is_streaming_active = False
            self.update_stream_button_style()
            print("Cyteboard's 'streaming mode' is now inactive.")

    def update_stream_button_style(self):
        """ Updates the Stream button's text and style based on its active state. """
        if self.is_streaming_active:
            self.stream_button.setText("Streaming...")
            self.stream_button.setProperty("active", True) # Set a dynamic property for styling
        else:
            self.stream_button.setText("Stream")
            self.stream_button.setProperty("active", False) # Set property to false
        self.stream_button.style().unpolish(self.stream_button) # Force style re-evaluation
        self.stream_button.style().polish(self.stream_button)


    def handle_theme_selection(self, index):
        theme_name = self.theme_combo.currentText()
        if theme_name == "Custom":
            self.apply_theme("Custom")
            self.tab_widget.setCurrentWidget(self.theme_factory_widget) # Switch to theme factory
        else:
            self.apply_theme(theme_name)
            # If switching from Custom to a predefined theme, update Theme Factory's internal state
            # This is crucial so that when the user switches back to 'Custom' tab, it reflects the *current* active theme
            theme = THEMES.get(theme_name, THEMES["Cyber Green"])
            self.theme_factory_widget.current_custom_theme = theme.copy()
            self.theme_factory_widget.update_color_buttons()


    def rebuild_button_grid(self):
        """ Clears and rebuilds the grid of sound buttons based on self.num_rows. """
        for button in self.buttons:
            self.button_layout.removeWidget(button)
            button.deleteLater()
        self.buttons.clear()

        num_buttons_to_create = self.num_rows * BUTTONS_PER_ROW
        for i in range(num_buttons_to_create):
            row, col = divmod(i, BUTTONS_PER_ROW)
            btn = SoundButton(f"Empty {i+1}", i, self)
            
            if str(i) in self.audio_files:
                data = self.audio_files[str(i)]
                btn.setText(data["nickname"])
                btn.setToolTip(f"Path: {data['path']}")
                btn.icon_path = data.get("icon", "") # Load icon path
                
                if not os.path.exists(data["path"]):
                    btn.setProperty("broken", True)
                    btn.setToolTip(f"FILE NOT FOUND. Click to relocate.\nOriginal path: {data['path']}")

            self.button_layout.addWidget(btn, row, col)
            self.buttons.append(btn)
        
        for btn in self.buttons:
            btn.update_style() # This also calls update_icon() for each button

        self.updateGeometry()

    def show_background_context_menu(self, pos):
        """ Shows a context menu to add or remove rows of buttons. """
        menu = QMenu(self)
        add_row_action = QAction("Add Row", self)
        add_row_action.triggered.connect(self.add_row)
        if self.num_rows >= MAX_ROWS:
            add_row_action.setEnabled(False)
        menu.addAction(add_row_action)

        remove_row_action = QAction("Remove Last Row", self)
        remove_row_action.triggered.connect(self.remove_row)
        if self.num_rows <= MIN_ROWS:
            remove_row_action.setEnabled(False)
        menu.addAction(remove_row_action)
        
        menu.exec(self.grid_container.mapToGlobal(pos))

    def add_row(self):
        if self.num_rows < MAX_ROWS:
            self.num_rows += 1
            self.rebuild_button_grid()

    def remove_row(self):
        if self.num_rows > MIN_ROWS:
            # Check if there are active buttons in the last row
            last_row_start_index = (self.num_rows - 1) * BUTTONS_PER_ROW
            has_active_buttons = False
            for i in range(BUTTONS_PER_ROW):
                btn_index = last_row_start_index + i
                if str(btn_index) in self.audio_files:
                    has_active_buttons = True
                    break
            
            if has_active_buttons:
                reply = QMessageBox.question(self, 'Confirm Row Removal',
                                             "Removing the last row will delete all sounds assigned to it. Are you sure?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    return

                # If confirmed, remove data for buttons in the last row
                for i in range(BUTTONS_PER_ROW):
                    btn_index = last_row_start_index + i
                    self.audio_files.pop(str(btn_index), None)

            self.num_rows -= 1
            self.rebuild_button_grid()


    def populate_device_lists(self):
        self.output_combo.clear()
        self.virtual_combo.clear()

        all_audio_outputs = QMediaDevices.audioOutputs()

        # Filter out virtual devices for the main output
        self.output_devices = [
            d for d in all_audio_outputs
            if "virtual" not in d.description().lower() and "cable" not in d.description().lower()
        ]

        if not self.output_devices:
            self.output_combo.addItem("No Non-Virtual Output Devices Found")
            self.output_combo.setEnabled(False)
        else:
            for device in self.output_devices:
                self.output_combo.addItem(device.description())
            self.output_combo.currentIndexChanged.connect(self.change_output_device)
            # Set the default output device
            self.audio_output_device.setDevice(self.output_devices[self.output_combo.currentIndex()])


        # Identify virtual devices for the virtual input
        self.virtual_devices = [
            d for d in all_audio_outputs
            if "virtual" in d.description().lower() or "cable" in d.description().lower()
        ]
        
        if not self.virtual_devices:
            self.virtual_combo.addItem("No Virtual Device Found")
            self.virtual_combo.setEnabled(False)
        else:
            for device in self.virtual_devices:
                self.virtual_combo.addItem(device.description())
            self.virtual_combo.currentIndexChanged.connect(self.change_virtual_device)
            if self.virtual_devices:
                    self.audio_virtual_device.setDevice(self.virtual_devices[self.virtual_combo.currentIndex()])

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        
        if theme_name == "Custom" and self.custom_theme:
            theme = self.custom_theme
        else:
            theme = THEMES.get(theme_name, THEMES["Cyber Green"]) # Fallback to default
            # If a predefined theme is selected, ensure the custom theme is not accidentally loaded
            if theme_name != "Custom" and self.custom_theme:
                 # Update the theme factory's current theme to match the newly applied one
                 # This is crucial so that when the user switches to 'Custom' tab, it reflects the *current* active theme
                 self.theme_factory_widget.current_custom_theme = theme.copy()
                 self.theme_factory_widget.update_color_buttons()


        style = f"""
            QMainWindow, QWidget {{
                background-color: {theme["bg_color"]};
                color: {theme["text_color"]};
                font-family: "Lucida Console", "Courier New", monospace;
            }}
            QPushButton {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {theme["button_bg_gradient_stop0"]}, stop: 1 {theme["button_bg_gradient_stop1"]});
                border: 1px solid {theme["button_border"]};
                border-radius: 8px;
                color: {theme["text_color"]};
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
                min-width: 70px;
                max-width: 100px;
                min-height: 30px;
                max-height: 50px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {theme["button_hover_bg"]};
                color: {theme["button_hover_text"]};
                border: 1px solid {theme["button_border"]};
            }}
            QPushButton:pressed {{
                background-color: {theme["button_pressed_bg"]};
                border-color: {theme["button_pressed_bg"]};
                color: {theme["button_hover_text"]};
            }}
            QPushButton[broken="true"] {{
                border: 1px solid {theme["broken_button_border"]};
                color: {theme["broken_button_text"]};
                background-color: {theme["broken_button_bg"]};
            }}
            QPushButton[broken="true"]:hover {{
                border-color: {theme["broken_button_hover_border"]};
                color: {theme["button_hover_text"]};
                background-color: {theme["broken_button_hover_bg"]};
            }}
            QLabel {{
                color: {theme["text_color"]};
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            QSlider::groove:horizontal {{ background: {theme["slider_groove_bg"]}; border: 1px solid #3a3a3a; height: 4px; border-radius: 2px; }}
            QSlider::handle:horizontal {{ background: {theme["slider_handle_bg"]}; border: 2px solid {theme["slider_handle_border"]}; width: 16px; height: 16px; margin: -8px 0; border-radius: 8px; }}
            QSlider::handle:horizontal:hover {{ background: {theme["button_hover_bg"]}; }}
            QComboBox {{ background-color: {theme["combo_bg"]}; border: 1px solid {theme["combo_border"]}; border-radius: 5px; padding: 5px 10px; color: {theme["text_color"]}; font-weight: bold; }}
            QComboBox:hover {{ border: 1px solid {theme["button_hover_bg"]}; }}
            QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 25px; border-left-width: 1px; border-left-color: {theme["combo_border"]}; border-left-style: solid; border-top-right-radius: 5px; border-bottom-right-radius: 5px; }}
            QComboBox QAbstractItemView {{ background-color: {theme["bg_color"]}; border: 1px solid {theme["combo_border"]}; selection-background-color: {theme["button_hover_bg"]}; selection-color: {theme["button_hover_text"]}; color: {theme["text_color"]}; outline: 0px; padding: 5px; }}
            QMenu {{ background-color: {theme["menu_bg"]}; border: 1px solid {theme["menu_border"]}; color: {theme["text_color"]}; padding: 5px; }}
            QMenu::item {{ padding: 8px 25px; border-radius: 4px; }}
            QMenu::item:selected {{ background-color: {theme["button_hover_bg"]}; color: {theme["button_hover_text"]}; }}
            QMenu::item:disabled {{ color: #555; }}
            QMenu::separator {{ height: 1px; background: {theme["separator_border"]}; margin: 5px 5px; }}
            #SeparatorFrame {{ border: 1px solid {theme["separator_border"]}; }}
            QDialog, QMessageBox, QInputDialog {{ background-color: {theme["bg_color"]}; }}
            QLineEdit {{ background-color: {theme["input_bg"]}; border: 1px solid {theme["input_border"]}; border-radius: 5px; color: {theme["text_color"]}; padding: 5px; font-size: 14px; }}
            QLineEdit:focus {{ border: 1px solid {theme["button_hover_bg"]}; }}
            QPushButton {{
                /* Apply border-radius to the icon as well, if supported, otherwise it's just the button */
                border-image: url(none); /* Prevents default image styling interfering */
                qproperty-iconSize: 32px 32px; /* Set desired icon size to be smaller */
            }}
            QPushButton::hover {{
                border-image: url(none);
            }}
            QPushButton::pressed {{
                border-image: url(none);
            }}
            QTabWidget::pane {{ /* The tab widget frame */
                border: 1px solid {theme["separator_border"]};
                background-color: {theme["bg_color"]};
            }}
            QTabWidget::tab-bar {{
                left: 5px; /* move to the right */
            }}
            QTabBar::tab {{
                background: {theme["combo_bg"]};
                border: 1px solid {theme["combo_border"]};
                border-bottom-color: {theme["combo_border"]}; /* same as pane color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 5px 10px;
                color: {theme["text_color"]};
                font-weight: bold;
            }}
            QTabBar::tab:selected, QTabBar::tab:hover {{
                background: {theme["button_hover_bg"]};
                color: {theme["button_hover_text"]};
            }}
            QTabBar::tab:selected {{
                border-color: {theme["button_hover_bg"]};
                border-bottom-color: {theme["bg_color"]}; /* make selected tab appear connected to the pane */
            }}
            #StreamButton {{ /* Default style for the Stream button (inactive) */
                background-color: #dc3545; /* Red color */
                border: 1px solid #dc3545;
                color: white;
            }}
            #StreamButton:hover {{
                background-color: #c82333; /* Darker red on hover */
                border: 1px solid #c82333;
            }}
            #StreamButton:pressed {{
                background-color: #bd2130; /* Even darker red when pressed */
                border: 1px solid #bd2130;
            }}
            #StreamButton[active="true"] {{ /* Style when streaming is active */
                background-color: #28a745; /* Green color */
                border: 1px solid #28a745;
                color: white;
            }}
            #StreamButton[active="true"]:hover {{
                background-color: #218838; /* Darker green on hover */
                border: 1px solid #218838;
            }}
            #StreamButton[active="true"]:pressed {{
                background-color: #1e7e34; /* Even darker green when pressed */
                border: 1px solid #1e7e34;
            }}
        """
        self.setStyleSheet(style)
        # Force re-style on all buttons to ensure icon border-radius property is re-evaluated
        for button in self.buttons:
            button.update_style()
        # Also update the stream button's style specifically
        self.update_stream_button_style()
        
    def set_volume(self, value):
        vol = value / 100.0
        self.audio_output_device.setVolume(vol)
        self.audio_virtual_device.setVolume(vol)

    def change_output_device(self, index):
        if not self.output_devices or not (0 <= index < len(self.output_devices)): return
        device = self.output_devices[index]
        self.audio_output_device.setDevice(device)
        self.audio_output_device.setVolume(self.volume_slider.value() / 100.0)

    def change_virtual_device(self, index):
        if not self.virtual_devices or not (0 <= index < len(self.virtual_devices)): return
        device = self.virtual_devices[index]
        self.audio_virtual_device.setDevice(device)
        self.audio_virtual_device.setVolume(self.volume_slider.value() / 100.0)

    def play_on_all_outputs(self, url: QUrl):
        self.player_output.setSource(url)
        self.player_virtual.setSource(url)
        self.player_output.play()
        self.player_virtual.play()

    def duration_changed(self, duration):
        # Duration is in milliseconds
        self.position_slider.setRange(0, duration)
        self.total_time_label.setText(self.format_time(duration))

    def position_changed(self, position):
        # Position is in milliseconds
        # Only update slider value if the user is not currently dragging it
        if not self.position_slider.isSliderDown():
            self.position_slider.setValue(position)
        self.current_time_label.setText(self.format_time(position))

    def set_position_from_slider(self):
        # Set position in milliseconds from the slider's current value
        position = self.position_slider.value()
        self.player_output.setPosition(position)
        self.player_virtual.setPosition(position)

    def format_time(self, ms):
        # Helper function to format milliseconds into MM:SS
        seconds = ms // 1000
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02}:{seconds:02}"


    def load_data(self):
        """ Loads sound data and UI state from the JSON file. """
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.audio_files = data.get("audio_files", {})
                    self.num_rows = data.get("ui_state", {}).get("num_rows", DEFAULT_ROWS)
                    self.current_theme_name = data.get("ui_state", {}).get("theme", "Cyber Green")
                    self.custom_theme = data.get("ui_state", {}).get("custom_theme", None)
                    # Load the streaming state
                    self.is_streaming_active = data.get("ui_state", {}).get("is_streaming_active", False)
                    
                    self.num_rows = max(MIN_ROWS, min(self.num_rows, MAX_ROWS))

            except (json.JSONDecodeError, TypeError):
                print(f"Warning: Could not parse {DATA_FILE}. Starting fresh.")
                self.audio_files = {}
                self.num_rows = DEFAULT_ROWS
                self.current_theme_name = "Cyber Green"
                self.custom_theme = None
                self.is_streaming_active = False # Reset on error
        else:
            self.audio_files = {}
            self.num_rows = DEFAULT_ROWS
            self.current_theme_name = "Cyber Green"
            self.custom_theme = None
            self.is_streaming_active = False

    def closeEvent(self, event):
        """ Saves all data to the JSON file when the application closes. """
        data_to_save = {
            "audio_files": self.audio_files,
            "ui_state": {
                "num_rows": self.num_rows,
                "theme": self.current_theme_name,
                "custom_theme": self.custom_theme, # Save custom theme data
                "is_streaming_active": self.is_streaming_active # Save streaming state
            }
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data_to_save, f, indent=4)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Cyteboard()
    window.show()
    sys.exit(app.exec())
