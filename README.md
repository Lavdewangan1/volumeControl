# Hand Gesture Volume Control 

## Overview
This Python program utilizes computer vision and gesture recognition to control media playback and adjust system volume through hand gestures. It utilizes the following libraries:

OpenCV: For capturing video and image processing.
MediaPipe: For hand tracking and landmark detection.
NumPy: For numerical operations.
Keyboard: For simulating keyboard events.
PyAutoGUI: For programmatically controlling the mouse and keyboard.
PyCaw: For interacting with the Windows Audio Control API.

## Running the Program
Save the provided Python script as volumeControl.py.
Save the provided CMD script as run_program.cmd.
Place both files in the same directory.
Run the CMD file (i.e. "volumeApp.cmd")
## Usage
The program uses your computer's default camera to capture video.
It detects hand landmarks using MediaPipe.
Gestures are recognized to control media playback and adjust system volume.
Specific gestures include play/pause (closing thumb and index finger) and volume adjustment (changing the angle of a line(imaginary) between thumb and index finger minimum angle is 30 and maximum is 150).
## Note
This program is specifically designed for Windows and may not work on other operating systems.
Ensure your system's camera is properly configured for accurate hand tracking.
