"""
gui_main.py
"""

import cv2
import sys
import numpy as np

from camera_srv import CameraService, to_grayscale, compute_histogram, display_histogram

import tkinter as tk
from tkinter import ttk
import matplotlib
import PIL.Image, PIL.ImageTk

# IMPORTANT: To embed matplotlib in Tk, use the TkAgg backend
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Webcam Image Processing")

        # 1) Initialize camera
        self.camera = CameraService(camera_index=0)
        try:
            self.camera.open_camera()
        except Exception as e:
            print(f"Error opening camera: {e}")
            self.destroy()
            return

        # 2) Configure overall window grid
        #    We'll have multiple rows/columns for the images, histogram, and sliders
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        # 3) Create image labels for a 2x2 grid
        #    (0,0) -> original, (0,1) -> grayscale,
        #    (1,0) -> blurred,  (1,1) -> edges
        self.original_label = tk.Label(self, text="Original")
        self.original_label.grid(row=0, column=0, padx=5, pady=5)

        self.gray_label = tk.Label(self, text="Grayscale")
        self.gray_label.grid(row=0, column=1, padx=5, pady=5)

        self.blur_label = tk.Label(self, text="Blurred")
        self.blur_label.grid(row=1, column=0, padx=5, pady=5)

        self.edge_label = tk.Label(self, text="Edges")
        self.edge_label.grid(row=1, column=1, padx=5, pady=5)

        # 4) Create a matplotlib Figure for the grayscale histogram
        self.fig = Figure(figsize=(4, 2))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Grayscale Histogram")
        self.ax.set_xlabel("Pixel Value")
        self.ax.set_ylabel("Count")

        # 5) Embed the histogram figure beneath the grayscale image (row=2, col=1)
        self.hist_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.hist_canvas_widget = self.hist_canvas.get_tk_widget()
        self.hist_canvas_widget.grid(row=2, column=0, columnspan=2, padx=5, pady=(0,5))

        # 6) Sliders for blur kernel size + edge detection thresholds (row=3)
        #    We'll place them all in a frame that spans columns
        self.controls_frame = tk.Frame(self)
        self.controls_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Blur kernel size (odd values from 1..31)
        tk.Label(self.controls_frame, text="Blur Kernel Size:").pack(side=tk.LEFT, padx=5)
        self.blur_slider = tk.Scale(
            self.controls_frame, from_=1, to=31, orient="horizontal", length=150,
            resolution=2,  # step by 2 to ensure mostly odd numbers
        )
        self.blur_slider.set(5)  # default kernel size
        self.blur_slider.pack(side=tk.LEFT, padx=5)

        # Edge detection thresholds
        tk.Label(self.controls_frame, text="Edge Min:").pack(side=tk.LEFT, padx=5)
        self.edge_min_slider = tk.Scale(
            self.controls_frame, from_=0, to=255, orient="horizontal", length=100
        )
        self.edge_min_slider.set(50)
        self.edge_min_slider.pack(side=tk.LEFT, padx=5)

        tk.Label(self.controls_frame, text="Edge Max:").pack(side=tk.LEFT, padx=5)
        self.edge_max_slider = tk.Scale(
            self.controls_frame, from_=0, to=255, orient="horizontal", length=100
        )
        self.edge_max_slider.set(150)
        self.edge_max_slider.pack(side=tk.LEFT, padx=5)

        # 7) Start the continuous frame loop
        self.update_frame()

        # 8) Clean up camera on exit
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_frame(self):
        """
        Continuously fetch frames from the webcam,
        process them into original, grayscale, blur, edges,
        then display all four images and update the histogram (for grayscale).
        """
        success, frame = self.camera.read_frame()
        if not success:
            self.after(50, self.update_frame)
            return

        ##################################################
        # 1) Original
        ##################################################
        original_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        original_pil = PIL.Image.fromarray(original_rgb)
        original_imgtk = PIL.ImageTk.PhotoImage(image=original_pil)
        self.original_label.imgtk = original_imgtk
        self.original_label.config(image=original_imgtk)

        ##################################################
        # 2) Grayscale
        ##################################################
        gray = to_grayscale(frame)
        # Convert single-channel grayscale to RGB for display
        gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        gray_pil = PIL.Image.fromarray(gray_rgb)
        gray_imgtk = PIL.ImageTk.PhotoImage(image=gray_pil)
        self.gray_label.imgtk = gray_imgtk
        self.gray_label.config(image=gray_imgtk)

        # Update histogram for the grayscale image
        self.update_histogram(gray)

        ##################################################
        # 3) Blur (adjustable via blur_slider)
        ##################################################
        kernel_size = self.blur_slider.get()
        # Kernel size must be odd and > 1 for GaussianBlur.
        # We can ensure it's odd:
        if kernel_size % 2 == 0:
            kernel_size += 1
        blurred = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
        blurred_rgb = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
        blurred_pil = PIL.Image.fromarray(blurred_rgb)
        blur_imgtk = PIL.ImageTk.PhotoImage(image=blurred_pil)
        self.blur_label.imgtk = blur_imgtk
        self.blur_label.config(image=blur_imgtk)

        ##################################################
        # 4) Edge Detection (adjustable min/max thresholds)
        ##################################################
        edge_min = self.edge_min_slider.get()
        edge_max = self.edge_max_slider.get()
        edges = cv2.Canny(gray, edge_min, edge_max)
        # Convert edges (single-channel) to RGB for display
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        edges_pil = PIL.Image.fromarray(edges_rgb)
        edge_imgtk = PIL.ImageTk.PhotoImage(image=edges_pil)
        self.edge_label.imgtk = edge_imgtk
        self.edge_label.config(image=edge_imgtk)

        # Schedule next frame
        self.after(10, self.update_frame)

    def update_histogram(self, gray_image):
        """
        Update the histogram figure for the given grayscale image.
        """
        hist = compute_histogram(gray_image)

        self.ax.clear()
        self.ax.set_title("Grayscale Histogram")
        self.ax.set_xlabel("Pixel Value")
        self.ax.set_ylabel("Count")
        self.ax.plot(hist)
        self.ax.set_xlim([0, 255])
        self.hist_canvas.draw()

    def on_closing(self):
        """
        Cleanup when window closes.
        """
        self.camera.close_camera()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()