"""
image_processor.py

Module for image processing utilities, including conversion to grayscale.
"""

import cv2

def to_grayscale(image):
    """
    Converts a BGR image to 8-bit grayscale.
    Args:
        image (numpy.ndarray): Input image in BGR format.
    Returns:
        (numpy.ndarray): 8-bit grayscale image.
    """
    if image is None:
        raise ValueError("Input image is None.")
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
