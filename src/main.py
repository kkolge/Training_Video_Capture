import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import configparser
import cv2
from PIL import Image, ImageTk
from datetime import datetime
import time

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Video Capture Tool for AI Model Training")
        self.geometry("1024x768")
        self.resizable(False, False)

        # Allow the main window grid to expand
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Set a modern theme for better appearance
        style = ttk.Style(self)
        style.theme_use('clam')

        # Set up the main frame and use grid for a two-column layout
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Configure the main_frame grid to distribute space
        self.main_frame.columnconfigure(0, weight=1)  # Left column
        self.main_frame.columnconfigure(1, weight=5)  # Right column (video)
        self.main_frame.rowconfigure(0, weight=1)

        # Camera and Recording variables
        self.camera = None
        self.is_camera_on = False
        self.frame_update_id = None
        self.is_recording = False 
        self.video_writer = None
        self.recording_timer = None
        self.start_time = 0 

        # UI components
        self.create_left_panel()
        self.create_right_panel()

        # Callbacks
        self.test_connection_button.config(command=self.test_camera_connection)
        self.start_stop_camera_button.config(command=self.toggle_camera)
        self.record_button.config(command=self.toggle_recording)

        # Manage settings
        self.settings_file = os.path.join("config", "config.ini")
        self.load_settings()

        # Bind the window closing event to save settings
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # Version and company info
        ttk.Label(self.main_frame, text="Version: 1.0.0", 
                font=("Arial", 8)).grid(row=2, column=1, sticky=tk.SE, pady=(5, 0), padx=5)
        ttk.Label(self.main_frame, text="© 2024 Panache IoT (a division of Panache DigiLife LTD)", 
                font=("Arial", 8)).grid(row=3, column=1, sticky=tk.SE, padx=5)

    def load_settings(self):
        """Loads settings from the config file and populates the UI."""
        config = configparser.ConfigParser()

        # Create config directory and file if they don't exist
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)

        if os.path.exists(self.settings_file):
            config.read(self.settings_file)

            # Load from the file or use defaults
            camera_source = config.get("Settings", "camera_source", fallback="0")
            output_dir = config.get("Settings", "output_dir", fallback=os.path.join(os.getcwd(), "videos"))

            self.camera_source_entry.delete(0, tk.END)
            self.camera_source_entry.insert(0, camera_source)

            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, output_dir)
        else:
            # If no file exists, create the default directory
            default_dir = os.path.join(os.getcwd(), "videos")
            os.makedirs(default_dir, exist_ok=True)
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, default_dir)

    def save_settings(self):
        """Saves current settings from the UI to the config file."""
        config = configparser.ConfigParser()
        config['Settings'] = {
            'camera_source': self.camera_source_entry.get(),
            'output_dir': self.output_dir_entry.get()
        }

        # Ensure the directory exists before saving the file
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)

        with open(self.settings_file, 'w') as configfile:
            config.write(configfile)

    def on_close(self):
        """Saves settings and then closes the application."""
        self.save_settings()
        self.destroy()

    def create_left_panel(self):
        """Creates the left-hand panel with all the controls."""
        left_panel = ttk.Frame(self.main_frame, padding="10")
        left_panel.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        left_panel.rowconfigure(0, weight=1)

        # Setup and Review sections
        self.create_setup_section(left_panel)
        self.create_review_section(left_panel)

        # Configure the left panel to expand
        left_panel.columnconfigure(0, weight=1)

    # def create_right_panel(self):
    #     """Creates the right-hand panel for the video feed and recording controls."""
    #     right_panel = ttk.Frame(self.main_frame, padding="10")
    #     right_panel.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
    #     right_panel.columnconfigure(0, weight=1)
    #     right_panel.rowconfigure(0, weight=1)

    #     # Section View/Record
    #     view_record_frame = ttk.LabelFrame(right_panel, text="2. Live View and Recording", padding="10")
    #     view_record_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    #     view_record_frame.columnconfigure(0, weight=1)
    #     view_record_frame.rowconfigure(0, weight=1)

    #     # Create a container frame for the video with a fixed size
    #     video_container = ttk.Frame(view_record_frame, width=640, height=480)
    #     video_container.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)

    #     # Prevent the container from shrinking below its specified size
    #     video_container.grid_propagate(False)

    #     # Placeholder for the video feed inside the container
    #     self.video_label = ttk.Label(video_container, text="Live Video Feed", relief="solid", background="black", foreground="white", anchor="center")
    #     self.video_label.pack(fill=tk.BOTH, expand=True)

    #     # Controls
    #     control_frame = ttk.Frame(view_record_frame)
    #     control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
    #     control_frame.columnconfigure(0, weight=1)
    #     control_frame.columnconfigure(1, weight=1)
    #     control_frame.columnconfigure(2, weight=1)

    #     self.start_stop_camera_button = ttk.Button(control_frame, text="Start Camera")
    #     self.start_stop_camera_button.grid(row=0, column=0, padx=5, sticky=tk.W)

    #     self.record_button = ttk.Button(control_frame, text="Start Recording")
    #     self.record_button.grid(row=0, column=1, padx=5, sticky=tk.W)

    #     self.record_duration_label = ttk.Label(control_frame, text="Duration: 00:00:00")
    #     self.record_duration_label.grid(row=0, column=2, padx=5, sticky=tk.E)
    def create_right_panel(self):
        """Creates the right-hand panel for the video feed and recording controls."""
        right_panel = ttk.Frame(self.main_frame, padding="10")
        right_panel.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=0) # Controls row does not expand

        view_record_frame = ttk.LabelFrame(right_panel, text="2. Live View and Recording", padding="10")
        view_record_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        view_record_frame.columnconfigure(0, weight=1)
        view_record_frame.rowconfigure(0, weight=1)

        self.video_label = ttk.Label(view_record_frame, text="Live Video Feed", relief="solid", background="black", foreground="white", anchor="center")
        self.video_label.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)

        # Controls are now in a separate frame below the video frame
        control_frame = ttk.Frame(right_panel)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=1)

        self.start_stop_camera_button = ttk.Button(control_frame, text="Start Camera")
        self.start_stop_camera_button.grid(row=0, column=0, padx=5, sticky=tk.W)

        self.record_button = ttk.Button(control_frame, text="Start Recording")
        self.record_button.grid(row=0, column=1, padx=5, sticky=tk.W)

        self.record_duration_label = ttk.Label(control_frame, text="Duration: 00:00:00")
        self.record_duration_label.grid(row=0, column=2, padx=5, sticky=tk.E)

    def create_setup_section(self, parent_frame):
        # Section Setup
        setup_frame = ttk.LabelFrame(parent_frame, text="1. Camera and Directory Setup", padding="10")
        setup_frame.pack(fill=tk.X, pady=10)

        # Camera Source
        ttk.Label(setup_frame, text="Camera Source:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.camera_source_entry = ttk.Entry(setup_frame)
        self.camera_source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.camera_source_entry.insert(0, "0")

        # Test Connection and Status
        self.test_connection_button = ttk.Button(setup_frame, text="Test Connection")
        self.test_connection_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.connection_status_label = ttk.Label(setup_frame, text="Status: Disconnected")
        self.connection_status_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Output Directory
        ttk.Label(setup_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        output_dir_frame = ttk.Frame(setup_frame)
        output_dir_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        output_dir_frame.columnconfigure(0, weight=1)

        self.output_dir_entry = ttk.Entry(output_dir_frame)
        self.output_dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.browse_button = ttk.Button(output_dir_frame, text="Browse...", command=self.browse_output_directory)
        self.browse_button.grid(row=0, column=1, padx=5)

        # Video Name
        ttk.Label(setup_frame, text="Video Name:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.video_name_entry = ttk.Entry(setup_frame)
        self.video_name_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Configure column weights for resizing
        setup_frame.columnconfigure(1, weight=1)

    def create_view_record_section(self, parent_frame):
        # Section View/Record
        view_record_frame = ttk.LabelFrame(parent_frame, text="2. Live View and Recording", padding="10")
        view_record_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Placeholder for the video feed
        # Set the size of the label to a fixed size for a consistent layout
        self.video_label = ttk.Label(view_record_frame, text="Live Video Feed", relief="solid", background="black", foreground="white", anchor="center")
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Controls
        control_frame = ttk.Frame(view_record_frame)
        control_frame.pack(fill=tk.X, pady=5)

        self.start_stop_camera_button = ttk.Button(control_frame, text="Start Camera", command=self.toggle_camera)
        self.start_stop_camera_button.pack(side=tk.LEFT, padx=5, expand=True)

        self.record_button = ttk.Button(control_frame, text="Start Recording")
        self.record_button.pack(side=tk.LEFT, padx=5, expand=True)

        self.record_duration_label = ttk.Label(control_frame, text="Duration: 00:00:00")
        self.record_duration_label.pack(side=tk.LEFT, padx=5)

    def create_review_section(self, parent_frame):
        # Section Review
        review_frame = ttk.LabelFrame(parent_frame, text="3. Review Video", padding="10")
        review_frame.pack(fill=tk.X, pady=10)

        # Open Video
        open_video_frame = ttk.Frame(review_frame)
        open_video_frame.pack(fill=tk.X, pady=5)
        self.open_video_button = ttk.Button(open_video_frame, text="Open Video")
        self.open_video_button.pack(side=tk.LEFT, padx=5)

        # Playback controls
        playback_frame = ttk.Frame(review_frame)
        playback_frame.pack(fill=tk.X, pady=5)

        self.playback_button = ttk.Button(playback_frame, text="Play/Pause")
        self.playback_button.pack(side=tk.LEFT, padx=5)

        self.delete_video_button = ttk.Button(playback_frame, text="Delete Video")
        self.delete_video_button.pack(side=tk.LEFT, padx=5)

        # Duration label
        self.playback_duration_label = ttk.Label(review_frame, text="Time: 00:00:00 / 00:00:00")
        self.playback_duration_label.pack(side=tk.LEFT, padx=5)

    def test_camera_connection(self):
        """Tests the connection to the camera source."""
        source = self.camera_source_entry.get()
        try:
            # Check if source is a number (USB port) or a string (IP/Stream)
            if source.isdigit():
                source = int(source)

            cap = cv2.VideoCapture(source)
            if not cap.isOpened():
                raise IOError("Cannot open camera source.")

            # Connection successful
            self.connection_status_label.config(text="Status: Connected", foreground="green")
            messagebox.showinfo("Connection Status", "Successfully connected to the camera.")

            cap.release()
        except Exception as e:
            self.connection_status_label.config(text="Status: Error", foreground="red")
            messagebox.showerror("Connection Error", f"Failed to connect to camera.\n\nDetails: {e}")

    def toggle_camera(self):
        """Starts or stops the camera feed."""
        if self.is_camera_on:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self):
        """Starts the camera feed using the after() method."""
        source = self.camera_source_entry.get()
        try:
            if source.isdigit():
                source = int(source)

            self.camera = cv2.VideoCapture(source)

            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            if not self.camera.isOpened():
                raise IOError("Cannot open camera source.")

            self.is_camera_on = True
            self.start_stop_camera_button.config(text="Stop Camera")
            self.connection_status_label.config(text="Status: Streaming", foreground="blue")

            # Force the label to update its size before the update loop begins
            self.video_label.update()

            # Start the frame update loop
            self.update_video_feed()

        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to start camera feed.\n\nDetails: {e}")
            self.stop_camera()

    def stop_camera(self):
        """Stops the camera feed."""
        if self.camera and self.camera.isOpened():
            self.camera.release()
            self.is_camera_on = False
            self.video_label.config(image='', text="Live Video Feed", background="black")
            self.start_stop_camera_button.config(text="Start Camera")
            self.connection_status_label.config(text="Status: Disconnected", foreground="black")

        # Cancel the scheduled update
        if self.frame_update_id:
            self.after_cancel(self.frame_update_id)
            self.frame_update_id = None
        
    # def update_video_feed(self):
    #     """Reads frames from the camera, scales them to fit the display, and updates the label."""
    #     if self.is_camera_on and self.camera:
    #         ret, frame = self.camera.read()
    #         if ret:
    #             # Wait until the widget has been drawn and has a valid size
    #             if self.video_label.winfo_width() > 1 and self.video_label.winfo_height() > 1:
    #                 container_width = self.video_label.winfo_width()
    #                 container_height = self.video_label.winfo_height()

    #                 rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #                 frame_height, frame_width, _ = rgb_frame.shape

    #                 # Calculate the scaling factor to fit the entire frame (letterboxing)
    #                 scale_w = container_width / frame_width
    #                 scale_h = container_height / frame_height

    #                 print(f"Frame w/h: {frame_width}/{frame_height}, Container w/h: {container_width}/{container_height}, Scales: {scale_w:.2f}/{scale_h:.2f}")

    #                 scale = min(scale_w, scale_h)

    #                 new_w = int(frame_width * scale)
    #                 new_h = int(frame_height * scale)

    #                 resized_frame = cv2.resize(rgb_frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

    #                 bg = Image.new('RGB', (container_width, container_height), 'black')
    #                 x_offset = (container_width - new_w) // 2
    #                 y_offset = (container_height - new_h) // 2
    #                 bg.paste(Image.fromarray(resized_frame), (x_offset, y_offset))

    #                 imgtk = ImageTk.PhotoImage(image=bg)
    #                 self.video_label.imgtk = imgtk
    #                 self.video_label.config(image=imgtk)

    #         self.frame_update_id = self.after(10, self.update_video_feed)

    def update_video_feed(self):
        """Reads frames from the camera, scales them to fit the display, and updates the label."""
        if self.is_camera_on and self.camera:
            ret, frame = self.camera.read()
            if ret:
                if self.is_recording and self.video_writer:
                    self.video_writer.write(frame)

                label_width = self.video_label.winfo_width()
                label_height = self.video_label.winfo_height()

                if label_width > 1 and label_height > 1:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_height, frame_width, _ = rgb_frame.shape

                    scale_w = label_width / frame_width
                    scale_h = label_height / frame_height
                    scale = min(scale_w, scale_h)

                    new_w = int(frame_width * scale)
                    new_h = int(frame_height * scale)
                    resized_frame = cv2.resize(rgb_frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

                    bg = Image.new('RGB', (label_width, label_height), 'black')
                    x_offset = (label_width - new_w) // 2
                    y_offset = (label_height - new_h) // 2
                    bg.paste(Image.fromarray(resized_frame), (x_offset, y_offset))

                    imgtk = ImageTk.PhotoImage(image=bg)
                    self.video_label.imgtk = imgtk
                    self.video_label.config(image=imgtk)

            self.frame_update_id = self.after(10, self.update_video_feed)

    def browse_output_directory(self):
        # We will implement the functionality for this button in the next step
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, directory)

    # Recording related methods
    def toggle_recording(self):
        """Starts or stops the video recording."""
        if not self.is_camera_on:
            messagebox.showerror("Recording Error", "Please start the camera before recording.")
            return

        if self.is_recording:
            # Stop recording
            self.stop_recording()
        else:
            # Start recording
            self.start_recording()

    def start_recording(self):
        """Initializes the video writer and starts the recording."""
        # Check for required fields
        output_dir = self.output_dir_entry.get()
        video_name = self.video_name_entry.get()

        if not output_dir or not video_name:
            messagebox.showerror("Recording Error", "Please specify an output directory and video name.")
            return

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Get frame properties from the camera
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.camera.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30 # Default to 30 FPS if camera returns 0

        # Create a unique filename with a timestamp and camelCase format
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        final_filename = f"{video_name.replace(' ', '')}{current_time}.avi"
        output_path = os.path.join(output_dir, final_filename)

        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        self.is_recording = True
        self.record_button.config(text="Stop Recording")

        # Start the timer for recording duration
        self.start_time = time.time()
        self.update_duration_label()

    def stop_recording(self):
        """Releases the video writer and stops the timer."""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

        self.is_recording = False
        self.record_button.config(text="Start Recording")

        if self.recording_timer:
            self.after_cancel(self.recording_timer)
            self.recording_timer = None

        self.record_duration_label.config(text="Duration: 00:00:00")
        messagebox.showinfo("Recording Finished", "Video saved successfully!")

    def update_duration_label(self):
        """Updates the duration label every second."""
        if self.is_recording:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            self.record_duration_label.config(text=f"Duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.recording_timer = self.after(1000, self.update_duration_label)

if __name__ == "__main__":
    app = App()
    app.mainloop()