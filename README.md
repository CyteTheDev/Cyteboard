# Cyteboard

Cyteboard is a customizable soundboard application built with PyQt6, designed to provide an intuitive way to play audio files, manage your sound library, and personalize the application's appearance. It allows for simultaneous playback on multiple audio output devices, including virtual audio cables, making it ideal for streaming, online meetings, or personal use.

## Features

* **Sound Playback**: Supports `.mp3`, `.wav`, and `.ogg` audio formats.
* **Multi-Output Support**: Play sounds through your default audio output and a virtual audio device (e.g., VB-Cable, Voicemeeter) concurrently.
* **Customizable Sound Buttons**:
    * Load audio files via a standard file dialog or by dragging and dropping them directly onto a button.
    * Easily rename buttons with custom nicknames.
    * Assign custom images/icons to buttons, also supporting drag-and-drop for image files.
    * Remove assigned sounds, reverting buttons to their default "Empty" state.
    * Automatic detection and visual indication for "broken" file paths, prompting users to relocate missing audio files.
* **Dynamic Grid Layout**:
    * Flexibly add and remove rows of sound buttons to suit your needs.
    * Includes a confirmation prompt when removing rows that contain assigned sounds to prevent accidental data loss.
* **Master Volume Control**: A global slider to adjust the output volume across all active audio devices.
* **Audio Device Selection**: Dedicated dropdowns for selecting your preferred primary audio output and virtual input devices.
* **Advanced Theming**:
    * Choose from a selection of aesthetically pleasing, predefined dark themes.
    * **Theme Factory**: A dedicated tab allowing users to create and fine-tune their own custom themes by picking colors for every UI element. Custom themes can be saved for persistence.
* **Persistent Configuration**: All settings, including sound assignments (paths, nicknames, icons), UI layout (number of rows), selected theme, and custom theme configurations, are automatically saved upon exit and reloaded on startup.

## Installation

### Prerequisites

* Python 3.x
* `PyQt6`: The core GUI framework.
* `PyQt6-QtMultimedia`: Provides multimedia functionalities, including audio playback.

### Setup Steps

1.  **Download the `main.py` file:**
    Save the `main.py` file to a directory of your choice. For better organization, you might want to create a dedicated folder for your Cyteboard application.

    ```bash
    # Example for creating a folder and navigating into it
    mkdir Cyteboard
    cd Cyteboard
    # Then place main.py inside this folder
    ```

2.  **Create a Python Virtual Environment (Recommended):**
    Using a virtual environment helps manage project dependencies and avoids conflicts with other Python projects.

    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**

    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Required Libraries:**
    With your virtual environment activated, install PyQt6 and PyQt6-QtMultimedia:

    ```bash
    pip install PyQt6 PyQt6-QtMultimedia
    ```

## Usage

1.  **Run the Application:**
    Navigate to the directory where `main.py` is saved and run:

    ```bash
    python main.py
    ```

2.  **Adding Sounds:**
    * **Click to Load:** Click on any "Empty" button. A file dialog will appear, allowing you to browse and select an audio file (MP3, WAV, OGG).
    * **Drag & Drop:** Simply drag an audio file from your file explorer and drop it onto any sound button to assign it.

3.  **Button Options (Right-Click Context Menu):**
    Right-clicking on a configured sound button (not an "Empty" one) will bring up a context menu with the following options:
    * **Load Sound**: Replace the current sound with a new audio file.
    * **Change Nickname**: Customize the text displayed on the button.
    * **Set Image**: Add a visual icon to the button. You can select an image file (PNG, JPG, JPEG, GIF, BMP). Dragging and dropping an image directly onto a button also works.
    * **Clear Image**: Remove the assigned icon, leaving only the text.
    * **Remove Sound**: Unassign the audio file from the button, resetting it to an "Empty" state.

4.  **Managing Button Rows:**
    Right-click on the main soundboard grid's empty background area to access options:
    * **Add Row**: Increases the number of sound button rows.
    * **Remove Last Row**: Decreases the number of sound button rows. Be advised: if the row contains assigned sounds, a confirmation message will appear before deletion.

5.  **Volume and Audio Device Configuration:**
    * **MASTER VOLUME**: Adjust the slider to set the overall playback volume for all outputs.
    * **OUTPUT DEVICE**: Select your primary audio output device from the dropdown.
    * **VIRTUAL INPUT**: Choose a virtual audio device (e.g., virtual cable) from this dropdown if you wish to route audio to another application.

6.  **Customizing Themes:**
    * **Predefined Themes**: In the "Soundboard" tab, use the "THEME" dropdown to switch between various built-in dark themes.
    * **Theme Factory**: Navigate to the "Theme Factory" tab to unleash your creativity! Here, you can pick specific colors for almost every element of the UI.
        * Changes are applied instantly for preview.
        * Click "Apply Custom Theme" to make your custom creation the active theme.
        * Click "Save Custom Theme" to ensure your custom color scheme is saved and loaded automatically next time you open Cyteboard.
        * "Reset to Default Custom" will revert your custom theme settings to their initial state.

## Data Storage

Cyteboard automatically saves your application's state and sound configurations to a JSON file named `cyteboard_data.json`. This file is located in your operating system's standard application data directory:

* **Windows:** `%APPDATA%\Cyteboard\` (e.g., `C:\Users\YourUser\AppData\Roaming\Cyteboard\`)
* **macOS:** `~/Library/Application Support/Cyteboard/`
* **Linux:** `~/.local/share/Cyteboard/`

## Troubleshooting

* **No Sound or Device Issues:** Verify that your audio output devices and any virtual cables are correctly installed and recognized by your operating system.
* **"FILE NOT FOUND" on a Button:** This indicates that the associated audio file has been moved, renamed, or deleted from its original location. Simply click the button to open a file dialog and re-select the correct file.
* **Unexpected Application Behavior/Crashes:** In rare cases, the `cyteboard_data.json` file might become corrupted. You can try deleting this file (after making a backup, if desired) to reset the application to its default state.
* **Missing Features/Errors:** Ensure all required PyQt6 packages (`PyQt6` and `PyQt6-QtMultimedia`) are correctly installed within your active Python environment.
