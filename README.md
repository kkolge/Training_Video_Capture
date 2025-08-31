# Video Capture Tool for AI Model Training

    A simple desktop application developed for Panache IoT, a division of Panache DigiLife LTD, to capture and manage video footage for training AI models.

# Project Overview

    This application provides a user-friendly graphical interface (GUI) to configure, record, and manage video streams from various camera sources, including USB, IP, and stream URLs. The primary goal is to provide a stable and intuitive tool for capturing high-quality video data for AI model development.

# Features

## Camera Setup:

    Input fields for camera source (USB port, IP address, or stream URL).

    A "Test Connection" button with a detailed status and error log for troubleshooting.

    Persistent configuration for output directory to save videos.

    Automatic filename generation with user-defined labels, converted to camelCase, and appended with a timestamp.

## Recording & Live View:

    **Stable and responsive live video feed** with dynamic aspect ratio handling.

    Start/Stop buttons for both camera feed and video recording.

    Real-time display of recording duration.

## Video Management:

    A "Browse" button to select and load previously saved videos for review.

    Play/Pause functionality for video playback.

    Display of current time and total duration during playback.

    A "Delete Video" button to remove the currently loaded file.

## User Experience (UX):

    Intuitive and easy-to-use interface with a two-panel layout emphasizing the live video feed.

    Non-blocking I/O operations for camera capture and video playback, handled by a responsive self.after() loop to prevent the application from freezing.

    Robust error handling with user-friendly pop-up messages.

## Persistence:

    Application settings (camera source, output directory) are automatically saved to and loaded from an external config.ini file.

## About:

    Application name: Video Capture Tool for AI Model Training

    Company: Panache IoT (a division of Panache DigiLife LTD)

    Version: 1.0.0

    License: MIT License

# Getting Started with Git

To get a local copy of this project, you will need to clone the repository. If you don't have Git installed, please visit the official Git website for installation instructions.

Clone the repository: Open your terminal or command prompt and run the following command. This will download the entire project to your local machine.
    

git clone https://github.com/kkolge/Training_Video_Capture.git


Navigate to the project directory:

cd Training_Video_Capture 

Set up the virtual environment: This is a crucial step to manage project dependencies.

bash
python3 -m venv venv

Activate the virtual environment:

On macOS and Linux:
bash
source venv/bin/activate

On Windows:
powershell
    .\venv\Scripts\activate

Install dependencies: Once the virtual environment is active, install the required libraries.

pip install -r requirements.txt



# Development Plan

## Step 1: Planning and Setup

The project was initiated by creating a README.md file, setting up a Python virtual environment, and installing core dependencies: opencv-python, pillow, and tkinter. The basic file structure was established with the main script in a src directory and the configuration file in a separate config directory.

## Step 2: UI Development & Refinement

The user interface was built using Tkinter's grid and pack layout managers. The initial design was refined through an iterative process to improve user experience, including:

    Adjusting the grid weights to prioritize the video frame.

    Reorganizing widgets for a cleaner, more intuitive layout.

    Implementing dynamic aspect ratio handling to prevent video feed distortion, ensuring the full camera frame is always visible.

## Step 3: Core Functionality

    Configuration Management: Functions were created to load and save application settings from the config.ini file, ensuring settings persist between sessions.

    Camera Handling: The start_camera method was implemented to connect to a camera using cv2.VideoCapture. The live video feed is handled by a responsive self.after() loop, which prevents the GUI from freezing.

    Video Recording: A cv2.VideoWriter object was used to save frames to a file. A timer was added to display the recording duration in real-time.

## Step 4: Video Management and Playback

    Playback: Video playback was implemented using a separate self.after() loop, similar to the live camera feed. This approach ensured smooth playback without introducing a new thread, thereby preventing common threading-related issues.

    Deletion: A function was added to safely delete a video file from the system after a user confirmation.

## Step 5: Final Touches & Deployment

    Error Handling: Robust error handling was added for camera connections, file operations, and invalid inputs.

    Graceful Shutdown: The application was configured to gracefully handle keyboard interrupts (Ctrl+C), ensuring all camera resources are released on exit.

    Application Packaging: The final application was packaged into a single executable file using PyInstaller. This process required explicitly including hidden dependencies and configuring the build to keep the config.ini file external for user-defined settings.

# License

MIT License

# Development Team

Ketan Kolge  
ketan.k@panacheiot.com