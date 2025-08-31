# Video Capture Tool for AI Model Training

A simple desktop application developed for Panache IoT, a division of Panache DigiLife LTD, to capture and manage video footage for training AI models.

# Project Overview

    This application provides a user-friendly graphical interface (GUI) to configure, record, and manage video streams from various camera sources. The primary goal is to provide a stable tool for capturing high-quality video data for AI model development.

# Features

## Camera Setup:

    Input fields for camera source (USB port, IP address, or stream URL).

    A "Test Connection" button with a detailed error log for troubleshooting.

    Configuration for output directory to save videos.

    Automatic filename generation with user-defined labels, converted to camelCase, and appended with a timestamp.

## Recording & Playback:

    Start/Stop buttons for both camera feed and video recording.

    Real-time display of recording duration.

## Video Management:

    Buttons for playing back and deleting saved videos.

    Display of current time and total duration during playback.

## User Experience (UX):

    Intuitive and easy-to-use interface.

    Background processing for I/O operations to prevent the application from hanging.

## Persistence:

    Save application settings (camera source, output directory) to a configuration file for future use.

## About:

    Application name: Video Capture Tool for AI Model Training

    Company: Panache IoT (a division of Panache DigiLife LTD)

    Version: 1.0.0

    License: MIT License

# Development Plan

## Step 1: Planning and Setup

    Create a README.md file: This document will serve as our project plan.

    Set up a virtual environment: Create and activate a new Python virtual environment to manage dependencies.

    Install necessary libraries: Install opencv-python for video capture and playback, and a GUI library like Tkinter (which is a standard Python library) for the user interface. We'll also use Pillow for image handling in the UI if needed.

    Create the basic file structure: Set up the main Python script and a directory for the configuration file.

## Step 2: Building the UI (User Interface)

    Design the main window: Lay out the different sections as requested (Setup, View/Record, Review).

    Add widgets: Create input fields, buttons, and labels as per the feature list.

    Implement callbacks: Attach functions to the buttons to handle user interactions (e.g., on_test_connection_click, on_start_record_click).

## Step 3: Implementing Core Functionality

### Configuration Management:

    Create functions to load settings from a config file (e.g., config.ini).

    Create functions to save settings when the user changes them.

### Camera Handling:

    Implement the logic to connect to a camera using OpenCV's cv2.VideoCapture.

    Create a separate thread for continuous frame capture to avoid freezing the GUI.

### Video Recording:

    Use OpenCV's cv2.VideoWriter to save the captured frames to a file.

    Implement the filename logic to handle camelCase conversion and add timestamps.

### Threading:

    Utilize Python's threading module to perform I/O operations (camera capture, recording, file saving) in the background. This is crucial to keep the UI responsive.

## Step 4: Adding Video Management

### Playback:

    Use cv2.VideoCapture to read and display a saved video file.

    Update a label to show the current playback time and total duration.

### Deletion:

    Implement a button to delete a selected video file from the output directory.

## Step 5: Final Touches

### Error Handling:

    Add robust error handling for camera connections, file operations, and invalid inputs.

    Implement the "Details" button to show a detailed error log.

### Refinement:

        Clean up the code, add comments, and ensure all features work as intended.

        Add the MIT License to the project.

# License

MIT License

# Development Team

Ketan Kolge  
ketan.k@panacheiot.com