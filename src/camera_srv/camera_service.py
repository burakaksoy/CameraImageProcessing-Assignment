"""
camera_service.py

Concrete implementation of CameraInterface that uses OpenCV
to interface with the webcam.
"""

import cv2

class CameraService():
    """Service that uses OpenCV to capture frames from the webcam."""

    def __init__(self, camera_index=0):
        """
        Initialize the camera service.
        Args:
            camera_index (int): Index of the webcam. Typically 0 for default camera.
        """
        self.camera_index = camera_index
        self.cap = None

    def open_camera(self) -> None:
        """Open the webcam/camera resource."""
        self.cap = cv2.VideoCapture(self.camera_index)

    def read_frame(self):
        """
        Read a single frame from the camera.
        Returns:
            (success, frame): success is a boolean,
                              frame is the captured image (numpy array).
        """
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("Camera is not opened. Call open_camera() first.")
        success, frame = self.cap.read()
        return success, frame

    def close_camera(self) -> None:
        """Release the camera resource."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
