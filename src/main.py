"""
main.py

Application entry point for capturing an image from the webcam,
converting to grayscale, and generating/displaying a histogram.
"""

import cv2
import sys
import numpy as np

from camera_srv import CameraService, to_grayscale, compute_histogram, display_histogram

def run():
    camera = CameraService(camera_index=0)

    try:
        camera.open_camera()
    except Exception as e:
        print(f"Failed to open camera: {e}")
        sys.exit(1)

    cv2.namedWindow("Webcam Feed", cv2.WINDOW_AUTOSIZE)

    print("Press SPACE to capture an image, or ESC to exit.")

    while True:
        success, frame = camera.read_frame()
        if not success:
            print("Failed to read frame from camera.")
            break

        cv2.imshow("Webcam Feed", frame)

        key = cv2.waitKey(1) & 0xFF
        # Press ESC to exit
        if key == 27:  # ESC
            break
        # Press SPACE to capture an image
        if key == 32:  # SPACE
            # Convert to grayscale
            gray_frame = to_grayscale(frame)

            # Display the grayscale image
            cv2.imshow("Grayscale Image", gray_frame)

            # Compute and display histogram
            hist = compute_histogram(gray_frame)
            display_histogram(hist)

            print("Captured and displayed grayscale + histogram. Press ESC to exit.")
    
    camera.close_camera()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
